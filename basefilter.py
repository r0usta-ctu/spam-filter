from abc import abstractmethod, ABC

from corpus import Corpus
from paths import jpath, PREDICTION_FILENAME


class BaseFilter(ABC):
    """
    Abstract base class for all filters.
    """

    def __init__(self):
        self._corpus = None
        self._prediction_file_path = None
        self._predictions = dict()

    @abstractmethod
    def train(self, emails_path):
        """
        Train the filter on a corpus.
        Must be implemented by subclasses.
        :param emails_path: Path to the training emails.
        """
        pass

    def test(self, emails_path):
        """
        Prepare the corpus and prediction path for testing.
        Subclasses typically extend this method.
        :param emails_path: Path to the emails for testing.
        """
        self._corpus = Corpus(emails_path)
        self._prediction_file_path = jpath(emails_path, PREDICTION_FILENAME)
