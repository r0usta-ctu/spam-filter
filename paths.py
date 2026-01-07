import os

# ? Standard filenames for truth and prediction
TRUTH_FILENAME = '!truth.txt'
PREDICTION_FILENAME = '!prediction.txt'


def jpath(directory, filename):
    """
    Join a directory path and a filename into a full path.
    :param directory: Absolute or relative path to the directory.
    :param filename: Name of the file.
    :return: Full path to the file inside the directory.
    """
    return os.path.join(directory, filename)
