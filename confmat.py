class BinaryConfusionMatrix:
    """
    Binary confusion matrix for a fixed positive and negative label.

    Matrix layout:
        [ [TP, FN], [FP, TN] ]
    """

    def __init__(self, pos_tag, neg_tag):
        """
        Constructor.
        :param pos_tag: Label considered positive.
        :param neg_tag: Label considered negative.
        """
        self._tag_to_index = {pos_tag: 0, neg_tag: 1}
        self._matrix = [[0, 0], [0, 0]]

    def _validate_tag(self, tag, name):
        """
        Check that a label tag is valid.
        :param tag: The label tag to validate.
        :param name: Context for error message

        :raises ValueError: If the tag is invalid.
        """
        if tag not in self._tag_to_index:
            raise ValueError(f"Unknown {name} tag: {tag}")

    def update(self, truth, prediction):
        """
        Update the confusion matrix with a single prediction.
        :param truth: The true label of the instance.
        :param prediction: The predicted label of the instance.
        """
        self._validate_tag(truth, "truth")
        self._validate_tag(prediction, "prediction")

        i = self._tag_to_index[truth]
        j = self._tag_to_index[prediction]
        self._matrix[i][j] += 1

    def as_dict(self):
        """
        Return the confusion matrix as a dictionary.
        :return: A dictionary that contains counts with keys 'tp', 'fp', 'fn', 'tn'.
        """
        return {
            'tp': self._matrix[0][0],
            'fp': self._matrix[1][0],
            'fn': self._matrix[0][1],
            'tn': self._matrix[1][1]
        }

    def compute_from_dicts(self, truth_dict, pred_dict):
        """
        Update the confusion matrix from dictionaries.
        :param truth_dict: Dictionary with email names and true labels.
        :param pred_dict: Dictionary with email names and predicted labels.

        :raises ValueError: If a key in truth_dict is missing in pred_dict.
        """
        for email_name, truth_label in truth_dict.items():
            if email_name not in pred_dict:
                raise KeyError(f"Missing prediction for email: {email_name}")

            self.update(truth_label, pred_dict[email_name])
