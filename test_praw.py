import os
from dotenv import load_dotenv
import praw

load_dotenv()


print("CLIENT ID:", os.getenv("REDDIT_CLIENT_ID"))
print("CLIENT SECRET:", os.getenv("REDDIT_CLIENT_SECRET"))
print("USER AGENT:", os.getenv("REDDIT_USER_AGENT"))

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

print("Reddit client created successfully!")
print("Authenticated as:", reddit.user.me())