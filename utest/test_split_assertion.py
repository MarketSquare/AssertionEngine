from approvaltests import verify_all  # type: ignore

from assertionengine.assertion_engine import split_operator, Assertion


def test_split_assertion():
    results = []
    results.append(split_operator("=="))
    results.append(split_operator("==::substitute space"))
    try:
        split_operator("==::substitute::space")
    except Exception as error:
        results.append(str(error))
    verify_all("Test split_operator", results)


def to_string(operator: Assertion):
    return f"'{operator.assertion}''{operator.rule}'"
