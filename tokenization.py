import re
import base64

SENDER_MAIL = '<(.*?)>'

BASE64_START = 'Content-Transfer-Encoding: base64'

BASE64_END = '------=_NextPart_'

PUNCTUATION_DIGITS = {49: 32, 50: 32, 51: 32, 52: 32, 53: 32, 54: 32, 55: 32, 56: 32, 57: 32, 48: 32, 42: 32,
                      93: 32, 91: 32, 125: 32, 123: 32, 43: 32, 44: 32, 46: 32, 45: 32,
                      39: 32, 92: 32, 38: 32, 33: 32, 63: 32, 58: 32, 59: 32, 35: 32, 126: 32, 61: 32, 47: 32,
                      94: 32, 40: 32, 41: 32, 95: 32, 60: 32, 62: 32, 64: 32, 34: 32}

STOP_WORDS = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during",
              "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours",
              "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from",
              "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his",
              "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our",
              "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at",
              "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves",
              "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "he",
              "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after",
              "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how",
              "further", "was", "here", "than", "us", "http", "www", "html", "fff", "com", "ffffff", "could",
              "ffff"}

EXCEPTIONS = {"$", "%", "sex", "xxx", "pee", "day", "wet", "dvd"}


class Tokenization:
    def __init__(self, email_body):
        self.email_body = email_body
        self.message = []
        self.base64_check = 0

    # function for getting sender's mail adress
    def get_sender(self):
        sub_string = re.search(SENDER_MAIL, self.email_body)
        if sub_string:
            sender = sub_string.group(1)
            return sender
        return None

    # function to convert base64 text to normal
    def base64_to_text(self, base64_string):
        base64_bytes = base64_string.encode('utf-8')
        string_bytes = base64.b64decode(base64_bytes)
        text_string = string_bytes.decode('utf-8')
        return text_string

    # function to check email for base64
    def is_base64(self):
        email_body_copy = self.email_body
        if re.search(BASE64_START, email_body_copy):
            temporary_message = email_body_copy.split(BASE64_START, 1)
            if re.search(BASE64_END, temporary_message[1]):
                message = temporary_message[1].split(BASE64_END, 1)
                try:
                    converted_message = self.base64_to_text(message[0])
                    self.message = converted_message
                    self.base64_check = 1
                finally:
                    return

    # function to divide message with other data in mail
    def find_message(self):
        message = self.email_body.split('\n\n', 1)  # before every message goes '\n\n'
        self.message = message[1]

    # function to make letters equal
    def lower_case(self):
        self.message = self.message.lower()

    # function for cleaning message
    def clean_message(self):
        self.message = self.message.translate(PUNCTUATION_DIGITS)
        self.message = self.message.replace('\n', ' ').split()
        self.remove_stopwords()

    # function for removing useless words from message
    def remove_stopwords(self):
        message = [word for word in self.message if word not in STOP_WORDS]
        message_r = [word for word in message if len(word) > 3 or word in EXCEPTIONS]
        self.message = message_r

    # function for tokenizing message
    def tokenize_message(self):
        self.is_base64()
        if self.base64_check == 0:
            self.find_message()
        self.lower_case()
        self.clean_message()
        return self.message
