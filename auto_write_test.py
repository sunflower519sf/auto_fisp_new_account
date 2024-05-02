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
def question_search_ans(all_original_and_ans, question, choose_id):
    question_check = True
    question_str = ""
    for question_ans in all_original_and_ans:
        # if question in question_ans[0]:
        #     if question_check:
        #         question_str = question_ans[1]
        #         question_check = False
        #     else:
        original_id = question_ans[2]
        if choose_id == original_id:
            question_str = question_ans[1]
            return question_str
        # else:
        #     question_str = ""
        # print("重複題目")
    
def option_num_convert(option_num):
    match option_num:
        case 1: return 0
        case 3: return 1
        case 5: return 2
        case 7: return 3
def segmentation_ans(ans:str):
    ans_original_a = ans.split(" (B)")
    ans_a = ans_original_a[0][3:]
    ans_original_b = ans_original_a[1].split(" (C)")
    ans_b = ans_original_b[0]
    ans_original_c = ans_original_b[1].split(" (D)")
    ans_c = ans_original_c[0]
    ans_d = ans_original_c[1]
    return [ans_a, ans_b, ans_c, ans_d]
chrome_driver_path = "./chromedriver.exe" # 在此輸入chrome driver路徑
driver = webdriver.Chrome()
# driver = webdriver.Chrome(chrome_driver_path) # 不想手動下載chrome driver 可用上方程式 不過可能出現錯誤
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
ssid_num.send_keys(f"149331")
ssid_name.send_keys("曾宇皓")
ssid_no.send_keys("31")
ssid_login.click()
# 確認資料
time.sleep(0.1)
ssid_login = driver.find_element(by=By.NAME, value="Submit")
ssid_login.click()
# 輸入密碼
ssid_pwd = driver.find_element(by=By.ID, value="s_passwd")
ssid_pwd.send_keys("123")
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
all_window_handles = driver.window_handles # driver定位到新頁面

# 遍歷所有窗口 找到新窗口
for window_handle in all_window_handles:
    if window_handle != current_window_handle:
        # 切换到新窗口
        driver.switch_to.window(window_handle)
        break
# 提取題目+答案
time.sleep(1)
question_original_data = driver.find_elements(by=By.CLASS_NAME, value="incorrect")
all_original_and_ans = []
for data in question_original_data:
    ans_original_data = data.find_element(by=By.CLASS_NAME, value="correctAnser")
    question_text = data.find_elements(by=By.TAG_NAME, value="td")[3].text.split(f" = {ans_original_data.text})\n")
    ans_out =segmentation_ans(question_text[1])[options_convert_number(ans_original_data.text)]
    all_original_and_ans.append([question_text[0], ans_out, question_text[0].rsplit("(")[1]])
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
time.sleep(0.1)
question_original_data = driver.find_element(by=By.CLASS_NAME, value="question")
question_original_rows = question_original_data.find_elements(By.CSS_SELECTOR, value="tr[valign='top']")

run_error_num = 0
for data in question_original_rows:
    
    # 抓取題目
    answer_pos = data.find_elements(by=By.TAG_NAME, value="td")
    question_text_all = answer_pos[2].text.split("\n")
    # 題目取得答案
    options_choose = answer_pos[1].find_elements(by=By.CSS_SELECTOR, value=f"label")
    choose_id = options_choose[0].find_elements(by=By.TAG_NAME, value="input")[0].get_attribute("data-id")
    end_ans = question_search_ans(all_original_and_ans, question_text_all[0], choose_id)
    # 取得選項
    options_txt_list = answer_pos[2].find_elements(by=By.CLASS_NAME, value="content")
    options_txt = [data.text for data in options_txt_list]
    for option_data in options_txt:
        if end_ans in option_data:
            option_choose = options_txt.index(option_data)
            break
    else:
        print("查無資料")

    # 點擊選項
    options_fill = options_choose[option_choose]
    options_fill.click()
    print(question_text_all[0], end_ans)

input("點擊ENTER交卷繼續")
# 交卷
exam_submit = driver.find_element(by=By.NAME, value="Submit")
exam_submit .click()
# 點擊彈出提示框
alert = driver.switch_to.alert
alert.accept()

input("您可以使用ctrl+c結束或按下ENTER結束")