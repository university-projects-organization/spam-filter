import os
from corpus import Corpus
from utils import read_classification_from_file
from tokenization import Tokenization

SPAM = "SPAM"
HAM = "OK"


class TrainingCorpus:

    def __init__(self, path):
        self.folder_path = path
        self.email_names = {}

    # function read mail status from '!truth.txt'
    def rate_names(self):
        my_filenames = os.listdir(self.folder_path)
        for file_name in my_filenames:
            if file_name[0] == '!' and file_name[1] == 't':
                file_path = os.path.join(self.folder_path, file_name)
                self.email_names = read_classification_from_file(file_path)
                break

    # function returns mail status from '!truth.txt'
    def get_status(self, email_name):
        return self.email_names[email_name]

    # function returns multiplying factor for words
    def proportional_factor(self):
        corpus = Corpus(self.folder_path)
        spam_counter = 0
        ham_counter = 0
        for email, email_body in corpus.emails():
            if self.get_status(email) == SPAM:
                spam_counter += 1
            else:
                ham_counter += 1
        if ham_counter != 0:
            return spam_counter / ham_counter
        else:
            return 1

    # function returns dicts with read messages from mails
    def get_bodies(self):
        self.rate_names()
        dictionary_senders = {SPAM: [], HAM: []}
        dictionary_words = {SPAM: [], HAM: []}
        corpus = Corpus(self.folder_path)
        for email, email_body in corpus.emails():
            tokens = Tokenization(email_body)
            status = self.get_status(email)
            dictionary_senders[status].append(tokens.get_sender())
            for word in tokens.tokenize_message():
                dictionary_words[status].append(word)
        return dictionary_senders, dictionary_words

    # function for calculating the frequency of occurrence of a word
    def count_words(self, dictionary_words):
        dict = {SPAM: {}, HAM: {}}
        for word in dictionary_words[SPAM]:
            if dict[SPAM].get(word) is None:
                dict[SPAM][word] = 1
            else:
                dict[SPAM][word] += 1
        for word in dictionary_words[HAM]:
            if dict[HAM].get(word) is None:
                dict[HAM][word] = 1
            else:
                dict[HAM][word] += 1
        return dict

    # function returns trained data
    def return_training_data(self):
        dictionary_senders, dictionary_words = self.get_bodies()
        return dictionary_senders, self.count_words(dictionary_words)
