from approvaltests import verify  # type: ignore

from assertionengine import AssertionOperator
from assertionengine.assertion_engine import NumericalOperators, SequenceOperators, EvaluationOperators, handlers


def test_assertion_operator():
    results = [f"{item.name}::{item.value}" for item in AssertionOperator]
    results.insert(0, str(AssertionOperator))
    verify("\n".join(results))


def test_numerical_operators():
    results = [f"{item}" for item in NumericalOperators]
    verify("\n".join(results))


def test_sequence_operators():
    results = [f"{item}" for item in SequenceOperators]
    verify("\n".join(results))


def test_evaluation_operators():
    results = [f"{item}" for item in EvaluationOperators]
    verify("\n".join(results))


def test_handlers():
    results = [f"{item}::{str(handlers[item]).split(' ')[4:]}" for item in handlers]
    verify("\n".join(results))
