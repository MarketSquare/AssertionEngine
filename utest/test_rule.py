from approvaltests import verify_all  # type: ignore

from assertionengine.rule import apply


def test_rule():
    results = [
        formatting(apply(None, "tidii")),
        formatting(apply("normalize spaces", "   tidii kala   ")),
    ]
    try:
        apply("not valid rule", "tidii")
    except Exception as error:
        results.append(str(error))
    verify_all("Apply rules", results)


def formatting(value):
    return f'""{value}""'
