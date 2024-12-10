import pandas as pd
from sdamgia import SdamGIA


class SdamGIAParser:
    def __init__(self, source="olymp", subject="hist"):
        self.sdamgia = SdamGIA()
        self.source = source
        self.subject = subject

    def get_all_category_data(self, category_id, end, start=1):
        all_data = []
        for page in range(start, end + 1):
            data = self.sdamgia.get_category_by_id(self.subject, category_id, page)
            all_data.extend(data)
        return all_data

    def get_all_problems(self, category_id, end_page):
        all_data = self.get_all_category_data(category_id, end_page)
        problem_data = []

        for problem_id in all_data:
            problem = self.sdamgia.get_problem_by_id(self.subject, problem_id)
            problem_info = {
                "id": problem.get("id"),
                "topic": problem.get("topic"),
                "condition_text": problem.get("condition", {}).get("text", ""),
                "condition_images": problem.get("condition", {}).get("images", []),
                "solution_text": problem.get("solution", {}).get("text", ""),
                "solution_images": problem.get("solution", {}).get("images", []),
                "answer": problem.get("answer"),
                "analogs": problem.get("analogs", []),
                "url": problem.get("url"),
            }
            problem_data.append(problem_info)

        df = (
            pd.DataFrame(problem_data)
            .drop_duplicates(subset=["id"])
            .reset_index(drop=True)
        )
        return df

    def save_to_csv(self, df, filename):
        df.to_csv(filename, index=False)


if __name__ == "__main__":
    parser = SdamGIAParser()
    df = parser.get_all_problems(category_id="44", end_page=277)
    parser.save_to_csv(df, "data/processed/parsed_olymp_data.csv")
