import quopri
import re
from html import unescape


class EmailTokenizer:
    """
    Handles tokenization of raw email text by normalizing and cleaning input data.

    This class is designed to convert raw email text into a list of meaningful tokens
    by applying normalization, HTML decoding, tag removal, and simple stemming.

    :ivar URL_RE: A regular expression pattern for identifying URLs in the text.
    :ivar EMAIL_RE: A regular expression pattern for identifying email addresses in the text.
    :ivar NUMBER_RE: A regular expression pattern for recognizing numeric values in the text.
    :ivar CURRENCY_RE: A regular expression pattern for identifying currency symbols or names.
    :ivar HTML_RE: A regular expression pattern for detecting HTML tags.
    :ivar NON_WORD_RE: A regular expression pattern for isolating non-word characters.
    :ivar SUFFIXES: A tuple of common suffixes considered for stemming words.
    :ivar PREFIXES: A tuple of common prefixes considered for stemming words.
    :ivar STOP_WORDS: A set of common stop words to be ignored during tokenization.
    """
    URL_RE = re.compile(r"(http|https)://[^\s]+", re.IGNORECASE)
    EMAIL_RE = re.compile(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", re.IGNORECASE)
    NUMBER_RE = re.compile(r"\b\d+(\.\d+)?\b")
    CURRENCY_RE = re.compile(r"(\$|€|eur|usd)", re.IGNORECASE)
    HTML_RE = re.compile(r"<[^<>]+>")
    NON_WORD_RE = re.compile(r"[^a-z0-9]+")

    SUFFIXES = ("ing", "ed", "es", "s")
    PREFIXES = ("dis", "pre", "un", "re")

    STOP_WORDS = {
        "the", "to", "and", "of", "in", "is", "for", "it", "on",
        "with", "this", "that", "from", "are", "be", "you", "your",
        "we", "will", "not", "can", "as", "by", "or", "if", "all",
    }

    def _stem(self, word):
        """
        Apply a simple rule-based stemming by removing common English prefixes and suffixes.

        This is a lightweight approximation of stemming intended to reduce vocabulary size.
        """

        # Remove suffixes
        for suffix in self.SUFFIXES:
            if len(word) <= len(suffix) + 2:
                continue
            if word.endswith(suffix):
                word = word[:-len(suffix)]
                break

        # Remove prefixes
        for prefix in self.PREFIXES:
            if len(word) <= len(prefix) + 2:
                continue
            if word.startswith(prefix):
                word = word[len(prefix):]
                break

        return word

    def tokenize(self, decoded_text_bytes):
        """
        Normalize and tokenize raw email text into a list of cleaned tokens.

        This method performs the following steps:
          1. Lowercases all text.
          2. Decodes HTML entities.
          3. Removes HTML tags.
          4. Normalizes URLs, email addresses, numbers, and currency symbols to placeholders.
          5. Removes non-word characters and punctuation.
          6. Normalizes whitespace.
          7. Splits the text into words.
          8. Applies rule-based stemming to words longer than 4 characters.
          9. Ignores single-character tokens and stop words.

        :param decoded_text_bytes: Raw email text (bytes).
        :return: List of normalized tokens.
        """
        if not decoded_text_bytes:
            return []

        # Decode quoted-printable
        decoded_bytes = quopri.decodestring(decoded_text_bytes)

        # Convert back to string safely
        text = decoded_bytes.decode('utf-8', errors='replace')

        # Step 1: lowercase
        text = text.lower()

        # Step 2: decode HTML entities
        text = unescape(text)

        # Step 3: remove HTML tags
        text = self.HTML_RE.sub(" ", text)

        # Step 4: normalize URLs, emails, numbers, currencies
        text = self.URL_RE.sub(" httpaddr ", text)
        text = self.EMAIL_RE.sub(" emailaddr ", text)
        text = self.NUMBER_RE.sub(" number ", text)
        text = self.CURRENCY_RE.sub(" currency ", text)

        # Step 5: remove non-word characters / punctuation
        text = self.NON_WORD_RE.sub(" ", text)

        # Step 6: normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Step 7: split into words
        words = text.split(" ")

        # Step 8 & 9: stem long words, skip single-character tokens and stop words
        tokens = [
            self._stem(word) if len(word) > 4 else word
            for word in words
            if len(word) > 1 and word not in self.STOP_WORDS
        ]

        return tokens
