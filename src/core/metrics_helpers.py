import pandas as pd
from fuzzywuzzy import fuzz
from metrics_utils import calculate_f1_score, calculate_pm


def exact_match(questions: pd.DataFrame) -> pd.DataFrame:
    questions["exact_match"] = (
        questions["real_answer"] == questions["model_answer"]
    ).astype(int)
    return questions


def levenshtein_ratio(open_questions: pd.DataFrame) -> pd.DataFrame:
    open_questions["levenshtein_ratio"] = open_questions.apply(
        lambda row: fuzz.ratio(row["real_answer"], row["model_answer"]) / 100, axis=1
    )
    return open_questions


def f1_score(open_questions: pd.DataFrame) -> pd.DataFrame:
    open_questions["f1_score"] = open_questions.apply(
        lambda row: calculate_f1_score(row["real_answer"], row["model_answer"]), axis=1
    )
    return open_questions


def is_substring(not_open_questions: pd.DataFrame) -> pd.DataFrame:
    not_open_questions["is_substring"] = not_open_questions.apply(
        lambda row: row["real_answer"] in row["model_answer"], axis=1
    ).astype(int)
    return not_open_questions


def partially_match(not_open_questions: pd.DataFrame) -> pd.DataFrame:
    not_open_questions["only_numbers_model_answer"] = not_open_questions[
        "model_answer"
    ].apply(only_numbers)
    not_open_questions["partially_match"] = not_open_questions.apply(
        calculate_pm, axis=1
    )
    return not_open_questions
