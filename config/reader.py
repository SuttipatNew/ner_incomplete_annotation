# 
# @author: Allan
#

from tqdm import tqdm
from common import Sentence, Instance
from typing import List
import re


class Reader:

    def __init__(self, digit2zero:bool=True):
        """
        Read the dataset into Instance
        :param digit2zero: convert the digits into 0, which is a common practice for LSTM-CRF.
        """
        self.digit2zero = digit2zero
        self.vocab = set()

    def read_txt(self, file: str, number: int = -1) -> List[Instance]:
        print("Reading file: " + file)
        insts = []
        with open(file, 'r', encoding='utf-8') as f:
            words = []
            labels = []
            for line in tqdm(f.readlines()):
                line = line.rstrip()
                if line == "":
                    inst = Instance(Sentence(words), labels)
                    inst.set_id(len(insts))
                    insts.append(inst)
                    words = []
                    labels = []
                    if len(insts) == number:
                        break
                    continue
                word, label = line.split('<|>')
                if self.digit2zero:
                    word = re.sub('\d', '0', word) # replace digit with 0.
                words.append(word)
                self.vocab.add(word)
                labels.append(label)
        print("number of sentences: {}".format(len(insts)))
        return insts



