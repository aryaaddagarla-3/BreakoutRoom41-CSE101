print("Let's play Hangman!")
import random 
word_bank = ["music","tree","mongol","cucumber","asdrp","cunha"]
def function():
    # picks word from word bank and removes it
    random_value = random.choice(word_bank)
    word_bank.remove(random_value)
    
    # sets up way to check answer at the end
    check_answer = str(random_value)
    check_answer = " ".join(check_answer)
    
    # count number of characters
    character_count = len(random_value)
    #turns number of characters into a list of dashes to show the player
    question = ("_") * character_count
    # makes a string of the question list
    joined_string = " ".join(question)
    print(joined_string)
    
    # turns random value into a list
    guessing_reference = list(random_value)
    
    # makes a list to store previous guesses
    previous_guesses = list()

    # list of alphabets to check guess against
    alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    # this is the lives you have remaining
    lives_remaining = str(6)
    print("Lives remaining: " + lives_remaining)
    lives_remaining = int(lives_remaining)
    
    while lives_remaining > 0:
        if joined_string == check_answer:
            # person guesses the word
            print("Word guessed, you've won!")
            break
        user_guess = input("Guess a letter: ")
        user_guess_length = len(user_guess)
        while(user_guess_length > 1):
            # this makes sure ppl don't guess multiple characters
            print("Invalid. Try again")
            user_guess = input("Guess a letter: ")
            user_guess_length = len(user_guess)
            if (user_guess_length == 1):
                break
        if user_guess not in alphabet_list:
            # makes sure guess is not a special character
            print("Invalid. Try again")
            user_guess = input("Guess a letter: ")
        while user_guess in previous_guesses:
            # makes sure user doesn't guess smth multiple times
            print("Invalid. Try again")
            user_guess = input("Guess a letter: ")
            user_guess = user_guess.lower()
            if user_guess not in previous_guesses:
                break
        previous_guesses.append(user_guess)
        if user_guess in guessing_reference:
            # loop to remove all instances of letter 
            while user_guess in guessing_reference:
                guess_number = guessing_reference.index(user_guess)
                question = list(question)
                question[guess_number] = user_guess
                guessing_reference[guess_number] = (" ")
            joined_string = " ".join(question)
            print(joined_string)
            continue
        else:
            # if the letter isn't found in letter
            print("Letter not found!")
            lives_remaining = lives_remaining - 1
            print("Lives remaining: " + str(lives_remaining))
            if lives_remaining == 0:
                # person guesses too many times
                print("Out of lives, game over!")
            continue
# allow user to play again
while True:
    function()
    play_again = input("Do you want to play again? (Y/N) ")
    if play_again == "Y":
        continue
    else:
        break
