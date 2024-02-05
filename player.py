from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import chess
import chess.engine
import time
import random


def make_stockfish_move(board):
    with chess.engine.SimpleEngine.popen_uci("./stockfish_8_x64") as engine:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        return result.move


def add_randomness(move):
    random_offset = random.randint(-2, 2)
    return chess.Move(
        from_square=move.from_square, to_square=move.to_square + random_offset
    )


service = Service(executable_path="./chromedriver")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/ ")

driver.find_element(By.ID, "username").send_keys("YOUR_USERNAME")
driver.find_element(By.ID, "password").send_keys("YOUR_PASSWORD")
driver.find_element(By.ID, "login").click()

time.sleep(5)

driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[4]/div[1]/div/a[1]").click()

board = chess.Board()

for _ in range(10):
    stockfish_move = make_stockfish_move(board)

    random_move = add_randomness(stockfish_move)

    square_id = f"square-{random_move.from_square}{random_move.to_square}"
    driver.find_element(By.ID, square_id).click()

    board.push(random_move)

    time.sleep(2)

driver.quit()
