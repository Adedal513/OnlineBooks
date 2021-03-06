# Tululu Script

Утилита скачивает книги c веб-ресурса [tululu.org](https://tululu.org/) в формате .txt, а также обложки к ним

##  Установка и настройка

---

Для работы скрипта необходим установленный `Python3`. Клонируйте репозиторий и перейдите в корневую папку проекта,
а затем используйте `pip` или `pip3` для установки зависимостей:
```shell
pip install -r requirements.txt
```

## Использование

---

Для работы скрипту требуются два **обязательных** аргумента: 
- `id` начальной книги
- `id` конечной книги

Помимо обязательных, утилита также использует **опциональные флаги**:
- `--silent`: Отключить вывод названий и авторов книг при скачивании
- `--parse_only`: Не скачивать книги, только выводить информацию о них

Утилита скачает все книги в текстовом формате в папку `Library`, а обложки - в `Covers`. 
В случае, если какую-то книгу или обложку найти не удастся, скрипт выведет соответствующее сообщение и продолжит работу.

### Пример:
Скачаем книги с 45-й по 46-ю:
```shell
user@user$ python tululu.py 45 46
```
Краткая информация о скачанных книгах выведена в консоль:
```shell
Название: Экономический смысл американской агрессии
Автор: Глазьев Сергей

Название: Экономика, политика, общество (Новые реалии России, Сборник научных трудов)
Автор: Автор неизвестен

```

В случае, если книги не существует, будет выведено сообщение:
```shell
user@user$ python tululu.py 2 3 

No book or cover with index 2 found :(
...
```
