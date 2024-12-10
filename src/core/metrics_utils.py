import re
import string
from collections import Counter

REGEX = re.compile("[%s]" % re.escape(string.punctuation + "\\n"))


def only_numbers(raw_text: str) -> str:
    text = REGEX.sub("", raw_text).replace(" ", "")
    match = re.search(r"\d+", text)
    return match.group(0) if match else "-"


def calculate_f1_score(real_answer, model_answer):
    real_tokens = get_tokens(real_answer)
    model_tokens = get_tokens(model_answer)

    common = Counter(real_tokens) & Counter(model_tokens)
    num_same = sum(common.values())

    if len(real_tokens) == 0 or len(model_tokens) == 0:
        return int(real_tokens == model_tokens)

    if num_same == 0:
        return 0

    precision = num_same / len(model_tokens)
    recall = num_same / len(real_tokens)
    return 2 * precision * recall / (precision + recall)


def get_tokens(text: str):
    if not text:
        return []
    return normalize_answer(text).split()


def normalize_answer(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = "".join(ch for ch in text if ch not in string.punctuation)
    return " ".join(text.split())
