from labels import SPAM_TAG, HAM_TAG
from utils import read_classification_from_file
from confmat import BinaryConfusionMatrix
from paths import jpath, TRUTH_FILENAME, PREDICTION_FILENAME


def quality_score(tp, tn, fp, fn):
    """
    Compute a custom quality score based on confusion matrix counts.
    :param tp: True positive.
    :param tn: True negative.
    :param fp: False positive.
    :param fn: False negative.
    :return: Quality score.
    """
    tp_p_tn = tp + tn
    return tp_p_tn / float(tp_p_tn + 10 * fp + fn)


def compute_quality_for_corpus(corpus_dir):
    """
    Compute the quality score for a given email corpus directory.
    :param corpus_dir: Path to the corpus directory containing the truth and prediction files.
    :return: Quality score for the corpus.
    """
    # Load truth and prediction labels
    truth_dict = read_classification_from_file(
        jpath(corpus_dir, TRUTH_FILENAME)
    )
    prediction_dict = read_classification_from_file(
        jpath(corpus_dir, PREDICTION_FILENAME)
    )

    # Create and compute binary confusion matrix
    bc_matrix = BinaryConfusionMatrix(SPAM_TAG, HAM_TAG)
    bc_matrix.compute_from_dicts(truth_dict, prediction_dict)

    # Compute and return quality score
    return quality_score(**bc_matrix.as_dict())
