# Spam Filter – Naive Bayes Implementation

A Python-based email spam filter using a combination of rule-based preprocessing and a Multinomial Naive Bayes classifier with Laplace smoothing. Designed for training, testing, and extending with new datasets.

## Features

- **Email Preprocessing**
  - Lowercasing
  - HTML entity decoding and tag removal
  - Quoted-printable decoding
  - Replacement of URLs, email addresses, numbers, and currency symbols with placeholder tokens
  - Removal of punctuation and non-word characters
  - Rule-based stemming (common prefixes and suffixes)
  - Optional stopword filtering

- **Model Training**
  - Counts token frequencies separately for ham and spam
  - Applies Laplace smoothing
  - Stores prior probabilities and conditional probabilities per token

- **Prediction / Testing**
  - Computes log-probabilities of ham vs spam for each email
  - Supports offline pretrained models

- **Extensible Design**
  - Easily retrain or extend the model with new datasets
  - Modular classes for tokenization, email body extraction, and corpus handling

## Usage

**Train the model:**
```python
filter.train("path/to/train_dataset")
filter.save_model("pretrained_model.pkl")
```

**Load a pretrained model and test:**
```python
filter.load_model("pretrained_model.pkl")
filter.test("path/to/test_dataset")
```

**Extend the model with new data without full retraining:**
```python
filter.extend("path/to/additional_dataset")
```

**Requirements**
- Python 3.12
- Standard libraries: `re`, `collections`, `quopri`, `email`, `pickle`, `math`
