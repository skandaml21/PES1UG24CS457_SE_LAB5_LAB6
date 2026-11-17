import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ==========================================
# 1. SCORE MESSAGE - BRANCH TESTING
# ==========================================

def test_spam_word_branch():
    assert score_message("free", False, 0) == 2


def test_uppercase_word_branch():
    assert score_message("IMPORTANT", False, 0) == 1


def test_normal_word_branch():
    assert score_message("hello", False, 0) == 0


def test_link_count_greater_than_three():
    assert score_message("hello", False, 4) == 4


def test_link_count_between_one_and_three():
    assert score_message("hello", False, 2) == 1


def test_link_count_zero():
    assert score_message("hello", False, 0) == 0


def test_known_sender_negative_score():
    assert score_message("", True, 0) == 0


def test_known_sender_positive_remaining_score():
    assert score_message("free winner", True, 4) == 5


def test_unknown_sender():
    assert score_message("free", False, 0) == 2


# ==========================================
# 2. CLASSIFY - BRANCH TESTING
# ==========================================

def test_classify_spam_boundary():
    assert classify(8) == "spam"


def test_classify_suspicious_boundary():
    assert classify(4) == "suspicious"


def test_classify_clean_boundary():
    assert classify(3) == "clean"


# ==========================================
# 3. FILTER INBOX - BRANCH TESTING
# ==========================================

def test_filter_inbox_empty():
    assert filter_inbox([]) == {
        "spam": 0,
        "suspicious": 0,
        "clean": 0
    }


def test_filter_inbox_with_all_categories():
    messages = [
        ("free winner prize urgent", False, 4),
        ("free winner", False, 0),
        ("hello", False, 0)
    ]

    assert filter_inbox(messages) == {
        "spam": 1,
        "suspicious": 1,
        "clean": 1
    }


# ==========================================
# 4. INBOX STATUS - BRANCH TESTING
# ==========================================

def test_empty_inbox_status():
    assert inbox_status({
        "spam": 0,
        "suspicious": 0,
        "clean": 0
    }) == "empty"


def test_flooded_inbox_status():
    assert inbox_status({
        "spam": 4,
        "suspicious": 1,
        "clean": 2
    }) == "flooded"


def test_noisy_inbox_status():
    assert inbox_status({
        "spam": 2,
        "suspicious": 1,
        "clean": 2
    }) == "noisy"


def test_healthy_inbox_status():
    assert inbox_status({
        "spam": 1,
        "suspicious": 1,
        "clean": 4
    }) == "healthy"


def test_exactly_fifty_percent_spam():
    assert inbox_status({
        "spam": 2,
        "suspicious": 1,
        "clean": 1
    }) == "noisy"


def test_exactly_twenty_percent_spam():
    assert inbox_status({
        "spam": 1,
        "suspicious": 1,
        "clean": 3
    }) == "healthy"

