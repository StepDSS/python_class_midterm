import time
from okx_api import get_price

def make_a_log(action):
    with open("logs.txt", "a") as f:
        f.write(action + "\n")

def get_last_score(username):
    try:
        with open("logs.txt", "r") as f:
            lines = f.readlines()
        for line in reversed(lines):
            if line.startswith(f"{username} - Final Score:"):
                return int(line.split(":")[-1].strip())
    except FileNotFoundError:
        pass
    return 0

def game():
    print("Welcome to the Jungle! (game)")
    username = input("Enter your name: ").strip()

    last_score = get_last_score(username)
    if last_score != 0:
        print(f"Welcome back, {username}! Your last score was: {last_score}")
        reset = input("Do you want to reset your score? (yes/no): ").strip().lower()
        if reset == "yes":
            last_score = 0
            print("Your score now 0.")
    else:
        print(f"Hello, {username}! Let's begin.")

    score = last_score
    c_streak = 0
    w_streak = 0

    print("""Choose from the following assets:
1. Bitcoin (type 'btc')
2. Ethereum (type 'eth')
3. Litecoin (type 'ltc')
Type 'exit' to quit the game.""")

    easy_input = {
        "btc": "BTC-USDT",
        "eth": "ETH-USDT",
        "ltc": "LTC-USDT"
    }

    while True:
        asset_choose = input("Select an asset (btc/eth/ltc): ").strip().lower()

        if asset_choose == "exit":
            print(f"Exiting the game. Final Score: {score}")
            make_a_log(f"{username} - Final Score: {score}")
            break

        if asset_choose not in easy_input:
            print("Wrong choice. Type 'btc', 'eth', or 'ltc'.")
            continue

        asset = easy_input[asset_choose]
        print(f"Chosen asset: {asset_choose.upper()}!")

        while True:
            current_price = get_price(asset)
            if current_price is None:
                print("Problem getting the price, try again.")
                break

            print(f"Current {asset_choose.upper()} Price: ${current_price:.2f}")

            guess = input("Will the price go up, down, or stay the same? (type 'up', 'down', 'same', 'change'(to change the asset), 'exit'(to finish the game)): ").strip().lower()
            if guess == "exit":
                print(f"Exiting the game. Final Score: {score}")
                make_a_log(f"{username} - Final Score: {score}")
                return

            if guess == "change":
                print("Back to selection...\n")
                break

            if guess not in ["up", "down", "same"]:
                print("Invalid choice. Please type 'up', 'down', or 'same'.")
                continue

            print("Waiting for 5 seconds...")
            time.sleep(5)

            new_price = get_price(asset)
            if new_price is None:
                print("Problem getting the price. Try again.")
                break

            print(f"New {asset_choose.upper()} Price: ${new_price:.2f}")

            if guess == "up" and new_price > current_price:
                c_streak += 1
                w_streak = 0
                points = 10 + (c_streak - 1)
                score += points
                print(f"Right! You earned {points} points. Total score: {score}")
            elif guess == "down" and new_price < current_price:
                c_streak += 1
                w_streak = 0
                points = 10 + (c_streak - 1)
                score += points
                print(f"Right! You earned {points} points. Total score: {score}")
            elif guess == "same" and new_price == current_price:
                c_streak += 1
                w_streak = 0
                points = 10 + (c_streak - 1)
                score += points
                print(f"Right! You earned {points} points. Total score: {score}")
            else:
                w_streak += 1
                c_streak = 0
                points = 10 + (w_streak - 1)
                score -= points
                print(f"Wrong! You lost {points} points. Total score: {score}")

if __name__ == "__main__":
    game()