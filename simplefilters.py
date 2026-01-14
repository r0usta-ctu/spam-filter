import random
from abc import abstractmethod

from basefilter import BaseFilter
from labels import HAM_TAG, SPAM_TAG
from utils import write_classification_to_file


class _ConstantFilter(BaseFilter):
    """
    Internal helper class for filters that always return the same label.
    """

    TAG = None

    def test(self, emails_path):
        """
        Predict the same TAG for all emails in the corpus.
        :param emails_path: Path to the emails for testing.
        """
        super().test(emails_path)

        for filename, _ in self._corpus.emails():
            self._predictions[filename] = self.TAG

        write_classification_to_file(
            self._prediction_file_path,
            self._predictions
        )

    @abstractmethod
    def train(self, emails_path):
        """
        Abstract method. Subclasses must implement training logic if needed.
        :param emails_path: Path to the training emails.
        """
        pass


class NaiveFilter(_ConstantFilter):
    """
    Always predicts HAM for all emails.
    """

    TAG = HAM_TAG

    def train(self, emails_path):
        """No training needed."""
        pass


class ParanoidFilter(_ConstantFilter):
    """
    Always predicts SPAM for all emails.
    """

    TAG = SPAM_TAG

    def train(self, emails_path):
        """No training needed."""
        pass


class RandomFilter(BaseFilter):
    """
    Predicts randomly between HAM and SPAM for each email.
    """

    def test(self, emails_path):
        """
        Predict randomly for each email in the corpus.
        :param emails_path: Path to the emails for testing.
        """
        super().test(emails_path)

        tags = (HAM_TAG, SPAM_TAG)

        for filename, _ in self._corpus.emails():
            self._predictions[filename] = random.choice(tags)

        write_classification_to_file(
            self._prediction_file_path,
            self._predictions
        )

    def train(self, emails_path):
        """No training needed."""
        pass
