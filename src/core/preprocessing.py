import pandas as pd


def preprocess_answers(data: pd.DataFrame):
    data["real_answer"] = data["real_answer"].astype(str).str.lower().str.strip()
    data["model_answer"] = data["model_answer"].astype(str).str.lower().str.strip()

    data["is_open_question"] = (data["type"] == "open").astype(int)

    open_questions = data[data["is_open_question"] == 1].reset_index(drop=True)
    not_open_questions = data[data["is_open_question"] == 0].reset_index(drop=True)

    return open_questions, not_open_questions
