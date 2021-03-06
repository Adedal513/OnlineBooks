import argparse
import requests
import os

from os.path import join
from urllib.parse import urlencode, urlsplit, unquote, urljoin
from textwrap import dedent


from typing import Union
from pathlib import Path
from bs4 import BeautifulSoup
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

    os.makedirs(folder, exist_ok=True)

    file_path = join(folder, filename)

    with open(file_path, 'wb') as write_path:
        write_path.write(response.content)

    return file_path


def parse_book_page(book_id: int) -> (str, str, str, [str], str):
    book_html_url = f'{BASE_URL}b{book_id}'
    book_response = requests.get(
        url=book_html_url
    )

    book_response.raise_for_status()
    check_for_redirect(book_response)

    soup = BeautifulSoup(book_response.text, 'lxml')

    title, author = soup.find('h1').text.split('::')
    image = soup.find('div', class_='bookimage').find('img')['src']

    comments = soup.find_all('div', class_='texts')
    genres = soup.find('span', class_='d_book').find_all('a')

    comments_serialized = [comment.find('span', class_='black').text for comment in comments]
    genres_serialized = [genre.text for genre in genres]

    return title.strip(), author.strip(), image, comments_serialized, genres_serialized


def download_txt(url: str, filename: str, folder: Union[str, Path], params=None) -> str:
    if params is None:
        params = {}

    response = requests.get(url=url, params=params)

    response.raise_for_status()
    check_for_redirect(response)

    filename_sanitized = sanitize_filename(filename) + '.txt'

    os.makedirs(folder, exist_ok=True)

    file_path = join(folder, filename_sanitized)

    with open(file_path, 'w') as write_path:
        write_path.write(response.text)

    return file_path


def check_for_redirect(response: requests.Response):
    if 302 in [link.status_code for link in response.history]:
        raise requests.exceptions.HTTPError


def download_book(book_id: int, only_parsing_mode: bool, silent_mode: bool) -> bool:
    params = {'id': book_id}
    txt_request_url = urljoin(BASE_URL, 'txt.php')

    title, author, image, comments_list, genres = parse_book_page(book_id)

    book_filename = f'{title} [{author}]'

    if not only_parsing_mode:
        download_txt(
            url=txt_request_url,
            filename=book_filename,
            folder=LIBRARY_FOLDER_NAME,
            params=params
        )

        cover_request_url = urljoin(BASE_URL, image)

        download_image(
            url=cover_request_url,
            folder=COVER_FOLDER_NAME,
            filename=title
        )

    if not silent_mode:
        book_description = f'''\
        ????????????????: {title}
        ??????????: {author}
        '''
        print(dedent(book_description))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="???????????????????? ???????? ?? ??????-?????????????? tululu.org")
    parser.add_argument('--start', help='start index', type=int, default=1)
    parser.add_argument('end', help='end index', type=int)
    parser.add_argument('--parse_only', help='to only show books info without downloading', action='store_true')
    parser.add_argument('--silent', help='Turn off description show', action='store_true')

    args = parser.parse_args()

    for book_id in range(args.start, args.end + 1):
        try:
            download_book(book_id, only_parsing_mode=args.parse_only, silent_mode=args.silent)
        except requests.exceptions.HTTPError:
            print(f'No book or cover with index {book_id} found :(')
            break
