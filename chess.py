from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chess
import chess.engine
import time
import random

def make_stockfish_move(board):
    with chess.engine.SimpleEngine.popen_uci("stockfish") as engine:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        return result.move

def add_randomness(move):
    # Introduce a random factor to the move
    random_offset = random.randint(-2, 2)
    return chess.Move(from_square=move.from_square, to_square=move.to_square + random_offset)

# Set the path to the downloaded chromedriver executable
chromedriver_path = "/usr/local/bin/chromedriver"

# Create a Chrome WebDriver instance
driver = webdriver.Chrome(executable_path=chromedriver_path)

# Navigate to the chess website
driver.get("https://www.chess.com")

# Perform login (replace USERNAME and PASSWORD with your credentials)
driver.find_element_by_id("username").send_keys("YOUR_USERNAME")
driver.find_element_by_id("password").send_keys("YOUR_PASSWORD")
driver.find_element_by_id("login").click()

# Wait for the page to load
time.sleep(5)

# Initialize a chess board
board = chess.Board()

# Perform an example game loop with Stockfish and randomness
for _ in range(10):  # Replace with the desired number of moves
    # Make a move with Stockfish
    stockfish_move = make_stockfish_move(board)

    # Add randomness to the move
    random_move = add_randomness(stockfish_move)

    # Perform the modified move on the chess website
    square_id = f"square-{random_move.from_square}{random_move.to_square}"
    driver.find_element_by_id(square_id).click()

    # Update the internal board representation
    board.push(random_move)

    # Wait for the website to update (adjust sleep time as needed)
    time.sleep(2)

# Close the browser
driver.quit()