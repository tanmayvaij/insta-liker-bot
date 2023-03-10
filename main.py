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
loading_rounds = 0
limit = getenv("LIMIT")


if (limit == ""):
    print("Set a limit first")
    print("Exiting")
    exit(0)
else:
    loading_rounds = int(limit) // 12


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
            sleep(3)


    def get_followers(self): 

        try:
            # open window
            self.browser.get(f"https://www.instagram.com/{self.target}/followers")
            sleep(down_time)
        
        except:
            print("Enter target account first in config file and then retry")
            print("Exiting")
            exit(0)

        follower_window = "document.getElementsByClassName('_aano')[0]"

        # scrolling window for loading users in dom
        for _ in range(loading_rounds):
            self.browser.execute_script(f"{follower_window}.scrollBy(0, {follower_window}.scrollHeight)")
            sleep(down_time)

        lis  = self.browser.find_elements(By.CLASS_NAME, "_aarg")

        usernames = []

        for div in lis:
            spantags = div.find_element(By.TAG_NAME, "span")
            imgtags = spantags.find_element(By.TAG_NAME, "img")
            alt = imgtags.get_attribute("alt")
            usernames.append(alt.split("'")[0])

        print(f"Got stories with {len(usernames)} accounts")

        return usernames


    def like_story(self):

        counter = 0

        followers_list = self.get_followers()

        for username in followers_list:

            self.browser.get(f"https://www.instagram.com/{username}")
            sleep(down_time)
            sleep(3)

            try: 

                profile = self.browser.find_element(By.CLASS_NAME, "_aarf")
                profile.click()
                sleep(down_time)

                likebtn = self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[3]/div/div/div[2]/span/button")
                likebtn.click()

                counter += 1
                print(f"{counter}. Story of {username} liked")

                sleep(down_time)

            except:
                continue

        print(f"liked {counter} stories")


    def main(self):

        self.login()
        self.like_story()

        if self.cookies_exists == False:
            print(self.browser.get_cookies())


bot = InstaBot()
bot.main()
