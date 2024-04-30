from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json

num_now = 1394

with open("./setting.json", "r", encoding="utf-8") as setting_read:
    set_data = json.load(setting_read)

chrome_driver_path = "./chromedriver.exe" # 在此輸入chrome driver路徑
# driver = webdriver.Chrome()
driver = webdriver.Chrome(chrome_driver_path) # 不想手動下載chrome driver 可用上方程式 不過可能出現錯誤
driver.get("https://qe.fisp.com.tw/ep/login_stu.php")


while True:
    try:
        print(f"執行{num_now}31學號")
        # 登陸老師帳號
        time.sleep(0.1)
        teacher_mail = driver.find_element(by=By.ID, value="userAccount")
        teacher_click = driver.find_element(by=By.NAME, value="Submit")
        teacher_mail.send_keys(set_data["teacher_mail"])
        teacher_click.click()
        # 選擇個人資料
        select = Select(driver.find_element(by=By.ID, value="class_name"))
        select.select_by_index(1)
        ssid_num = driver.find_element(by=By.ID, value="s_sid")
        ssid_name = driver.find_element(by=By.ID, value="s_name")
        ssid_no = driver.find_element(by=By.ID, value="s_no")
        ssid_login = driver.find_element(by=By.NAME, value="Submit")
        ssid_num.send_keys(f"{num_now}31")
        ssid_name.send_keys(set_data["user_name"])
        ssid_no.send_keys("31")
        ssid_login.click()
        # 確認資料
        time.sleep(0.1)
        ssid_login = driver.find_element(by=By.NAME, value="Submit")
        ssid_login.click()
        # 輸入密碼
        ssid_pwd = driver.find_element(by=By.ID, value="s_passwd")
        ssid_pwd.send_keys(set_data["user_password"])
        ssid_login = driver.find_element(by=By.NAME, value="Submit")
        ssid_login.click()
        # 登出
        ssid_logout = driver.find_element(by=By.CLASS_NAME, value="logout")
        ssid_logout.click()
        ssid_login = driver.find_element(by=By.NAME, value="Submit")
        ssid_login.click()

        # 設定學號+1
        num_now += 1
    except:
        # 如視窗錯誤 或被關閉 重新開啟頁面
        print("發生錯誤 正在重啟")
        driver.get("https://qe.fisp.com.tw/ep/login_stu.php")