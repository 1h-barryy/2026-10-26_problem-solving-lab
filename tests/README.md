# Tests

Unit tests for `problem_solving_lab/concepts.py`: counting accuracy, scoring and
ranking, filtering, and classification boundaries. The full report is in
[`../TESTING.md`](../TESTING.md).

The tests use only small, fixed, in-memory inputs. They need no Streamlit,
ChromaDB, database, API keys, or network access.

## Files

```text
tests/
    README.md             This file
    pytest.ini            Collects this folder; puts the repository root on the import path
    requirements-dev.txt  Test dependency (pytest)
    test_concepts.py      23 tests (15 functions, some parameterized)
```

## Setup and Run (PowerShell)

Run from the repository root. Only pytest is needed; installing the full app
`requirements.txt` is not required for these tests.

```powershell
py -m pip install -r tests/requirements-dev.txt
py -m pytest -q tests/
```

Expected output: `23 passed`.

Always pass `tests/` explicitly. A bare `pytest` from the root can also collect
`scripts/smoke_test.py`, which needs ChromaDB and a local database. GitHub
Actions ([`../.github/workflows/tests.yml`](../.github/workflows/tests.yml)) runs
the same command with Python 3.13 on every push and pull request.

Useful variations:

```powershell
py -m pytest tests/test_concepts.py -v
py -m pytest tests/ -k candidate_terms -v
```

## Imports

New tests import from the package, for example
`from problem_solving_lab.concepts import candidate_terms`. The first,
handwritten test uses `from concepts import document_frequencies`; the root
`concepts.py` aliases the same module, and one test checks that both names
refer to the same code.

## Function Behavior Covered

`document_frequencies(documents)` counts distinct eligible one-, two-, and
three-word n-grams per document. It lowercases text and excludes stopwords,
pure-number tokens, and tokens of two letters or fewer. A term repeated within one
document is counted once.

`candidate_terms(query, hits, df, corpus_size, top=6, min_docs=2)` scores n-grams
found in the hits:

```text
number of matching hits × ln(corpus_size / max(document_frequency, 1))
```

A missing document frequency defaults to 1. Candidates are sorted by descending
score, then alphabetically. Terms containing a query word (with crude plural
folding) are excluded, terms found in fewer than `min_docs` hits are dropped, and
a term contained in an already-selected term is skipped. Paper IDs follow hit order.

`match_label(distance)`:

| Distance | Label |
|---|---|
| Below 0.60 | `strong` |
| 0.60 through 0.70, inclusive | `moderate` |
| Above 0.70 | `weak` |

Boundary tests use `math.nextafter` for the nearest floating-point values on
either side of each threshold.

## Known Untested Behaviors

These are current behaviors, not requirements: duplicate hit IDs count multiple
times, `top=0` can still return one candidate, and a nonpositive corpus size can
raise a math-domain error.
