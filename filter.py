import os
from training_corpus import TrainingCorpus
from prediction_corpus import PredictionCorpus

HAM = "OK"


class MyFilter:
    """ Spam filter teaches on dataset """

    def __init__(self):
        self.dictionary_senders = {}
        self.dictionary_words = {}
        self.factor = 1

    # function for training on dataset
    def train(self, train_corpus_dir):
        training = TrainingCorpus(train_corpus_dir)
        self.dictionary_senders, self.dictionary_words = training.return_training_data()
        self.factor = training.proportional_factor()

    # function for evaluation mails without training
    def test_without_train(self, test_corpus_dir):
        email_files = os.listdir(test_corpus_dir)
        prediction_path = os.path.join(test_corpus_dir, '!prediction.txt')
        with open(prediction_path, "w", encoding='utf-8') as f:
            for email in email_files:
                if email[0] != '!' and email[0] != '.':  # != '.' for checking hidden files in Unix platforms
                    f.write(email + ' ' + HAM + '\n')

    # function for evaluation mails after training
    def test(self, test_corpus_dir):
        if len(self.dictionary_words) == 0:
            self.test_without_train(test_corpus_dir)
        else:
            email_files = os.listdir(test_corpus_dir)
            prediction_path = os.path.join(test_corpus_dir, '!prediction.txt')
            with open(prediction_path, "w", encoding='utf-8') as f:
                for email in email_files:
                    if email[0] != '!' and email[0] != '.':  # != '.' for checking hidden files in Unix platforms
                        email_path = os.path.join(test_corpus_dir, email)
                        prediction = PredictionCorpus(email_path, self.dictionary_senders, self.dictionary_words, self.factor)
                        status = prediction.make_prediction()
                        f.write(email + ' ' + status + '\n')
