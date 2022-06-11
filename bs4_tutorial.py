from requests import get
from bs4 import BeautifulSoup


BASE_URL = 'https://tululu.org'
id = 70684

book = get(
    url=f'{BASE_URL}/b{id}'
)

soup = BeautifulSoup(book.text, 'lxml')
title = soup.find('h1').text.split('::')[0].strip()
author = soup.find('h1').text.split('::')[1].strip()

image = soup.find('div', class_='bookimage').find('img')['src']

desc = soup.find('table', class_='d_book').find('td').text

print(title)
print(author)
print(f'{BASE_URL}{image}')
print(desc)