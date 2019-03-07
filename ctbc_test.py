#import ticket_module as m
import cv2
from selenium import webdriver
from time import sleep
import pytesseract
#import re
#----↓ 開啟高鐵購票網站 ↓----#
url = 'https://www.win168.com.tw/ctsweb/WebLogin.aspx'
driver=webdriver.Chrome()
driver.get(url)
#m.input_ticket_info(driver) # 輸入購票資訊
is_success = False          # 用來判斷是否輸入驗證碼成功
#----↓ 嘗試破解驗證碼 20 次 ↓----#
for t in range(20):
    if is_success: # 判斷是否輸入驗證碼成功
        #m.input_train_and_person(driver) # 輸入購票人資訊
        break     # 如果輸入驗證碼成功, 離開 t 迴圈
    print(f'----第{t+1}次----')
    #----↓ 操作網頁元素 ↓----#
    imgurl = driver.find_element_by_id('captcha').get_attribute('src')
    imgurl2 = imgurl
# =============================================================================
#     print('imgurl:',imgurl)
#     while(imgurl == imgurl2):   #等待驗證圖更換完成
#         try:
#             imgurl2 = driver.find_element_by_id(
#                       'BookingS1Form_homeCaptcha_passCode').get_attribute('src')
#             print('imgurl2:',imgurl2)
#         except:
#             pass     # pass 表示不做事
#             print(f'----pass----')
#         sleep(0.5)  # 暫停一下
# =============================================================================
    captcha_tag = driver.find_element_by_id('captcha')      # 驗證碼圖片元素
    print(f'captcha_tag')    
    while(captcha_tag.size['width'] < 50 or         #等待圖檔載入完成
          captcha_tag.size['width'] > 180 ):
        pass    # pass 表示不做事
    captcha_tag.screenshot('captcha.png')           # 儲存驗證碼圖片
    #----↓ 驗證碼圖片的影像處理 ↓----#
    wrong = []    # 存放 ocr 辨識結果的 list (錯誤的驗證碼)
    img = cv2.imread('captcha.png')  
    print(f'----img----')# 讀取驗證碼圖片
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoise = cv2.fastNlMeansDenoising(img, h=50)
    cv2.imwrite('denoise.png', denoise)
    #ret, thresh = cv2.threshold(denoise,127,255,cv2.THRESH_BINARY_INV)
    ocr_txt = pytesseract.image_to_string(denoise)   # 對影像進行 OCR 文字辨識
    print('ocr結果', ocr_txt)
    key = ocr_txt   # 英文字轉大寫並將數字與英文取代成空字串
    print('key:',key)
    if len(key) != 5:
        continue
    #----↓ OCR 有辨識結果 ↓----#
    #key = re.sub(r'[0O]', 'Q', key)   #將 0 或 O 替換為 Q (因驗證碼中不會有0或O)
    #if key not in wrong:  # 不要重複輸入錯的驗證碼
    print('輸入驗證碼：',key)
    driver.find_element_by_id('txtLoginID').send_keys('A127831242')
    driver.find_element_by_id('txtPassword').send_keys('1q2w3e4r')
    driver.find_element_by_id('ImageCodeTextBox').send_keys(key)  # 輸入驗證碼    
    sleep(5)
    driver.find_element_by_id('btnLogin').click() # 按下查詢按鈕
    sleep(5)
    try:
            is_success = True
            print('驗證成功')
            break       # 驗證成功, 離開 b 迴圈
    except:
        print('驗證失敗')
        wrong.append(key) # 將錯的驗證碼存入清單
