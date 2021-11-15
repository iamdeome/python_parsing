import string
import os
import requests
from bs4 import BeautifulSoup


def page(link):
    re = requests.get(link)
    soup = BeautifulSoup(re.content, 'html.parser')
    return soup


number_of_page = int(input())
requested_type = input()
type_classes = {'new': 'c-article-body', 'research highlight': 'article-item__body'}

i = int(1)
while i <= number_of_page:
    url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={i}"
    directory = f'Page_{i}'

    if not os.path.exists(directory):
        os.makedirs(directory)

    articles = page(url).findAll("article")

    for item in articles:
        article_type = item.find("span", attrs={"data-test": "article.type"})
        article_link = item.find('a', {'data-track-action': 'view article'})
        tail = article_link.get('href')

        if article_type.text.strip() == requested_type:
            file_name = article_link.text.translate(str.maketrans(' ', '_', string.punctuation))

            created_file = open(f"{directory}/{file_name}.txt", 'w', encoding='UTF-8')
            subpage = page(f"https://www.nature.com{tail}")
            body = subpage.find("div", attrs={"class": "c-article-body"})
            created_file.write(body.text)
            created_file.close()
    i += 1


