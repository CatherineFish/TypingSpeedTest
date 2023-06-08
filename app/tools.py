"""Вспомогательные функции для генерации текста и расчета результатов."""

import re
import requests
from bs4 import BeautifulSoup


def generate_text(language, words_count, punct):
    """
    Генерирует текст на заданном языке с заданным количеством слов.

    Если флаг punct установлен в False, знаки пунктуации из текста удаляются.
    """
    if (language == 'en'):
        url = "https://generatefakename.com/text"
        data = ""
        for i in range(3):
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                data += soup.find_all('h3')[0].get_text() + " "

        if not punct:
            data = re.sub(r'[^\w\s]', ' ', data[:-1])

        test_text = " ".join(data.split()[:words_count])
    else:
        url = "https://fish-text.ru/get?&number=8"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['text']

            if not punct:
                data = re.sub(r'[^\w\s]', '', data)

            test_text = " ".join(data.split()[:words_count])
    return test_text


def calculate_result(test_text, user_text):
    """Рассчитывает точность ввода пользователя."""
    test_words = test_text.split()
    user_words = user_text.split()
    correct_words = [t for t, u in zip(test_words, user_words) if t == u]
    accuracy = len(correct_words) / len(test_words) * 100
    return accuracy


def calculate_cwpm(test_text, user_text, sec):
    """Рассчитывает скорость ввода пользователя в словах за минуту."""
    test_words = test_text.split()
    user_words = user_text.split()
    correct_words = [t for t, u in zip(test_words, user_words) if t == u]
    cwpm = len(correct_words) * 60 / sec
    return cwpm
