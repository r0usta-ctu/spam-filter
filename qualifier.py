import os

from paths import jpath, PREDICTION_FILENAME
from quality import compute_quality_for_corpus


def get_class_name(obj):
    """
    Return the class name of an object.
    :param obj: Any object.
    :return: Name of the object's class.
    """
    return type(obj).__name__


def compute_quality_for_filter(train_dir, test_dir, filter_instance):
    """
    Train and test a filter, then compute its quality score.
    :param train_dir: Path to the training emails directory.
    :param test_dir: Path to the testing emails directory.
    :param filter_instance: Instance of a filter (subclass of BaseFilter).
    :return: Quality score computed for the test directory.
    """
    filter_instance.train(train_dir)
    filter_instance.test(test_dir)

    quality_score = compute_quality_for_corpus(test_dir)

    # Remove temporary prediction file
    os.remove(jpath(test_dir, PREDICTION_FILENAME))

    return quality_score


def compute_quality_for_filters(train_dir, test_dir, filters):
    """
    Compute quality scores for multiple filters.
    :param train_dir: Path to the training emails directory.
    :param test_dir: Path to the testing emails directory.
    :param filters: List of filter instances to evaluate.
    :return: Dictionary with filter classes and their quality score.
    """
    quality_dict = dict()
    for fr in filters:
        filter_name = get_class_name(fr)
        quality_dict[filter_name] = compute_quality_for_filter(train_dir, test_dir, fr)

    return quality_dict
