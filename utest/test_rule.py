from approvaltests import verify_all  # type: ignore

from assertionengine.rule import apply_rule


def test_rule():
    results = [
        formatting(apply_rule(None, "tidii")),
        formatting(apply_rule("normalize spaces", "   tidii kala   ")),
    ]
    try:
        apply_rule("not valid rule", "tidii")
    except Exception as error:
        results.append(str(error))
    verify_all("Apply rules", results)


def formatting(value):
    return f'""{value}""'
