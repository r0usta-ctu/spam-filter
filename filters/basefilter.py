from abc import abstractmethod, ABC

from dataio.corpus import Corpus
from config.paths import jpath, PREDICTION_FILENAME


class BaseFilter(ABC):
    """
    Abstract base class for creating filters.

    The `BaseFilter` class serves as a foundation for implementing different types
    of filters. Subclasses must provide concrete implementations for the abstract
    methods `train` and `test`. The class manages a corpus and provides basic
    infrastructure to support training and testing operations.

    :ivar _corpus: A corpus object to handle email data.
    :ivar _prediction_file_path: Path to the prediction file generated during the
        testing phase.
    :ivar _predictions: A dictionary to store prediction results.
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

    @abstractmethod
    def test(self, emails_path):
        """
        Prepare the corpus and prediction path for testing.
        Subclasses typically extend this method.
        :param emails_path: Path to the emails for testing.
        """
        self._corpus = Corpus(emails_path)
        self._prediction_file_path = jpath(emails_path, PREDICTION_FILENAME)
