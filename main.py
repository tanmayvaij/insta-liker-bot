from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path=".env")
down_time = 4

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

browser.get("https://www.instagram.com")
sleep(down_time)

username = browser.find_element(By.NAME, "username")
password = browser.find_element(By.NAME, "password")
submitbtn = browser.find_element(By.TAG_NAME, "button")

username.send_keys(getenv("INSTAGRAM_USERNAME"))
sleep(down_time)

password.send_keys(getenv("INSTAGRAM_PASSWORD"))
sleep(down_time)

submitbtn.click()
sleep(down_time)

browser.get("https://www.instagram.com/boatxaman/followers")
sleep(down_time)

follower_window = browser.find_element(By.CLASS_NAME, "_aano")
follower_window.click()
sleep(down_time)

for _ in range (2):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(down_time)

d = browser.find_elements(By.CLASS_NAME, "_ab8y")

for i in d:
    print(i.text)
