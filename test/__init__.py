import sys
import os
import unittest
import re

testdir = os.path.dirname(__file__)
srcdir = '../app'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from tools import generate_text, calculate_result
sys.path.remove(os.path.abspath(os.path.join(testdir, srcdir)))

punct = re.compile(r"[^\w\s]")
ru = re.compile(r"[^A-Яа-я\s]")
en = re.compile(r"[^A-Za-z\s]")

class TestGenTest(unittest.TestCase):

    def test_0_ru(self):
        text = generate_text("ru", 10, False)
        self.assertFalse(re.findall(ru, text))

    def test_1_en(self):
        text = generate_text("en", 10, False)
        self.assertFalse(re.findall(en, text))

    def test_2_10(self):
        text = generate_text("ru", 10, False)
        self.assertEqual(len(text.split()), 10)

    def test_3_40(self):
        text = generate_text("ru", 40, False)
        self.assertEqual(len(text.split()), 40)


    def test_4_100(self):
        text = generate_text("ru", 100, False)
        self.assertEqual(len(text.split()), 100)

    
    def test_5_false(self):
        text = generate_text("ru", 10, False)
        self.assertFalse(re.findall(punct, text))

    def test_6_true(self):
        text = generate_text("ru", 10, True)
        self.assertTrue(re.findall(punct, text))

class TestCalcResult(unittest.TestCase):

    def setUp(self):
        self.test_text = '''
            King added in a furious passion and went back to
        '''

    def test_0_0(self):
        user_text = ""
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 0)

    def test_1_some_val(self):
        user_text = "King added in a furious"
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 50)

    def test_2_wrong_case(self):
        user_text = "king added in a furious"
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 40)

    def test_3_some_mistakes(self):
        user_text = "king adde In a furious and went back to"
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 20)


    def test_4_perfect(self):
        user_text = self.test_text
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 100)

    
    def test_5_too_much(self):
        user_text = self.test_text + "extra word"
        res = calculate_result(self.test_text, user_text)
        self.assertEqual(res, 0.8)
