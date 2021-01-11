import codecs
from common import Sentence, Instance
from config.reader import Reader
from unittest import TestCase

TEST_FILE_NAME = 'tests/data/test_reader.txt'

class ReaderTest(TestCase):
    def setUp(self):
        self.reader = Reader(digit2zero=False)
    
    def test_read_txt_one_doc(self):
        data = '''ฉัน<|>O
ชอบ<|>O
ใช้<|>O
iphone<|>B-PHONE

'''
        with codecs.open(TEST_FILE_NAME, 'w', 'utf-8') as f:
            f.write(data)
        
        result = self.reader.read_txt(TEST_FILE_NAME)
        self.assertListEqual(result[0].input.get_words(), ['ฉัน', 'ชอบ', 'ใช้', 'iphone'])
        self.assertListEqual(result[0].output, ['O', 'O', 'O', 'B-PHONE'])

    def test_read_txt_one_doc_multi_word(self):
        data = '''ฉัน<|>O
ชอบ<|>O
ใช้<|>O
iphone<|>B-PHONE
และ<|>O
Samsung<|>B-PHONE
Galaxy<|>I-PHONE
A6<|>I-PHONE
มาก<|>O

'''
        with codecs.open(TEST_FILE_NAME, 'w', 'utf-8') as f:
            f.write(data)
        
        result = self.reader.read_txt(TEST_FILE_NAME)
        self.assertListEqual(result[0].input.get_words(), ['ฉัน', 'ชอบ', 'ใช้', 'iphone', 'และ', 'Samsung', 'Galaxy', 'A6', 'มาก'])
        self.assertListEqual(result[0].output, ['O', 'O', 'O', 'B-PHONE', 'O', 'B-PHONE', 'I-PHONE', 'I-PHONE', 'O'])

    def test_read_txt_two_doc(self):
        data = '''ฉัน<|>O
ชอบ<|>O
ใช้<|>O
iphone<|>B-PHONE

สวัสดี<|>O

'''
        with codecs.open(TEST_FILE_NAME, 'w', 'utf-8') as f:
            f.write(data)
        
        result = self.reader.read_txt(TEST_FILE_NAME)
        self.assertListEqual([inst.input.get_words() for inst in result], [['ฉัน', 'ชอบ', 'ใช้', 'iphone'], ['สวัสดี']])
        self.assertListEqual([inst.output for inst in result], [['O', 'O', 'O', 'B-PHONE'], ['O']])