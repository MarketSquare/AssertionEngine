from approvaltests import verify_all  # type: ignore

from assertionengine.assertion_engine import split_operator, Assertion, AssertionOperator


def test_split_assertion():
    results = [
        split_operator(AssertionOperator.equal),
        split_operator(AssertionOperator["==::normalize spaces"]),
        split_operator(None)
    ]
    verify_all("Test split_operator", results)


def to_string(operator: Assertion):
    return f"'{operator.assertion}''{operator.rule}'"
