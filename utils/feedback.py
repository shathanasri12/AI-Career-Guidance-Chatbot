"""Save and read student feedback using a simple CSV file."""

import csv
from datetime import datetime
from pathlib import Path

FEEDBACK_FILE = Path(__file__).resolve().parent.parent / "data" / "feedback.csv"
FIELDS = ["timestamp", "name", "rating", "comment"]


def _clean(text):
    """Stop spreadsheet apps from running text like '=1+1' as a formula."""
    text = str(text).strip()
    if text and text[0] in "=+-@":
        text = "'" + text
    return text


def save_feedback(name, rating, comment, path=FEEDBACK_FILE):
    """Append one feedback row to the CSV file (creating it if needed)."""
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        is_new_file = not path.exists()
        with open(path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            if is_new_file:
                writer.writeheader()
            writer.writerow({
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "name": _clean(name),
                "rating": int(rating),
                "comment": _clean(comment),
            })
    except OSError as error:
        raise RuntimeError("Could not save your feedback. Please try again later.") from error


def load_feedback_summary(path=FEEDBACK_FILE):
    """Return (number_of_responses, average_rating). Returns (0, 0.0) if none."""
    path = Path(path)
    if not path.exists():
        return 0, 0.0
    try:
        with open(path, "r", newline="", encoding="utf-8") as file:
            ratings = [int(row["rating"]) for row in csv.DictReader(file)]
    except (OSError, KeyError, ValueError):
        return 0, 0.0
    if not ratings:
        return 0, 0.0
    return len(ratings), sum(ratings) / len(ratings)