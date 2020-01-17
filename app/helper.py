from flask_googlecharts import ColumnChart


# Function to turn unicode into a string representation
# Returns a string of reaction types or empty string.
def react_classifier(react):
    if react == "\u00f0\u009f\u0091\u008e":
        return 'thumbs_down'
    elif react == "\u00f0\u009f\u0091\u008d":
        return 'thumbs_up'
    elif react == "\u00f0\u009f\u0098\u00a0":
        return 'angry'
    elif react == "\u00f0\u009f\u0098\u00ae":
        return 'wow'
    elif react == "\u00f0\u009f\u0098\u0086":
        return 'laugh'
    elif react == "\u00f0\u009f\u0098\u00a2":
        return 'cry'
    elif react == "\u00f0\u009f\u0098\u008d" or react == "\u00e2\u009d\u00a4":
        return 'heart'
    else:
        return ''


# Helps compare Person object and Counter object for specific React type
# Updates the Person react count if counter count is higher and returns TrueFalse depending on if higher
def react_compare(person, counter, react):
    num_of_react = getattr(getattr(person, react), 'max_received')
    counter_count = getattr(counter, react)
    if num_of_react > counter_count:
        setattr(person, react, counter_count)
        return True
    else:
        return False


def react_chart_row_filler(chart, person):
    chart.append([person.id, person.heart.num_received, person.laugh.num_received, person.wow.num_received,
                  person.cry.num_received, person.angry.num_received, person.thumbs_up.num_received,
                  person.thumbs_down.num_received])
