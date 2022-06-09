import requests
import os

from typing import Union
from pathlib import Path


BOOK_URL = 'https://tululu.org/txt.php'
DIRECTORY_NAME = './Library'


def download_book(book_id: int) -> str:
    params = {
        'id': book_id
    }

    book_response = requests.get(
        url=BOOK_URL,
        params=params
    )

    book_response.raise_for_status()

    return book_response.text


def write_book_to_directory(book_id: int, book_text: str, directory_path: Union[str, Path]) -> bool:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_name = f'id{book_id}.txt'

    with open(directory_path + '/' + file_name, 'w') as book_file:
        book_file.write(book_text)

    return True


if __name__ == '__main__':

    for book_id in range(1, 11):
        book_text = download_book(book_id)

        write_book_to_directory(
            book_id=book_id,
            book_text=book_text,
            directory_path=DIRECTORY_NAME
        )
