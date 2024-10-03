import os
import string
import requests
from bs4 import BeautifulSoup
from http import HTTPStatus

number_of_page = int(input("Enter the number of pages: "))
article_type = input("Enter the article type: ").lower()
try:
    for page in range (1, number_of_page + 1):
        url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page}'

        response = requests.get(url)
        if response.status_code == HTTPStatus.OK:

            directory_name = f'Page_{page}'
            os.makedirs(directory_name, exist_ok=True)
            soup = BeautifulSoup(response.content, 'html.parser')

            articles = soup.find_all('article')

            for article in articles:
                article_search = article.find('span', {'data-test': 'article.type'}).text.lower()
                if article_search == article_type:

                    link = article.find('a', {'data-track-action': 'view article'})['href']

                    complete_link = 'https://www.nature.com' + link

                    article_response = requests.get(complete_link)

                    if article_response.status_code == HTTPStatus.OK:

                        article_soup = BeautifulSoup(article_response.content, 'html.parser')
                        title = article_soup.find('h1', {"class": "c-article-magazine-title"}).text
                        body = article_soup.find('p', {"class": "article__teaser"}).text

                        valid_filename = ''.join(char for char in title if char not in string.punctuation)
                        valid_filename = valid_filename.replace(' ', '_')

                        file_path = os.path.join(directory_name, f'{valid_filename}.txt')

                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(body)
                        print(f'The article "{valid_filename}" has been saved.')

                    else:
                        print(f'The URL returned {article_response.status_code}!')


        else:
            print(f'The URL returned {response.status_code}!')

    print('Saved all articles.')
except Exception as e:
    print(e)