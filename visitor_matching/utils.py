def exact_match(previous_value, new_value):
    """
    Verify an exact match between fields
    :return: Boolean indicating whether or not the fields match exactly
    """
    return previous_value == new_value


def asymmetric_match(previous_value, new_value):
    """
    Allow a field to flip from True -> False, but
    it cannot flip from False -> True
    :return: Boolean indicating whether or not the above logic is satisfied
    """
    return previous_value is True or previous_value == new_value


def match_set(previous_value, new_value, threshold=0.5):
    """
    Given two sets of fields, return True if they have the majority of fields
    in common
    :return: Boolean indicating whether or not 50% or more of the fields are in common
    """
    previous_value, new_value = (
        set(previous_value.split(",")),
        set(new_value.split(",")),
    )
    if len(previous_value) == 0:
        return len(new_value) == 0
    else:
        distance = dice_distance(previous_value, new_value)
        return distance <= threshold


def less_than_or_equal(previous_value, new_value):
    """
    Given two integers, or strings indicating version numbers (e.g. 5.4.10),
    return True if the second value is greater than or equal to the first
    :return: Boolean indicating whether or not the second value is >= the first
    """
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


def dice_distance(set1, set2):
    """
    Calculate the dice distance between two sets
    :return: Dice distance (https://en.wikipedia.org/wiki/Sørensen–Dice_coefficient)
    """
    matches = set1.intersection(set2)
    return 1 - ((2 * len(matches)) / (len(set1) + len(set2)))
