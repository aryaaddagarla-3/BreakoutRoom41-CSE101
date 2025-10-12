import random 
word_bank = ["musim"]
random_value = random.choice(word_bank)

character_count = len(random_value)
guessing_reference = list(random_value)

question = ("_") * character_count
joined_string = " ".join(question)
print(joined_string)
rounds_played = 0

lives_remaining = str(6)
print("Lives remaining: " + lives_remaining)
lives_remaining = int(lives_remaining)



while lives_remaining > 0:
    user_guess = input("Guess a letter: ")
    user_guess_length = len(user_guess)
    while(user_guess_length > 1):
        print("Invalid. Try again")
        user_guess = input("Guess a letter: ")
        user_guess_length = len(user_guess)
        if (user_guess_length == 1):
            break
    if rounds_played == character_count + 6:
        break
    if user_guess in guessing_reference:
        guess_number = guessing_reference.index(user_guess)
        question = list(question)
        question[guess_number] = user_guess
        joined_string = " ".join(question)
        print(joined_string)
        rounds_played = rounds_played + 1
        continue
    else:
        print("Letter not found!")
        lives_remaining = lives_remaining - 1
        print("Lives remaining: " + str(lives_remaining))
        rounds_played = rounds_played + 1
        if lives_remaining == 0:
            print("you are a failure my dude")
        continue

print("slayy")
