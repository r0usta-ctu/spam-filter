from corpus import Corpus
from paths import jpath, TRUTH_FILENAME
from utils import read_classification_from_file
from quality import SPAM_TAG, HAM_TAG


class TrainingCorpus(Corpus):
    """
    Represents a training corpus of email files in directory with known classifications.

    Author: Vojtěch Nejedlý,
    Created: 02-01-2026
    """

    def __init__(self, src):
        """
        Initialize the TrainingCorpus with a source directory.
        :param src: Path to the folder containing training email files.
        """
        super().__init__(src)
        self._classification_dict = read_classification_from_file(
            jpath(self.src, TRUTH_FILENAME))

    def get_class(self, filename):
        """
        Get the true classification of an email by its filename.
        :param filename: The name of the email file.
        :return: The classification label (SPAM_TAG or HAM_TAG).
        """
        return self._classification_dict.get(filename)

    def is_ham(self, filename):
        """
        Check if the email is classified as HAM.
        :param filename: The name of the email file.
        :return: True if classified as HAM, False otherwise.
        """
        return self.get_class(filename) == HAM_TAG

    def is_spam(self, filename):
        """
        Check if the email is classified as SPAM.
        :param filename: The name of the email file.
        :return: True if classified as SPAM, False otherwise.
        """
        return self.get_class(filename) == SPAM_TAG

    def spams(self):
        """
        Generator that yields all SPAM emails in the corpus.
        :return: A tuple `(filename, body)` for each SPAM email.
        """
        for filename, body in self.emails():
            if self.is_spam(filename):
                yield filename, body

    def hams(self):
        """
        Generator that yields all HAM emails in the corpus.
        :return: A tuple `(filename, body)` for each HAM email.
        """
        for filename, body in self.emails():
            if self.is_ham(filename):
                yield filename, body
