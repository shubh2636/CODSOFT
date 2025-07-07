import random

def rock_paper_scissors():
    choices = ['rock', 'paper', 'scissors']
    user_score = 0
    computer_score = 0
    
    print("Welcome to Rock, Paper, Scissors!")
    print("Rules: Rock beats scissors, scissors beat paper, and paper beats rock.")
    
    while True:
        print("\n--- New Round ---")
        print(f"Score - You: {user_score} | Computer: {computer_score}")
        
        # User input
        user_choice = input("Choose rock, paper, or scissors (or 'quit' to exit): ").lower()
        
        if user_choice == 'quit':
            break
            
        if user_choice not in choices:
            print("Invalid choice. Please try again.")
            continue
            
        # Computer selection
        computer_choice = random.choice(choices)
        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")
        
        # Determine winner
        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'scissors' and computer_choice == 'paper') or \
             (user_choice == 'paper' and computer_choice == 'rock'):
            print("You win!")
            user_score += 1
        else:
            print("Computer wins!")
            computer_score += 1
            
    print("\nFinal Score:")
    print(f"You: {user_score} | Computer: {computer_score}")
    print("Thanks for playing!")

rock_paper_scissors()