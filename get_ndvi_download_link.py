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
driver.get(r'https://www.gscloud.cn/sources/accessdata/345?pid=1')
time.sleep(3)


start = 'https://bjdl.gscloud.cn/sources/download/345/'
end = '?sid=MSasvPXy7ALzTPM7Zq21lX5mZjdzdVpOQTsJmXaesW5y2A&uid=617457'
links_list = []
names_list = []
for i in range(20):
    element = driver.find_elements(By.XPATH, "//table/tr/td[2]/div[@style='text-align: center;']")
    for i in element:
        i = i.text
        if i.startswith('MODND1M') and (i not in names_list):
            names_list.append(i)
            links_list.append(start + i + end)
    button = driver.find_element(By.XPATH, "//div/table/tr/td[10]")
    button.click()
    time.sleep(5)
# 新建一个文件, 用于存储下载链接
with open(r"/爬取/links/surtemp.txt", "w") as file:
    for item in links_list:
        if item.find('.LTD.AVG.V2'):
            file.write(item + "\n")

# with open(r"D:\pycharm_storage\DownScaling\爬取\surtemp.txt", "w") as file:
#     with open(r'D:\pycharm_storage\DownScaling\爬取\all_surtemp.txt', 'r') as f:
#         for line in f.readlines():
#             if 'LTD.AVG.V2' in line:
#                 file.write(line)






