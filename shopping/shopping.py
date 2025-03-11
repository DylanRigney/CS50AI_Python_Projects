import csv
from enum import Enum
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels   = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        # iterate over table and for each row
        for row in reader:
            boolean_val = convert_boolean(row[17])
            labels.append(boolean_val)

            current_evidence = []
            for i, value in enumerate(row[:-1]):
                converted_value = conversion_functions.get(i, lambda v: int(v))(value)
                current_evidence.append(converted_value)
            evidence.append(current_evidence)
                
    return (evidence, labels)

def convert_to_float(value):
    return float(value)

def convert_visitor_type(value):
    if value == "Returning_Visitor":
        return 1
    else:
        return 0
    
def convert_boolean(value):
    return 1 if value == "TRUE" else 0

months = {
    'Jan': 0,
    'Feb': 1,
    'Mar': 2,
    'Apr': 3,
    'May': 4,
    'June': 5,
    'Jul': 6,
    'Aug': 7,
    'Sep': 8,
    'Oct': 9,
    'Nov': 10,
    'Dec': 11
}

def convert_month(value):
    return months.get(value, 0)

conversion_functions = { 
    1 : convert_to_float, 
    3 : convert_to_float,
    5 : convert_to_float,
    6 : convert_to_float,
    7 : convert_to_float, 
    8 : convert_to_float,
    9 : convert_to_float,
    # Convert month to integer
    10: convert_month,
    15: convert_visitor_type,
    16: convert_boolean
}

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
   
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    if len(labels) != len(predictions) or set(labels) - {0,1}:
        raise ValueError("Inputs are wrong!!!")

    sensitivity = precision_score(labels, predictions, pos_label=1)
    specificity = precision_score(labels, predictions, pos_label=0)

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
