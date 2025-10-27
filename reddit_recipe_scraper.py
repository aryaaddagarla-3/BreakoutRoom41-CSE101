import os
import re
import requests
from dotenv import load_dotenv
import praw
from urllib.parse import urlparse

class RedditRecipeScraper:
    """
    A class to find recipe posts from r/recipes subreddit for Instagram content.
    """
    
    def __init__(self):
        """Initialize the Reddit client with authentication."""
        load_dotenv()
        
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT")
        
        if not all([client_id, client_secret, user_agent]):
            missing = []
            if not client_id: missing.append("REDDIT_CLIENT_ID")
            if not client_secret: missing.append("REDDIT_CLIENT_SECRET")
            if not user_agent: missing.append("REDDIT_USER_AGENT")
            
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        
        self.reddit.read_only = True
        if not os.path.exists('images'):
            os.makedirs('images')
            
        print(" Reddit Recipe Scraper initialized successfully!")
        print(f" Running in read-only mode for public content access")
        
    def search_recipes_by_topic(self, topic, limit=10):
        """
        Search r/recipes subreddit for posts related to a specific topic.
        
        Args:
            topic (str): The search topic (e.g., "christmas", "meatloaf")
            limit (int): Maximum number of posts to retrieve
            
        Returns:
            list: List of submission objects that match the search criteria
        """
        print(f"\n Searching for '{topic}' recipes...")
     
        subreddit = self.reddit.subreddit("recipes")
        
        search_results = subreddit.search(topic, limit=limit, sort='hot')
        
        recipe_posts = []
        for submission in search_results:
            if submission.link_flair_text and "recipe" in submission.link_flair_text.lower():
                recipe_posts.append(submission)
                print(f"Found recipe post: '{submission.title}' (Score: {submission.score})")
        
        if not recipe_posts:
            print(f"No recipe posts found for topic: {topic}")
        
        return recipe_posts
    
    def extract_recipe_from_comments(self, submission):
        """
        Extract the recipe content from the most upvoted comment.
        
        Args:
            submission: Reddit submission object
            
        Returns:
            tuple: (recipe_text, comment_author) or (None, None) if no recipe found
        """
        submission.comments.replace_more(limit=0)
        
        if not submission.comments:
            return None, None
            
        top_comment = submission.comments[0]

        comment_text = top_comment.body
        
        recipe_indicators = ['ingredient', 'cup', 'tbsp', 'tsp', 'oven', 'bake', 'cook', 'mix', 'add']
        if any(indicator in comment_text.lower() for indicator in recipe_indicators):
            return comment_text, top_comment.author.name if top_comment.author else "Unknown"
        
        for comment in submission.comments[1:5]:
            if comment.score > 10:
                comment_text = comment.body
                if any(indicator in comment_text.lower() for indicator in recipe_indicators):
                    return comment_text, comment.author.name if comment.author else "Unknown"
        
        return None, None
    
    def download_image(self, image_url, filename):
        """
        Download an image from a URL and save it locally.
        
        Args:
            image_url (str): URL of the image to download
            filename (str): Local filename to save the image as
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if 'i.redd.it' in image_url or 'i.imgur.com' in image_url:
                response = requests.get(image_url, headers={'User-Agent': 'Recipe Scraper 1.0'})
                response.raise_for_status()
                parsed_url = urlparse(image_url)
                if parsed_url.path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    extension = os.path.splitext(parsed_url.path)[1]
                else:
                    content_type = response.headers.get('content-type', '')
                    if 'jpeg' in content_type:
                        extension = '.jpg'
                    elif 'png' in content_type:
                        extension = '.png'
                    elif 'gif' in content_type:
                        extension = '.gif'
                    else:
                        extension = '.jpg'
                
                full_filename = f"images/{filename}{extension}"
                
                with open(full_filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"Image saved as: {full_filename}")
                return True
                
        except Exception as e:
            print(f"Failed to download image: {e}")
            return False
        
        return False
    
    def process_topic(self, topic):
        """
        Process a single topic: search, extract recipe, download image, and display results.
        
        Args:
            topic (str): The topic to search for
            
        Returns:
            dict: Dictionary containing all extracted information
        """
        print(f"\n{'='*50}")
        print(f"Processing topic: {topic.upper()}")
        print(f"{'='*50}")
        
        recipe_posts = self.search_recipes_by_topic(topic)
        
        if not recipe_posts:
            return None
        
        best_post = max(recipe_posts, key=lambda x: x.score)
        
        print(f"\nSelected post: '{best_post.title}'")
        print(f"Posted by: u/{best_post.author.name if best_post.author else 'Unknown'}")
        print(f"Upvotes: {best_post.score}")
        print(f"Comments: {best_post.num_comments}")
        
        recipe_text, recipe_author = self.extract_recipe_from_comments(best_post)
        
        if recipe_text:
            print(f"\n Recipe (from comment by u/{recipe_author}):")
            print("-" * 40)
            cleaned_recipe = re.sub(r'\n{3,}', '\n\n', recipe_text)
            print(cleaned_recipe[:500] + "..." if len(cleaned_recipe) > 500 else cleaned_recipe)
        else:
            print("No recipe found in comments")
            recipe_author = "Not found"

        image_downloaded = False
        if hasattr(best_post, 'url') and best_post.url:
            if any(best_post.url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                image_downloaded = self.download_image(best_post.url, topic.replace(" ", "_").replace("'", ""))
            elif 'i.redd.it' in best_post.url or 'i.imgur.com' in best_post.url:
                image_downloaded = self.download_image(best_post.url, topic.replace(" ", "_").replace("'", ""))
        
        if not image_downloaded:
            print("No image available or failed to download")

        return {
            'topic': topic,
            'post_title': best_post.title,
            'post_author': best_post.author.name if best_post.author else 'Unknown',
            'post_score': best_post.score,
            'recipe_text': recipe_text,
            'recipe_author': recipe_author,
            'image_downloaded': image_downloaded,
            'post_url': f"https://reddit.com{best_post.permalink}"
        }
    
    def run_scraper(self, topics):
        """
        Run the scraper for all provided topics.
        
        Args:
            topics (list): List of topics to search for
        """
        print("Starting Reddit Recipe Scraper")
        print(f"Topics to process: {', '.join(topics)}")
        
        results = []
        
        for topic in topics:
            result = self.process_topic(topic)
            if result:
                results.append(result)
        
        print(f"\n{'='*60}")
        print("SCRAPING SUMMARY")
        print(f"{'='*60}")
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Topic: {result['topic']}")
            print(f"   Recipe: {result['post_title']}")
            print(f"   Original Poster: u/{result['post_author']}")
            print(f"   Recipe Author: u/{result['recipe_author']}")
            print(f"   Upvotes: {result['post_score']}")
            print(f"   Image Downloaded: {'Yes' if result['image_downloaded'] else 'No'}")
            print(f"   Link: {result['post_url']}")
        
        print(f"\n Successfully processed {len(results)} out of {len(topics)} topics")

def get_user_topics():
    """Get a single recipe topic from user input."""
    print(" Welcome to the Reddit Recipe Scraper!")
    print("=" * 50)
    print("Enter a recipe topic you'd like to search for.")
    print("Examples: christmas, chocolate cake, pasta, chicken, pie")
    print("=" * 50)
    
    while True:
        topic = input("\nEnter recipe topic (or 'quit' to exit): ").strip()
        
        if topic.lower() == 'quit':
            print("Goodbye!")
            return None
        elif topic:
            print(f"Searching for: '{topic}'")
            return [topic]  # Return as single-item list
        else:
            print("Please enter a valid topic!")

def main():
    """Main function to run the Reddit recipe scraper."""
    try:
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == '--demo':
            print("Running in DEMO mode with sample topics...")
            topics = ["christmas", "fruitcake", "meatloaf", "new year's", "pie"]
        else:
            topics = get_user_topics()
            if topics is None:
                return
        
        scraper = RedditRecipeScraper()
        scraper.run_scraper(topics)
        
    except FileNotFoundError:
        print("Error: .env file not found!")
        print("\n Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Fill in your Reddit API credentials")
        print("3. Get credentials from: https://www.reddit.com/prefs/apps/")
        
    except Exception as e:
        print(f"Error running scraper: {e}")
        print("\n Troubleshooting:")
        print("• Make sure you have set up your Reddit API credentials in a .env file")
        print("• Verify your Reddit app is set to 'script' type")
        print("• Check your internet connection")

if __name__ == "__main__":
    main()
