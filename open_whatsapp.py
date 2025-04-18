# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from gemini import create_agent, get_response
# import time

# # ==== CONFIGURATION ====
# TARGET_NAME = "Mom"
# REPLIED_CONTACTS = set()

# # ==== SETUP CHROME ====
# options = Options()
# options.add_argument(r"--user-data-dir=C:\\Users\\Anuj Tewari\\AppData\\Local\\Google\\Chrome\\User Data")
# options.add_argument(r'--profile-directory=Default')

# driver = webdriver.Chrome(options=options)
# driver.get("https://web.whatsapp.com")
# print("🚀 Loading WhatsApp Web...")

# time.sleep(15)
# print("✅ WhatsApp Web loaded!")

# # ==== MAIN LOOP ====
# agent = create_agent()
# while True:
#     try:
#         unread_chats = driver.find_elements(By.XPATH, "//*[@id='pane-side']/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/span[1]/div[2]/span")

#         for chat in unread_chats:
#             try:
#                 chat.click()
#                 time.sleep(2)

#                 chat_name = driver.find_element(By.XPATH, "//*[@id='pane-side']/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/span").text
#                 print(f"📨 Message from: {chat_name}")

#                 if chat_name == TARGET_NAME and chat_name not in REPLIED_CONTACTS:
#                     print("✅ Target matched! Fetching last message...")

#                     last_message = WebDriverWait(driver, 30).until(
#                         EC.presence_of_element_located((
#                             By.XPATH,
#                             '(//div[@data-pre-plain-text])[last()]//span[@class="_ao3e selectable-text copyable-text"]/span'
#                         ))
#                     ).text
#                     print(f"💬 Last message: {last_message}")

#                     DEFAULT_REPLY = get_response(agent, last_message)
#                     message_box = driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p")
#                     message_box.send_keys(DEFAULT_REPLY + Keys.ENTER)

#                     print("✉️ Auto-reply sent!")
#                     REPLIED_CONTACTS.add(1)

#                     time.sleep(1)
#                     reset_button_1 = driver.find_element(By.XPATH, "//*[@id='app']/div/div[3]/div/header/div/div/div/div/span/div/div[1]/div[2]/button")
#                     reset_button_1.click()
#                     time.sleep(1)
#                     reset_button_2 = driver.find_element(By.XPATH, "//*[@id='app']/div/div[3]/div/header/div/div/div/div/span/div/div[1]/div[1]/button")
#                     reset_button_2.click()
#                     print("🔙 Chat reset. Back to chat list.")

#                 else:
#                     print("⏩ Not target contact or already replied.")
#                     message_box = driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p")
#                     message_box.send_keys("Something went wrong  :(" + Keys.ENTER)

#             except Exception as inner_error:
#                 print("⚠️ Error inside loop:", inner_error)
#                 message_box = driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p")
#                 message_box.send_keys("Something went wrong  :(" + Keys.ENTER)

#         time.sleep(5)

#     except Exception as outer_error:
#         print("⚠️ Error in main loop:", outer_error)
#         time.sleep(5)

#-----------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from gemini import create_agent, get_response
import time

# ==== CONFIGURATION ====
TARGET_NAMES = {
    "Mom",
    "Dad",
    "Ninja Niraj",
    "TripTime",
    "Anuj"
}
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

# ==== SETUP GEMINI AGENT ====
agent = create_agent()

# ==== MAIN LOOP ====
while True:
    try:
        print("🔍 Scanning top 5 chats for unread…")
        for i in range(1, 6):
            base_xpath = f"//*[@id='pane-side']/div[2]/div/div/div[{i}]"
            # badge xpath
            badge_xpath = f"{base_xpath}/div/div/div/div[2]/div[2]/div[2]/span[1]/div[2]/span"
            try:
                unreadChat = driver.find_element(By.XPATH, badge_xpath)
            except NoSuchElementException:
                continue  # no unread badge here

            # unread found → get chat name
            name_xpath = f"{base_xpath}/div/div/div/div[2]/div[1]/div[1]/div/div/span"
            chat_name = driver.find_element(By.XPATH, name_xpath).text.strip()
            print(f"📨 Unread chat [{i}]: {chat_name}")

            # only handle targets not yet replied
            if chat_name not in TARGET_NAMES or chat_name in REPLIED_CONTACTS:
                print("⏩ Skip (not in list or already replied).")
                continue

            # open chat
            time.sleep(2)
            unreadChat.click()

            # collect all message bubbles
            elems = driver.find_elements(By.XPATH, '//div[@data-pre-plain-text]')
            msg_data = []
            for e in elems:
                pre = e.get_attribute("data-pre-plain-text")
                text = e.find_element(
                    By.XPATH,
                    './/span[@class="_ao3e selectable-text copyable-text"]/span'
                ).text
                print(f"pre:{pre}\ntext:{text}\n--------")
                msg_data.append((pre, text))

            # find last "You:" index
            last_you_idx = -1
            for idx, (pre, _) in enumerate(msg_data):
                if "Anuj:" in pre:
                    last_you_idx = idx

            # gather new incoming messages
            new_msgs = [
                text for (pre, text) in msg_data[last_you_idx + 1 :]
                if "You:" not in pre
            ]
            print(f"💬 New msgs since your last reply: {new_msgs}")

            # reply to each
            for incoming in new_msgs:
                reply = get_response(agent, incoming)
                box = driver.find_element(By.XPATH, "//*[@id='main']/footer//p")
                box.send_keys(reply + Keys.ENTER)
                time.sleep(1)

            REPLIED_CONTACTS.add(1)
            print(f"✅ Replied to {chat_name}")

            # reset chat view via your two‑button flow
            reset1 = driver.find_element(
                By.XPATH,
                "//*[@id='app']/div/div[3]/div/header/div/div/div/div/span/div/div[1]/div[2]/button"
            )
            reset1.click()
            time.sleep(0.5)
            reset2 = driver.find_element(
                By.XPATH,
                "//*[@id='app']/div/div[3]/div/header/div/div/div/div/span/div/div[1]/div[1]/button"
            )
            reset2.click()
            print("🔙 Back to chat list.")

        time.sleep(5)

    except Exception as e:
        print("⚠️ Main loop error:", e)
        time.sleep(5)



# -----------------------------------------------------------------------

