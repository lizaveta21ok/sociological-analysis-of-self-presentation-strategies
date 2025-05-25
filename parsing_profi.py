from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

import pandas as pd
import time


def uploading_url():
    print('Начинаю выгрузку url-адрессов профилей психологов')
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

    pause = 1
    url = 'https://profi.ru/repetitor/psihologia/?seamless=1&tabName=PROFILES'
    driver.get(url)

    # Общее количество данных
    elements = int(driver.find_element(By.XPATH, '//*[@id="page"]/div/main/div/div/div[1]/div/ul/li[3]/span/span').text)

    number = 20 
    possibility = len(driver.find_elements(By.XPATH, '//*[@class="ui_1hi7c"]'))
    print(f'Должно быть {number} профилей на страннице, смогу выгрузить {possibility}')

    while number < 50:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3 * pause)
        driver.find_element(By.XPATH, '//*[@id="page"]/div/main/div/div/div[2]/div[2]/div/button').click()
        time.sleep(5 * pause)
        number = number + 20
        possibility = len(driver.find_elements(By.XPATH, '//*[@class="ui_1hi7c"]'))
        print(f'Выгружено {number} профилей на страннице, смогу выгрузить {possibility}')
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    print(f'Удалось найти {possibility} профилей психологов')
    print('Закончил прокручивать страницу. Увидел все доступные профили на данный момент')

    print('Начал выделять url для дальнейшего парсинга')
    links = driver.find_elements(By.XPATH, '//*[@class="ui_1hi7c"]')
    url_psy = []
    for link in links:
        url_psy.append(link.get_attribute('href'))
    print(f'Всего профилей {len(url_psy)} для дальнейшего анализа')
    url_psy = list(map(lambda x: x.split('profileId=')[1], url_psy))
    print('Сохранил все url!')

    print('Сохраняю в файл Excel')
    df = pd.DataFrame({'url_psychologist' : url_psy})
    df = df.drop_duplicates('url_psychologist', ignore_index = True)
    df.to_excel('url_psychologist.xlsx')
    print('Создал Excel-файл с url-психологами. Закончил с этой частью выгрузки')

name = []
rating = []
count_reviews = []
very_positive = []
passport = []
video = []
all_info = []
qualification = []
count_photo = []
docs = []
services_prices = []
reviews = []
errors = []

def downloading_characteristics():
    '''
    Выгрузка характеристик у каждого профиля
    '''
    df = pd.read_excel('url_psychologist.xlsx', index_col = 0)
    url_psy = df['url_psychologist'].tolist()
    url_psy = url_psy[:5]

    print('Началась выгрузка всех характеристик')
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    pause = 2 # для паузы

    n = 1 # для визуализации
    for link in url_psy:
        try:
            url = 'https://profi.ru/repetitor/psihologia/?seamless=1&tabName=PROFILES&profileTabName=reviews&profileId=' + link
            driver.get(url)
            name.append(driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/h1').text)

            try:
                driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/span').text
                if driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/span').text == 'Нет отзывов':
                    rating.append(0)
                else:
                    rating.append(float((driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/span').text).replace(',', '.')))
            except:
                rating.append(0)
        
        
            try:
                driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/span').text
                if driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/span').text == 'Нет отзывов':
                    count_reviews.append(0)
                else:
                    count_reviews.append(int((driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/a').text).split(' ')[0]))
            except:
                count_reviews.append(0)
                
                
            try:
                very_positive.append(driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div[2]').text)
            except:
                very_positive.append('')

            try:
                passport.append(driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[2]/div/div/div[1]/a').text)
            except:
                passport.append('')

            try:
                video.append(driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[2]/div/a/span[2]').text)
            except:
                video.append('')

            try:
                all_info.append(driver.find_element(By.XPATH, '//*[@id="assembledInfo"]').text)
            except:
                all_info.append('')

            try:
                qualification.append(driver.find_element(By.XPATH, '//*[@id="certification-info"]/div/span[2]').text)
            except:
                qualification.append('')
                
            try:
                count_photo.append(int(driver.find_element(By.XPATH, '//*[@id="media"]/h3/span').text))
            except:
                count_photo.append(0)

            try:
                docs.append(int(driver.find_element(By.XPATH, '//*[@id="documents"]/h3/span').text))
            except:
                docs.append(0)

            # скроллинг и открытие всей области, где прописаны предлагаемые услуги и цены
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="prices"]/div/div/a/span/span'))).click()
            except:
                f'пропуск'    
            
            try:
                services_prices.append(driver.find_element(By.XPATH, '//*[@id="prices"]').text)
            except:
                services_prices.append('')

            # отзывы (может быть вообще в отдельный датафрейм)
            try:
                driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/span').text
                if driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/span').text == 'Нет отзывов':
                    count_reviews1 = 0
                else:
                    count_reviews1 = int((driver.find_element(By.XPATH, '//*[@id="about"]/div[1]/div[2]/div[1]/div/a').text).split(' ')[0])
            except:
                count_reviews1 = 0
                
            quantity = 10
            while quantity < count_reviews1:
                try:
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    try:
                        driver.find_element(By.XPATH, '//*[@id="fullProfile"]/div/div/div[2]/div[4]/div[2]/div/div[5]/span/a').click()
                    except:
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fullProfile"]/div/div/div[2]/div[4]/div[3]/div/div[5]/span/a'))).click()
                except:
                    f'-'
                time.sleep(3 * pause)
                quantity += 10
            
            try:
                reviews.append(driver.find_element(By.XPATH, '//*[@id="fullProfile"]/div/div/div[2]/div[4]').text)
            except:
                reviews.append('')

        except:
            errors.append(link)
            print(f'Возникла ошибка в url:{link}')
            
            name.append('')
            rating.append('')
            count_reviews.append('')
            very_positive.append('')
            passport.append('')
            video.append('')
            all_info.append('')
            qualification.append('')
            count_photo.append('')
            docs.append('')
            services_prices.append('')
            reviews.append('')

        print(f'Выгрузил {n} профилей')
        n += 1

def save_to_dataframe():
    '''
    Запись данных в датафрейм
    '''
    print('Записываю в датафрейм')

    df = pd.read_excel('url_psychologist.xlsx', index_col = 0)
    url_psy = df['url_psychologist'].tolist()
    url_psy = url_psy[:5]

    new_df = pd.DataFrame({'url_psy' : url_psy, 
                       'name' : name, 
                       'rating' : rating,
                       'count_reviews' : count_reviews,
                       'very_positive' : very_positive,
                       'passport' : passport,
                       'video' : video,
                       'all_info': all_info,
                       'qualification' : qualification,
                       'count_photo' : count_photo,
                       'docs' : docs,
                       'services_prices' : services_prices,
                       'reviews' : reviews})
    new_df.to_excel('complete_1500_max.xlsx')
    
    if len(errors) > 0:
        errors_df = pd.DataFrame({'errors' : errors})
        errors_df.to_excel('error.xlsx')
        print(f'Было найдено {len(errors)} ошибок')
    else:
        print('Ошибок не было найдено!')
    
    print('Я закончил')

def main():
    uploading_url()
    downloading_characteristics()
    save_to_dataframe()

main()

