from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json

num_now = 1394

driver = webdriver.Chrome()
driver.get("https://qe.fisp.com.tw/ep/login_stu.php")


while True:
    print(f"執行{num_now}31學號")
    time.sleep(0.1)
    teacher_mail = driver.find_element(by=By.ID, value="userAccount")
    teacher_click = driver.find_element(by=By.NAME, value="Submit")
    teacher_mail.send_keys("samuel951753@gmail.com")
    teacher_click.click()

    select = Select(driver.find_element(by=By.ID, value="class_name"))
    select.select_by_index(1)

    ssid_num = driver.find_element(by=By.ID, value="s_sid")
    ssid_name = driver.find_element(by=By.ID, value="s_name")
    ssid_no = driver.find_element(by=By.ID, value="s_no")
    ssid_login = driver.find_element(by=By.NAME, value="Submit")
    ssid_num.send_keys(f"{num_now}31")
    ssid_name.send_keys("曾宇小皓皓")
    ssid_no.send_keys("31")
    ssid_login.click()
    time.sleep(0.1)
    ssid_login = driver.find_element(by=By.NAME, value="Submit")
    ssid_login.click()
    ssid_pwd = driver.find_element(by=By.ID, value="s_passwd")
    ssid_pwd.send_keys("123")
    ssid_login = driver.find_element(by=By.NAME, value="Submit")
    ssid_login.click()
    ssid_logout = driver.find_element(by=By.CLASS_NAME, value="logout")
    ssid_logout.click()
    ssid_login = driver.find_element(by=By.NAME, value="Submit")
    ssid_login.click()

    num_now += 1
