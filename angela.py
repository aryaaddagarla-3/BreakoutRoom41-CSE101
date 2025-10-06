import random 
word_bank = ["songwriting", "music", "beyond", "words", "wildcat", "review"]
random_value = random.choice(word_bank)
character_count = len(random_value)
question = ("_ ") * character_count
print(question)
lives_remaining = str(6)
print("Lives remaining: " + lives_remaining)
