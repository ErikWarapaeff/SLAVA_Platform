from typing import Final

# Columns
SUBJECT_COLUMN: Final[str] = "subject"
TYPE_COLUMN: Final[str] = "type"
PROVOC_SCORE_COLUMN: Final[str] = "provoc_score"

# Metrics
MODEL_COLUMN: Final = "model"
REAL_ANSWER_COLUMN: Final[str] = "outputs"
MODEL_ANSWER_COLUMN: Final[str] = "response"

OPEN_QUESTION_FLAG_COLUMN: Final[str] = "open_question_flag"
ONLY_NUMBERS_MODEL_ANSWER_COLUMN: Final[str] = "only_numbers_response"

OPEN_QUESTION_TYPE_NAME: Final[str] = "open_question"
NOT_OPEN_QUESTION_TYPE_NAME: Final[str] = "not_open_question"

OPEN_QUESTION_VALUE: Final[str] = "открытый ответ"
SINGLE_CHOICE: Final[str] = "выбор ответа (один)"
MULTI_CHOICE: Final[str] = "выбор ответа (мультивыбор)"
MATCHING: Final[str] = "установление соответствия"
SEQUENCE: Final[str] = "указание последовательности"

EXACT_MATCH_COLUMN: Final[str] = "exact_match"
LEVENSHTEIN_RATIO_COLUMN: Final[str] = "levenshtein_ratio"
F1_SCORE_COLUMN: Final[str] = "f1_score"
IS_SUBSTRING_COLUMN: Final[str] = "is_substring"
PARTIALLY_MATCH_COLUMN: Final[str] = "partially_match"

QUESTION_TYPES_NAMING = {OPEN_QUESTION_TYPE_NAME: "Open", NOT_OPEN_QUESTION_TYPE_NAME: "Not open"}

LEADERBOARD_SHEET_NAME = "Leaderboard"
TYPE_OF_QUESTION_SHEET_NAME = "Type of question"
SUBJECT_SHEET_NAME = "Subject"
PROVOCATIVENESS_SHEET_NAME = "Provocativeness"

KEYS_NAMING = {
    TYPE_COLUMN: TYPE_OF_QUESTION_SHEET_NAME,
    SUBJECT_COLUMN: SUBJECT_SHEET_NAME,
    PROVOC_SCORE_COLUMN: PROVOCATIVENESS_SHEET_NAME,
}

SUBJECTS_NAMING = {
    "Обществознание": "Social studies",
    "История": "History",
    "География": "Geography",
    "Политология": "Political science",
}

QUESTION_VALUES_NAMING = {
    OPEN_QUESTION_VALUE: "Open answer",
    SINGLE_CHOICE: "Single choice",
    MULTI_CHOICE: "Multiple choice",
    MATCHING: "Matching",
    SEQUENCE: "Sequence",
}

PROVOCATIVENESS_NAMING = {"1": "Low", "2": "Medium", "3": "High"}

COMBINED_VALUES_NAMING = {**SUBJECTS_NAMING, **QUESTION_VALUES_NAMING, **PROVOCATIVENESS_NAMING}

METRICS_NAMING = {
    EXACT_MATCH_COLUMN: "EM",
    LEVENSHTEIN_RATIO_COLUMN: "LR",
    F1_SCORE_COLUMN: "F1",
    IS_SUBSTRING_COLUMN: "IS",
    PARTIALLY_MATCH_COLUMN: "PM",
}

AGGFUNC: Final[str] = "mean"

# Pivot tables
OPEN_QUESTION_VALUES_FOR_PIVOT_TABLES: Final[list[str]] = [
    EXACT_MATCH_COLUMN,
    LEVENSHTEIN_RATIO_COLUMN,
    F1_SCORE_COLUMN,
]
NOT_OPEN_QUESTION_VALUES_FOR_PIVOT_TABLES: Final[list[str]] = [
    EXACT_MATCH_COLUMN,
    IS_SUBSTRING_COLUMN,
    PARTIALLY_MATCH_COLUMN,
]