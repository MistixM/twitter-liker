from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore

from getpass import getpass

import time
import pickle
import os

def main():
    global login_via_cookie
    # Print hello message
    print_log(Fore.GREEN, Fore.WHITE, "Hi there! I'm Like bot. I'll like all posts from the specified hashtag in Twitter.")
    
    login_via_cookie = False

    # In infinite loop check for input
    while True:
        hashtag = input(f"{Fore.GREEN}>{Fore.WHITE} Please provide a hashtag (without '#' symbol): ")
        
        if hashtag and hashtag != '#':
            break
        else:
            print_log(Fore.RED, Fore.WHITE, "You entered incorrect hashtag. Please, provide correct one!")

    # If all set, start work with Twitter
    print_log(Fore.GREEN, Fore.WHITE, "Got it! Now logging in to Twitter..")
    
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    if os.path.exists(f"{os.getcwd()}/cookies.pkl"):
        driver.get(f"https://x.com/search?q=%23{hashtag}&src=typeahead_click")

        print_log(Fore.GREEN, Fore.WHITE, "Cookie exists. Logging via cookies")
        driver.delete_all_cookies()

        cookies = pickle.load(open(f"{os.getcwd()}/cookies.pkl", "rb"))
        
        for cookie in cookies:
            driver.add_cookie(cookie)

        time.sleep(0.5)
        
        login_via_cookie = True
        driver.refresh()
    else:
        print_log(Fore.RED, Fore.WHITE, "Cookie file does not exist.. Start register prompt..")        
        
        while True:
            username_text = input(f"{Fore.GREEN}>{Fore.WHITE} Please provide username: ")
            password_text = getpass(f"{Fore.GREEN}>{Fore.WHITE} Please provide password (Invisible password entry field for security purposes): ")

            print_log(Fore.GREEN, Fore.WHITE, "Got all required information. Please stand by..")
            driver.get('https://twitter.com/i/flow/login')

            try:
                print_log(Fore.GREEN, Fore.WHITE, "Login form opened..")
                # Locate username input field
                username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete=username]')))
                time.sleep(2)
                username.send_keys(username_text) # Insert username

                # Locate continue button
                continue_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=button].r-13qz1uu')))
                continue_button.click()

                # Locate password input field
                password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[type=password]')))
                time.sleep(2)
                password.send_keys(password_text) # Insert password

                print_log(Fore.GREEN, Fore.WHITE, "Information inserted successfully.. Continue..")
                # Locate continue button and then click
                continue_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid*=Login_Button]')))
                continue_button.click()

                break

            except Exception as e:
                print_log(Fore.RED, Fore.WHITE, f"Unable to login to Twitter! Double check your data and try again.")

    print_log(Fore.GREEN, Fore.WHITE, "You're all set! Preparing posts to like..")
    
    # Wait a bit
    time.sleep(5)

    # When registered, save cookie
    driver.get(f'https://x.com/search?q=%23{hashtag}&src=typeahead_click&f=live')
    
    if not login_via_cookie:
        print_log(Fore.GREEN, Fore.WHITE, "Cookies saved!")
        pickle.dump(driver.get_cookies(), open(os.getcwd() + '/cookies.pkl', 'wb'))

    time.sleep(2)

    print_log(Fore.GREEN, Fore.WHITE, "Start liking.. Close console to finish liking")
    
    liked = 0
    while True:
        like_buttons = driver.find_elements(By.XPATH, "//button[@data-testid='like' and contains(@aria-label, 'Like')]")
        try:
            like_buttons[0].click()
            liked += 1
            print_log(Fore.GREEN, Fore.WHITE, f"You've already liked: {liked}", end='\r')

        except Exception as e:
            driver.refresh()

        time.sleep(15)
        driver.refresh()
        time.sleep(5)

def print_log(first_c, second_c, log, end='\n'):
    print(f"{first_c}>{second_c} {log}", end=end)

if __name__ == '__main__':
    main()