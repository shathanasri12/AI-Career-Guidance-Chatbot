"""Input validation helpers.

Every function returns a tuple: (is_valid, error_message).
If is_valid is True, error_message is an empty string.
"""

import re

# 2-50 characters, starts with a letter, then letters/spaces/. ' -
NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,49}$")


def validate_name(name):
    """Check that the name is present and made of sensible characters."""
    name = (name or "").strip()
    if not name:
        return False, "Please enter your name."
    if not NAME_PATTERN.match(name):
        return False, (
            "Name must be 2-50 characters and contain only letters, "
            "spaces, dots, apostrophes or hyphens."
        )
    return True, ""


def validate_age(age):
    """Check that age is a whole number between 13 and 60."""
    try:
        age = int(age)
    except (TypeError, ValueError):
        return False, "Age must be a whole number."
    if age < 13 or age > 60:
        return False, "Age must be between 13 and 60."
    return True, ""


def validate_selection(items, label, minimum=1, maximum=None):
    """Check how many options the student picked in a multi-select."""
    count = len(items or [])
    if count < minimum:
        return False, f"Please select at least {minimum} {label}."
    if maximum is not None and count > maximum:
        return False, f"Please select no more than {maximum} {label}."
    return True, ""


def validate_rating(rating):
    """Check that a feedback rating is an integer from 1 to 5."""
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return False, "Rating must be a number from 1 to 5."
    if rating < 1 or rating > 5:
        return False, "Rating must be between 1 and 5."
    return True, ""


def validate_feedback_comment(comment, max_length=500):
    """Comments are optional, but must not be too long."""
    comment = (comment or "").strip()
    if len(comment) > max_length:
        return False, f"Comment is too long ({len(comment)}/{max_length} characters)."
    return True, ""