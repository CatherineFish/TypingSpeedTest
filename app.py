from flask import Flask, render_template, request
import re
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, RadioField
import os
from flask_babel import Babel, lazy_gettext as _, force_locale
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECRET_KEY = os.urandom(32)


curr_language = 'en'
words_count = 40
punctuation = False
sec = 60
test_text = ""

def generate_text(language, words_count, punct):
    if (language == 'en'):
        url = "https://generatefakename.com/text"
        data = ""
        for i in range(3):
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                data += soup.find_all('h3')[0].get_text() + " "

        if not punct:
            data = re.sub(r'[^\w\s]', '', data[:-1])

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


def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

class Buttons(FlaskForm):
    language = SelectField(_('Language'),
                           choices=[('ru', 'Русский'),('en', 'English')],
                           default='en')
    punct = BooleanField(_('Punctuation'), default=False)
    word = RadioField(_('Word Count'),
                      choices=[(10, 10), (40, 40), (100, 100)],
                      default=40)
    sec = RadioField(_('Seconds'),
                      choices=[(10, 10), (30, 30), (60, 60)],
                      default=60)
    


@app.route('/home', methods=['GET', 'POST'])
def home():
    global curr_language, punctuation, words_count, test_text
    
    if request.method == 'POST':
        buttons = Buttons(request.form)
        new_language = str(buttons.language.data)
        new_punctuation = bool(buttons.punct.data)
        new_word_cnt = int(buttons.word.data)
        if (request.form.get('submit_button') != None):
            user_text = request.form['user_text']
            result = calculate_result(test_text, user_text)
            return render_template('result.html', result=round(result, 2),
                                                  user_words=user_text.split(),
                                                  correct_words=test_text.split(),
                                                  time=request.form['submit_button'], 
                                                  entered_words_number=len(user_text.split()))
                
        if (new_language != curr_language
                    or new_punctuation != punctuation
                    or new_word_cnt != words_count):
            curr_language = new_language
            punctuation = new_punctuation
            words_count = new_word_cnt
            test_text = generate_text(curr_language, words_count, punctuation)
            return render_template('home.html',
                                        title=_('Print Speed Test'),
                                        instruction=_('Type the following text as quickly and accurately as you can:'),
                                        label_input = _('Your input:'),
                                        submit_button = _('Submit'),
                                        test_text=test_text,
                                        buttons=buttons)
        

    if request.method == 'GET':
        buttons = Buttons(request.form)
        test_text = generate_text(curr_language, words_count, punctuation)
        return render_template('home.html',
                                        title=_("Print Speed Test"),
                                        instruction=_("Type the following text as quickly and accurately as you can:"),
                                        label_input = _("Your input:"),
                                        submit_button = _("Submit"),
                                        test_text=test_text,
                                        buttons=buttons)

@app.route('/home2', methods=['GET', 'POST'])
def maxWordFixedTime():
    global curr_language, punctuation, sec, test_text
    
    if request.method == 'POST':
        buttons = Buttons(request.form)
        new_language = str(buttons.language.data)
        new_punctuation = bool(buttons.punct.data)
        new_sec = int(buttons.sec.data)
        if (request.form.get('submit_button') != None):
            user_text = request.form['user_text']
            result = calculate_result(test_text, user_text)
            return render_template('result2.html', result=round(result, 2),
                                                  user_words=user_text.split(),
                                                  correct_words=test_text.split(),
                                                  time=sec, 
                                                  entered_words_number=len(user_text.split()))

        if (new_language != curr_language
                    or new_punctuation != punctuation
                    or new_sec != sec):
            curr_language = new_language
            punctuation = new_punctuation
            sec = new_sec
            test_text = generate_text(curr_language, 40, punctuation)
            with force_locale(curr_language):
                return render_template('maxWordFixedTime.html',
                                        title=_('Print Speed Test'),
                                        instruction=_('Type the following text as quickly and accurately as you can:'),
                                        label_input = _('Your input:'),
                                        submit_button = _('Submit'),
                                        test_text=test_text,
                                        buttons=buttons,
                                        sec=sec)
        print("HERE")        
        # test_text = request.form['test_text'] ## No .form['test_text'] in 'POST'
        user_text = request.form['user_text']
        result = calculate_result(test_text, user_text)
        return render_template('result2.html', result=result)

    if request.method == 'GET':
        buttons = Buttons(request.form)
        test_text = generate_text(curr_language, 100, punctuation)
        with force_locale(curr_language):
            return render_template('maxWordFixedTime.html',
                                        title=_("Print Speed Test"),
                                        instruction=_("Type the following text as quickly and accurately as you can:"),
                                        label_input = _("Your input:"),
                                        submit_button = _("Submit"),
                                        test_text=test_text,
                                        buttons=buttons,
                                        sec=sec)

@app.route('/result2', methods=['GET', 'POST'])
def result():
    return "result2"

def calculate_result(test_text, user_text):
    test_words = test_text.split()
    user_words = user_text.split()
    correct_words = [t for t, u in zip(test_words, user_words) if t == u]
    accuracy = len(correct_words) / len(test_words) * 100
    return accuracy

if __name__ == '__main__':
    app.run(debug=True)
