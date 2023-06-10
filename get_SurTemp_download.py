# @炒茄子  2023-03-29

from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = webdriver.Edge(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe')
driver.get(r'https://www.gscloud.cn/accounts/login_user')

email = driver.find_element(By.ID, "email")
email.send_keys('3223758990@qq.com') #账号
password = driver.find_element(By.ID, "password")
password.send_keys('qweqwe510928') #密码

captcha = driver.find_element(By.ID, "id_captcha_1")
captcha_sj = input('请输入验证码：').strip()
captcha.send_keys(captcha_sj)

driver.find_element(By.ID, "btn-login").click() #输入验证码后点击登入按钮
time.sleep(3)
driver.get(r'https://www.gscloud.cn/sources/accessdata/336?pid=1')  # 进入地表温度下载页面
time.sleep(3)

start = "https://bjdl.gscloud.cn/sources/download/336/"
end = "?sid=2SavFC9bu_C2wrsE7p-tR9rxvxOkp41dEeLzUvF235kpYQ&uid=617457"
links_list = []
names_list = []
for i in range(90):
    element = driver.find_elements(By.XPATH, "//table/tr/td[2]/div[@style='text-align: center;']")
    for i in element:
        i = i.text
        if i.startswith('MODLT1M') and (i not in names_list):
            names_list.append(i)
            links_list.append(start + i + end)
    button = driver.find_element(By.XPATH, "//div/table/tr/td[10]")
    button.click()
    time.sleep(5)
# 新建一个文件, 用于存储下载链接
with open(r'links/all_surtemp.txt', 'w') as f:
    for i in links_list:
        f.write(i + '\n')






