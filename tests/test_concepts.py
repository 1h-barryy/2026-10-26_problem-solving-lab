"""Unit tests for concepts.py, portable to the Problem-Solving Lab repo.

"""

from concepts import document_frequencies

def test_document_frequency():
    # Arrange
    documents = ["signal and signal", "signal"]

    # Act
    actual = document_frequencies(documents)

    # Assert
    expected = {"signal": 2}
    assert actual == expected


# First test: document_frequencies should count a term once per document.
# Arrange: documents containing "signal and signal" and "signal".
# Act: call document_frequencies with those documents.
# Assert: compare the result with the hand-calculated expected dictionary.
# Write your own test_ function below. See README.md for the remaining plan.


# ---------------------------------------------------------------------------
# Additional tests. Expected values below are calculated by hand from the
# documented rules, not produced by calling the function under test.
# ---------------------------------------------------------------------------

import math

import pytest

import problem_solving_lab.concepts as concepts_module
from problem_solving_lab.concepts import (
    STRONG_BELOW,
    WEAK_ABOVE,
    candidate_terms,
    match_label,
)
from problem_solving_lab.concepts import document_frequencies as pkg_document_frequencies


def test_shim_and_package_expose_the_same_logic():
    # The legacy top-level ``concepts`` import must resolve to the restructured package.
    import concepts

    assert concepts is concepts_module
    assert document_frequencies is pkg_document_frequencies


# --- document_frequencies -------------------------------------------------

def test_document_frequencies_empty_inputs():
    assert pkg_document_frequencies([]) == {}
    assert pkg_document_frequencies(["", "   "]) == {}


def test_document_frequencies_aggregates_ngrams_across_documents():
    documents = ["collective motion", "motion", ""]

    actual = pkg_document_frequencies(documents)

    assert actual == {"collective": 1, "collective motion": 1, "motion": 2}


def test_document_frequencies_counts_duplicates_once_per_document():
    documents = ["swarm swarm swarm", "Swarm robots"]

    actual = pkg_document_frequencies(documents)

    # "swarm" appears 4 times in total but only in 2 documents; case is folded.
    assert actual == {
        "swarm": 2,
        "swarm swarm": 1,
        "swarm swarm swarm": 1,
        "robots": 1,
        "swarm robots": 1,
    }


def test_document_frequencies_excludes_stopwords_numbers_and_short_tokens():
    assert pkg_document_frequencies(["THE and 123 ab"]) == {}
    # Ineligible tokens also break n-grams: no "flocking birds" across "of".
    assert pkg_document_frequencies(["flocking of birds"]) == {"flocking": 1, "birds": 1}


# --- candidate_terms ------------------------------------------------------

def _hits(*documents):
    return [{"id": f"p{i}", "document": doc} for i, doc in enumerate(documents, start=1)]


def test_candidate_terms_empty_hits_returns_empty_list():
    assert candidate_terms("anything", [], {"alpha": 1}, corpus_size=10) == []


def test_candidate_terms_scores_and_ranks_by_formula():
    hits = _hits("alpha and beta", "alpha and beta")
    df = {"alpha": 2, "beta": 4}

    actual = candidate_terms("unrelated", hits, df, corpus_size=4)

    # alpha: 2 hits * ln(4/2) = 2 ln 2 ; beta: 2 hits * ln(4/4) = 0
    assert [t["term"] for t in actual] == ["alpha", "beta"]
    assert actual[0]["score"] == pytest.approx(2 * math.log(2))
    assert actual[1]["score"] == pytest.approx(0.0)
    assert actual[0]["paper_ids"] == ["p1", "p2"]
    assert actual[1]["paper_ids"] == ["p1", "p2"]


def test_candidate_terms_breaks_score_ties_alphabetically():
    hits = _hits("beta and alpha", "beta and alpha")
    df = {"alpha": 2, "beta": 2}

    actual = candidate_terms("unrelated", hits, df, corpus_size=8)

    assert [t["term"] for t in actual] == ["alpha", "beta"]
    assert actual[0]["score"] == pytest.approx(actual[1]["score"])
    assert actual[0]["score"] == pytest.approx(2 * math.log(4))


def test_candidate_terms_min_docs_boundary_and_missing_df_default():
    # alpha is in exactly 2 hits (kept), beta in only 1 (dropped by min_docs=2).
    hits = _hits("alpha and beta", "alpha")

    actual = candidate_terms("unrelated", hits, df={}, corpus_size=10)

    assert actual == [
        {"term": "alpha", "score": pytest.approx(2 * math.log(10 / 1)), "paper_ids": ["p1", "p2"]}
    ]


def test_candidate_terms_excludes_query_words_with_plural_folding():
    hits = _hits("group dynamics", "group dynamics")

    actual = candidate_terms("groups", hits, df={}, corpus_size=5)

    # "group" and "group dynamics" contain the (folded) query word and are excluded.
    assert [t["term"] for t in actual] == ["dynamics"]
    assert actual[0]["score"] == pytest.approx(2 * math.log(5))


def test_candidate_terms_suppresses_components_of_selected_phrase():
    hits = _hits("collective motion", "collective motion")
    df = {"collective motion": 1, "collective": 3, "motion": 3}

    actual = candidate_terms("unrelated", hits, df, corpus_size=9)

    # Phrase scores 2 ln 9 > components 2 ln 3, is selected first, then suppresses both.
    assert [t["term"] for t in actual] == ["collective motion"]
    assert actual[0]["score"] == pytest.approx(2 * math.log(9))


def test_candidate_terms_top_limits_results_to_best_ranked():
    hits = _hits("alpha and gamma", "alpha and gamma", "gamma")
    df = {"alpha": 1, "gamma": 3}

    full = candidate_terms("unrelated", hits, df, corpus_size=3)
    limited = candidate_terms("unrelated", hits, df, corpus_size=3, top=1)

    # alpha: 2 * ln 3 ; gamma: 3 * ln 1 = 0
    assert [t["term"] for t in full] == ["alpha", "gamma"]
    assert full[1]["paper_ids"] == ["p1", "p2", "p3"]
    assert limited == [
        {"term": "alpha", "score": pytest.approx(2 * math.log(3)), "paper_ids": ["p1", "p2"]}
    ]


# --- match_label ----------------------------------------------------------

def test_match_label_thresholds_are_as_documented():
    assert STRONG_BELOW == 0.60
    assert WEAK_ABOVE == 0.70


@pytest.mark.parametrize(
    "distance, expected",
    [
        (math.nextafter(0.60, 0.0), "strong"),
        (0.60, "moderate"),
        (math.nextafter(0.60, 1.0), "moderate"),
    ],
)
def test_match_label_strong_moderate_boundary(distance, expected):
    assert match_label(distance) == expected


@pytest.mark.parametrize(
    "distance, expected",
    [
        (math.nextafter(0.70, 0.0), "moderate"),
        (0.70, "moderate"),
        (math.nextafter(0.70, 1.0), "weak"),
    ],
)
def test_match_label_moderate_weak_boundary(distance, expected):
    assert match_label(distance) == expected


@pytest.mark.parametrize("distance, expected", [(0.0, "strong"), (0.65, "moderate"), (2.0, "weak")])
def test_match_label_representative_values(distance, expected):
    assert match_label(distance) == expected
