import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
from time import sleep

parser = argparse.ArgumentParser()

parser.add_argument("-e", "--Email", required=True, help="The email of the groupme account you want to log in with")
parser.add_argument("-p", "--Password", required=True, help="The password of the groupme account you want to log in with")
parser.add_argument("-n", "--Name", required=True, help="The name of the groupme chat you want to Thanos snap")
parser.add_argument("-m", "--Message", default="I am inevitable.", help="The message you want to send to the groupme chat.")
parser.add_argument("-s", "--Safenames", default="", help="A comma-separated list of names you want to be safe from snapping (add your name and the admin names, since they can't be kicked and will screw up the code)")

args = parser.parse_args()

driver = webdriver.Chrome()
achain = ActionChains(driver)
scrollscript = "arguments[0].scrollIntoView();"
driver.get("https://groupme.com")

# Log In

driver.implicitly_wait(10)
signin_btn = driver.find_element(by=By.CSS_SELECTOR, value=".login-wrap.svelte-1pxnud7 > a")
signin_btn.click()

driver.implicitly_wait(10)
uname_inp = driver.find_element(by=By.ID, value = "usernameInput")
uname_inp.send_keys(args.Email)
pword_inp = driver.find_element(by=By.ID, value = "passwordInput")
pword_inp.send_keys(args.Password)
submit_btn = driver.find_element(by=By.CSS_SELECTOR, value="[type='submit']")
submit_btn.click()


# get correct chat
# chat_name = "test group"
chat_name = args.Name

possible_chat_buttons = driver.find_elements(by=By.CSS_SELECTOR, value="button[data-v-532f8ef2]")
for btn in possible_chat_buttons:
    name_el = btn.find_element(by=By.CLASS_NAME, value="chat-name")
    if name_el.text == chat_name:
        name_el.click()

# send the message of doom
message_box = driver.find_element(by=By.CLASS_NAME, value="emoji-wysiwyg-editor")
message_box.send_keys(args.Message)
message_box.send_keys(Keys.ENTER)

# open the menu of doom
menu_button = driver.find_element(by=By.CLASS_NAME, value="chat-name-container")
menu_button.click()

members_sec_btn = driver.find_element(by= By.CSS_SELECTOR, value="button.members.section")
members_sec_btn.click()

# do the dew
safe_names = args.Safenames.split(",")

driver.implicitly_wait(10)
members_divs = driver.find_elements(by=By.CSS_SELECTOR, value="div.member")
num_deleted = 0
i = 0
while i + num_deleted < len(members_divs):
    try:
        mdiv = driver.find_elements(by=By.CSS_SELECTOR, value="div.member")[i]
        print("JUDGING", mdiv.find_element(by=By.CSS_SELECTOR, value="h5 > span").text)
        if mdiv.find_element(by=By.CSS_SELECTOR, value="h5 > span").text in safe_names:
            print (mdiv.find_element(by=By.CSS_SELECTOR, value="h5 > span").text, "safe")
            i += 1
        elif random.random() > 0.5:
            print (mdiv.find_element(by=By.CSS_SELECTOR, value="h5 > span").text, "gone")
            driver.execute_script(scrollscript, mdiv)
            achain.move_to_element(mdiv).perform()
            mdiv.find_element(by=By.CSS_SELECTOR, value="button[aria-label='Remove Member']").click()
            driver.find_element(by=By.CSS_SELECTOR, value=".modal-content .btn-primary").click()
            num_deleted += 1
            # i += 1
            sleep(5)
        else:
            print (mdiv.find_element(by=By.CSS_SELECTOR, value="h5 > span").text, "spared")
            i += 1
    except:
        print("oops, whatever")
        i +=1


a = input("")

driver.quit()