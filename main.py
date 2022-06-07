from selenium import webdriver
import keyboard
import time
from selenium.webdriver.common.by import By

browser = webdriver.Chrome('/Users/sathwikdoddi/Desktop/chromedriver')

guesses = []
with open('possible_guesses.txt', "r") as g:
    for line in g:
        guesses.append(line.strip())

def evaluate_and_filter():
    last_non_null = ""
    arr = []
    game_app = browser.find_element(By.TAG_NAME, "game-app")
    game = browser.execute_script("return arguments[0].shadowRoot.getElementById('game')", game_app)
    rows = game.find_elements(By.TAG_NAME, "game-row")
    for row in rows:
        arr.append(row.get_attribute("letters"))
        if row.get_attribute("letters") != "":
            last_non_null = row.get_attribute("letters")
    current_row = rows[arr.index(last_non_null)]
    root = browser.execute_script("return arguments[0].shadowRoot.querySelector('div')", current_row)
    tiles = root.find_elements(By.TAG_NAME, "game-tile")
    for tile in tiles:
        evaluation = tile.get_attribute("evaluation")
        letter = tile.get_attribute("letter")
        if evaluation.strip() == "absent":
            guesses[:] = [guess for guess in guesses if guess.find(letter) == -1]
            print(len(guesses))
        elif evaluation.strip() == "present":
            # for guess in guesses:
            #     if guess.find(letter) == -1:
            #         guesses.remove(guess)
            #     elif guess.find(letter) == last_non_null.find(letter):
            #         guesses.remove(guess)
            guesses[:] = [guess for guess in guesses if guess.find(letter) > -1 and guess.find(letter) != last_non_null.find(letter)]
            print(len(guesses))
        else:
            # for guess in guesses:
            #     if guess.find(letter) != last_non_null.find(letter):
            #         guesses.remove(guess)
            guesses[:] = [guess for guess in guesses if guess.find(letter) == last_non_null.find(letter)]
    return guesses[0]

def enter_guess(word):
    keyboard.write(word, delay=0.05)
    keyboard.press_and_release('enter')

def main():
    browser.get("https://www.nytimes.com/games/wordle/index.html")
    keyboard.wait("enter")
    time.sleep(2)
    enter_guess("salet")
    time.sleep(2)
    enter_guess(evaluate_and_filter())
    time.sleep(2)
    enter_guess(evaluate_and_filter())
    time.sleep(2)
    enter_guess(evaluate_and_filter())
    time.sleep(2)
    enter_guess(evaluate_and_filter())

if __name__ == '__main__':
    main()