from bs4 import BeautifulSoup
from selenium import webdriver
import json, io
from selenium.webdriver.chrome.options import Options


def get_count(url): # Получаем количество страниц, которые удалось найти поисковику статей

    path = r'C:\\Users\\AlexWells\\Desktop\\Chromedriver'

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.get(url)

    generated_html = driver.page_source
    driver.quit()

    html_articles_search = BeautifulSoup(generated_html, 'html.parser')
    pageListHTML = html_articles_search.find('ul', {'class': 'paginator'}).find_all('a')
    count = 0

    for el in pageListHTML:
        count += 1

    return count


def get_content(url, count):
    path = r'C:\\Users\\AlexWells\\Desktop\\Chromedriver'
    result = []
    for q in range(1, count):

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path=path, options=options)

        driver.get(url + "&page=" + str(q))
        generated_html = driver.page_source
        driver.quit()

        html_articles_search = BeautifulSoup(generated_html, 'html.parser')
        articlesList = html_articles_search.find('ul', {'id':'search-results'})
        a_list = articlesList.find_all('li')

        for i in a_list:
            result.append({"name": i.find('h2', {'class':'title'}).get_text(),
                           "author": i.find('span').get_text(),
                           "magazine": i.find('span', {'class':'span-block'}).get_text()})
    return result


input_request = "JavaScript" #Наш запрос
url = "https://cyberleninka.ru/search?q=" + input_request #Ссылка с запросом

count_pages = get_count(url) # Получаем количество страниц
content = get_content(url, count_pages) #Получаем статьи со всех страниц

print("Запускаем скрапинг сайта, ожидайте...")

with io.open('data.json','w',encoding='utf-8') as f: #Выводим результат в Json файл
    json.dump(content, f, indent=4, ensure_ascii=False)

print("Завершено!")