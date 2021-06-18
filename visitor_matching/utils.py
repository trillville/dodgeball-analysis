from math import radians, cos, sin, asin, sqrt
from datetime import datetime
from difflib import ndiff


def exact_match(previous_value, new_value):
    """
    Verify an exact match between fields
    :return: Boolean indicating whether or not the fields match exactly
    """
    if previous_value and new_value:
        return previous_value == new_value
    else:
        return False # return false if either are missing


def asymmetric_match(previous_value, new_value):
    """
    Allow a field to flip from True -> False, but
    it cannot flip from False -> True
    :return: Boolean indicating whether or not the above logic is satisfied
    """
    if previous_value and new_value:
        return previous_value is True or previous_value == new_value
    else:
        return False


def match_set(previous_value, new_value, threshold=0.5):
    """
    Given two sets of fields, return True if they have the majority of fields
    in common
    :return: Boolean indicating whether or not 50% or more of the fields are in common
    """
    if previous_value and new_value:
        previous_value, new_value = (
            set(previous_value.split(",")),
            set(new_value.split(",")),
        )
        if len(previous_value) == 0:
            return len(new_value) == 0
        else:
            distance = dice_distance(previous_value, new_value)
            return distance <= threshold
    else:
        return 0


def less_than_or_equal(previous_value, new_value):
    """
    Given two integers, or strings indicating version numbers (e.g. 5.4.10),
    return True if the second value is greater than or equal to the first
    :return: Boolean indicating whether or not the second value is >= the first
    """
    if previous_value and new_value:
        if type(previous_value) == int or previous_value.isdigit():
            return int(previous_value) <= int(new_value)
        else:
            previous_value, new_value = (
                previous_value.split("."),
                new_value.split("."),
            )
            for i in range(len(previous_value)):
                if i >= len(new_value):
                    return False
                else:
                    if int(previous_value[i]) > int(new_value[i]):
                        return False
                    elif int(new_value[i]) > int(previous_value[i]):
                        return True
                    else:
                        pass
            return True
    else:
        return False


def dice_distance(set1, set2):
    """
    Calculate the dice distance between two sets
    :return: Dice distance (https://en.wikipedia.org/wiki/Sørensen–Dice_coefficient)
    """
    if set1 and set2:
        matches = set1.intersection(set2)
        return 1 - ((2 * len(matches)) / (len(set1) + len(set2)))
    else:
        return 0


def haversine_distance(previous_props, new_props):
    """
    Calculate the haversine distance between two points
    on the earth (specified in decimal degrees)
    :return: Distance in km
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(
        radians,
        [
            previous_props["longitude"],
            previous_props["latitude"],
            new_props["longitude"],
            new_props["latitude"],
        ],
    )
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers is 6371
    km_distance = r * c
    return km_distance


def edit_distance(previous_value, new_value):
    """
    Calculate the levenshtein (edit) distance between two strings
    :return: Edit distance divided by the length of the previous string
    """
    if previous_value and new_value:
        counter = {"+": 0, "-": 0}
        distance = 0
        for edit_code, *_ in ndiff(previous_value, new_value):
            if edit_code == " ":
                distance += max(counter.values())
                counter = {"+": 0, "-": 0}
            else:
                counter[edit_code] += 1
        distance += max(counter.values())
        return distance / len(previous_value)
    else:
        return 1


def timestamp_difference(previous_value, new_value):
    """
    Calculate the difference between two timestamps in seconds
    :return: Distance in seconds
    """
    if previous_value and new_value:
        prev_time, new_time = (
            datetime.strptime(previous_value, "%Y-%m-%d %H:%M:%S.%f"),
            datetime.strptime(new_value, "%Y-%m-%d %H:%M:%S.%f"),
        )
        return (new_time - prev_time).total_seconds()
    else:
        return 999999999999


def age_difference(previous_value, new_value):
    """
    Calculate the difference between two ages in seconds
    :return: Distance in seconds
    """
    if previous_value and new_value:
        prev_age, new_age = (
            datetime.today() - datetime.strptime(previous_value, "%Y-%m-%d %H:%M:%S.%f"),
            datetime.today() - datetime.strptime(new_value, "%Y-%m-%d %H:%M:%S.%f")
        )

        return max(1, (prev_age - new_age) / prev_age)
    return 999999999999


def generate_match_score(results, weights=None, return_avg=False):
    """
    Given the results and an optional dictionary of weights, return whether or not
    it is likely that they match
    :return: Float indicating fingerprint similarity
    """
    if weights:
        score = sum([weights[key] * float(results[key]) for key in results.keys()])
        denominator = sum([weights[key] for key in results.keys()])
    else:
        score = sum([int(results[key]) for key in results.keys()])
        denominator = len(results)
    if return_avg:
        return score / denominator
    else:
        return score
