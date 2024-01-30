from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from dotenv import load_dotenv
from os import getenv
from cookies import cookies

load_dotenv(dotenv_path="config.env")
down_time = 4

class InstaBot:

    def __init__(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.target = getenv("TARGET_USERNAME")
        self.cookies_exists = False

    def set_cookies_in_browser(self):
        if cookies != []:
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            self.cookies_exists = True

    def login(self):

        self.browser.get("https://www.instagram.com")

        self.set_cookies_in_browser()

        sleep(down_time)

        if self.cookies_exists == False:

            username = self.browser.find_element(By.NAME, "username")
            password = self.browser.find_element(By.NAME, "password")
            submitbtn = self.browser.find_element(By.TAG_NAME, "button")

            try:
                username.send_keys(getenv("INSTAGRAM_USERNAME"))
                sleep(down_time)

                password.send_keys(getenv("INSTAGRAM_PASSWORD"))
                sleep(down_time)
            
            except:
                print("Enter username, password in config file first and then retry")
                print("Exiting")
                exit()

            submitbtn.click()
            
            sleep(down_time)


    def main(self):
        self.login()

        if self.cookies_exists == False:
            print(self.browser.get_cookies())


bot = InstaBot()
bot.main()
