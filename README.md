<h1 align="center">Музыкальный бот</h1>

# О проекте
Этот проект представляет собой музыкального телеграмм бота с использованием [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) и [Shazamio](https://pypi.org/project/shazamio/) 

Исходный код данного бота расположен на сервере ..., поэтому его можно запускать не клонируя репозиторий

## Библиотеки
 - shazamio==0.5.1
 - python-telegram-bot==21.0.1
 - ffmpeg-downloader==0.3.0
 - SQLAlchemy==2.0.29
 - pymorphy2==0.9.1

# Установка бота на свой компьютер

### Клонирование репозитория
```bash
git clone https://github.com/ivanefr/musical_bot.git
cd musical_bot
```
### Установка зависимостей 

```bash
pip install -r requirements.txt
```

Для полноценного запуска бота также необходимо установить [FFmpeg](https://ru.wikipedia.org/wiki/FFmpeg) в PATH
```bash
ffdl install --add-path
```
### Токен
в [данной строчке](https://github.com/ivanefr/musical_bot/blob/0660d99fc0fff6d66559ad9b087b989f2ab8d342/main.py#L126) поменяте значение токена на ваш собственный

### Запуск

```bash
python main.py
```

# Запуск бота
Для запуска следует отправить боту сообщение `/start`

Бота можно найти по [ссылке](https://t.me/MusicalYandexLyceumBot).

# Функции бота
Данный музыкальный бот позволит вам распознавать музыку, получать информацию о треке и многое другое.

Подробно о функциях можно узнать отправив боту команду `/help`

## Авторы проекта:
 - Ефремов Иван
 - Ерохин Алексей