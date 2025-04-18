from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from gemini2 import create_agent, get_response
import time


options = Options()
options.add_argument(r"--user-data-dir=C:\\Users\\Anuj Tewari\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument(r'--profile-directory=Default')

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")
print("🚀 Loading WhatsApp Web...")
time.sleep(15)
print("✅ WhatsApp Web loaded!")
wait = WebDriverWait(driver, 100)
agent = create_agent()
target = 'Mom'
contact = driver.find_element(By.XPATH, f"//span[@title='{target}']")
contact.click()
while True:
    userInput = input("Enter what to send:")
    reply = get_response(agent, userInput)
    box = driver.find_element(By.XPATH, "//*[@id='main']/footer//p")
    box.send_keys(reply + Keys.ENTER)