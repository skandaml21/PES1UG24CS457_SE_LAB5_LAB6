
import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ==============================
# SCORE MESSAGE TEST CASES
# ==============================

def test_plain_message():
    assert score_message("hello there", False, 0) == 0


def test_spam_words():
    assert score_message("free winner prize", False, 0) == 6


def test_spam_words_with_punctuation():
    assert score_message("FREE! winner, PRIZE.", False, 0) == 6


def test_uppercase_word():
    assert score_message("IMPORTANT", False, 0) == 1


def test_short_uppercase_word():
    assert score_message("YES", False, 0) == 0


def test_lowercase_non_spam_word():
    assert score_message("hello world", False, 0) == 0


def test_link_count_above_three():
    assert score_message("hello", False, 4) == 4


def test_link_count_between_one_and_three():
    assert score_message("hello", False, 2) == 1


def test_link_count_zero():
    assert score_message("hello", False, 0) == 0


def test_known_sender_reduces_score():
    assert score_message("free urgent", True, 0) == 1


def test_known_sender_score_cannot_be_negative():
    assert score_message("hello", True, 0) == 0


def test_known_sender_with_zero_initial_score():
    assert score_message("", True, 0) == 0


def test_unknown_sender():
    assert score_message("free", False, 0) == 2


def test_empty_message():
    assert score_message("", False, 0) == 0


# ==============================
# CLASSIFY TEST CASES
# ==============================

def test_classify_spam():
    assert classify(8) == "spam"


def test_classify_high_spam_score():
    assert classify(10) == "spam"


def test_classify_suspicious():
    assert classify(4) == "suspicious"


def test_classify_suspicious_upper_boundary():
    assert classify(7) == "suspicious"


def test_classify_clean():
    assert classify(0) == "clean"


def test_classify_below_four():
    assert classify(3) == "clean"


# ==============================
# FILTER INBOX TEST CASES
# ==============================

def test_filter_empty_inbox():
    assert filter_inbox([]) == {
        "spam": 0,
        "suspicious": 0,
        "clean": 0
    }


def test_filter_inbox_all_categories():
    messages = [
        ("free winner prize urgent", False, 4),
        ("free urgent", False, 0),
        ("hello friend", False, 0)
    ]

    assert filter_inbox(messages) == {
        "spam": 1,
        "suspicious": 1,
        "clean": 1
    }


def test_filter_inbox_multiple_messages():
    messages = [
        ("hello", False, 0),
        ("free winner", False, 0),
        ("winner prize urgent", False, 4),
        ("IMPORTANT", False, 1)
    ]

    result = filter_inbox(messages)

    assert result["spam"] == 1
    assert result["suspicious"] == 1
    assert result["clean"] == 2


# ==============================
# INBOX STATUS TEST CASES
# ==============================

def test_inbox_status_empty():
    assert inbox_status({
        "spam": 0,
        "suspicious": 0,
        "clean": 0
    }) == "empty"


def test_inbox_status_flooded():
    assert inbox_status({
        "spam": 3,
        "suspicious": 1,
        "clean": 1
    }) == "flooded"


def test_inbox_status_noisy():
    assert inbox_status({
        "spam": 2,
        "suspicious": 1,
        "clean": 2
    }) == "noisy"


def test_inbox_status_healthy():
    assert inbox_status({
        "spam": 1,
        "suspicious": 0,
        "clean": 4
    }) == "healthy"


def test_inbox_status_exactly_twenty_percent():
    assert inbox_status({
        "spam": 1,
        "suspicious": 1,
        "clean": 3
    }) == "healthy"
