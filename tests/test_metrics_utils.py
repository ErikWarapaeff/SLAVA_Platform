import pytest

from src.core.metrics_utils import (
    calculate_f1_score,
    compute_matching,
    compute_multi_choice,
    compute_one_choice,
    compute_sequence,
    get_match_function,
    normalize_answer,
    only_numbers,
)


def test_answer_normalization_and_f1_are_deterministic() -> None:
    assert normalize_answer("The, Quick Fox!") == "quick fox"
    assert calculate_f1_score("red blue", "blue red") == 1.0
    assert calculate_f1_score("red", "blue") == 0


def test_numeric_answer_extractors_cover_supported_question_shapes() -> None:
    assert only_numbers("Answer: 314") == "314"
    assert only_numbers("no digits") == "-"
    assert compute_one_choice("2", "2") == 1.0
    assert compute_multi_choice("123", "124") == 0.5
    assert compute_matching("123", "12") == 0.0
    assert compute_sequence("123", "124") == 0.5


def test_unknown_question_type_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown type"):
        get_match_function("unsupported")
