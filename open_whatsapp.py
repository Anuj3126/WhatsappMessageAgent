from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gemini import create_agent, get_response
import time

# ==== CONFIGURATION ====
TARGET_NAME = "Mom"
REPLIED_CONTACTS = set()

# ==== SETUP CHROME ====
options = Options()
options.add_argument(r"--user-data-dir=C:\\Users\\Anuj Tewari\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument(r'--profile-directory=Default')

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")
print("🚀 Loading WhatsApp Web...")

time.sleep(15)
print("✅ WhatsApp Web loaded!")

# ==== MAIN LOOP ====
agent = create_agent()
while True:
    try:
        unread_chats = driver.find_elements(By.XPATH, "//*[@id='pane-side']/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/span[1]/div[2]/span")

        for chat in unread_chats:
            try:
                chat.click()
                time.sleep(2)

                chat_name = driver.find_element(By.XPATH, "//*[@id='pane-side']/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/span").text
                print(f"📨 Message from: {chat_name}")

                if chat_name == TARGET_NAME and chat_name not in REPLIED_CONTACTS:
                    print("✅ Target matched! Fetching last message...")

                    last_message = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            '(//div[@data-pre-plain-text])[last()]//span[@class="_ao3e selectable-text copyable-text"]/span'
                        ))
                    ).text
                    print(f"💬 Last message: {last_message}")

                    DEFAULT_REPLY = get_response(agent, last_message)
                    message_box = driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p")
                    message_box.send_keys(DEFAULT_REPLY + Keys.ENTER)

                    print("✉️ Auto-reply sent!")
                    REPLIED_CONTACTS.add(1)

                    time.sleep(1)
                    reset_button_1 = driver.find_element(By.XPATH, "//*[@id='app']/div/div[3]/div/header/div/div/div/div/span/div/div[1]/div[2]/button")
                    reset_button_1.click()
                    time.sleep(1)
                    reset_button_2 = driver.find_element(By.XPATH, "//*[@id='app']/div/div[3]/div/header/div/div/div/div/span/div/div[1]/div[1]/button")
                    reset_button_2.click()
                    print("🔙 Chat reset. Back to chat list.")

                else:
                    print("⏩ Not target contact or already replied.")
                    message_box = driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p")
                    message_box.send_keys("Something went wrong  :(" + Keys.ENTER)

            except Exception as inner_error:
                print("⚠️ Error inside loop:", inner_error)
                message_box = driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p")
                message_box.send_keys("Something went wrong  :(" + Keys.ENTER)

        time.sleep(5)

    except Exception as outer_error:
        print("⚠️ Error in main loop:", outer_error)
        time.sleep(5)

#------------------------------------------------------------------------

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# import time

# # ==== CONFIGURATION ====
# TARGET_NAME = "Mom"  # Contact name to auto-reply
# REPLIED_CONTACTS = set()  # Keeps track of whom you already replied to

# # ==== SETUP CHROME ====
# options = Options()
# options.add_argument(r"--user-data-dir=C:\\Users\\Anuj Tewari\\AppData\\Local\\Google\\Chrome\\User Data")
# options.add_argument(r'--profile-directory=Default')

# driver = webdriver.Chrome(options=options)
# driver.get("https://web.whatsapp.com")
# print("🚀 Loading WhatsApp Web...")

# # Wait for QR scan or session to load
# time.sleep(15)
# print("✅ WhatsApp Web loaded!")

# # ==== MAIN LOOP ====
# while True:
#     try:
#         # Use the updated XPath for unread messages (green dot)
#         unread_chats = driver.find_elements(By.XPATH, "//*[@id='pane-side']/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/span[1]/div[2]/span")

#         for chat in unread_chats:
#             try:
#                 chat.click()
#                 time.sleep(2)

#                 # Get current chat name using the provided XPath
#                 chat_name = driver.find_element(By.XPATH, "//*[@id='pane-side']/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/span").text
#                 print(f"📨 Message from: {chat_name}")

#                 if chat_name == TARGET_NAME and chat_name not in REPLIED_CONTACTS:
#                     print("✅ Target matched! Sending auto-reply...")
#                     DEFAULT_REPLY = f"Hi {chat_name},\nThis is an auto-generated text! Can't reach the phone now. Will get back to you!"

#                     # Wait for input box and send reply
#                     message_box = driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p")
#                     message_box.send_keys(DEFAULT_REPLY + Keys.ENTER)

#                     print("✉️ Auto-reply sent!")
#                     REPLIED_CONTACTS.add(1)  # Mark as replied

#                     # Wait a bit before navigating back to reset the chat
#                     time.sleep(1)

#                     # Click the first button to open the chat menu
#                     reset_button_1 = driver.find_element(By.XPATH, "//*[@id='app']/div/div[3]/div/header/div/div/div/div/span/div/div[1]/div[2]/button")
#                     reset_button_1.click()
#                     time.sleep(1)

#                     # Click the second button to reset the chat or go back
#                     reset_button_2 = driver.find_element(By.XPATH, "//*[@id='app']/div/div[3]/div/header/div/div/div/div/span/div/div[1]/div[1]/button")
#                     reset_button_2.click()
#                     print("🔙 Chat reset. Back to chat list.")

#                 else:
#                     print("⏩ Not target contact or already replied.")

#             except Exception as inner_error:
#                 print("⚠️ Error inside loop:", inner_error)

#         # Refresh the unread chats by waiting before starting the next iteration
#         time.sleep(5)

#     except Exception as outer_error:
#         print("⚠️ Error in main loop:", outer_error)
#         time.sleep(5)



#------------------------------------------------------------------------
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # Set up Chrome options
# options = Options()
# options.add_argument(r"--user-data-dir=C:\\Users\\Anuj Tewari\\AppData\\Local\\Google\\Chrome\\User Data")  # This makes it persistent between sessions
# options.add_argument(r"--profile-directory=Default")
# # Start the WebDriver
# driver = webdriver.Chrome(options=options)

# # Open WhatsApp Web
# print("🚀 Opening WhatsApp Web...")
# driver.get("https://web.whatsapp.com/")

# # Wait for WhatsApp Web to fully load
# WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div/div/div')))  # Search box XPath
# print("✅ WhatsApp Web loaded!")

# # Wait for the search bar to appear (Using the provided XPath)
# search_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div/div/div')))
# search_box.click()

# # Type "Mom" into the search box and hit Enter
# search_box.send_keys("Ninja Niraj")
# search_box.send_keys(Keys.RETURN)

# # Wait for the chat to load
# time.sleep(3)  # Adjust the sleep time if needed

# # Find the last message in the chat (Using the correct XPath)
# try:
#     last_message = WebDriverWait(driver, 30).until(
#         EC.presence_of_element_located((
#             By.XPATH,
#             '(//div[@data-pre-plain-text])[last()]//span[@class="_ao3e selectable-text copyable-text"]/span'
#         ))
#     )
#     message_text = last_message.text
#     print(f"Last message from Mom: {message_text}")
# except Exception as e:
#     print("Failed to retrieve the last message:", e)

# # Close the driver
# driver.quit()
