import os


class Corpus:
    def __init__(self, path):
        self.folder_path = path

    def emails(self):
        file_names = os.listdir(self.folder_path)
        for file_name in file_names:
            if file_name[0] != '!' and file_name[0] != '.':
                file_path = os.path.join(self.folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    body = f.read()
                    yield file_name, body
