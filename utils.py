def read_classification_from_file(filepath):
    """
    Read classifications from a file as a dictionary.
    :param filepath: Path to the classification file.
    :return: Dictionary with filenames and classification labels.
    """
    classifications = dict()

    # Read line by line to handle large files
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            filtered_line = line.strip()
            if not filtered_line:
                # Skip empty lines
                continue
            try:
                filename, classification = filtered_line.split()
                classifications[filename] = classification
            except ValueError:
                # Skip malformed
                continue

    return classifications


def write_classification_to_file(filepath, classifications):
    """
    Write a dictionary of classifications to a file.
    :param filepath: Path to the output file.
    :param classifications: Dictionary with filenames and classification labels.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for filename, classification in classifications.items():
            f.write(filename + ' ' + classification + '\n')
