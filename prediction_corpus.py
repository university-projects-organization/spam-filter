from tokenization import Tokenization

SPAM = "SPAM"
HAM = "OK"
PERCENTS = 100
SPAM_IN_TOTAL = 60


class PredictionCorpus:

    def __init__(self, path, dictionary_senders, dictionary_words, factor):
        self.email_path = path
        self.dictionary_senders = dictionary_senders
        self.dictionary_words = dictionary_words
        self.ham_factor = factor

    # function returns message from mail and it's sender's mail adress
    def get_sender_and_message(self):
        with open(self.email_path, "r", encoding='utf-8') as f:
            email_body = f.read()
            tokens = Tokenization(email_body)
            words_without_repetition = []
            words_in_email = tokens.tokenize_message()
            for word in words_in_email:
                if word not in words_without_repetition:
                    words_without_repetition.append(word)
            sender = tokens.get_sender()
        return sender, words_without_repetition

    # function for making prediction due to the dataset
    def make_prediction(self):
        sender, message = self.get_sender_and_message()

        if sender in self.dictionary_senders[SPAM] and sender not in self.dictionary_senders[HAM]:
            return SPAM
        elif sender in self.dictionary_senders[HAM] and sender not in self.dictionary_senders[SPAM]:
            return HAM

        spam_counter = 0
        ham_counter = 0
        for word in message:
            if self.dictionary_words[SPAM].get(word) is not None:
                spam_counter += self.dictionary_words[SPAM][word]
            if self.dictionary_words[HAM].get(word) is not None:
                ham_counter += self.dictionary_words[HAM][word] * self.ham_factor
        if spam_counter + ham_counter == 0:
            return HAM
        else:
            spam_percent = spam_counter / (spam_counter + ham_counter) * PERCENTS
            if spam_percent > SPAM_IN_TOTAL:
                return SPAM
            else:
                return HAM
