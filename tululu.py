import urllib.parse

import requests
import os

from os.path import join

from typing import Union
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlsplit, unquote
from pathvalidate import sanitize_filename


BASE_URL = 'https://tululu.org/'
LIBRARY_FOLDER_NAME = './Library'
COVER_FOLDER_NAME = './Covers'


def download_image(url: str, folder: Union[str, Path], filename='') -> str:
    file_format = urlsplit(unquote(url)).path.split('/')[-1].split('.')[-1]

    if not filename:
        filename = urlsplit(unquote(url)).path.split('/')[-1].split('.')[0]
    else:
        filename = sanitize_filename(filename) + '.' + file_format

    response = requests.get(url=url)
    response.raise_for_status()
    check_for_redirect(response)

    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = join(folder, filename)

    with open(file_path, 'wb') as write_path:
        write_path.write(response.content)

    return file_path


def parse_book_credentials(book_id: int) -> (str, str, str, [str]):
    book_response = requests.get(
        url=f'{BASE_URL}b{book_id}'
    )

    book_response.raise_for_status()
    check_for_redirect(book_response)

    soup = BeautifulSoup(book_response.text, 'lxml')

    title = soup.find('h1').text.split('::')[0].strip()
    author = soup.find('h1').text.split('::')[1].strip()
    image = soup.find('div', class_='bookimage').find('img')['src']
    comments_list = [comment.find('span', class_='black').text for comment in soup.find_all('div', class_='texts')]

    return title, author, image, comments_list


def download_txt(url: str, filename: str, folder: Union[str, Path]) -> str:
    response = requests.get(url=url)

    response.raise_for_status()
    check_for_redirect(response)

    filename_sanitized = sanitize_filename(filename) + '.txt'

    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = join(folder, filename_sanitized)

    with open(file_path, 'w') as write_path:
        write_path.write(response.text)

    return file_path


def check_for_redirect(response: requests.Response):
    if any([link.status_code == 302 for link in response.history]):
        raise requests.exceptions.HTTPError


def download_book(book_id: int) -> bool:
    params = {'id': book_id}
    txt_request_url = f'{BASE_URL}txt.php?' + urlencode(params)

    try:
        title, author, image, comments_list = parse_book_credentials(book_id)
        book_filename = f'{title} [{author}]'

        download_txt(
            url=txt_request_url,
            filename=book_filename,
            folder=LIBRARY_FOLDER_NAME
        )

        cover_request_url = f'{BASE_URL}{image}'

        download_image(
            url=cover_request_url,
            folder=COVER_FOLDER_NAME,
            filename=title
        )

    except requests.exceptions.HTTPError:
        print(f'No book or cover with index {book_id} found :(')
        return False

    return True


if __name__ == '__main__':

    for book_id in range(11):
        download_book(book_id)