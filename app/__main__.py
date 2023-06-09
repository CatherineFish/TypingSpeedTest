"""
Это приложение Flask, которое обслуживает две страницы.

Каждая страница выполняет специфическую функцию, связанную с обработкой текста.
"""

from flask import Flask, request
import os
from flask_babel import Babel
import urllib3
from .pages import post_page, get_page

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECRET_KEY = os.urandom(32)


def get_locale():
    """
    Получает локаль из переменной среды.

    По умолчанию 'en_US.UTF-8', если не указана.
    Возвращает только первые два символа локали.
    """
    return os.environ.get('LC_ALL', 'en_US.UTF-8')[:2]


app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.config['SECRET_KEY'] = SECRET_KEY
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Обслуживает страницу 'home.html'.

    Если метод запроса POST, обрабатывает форму и возвращает результат.
    Если метод запроса GET, возвращает страницу 'home.html'.
    """
    if request.method == 'POST':
        return post_page('home.html', 'result.html')

    if request.method == 'GET':
        return get_page('home.html')


@app.route('/home2', methods=['GET', 'POST'])
def maxWordFixedTime():
    """
    Обслуживает страницу 'maxWordFixedTime.html'.

    Если метод запроса POST, обрабатывает форму и возвращает результат.
    Если метод запроса GET, возвращает страницу 'maxWordFixedTime.html'.
    """
    if request.method == 'POST':
        return post_page('maxWordFixedTime.html', 'result2.html')

    if request.method == 'GET':
        return get_page('maxWordFixedTime.html')


if __name__ == '__main__':
    app.run(debug=True)
