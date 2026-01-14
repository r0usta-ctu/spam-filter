import math
import pickle
from collections import Counter

from basefilter import BaseFilter
from emailextractor import EmailBodyExtractor
from labels import HAM_TAG, SPAM_TAG
from tokenizer import EmailTokenizer
from trainingcorpus import TrainingCorpus
from utils import write_classification_to_file


class MyFilter(BaseFilter):
    """
    A spam filter class using a probabilistic model.

    The class is designed to train, extend, save, load, and test a spam-detection
    model using tokenized email data. It classifies emails as spam or ham
    (legitimate) based on calculated probabilities, using a naive Bayes-like
    approach.

    :ivar MODEL_PATH: The default path to save or load the pre-trained model.
    :ivar max_tokens: The maximum number of tokens to consider for building the
        vocabulary.
    :ivar model: The trained machine learning model that includes probabilities,
        vocabulary, and other attributes.
    """
    MODEL_PATH = "./model/nb_spam_data1_data2_vocab2500.pkl"

    def __init__(self, max_tokens=2500, pretrained_model=None):
        super().__init__()
        self.max_tokens = max_tokens
        self.model = pretrained_model

    def _process_training_corpus(self, emails_path, ham_counter=None, spam_counter=None, ham_count=0, spam_count=0):
        """
        Processes the training corpus to extract words from ham and spam emails, updating counters,
        and counts accordingly. The corpus is tokenized, and each token is classified as part of
        either the ham or spam collection.

        :param emails_path: The path to the directory of the training corpus.
        :param ham_counter: A Counter object to track token frequencies in `hams`. If None, a
            new Counter is created.
        :param spam_counter: A Counter object to track token frequencies in `spams`. If None, a
            new Counter is created.
        :param ham_count: An integer denoting the total number of ham emails processed.
        :param spam_count: An integer denoting the total number of spam emails processed.
        :return: A tuple containing the updated ham_counter, spam_counter, ham_count, and spam_count.
        """
        corpus = TrainingCorpus(emails_path)
        tokenizer = EmailTokenizer()
        extractor = EmailBodyExtractor()

        if ham_counter is None:
            ham_counter = Counter()
        if spam_counter is None:
            spam_counter = Counter()

        for _, email in corpus.hams():
            body = extractor.extract(email)
            tokens = tokenizer.tokenize(body)
            ham_counter.update(tokens)
            ham_count += 1

        for _, email in corpus.spams():
            body = extractor.extract(email)
            tokens = tokenizer.tokenize(body)
            spam_counter.update(tokens)
            spam_count += 1

        return ham_counter, spam_counter, ham_count, spam_count

    def _build_model(self, ham_counter, spam_counter, ham_count, spam_count):
        """
        Builds the probabilistic model for classifying text based on given counts of ham and spam
        emails. This method calculates prior probabilities for ham and spam, determines the most
        frequent tokens in the data sets, constructs the vocabulary, and computes token probabilities
        for each category using Laplace smoothing.

        :param ham_counter: Counter object containing token frequencies in ham emails
        :param spam_counter: Counter object containing token frequencies in spam emails
        :param ham_count: Total number of ham emails
        :param spam_count: Total number of spam emails
        """
        total_emails = ham_count + spam_count
        prior_ham = ham_count / total_emails
        prior_spam = spam_count / total_emails

        ham_top = [w for w, _ in ham_counter.most_common(self.max_tokens)]
        spam_top = [w for w, _ in spam_counter.most_common(self.max_tokens)]
        vocabulary = set(ham_top) | set(spam_top)
        vocab_size = len(vocabulary)

        total_ham_tokens = sum(ham_counter[w] for w in vocabulary)
        total_spam_tokens = sum(spam_counter[w] for w in vocabulary)

        ham_probs = {w: (ham_counter.get(w, 0) + 1) / (total_ham_tokens + vocab_size) for w in vocabulary}
        spam_probs = {w: (spam_counter.get(w, 0) + 1) / (total_spam_tokens + vocab_size) for w in vocabulary}

        self.model = {
            "prior_ham": prior_ham,
            "prior_spam": prior_spam,
            "ham_probs": ham_probs,
            "spam_probs": spam_probs,
            "vocabulary": vocabulary,
            "total_ham_tokens": total_ham_tokens,
            "total_spam_tokens": total_spam_tokens
        }

    def save_model(self, model_path=MODEL_PATH):
        """
        Saves the trained model to the specified file path in binary format.

        :param model_path: Path to save the serialized model
        :raises RuntimeError: If no model is present to save
        """
        if self.model is None:
            raise RuntimeError("No model to save. Train or load first.")
        with open(model_path, "wb") as f:
            pickle.dump(self.model, f)

    def load_model(self, model_path=MODEL_PATH):
        """
        Loads a machine learning model from the given file path.

        :param model_path: The file path to the serialized machine learning model.
        """
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def train(self, emails_path):
        """
        Processes a training corpus of emails to build a spam-detection model. The method
        analyzes the emails in the specified path, separates them into ham and spam categories,
        and computes the necessary probabilities for the model.

        :param emails_path: Path to the directory containing the training emails.
        """
        ham_counter, spam_counter, ham_count, spam_count = self._process_training_corpus(emails_path)
        self._build_model(ham_counter, spam_counter, ham_count, spam_count)

    # ? This method was used to build a pretrained model from 2 datasets
    def extend(self, emails_path):
        """
        Extends the trained model by processing additional emails from the specified path and
        adjusting token probabilities and counts accordingly. This function modifies the
        counters and statistics used in the existing model based on new training data.

        :param emails_path: The path to the email dataset for model extension.
        :raises RuntimeError: If the model has not been loaded or trained before calling this method.
        """
        if self.model is None:
            raise RuntimeError("Model not loaded or trained")

        ham_counter = Counter()
        spam_counter = Counter()
        for w, prob in self.model["ham_probs"].items():
            ham_counter[w] = prob * self.model["total_ham_tokens"]
        for w, prob in self.model["spam_probs"].items():
            spam_counter[w] = prob * self.model["total_spam_tokens"]

        ham_count = int(self.model["prior_ham"] * (self.model["total_ham_tokens"] + self.model["total_spam_tokens"]))
        spam_count = int(self.model["prior_spam"] * (self.model["total_ham_tokens"] + self.model["total_spam_tokens"]))

        ham_counter, spam_counter, ham_count, spam_count \
            = self._process_training_corpus(emails_path, ham_counter, spam_counter, ham_count, spam_count)
        self._build_model(ham_counter, spam_counter, ham_count, spam_count)

    def test(self, emails_path):
        """
        Tests the spam classifier on a set of emails, processes each email using a tokenizer
        and an extractor, and classifies them based on calculated probabilities for ham or spam.

        :param emails_path: The path to the directory containing the emails to be
            tested.
        """
        super().test(emails_path)

        if self.model is None:
            self.load_model(self.MODEL_PATH)

        tokenizer = EmailTokenizer()
        extractor = EmailBodyExtractor()

        for filename, email in self._corpus.emails():
            body = extractor.extract(email)
            tokens = tokenizer.tokenize(body)

            log_ham = math.log(self.model["prior_ham"])
            log_spam = math.log(self.model["prior_spam"])

            for token in tokens:
                if token in self.model["vocabulary"]:
                    log_ham += math.log(self.model["ham_probs"][token])
                    log_spam += math.log(self.model["spam_probs"][token])

            self._predictions[filename] = HAM_TAG if log_ham > log_spam else SPAM_TAG

        write_classification_to_file(
            self._prediction_file_path,
            self._predictions
        )
