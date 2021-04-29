import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


filename = 'kaktus_parse.json'
data_list = []


def start():
    with open(filename, 'w') as f1:
        pass
    
def save_to_json(data):
    a = json.dumps(data, ensure_ascii=False)
    with open(filename, 'a') as f:
        f.write(f'{a}\n' )

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'
    }
    response = requests.get(url, headers=headers)
    return response.text

def get_description(link):
    lin = get_html(link)
    soup = BeautifulSoup(lin, 'lxml')
    description = soup.find('div', class_='BbCode').text.replace('\n', '').replace('"', '\'')
    return description

def parsing_kaktus(html):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find('div', class_="Tag--articles").find_all('div', class_="Tag--article")[:10]
    count=0
    for new in news:
        count+=1
        try:
            title = new.find('a', class_='ArticleItem--name').text.strip()
        except:
            title = 'no title'
        
        try:
            photo = new.find('a', class_='ArticleItem--image').find('img').get('data-src')
        
        except Exception as e:
            print(e)
        
        try:
            link = new.find('a', class_='ArticleItem--name').get('href')
        except:
            link = 'no link'
        
        try:
            description = get_description(link)
        except:
            description = 'no description'
        data = {'count':count, 'title': title, 'link': link, 'photo': photo, 'description': description}
        if count>16:
            pass
        else:
            data_list.append(data)
        # save_to_json(data)

    return data_list


def main():
    date = str(datetime.now())[:15]
    url = f'https://kaktus.media/?date={date}&lable=8&order=time'
    start()
    data_list.clear()
    return parsing_kaktus(get_html(url))


main()

