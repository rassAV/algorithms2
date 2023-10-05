import pytest
from pref_to_inf import pref_to_inf

@pytest.fixture
def expressions():
    return "+ - 13 4 55", "+ 2 * 2 - 2 1", "+ + 10 20 30", "- - 1 2", "/ + 3 10 * - 2 3 - 3 5", "1 2", "dfg", "+ 1 2 - 3 567", "+ - * 1 2", "2 34 fd 43", -1

@pytest.fixture
def answers():
    return "13 + 4 - 55", "2 * 2 - 2 + 1", "10 + 20 + 30", "1 - 2 -", "3 / 10 * 2 + 3 - 3 - 5", "1 2", "dfg", "1 + 2 - 3 567", "1 + 2 - *", "2 34 fd 43", -1

def test_pref_to_inf(expressions, answers):
    exp = expressions
    ans = answers
    for i in range(len(exp)):
        assert pref_to_inf(exp[i]) == ans[i]