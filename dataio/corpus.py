import os

from config.paths import jpath


class Corpus:
    """
    Represents a collection of email files in a directory.
    """

    def __init__(self, src):
        """
        Initialize the Corpus with a source directory.
        :param src: Path to the folder containing email files.
        """
        if not os.path.isdir(src):
            raise ValueError(f"Invalid directory path: {src}")

        self.src = src

    def emails(self):
        """
        Generator that yields all emails in the corpus.
        :return: A tuple `(filename, body)`, where `filename` is the name of the email file
         and `body` is its full text content.
        """
        filenames = os.listdir(self.src)

        for filename in filenames:
            if filename.startswith('!'):
                continue

            abspath = jpath(self.src, filename)
            with open(abspath, 'r', encoding='utf-8') as f:
                body = f.read()
                yield filename, body
