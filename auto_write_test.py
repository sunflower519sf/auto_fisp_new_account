from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json

with open("./setting.json", "r", encoding="utf-8") as setting_read:
    set_data = json.load(setting_read)

def options_convert_number(options_str):
    match options_str:
        case "A": return 0
        case "B": return 1
        case "C": return 2
        case "D": return 3
def question_search_ans(all_original_and_ans, question):
    for question_ans in all_original_and_ans:
        if question in question_ans[0]:
            return question_ans[1]
    print("查無此題")
def option_num_convert(option_num):
    match option_num:
        case 1: return 0
        case 3: return 1
        case 5: return 2
        case 7: return 3
chrome_driver_path = "./chromedriver.exe" # 在此輸入chrome driver路徑
# driver = webdriver.Chrome()
driver = webdriver.Chrome(chrome_driver_path) # 不想手動下載chrome driver 可用上方程式 不過可能出現錯誤
driver.get("https://qe.fisp.com.tw/ep/login_stu.php")

# 紀錄窗口句柄 切換頁面需要
current_window_handle = driver.current_window_handle

# 登入其他帳號取得答案
print(f"執行")
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
ssid_num.send_keys(f"139331")
ssid_name.send_keys("曾宇皓")
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
# 進入考卷並直接交卷
time.sleep(0.1)
exam_number = int(input("請輸入是第幾張考卷：")) - 1
enter_exam = driver.find_elements(by=By.NAME, value="button")
enter_exam[exam_number].click()
exam_submit = driver.find_element(by=By.NAME, value="Submit")
exam_submit .click()
# 點擊彈出提示框
alert = driver.switch_to.alert
alert.accept()
#點擊檢視改卷結果(取得答案用)
exam_look_ans = driver.find_element(by=By.CLASS_NAME, value="alink")
exam_look_ans .click()
# 取得答案 並存入變數
time.sleep(1)
all_window_handles = driver.window_handles

# 遍歷所有窗口 找到新窗口
for window_handle in all_window_handles:
    if window_handle != current_window_handle:
        # 切换到新窗口
        driver.switch_to.window(window_handle)
        break
# 提取題目+答案
question_original_data = driver.find_elements(by=By.CLASS_NAME, value="incorrect")
ans_original_data = driver.find_elements(by=By.CLASS_NAME, value="correctAnser")
all_original_and_ans = []
for data in range(len(question_original_data)):
    question_text = question_original_data[data].find_elements(by=By.TAG_NAME, value="td")[3].text.split("\n")
    ans_out = question_text[1].split()[options_convert_number(ans_original_data[data].text)][3:]
    all_original_and_ans.append([question_text[0], ans_out])
# print(all_original_and_ans)
# 返回頁面
driver.get("https://qe.fisp.com.tw/ep/login_stu.php") 
# 登出
ssid_logout = driver.find_element(by=By.CLASS_NAME, value="logout")
ssid_logout.click()
ssid_login = driver.find_element(by=By.NAME, value="Submit")
ssid_login.click()

# 開始作答
# 重新登錄作答帳號
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
ssid_num.send_keys(set_data["auto_exam_data"][0])
ssid_name.send_keys(set_data["auto_exam_data"][1])
ssid_no.send_keys(set_data["auto_exam_data"][2])
ssid_login.click()
# 確認資料
time.sleep(0.1)
ssid_login = driver.find_element(by=By.NAME, value="Submit")
ssid_login.click()
# 輸入密碼
ssid_pwd = driver.find_element(by=By.ID, value="s_passwd")
ssid_pwd.send_keys(set_data["auto_exam_data"][3])
ssid_login = driver.find_element(by=By.NAME, value="Submit")
ssid_login.click()

# 進入考卷
enter_exam = driver.find_elements(by=By.NAME, value="button")
enter_exam[exam_number].click()
# 取得題目和選項按鈕
question_original_data = driver.find_element(by=By.CLASS_NAME, value="question")
question_original_rows = question_original_data.find_elements(By.CSS_SELECTOR, value="tr[valign='top']")

choose_list = []
for data in question_original_rows:
    question_text_all = data.find_elements(by=By.TAG_NAME, value="td")[2].text.split("\n")
    end_ans = question_search_ans(all_original_and_ans, question_text_all[0])
    options_list = question_text_all[1].split()
    option_num = options_list.index(end_ans) # 1 3 5 7
    option_choose = option_num_convert(option_num)
    choose_list.append(option_choose)

option_ans_data = driver.find_elements(by=By.CLASS_NAME, value="radio-options")
for data in range(len(option_ans_data)):
    option_click = option_ans_data[data].find_elements(by=By.TAG_NAME, value="label")[choose_list[data]]
    option_click.click()
input()