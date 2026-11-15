# HW9 Mutation Testing Evidence

- **Date:** 2026-11-15
- **Source under test:** `problem_solving_lab/concepts.py` (baseline commit `7209545`)
- **Test suite:** `tests/test_concepts.py`, 23 tests, unchanged during this exercise
- **Command (run after each mutation):** `py -m pytest -q tests/`
- **Environment:** Python 3.13.15, pytest 9.2.0, Windows 11

Procedure: apply exactly one one-line change to the source, run the suite, record
the result, then restore the file with `git checkout -- problem_solving_lab/concepts.py`
before the next mutation. Test assertions were not modified.

Baseline before mutations: `23 passed`.

## Summary

| # | Function | Mutation | Result | Failing tests |
|---|---|---|---|---|
| M1 | `match_label` | `<` → `<=` on the strong threshold | Killed | 1 |
| M2 | `match_label` | `<=` → `<` on the weak threshold | Killed | 1 |
| M3 | `document_frequencies` | Counter increment replaced by constant `1` | Killed | 3 |
| M4 | `candidate_terms` | `<` → `<=` in the `min_docs` filter | Killed | 6 |
| M5 | `candidate_terms` | Score sort order inverted (`-score` → `score`) | Killed | 3 |

5 of 5 mutations killed (mutation score 100% for this sample).

## M1 — strong/moderate boundary

Line 63:

```diff
-    if distance < STRONG_BELOW:
+    if distance <= STRONG_BELOW:
```

Result: `1 failed, 22 passed`, exit code 1.

```text
FAILED tests\test_concepts.py::test_match_label_strong_moderate_boundary[0.6-moderate]
>       assert match_label(distance) == expected
E       AssertionError: assert 'strong' == 'moderate'
```

## M2 — moderate/weak boundary

Line 65:

```diff
-    if distance <= WEAK_ABOVE:
+    if distance < WEAK_ABOVE:
```

Result: `1 failed, 22 passed`, exit code 1.

```text
FAILED tests\test_concepts.py::test_match_label_moderate_weak_boundary[0.7-moderate]
>       assert match_label(distance) == expected
E       AssertionError: assert 'weak' == 'moderate'
```

## M3 — document frequency stops aggregating

Line 95:

```diff
-            df[gram] = df.get(gram, 0) + 1
+            df[gram] = 1
```

Result: `3 failed, 20 passed`, exit code 1.

```text
FAILED tests\test_concepts.py::test_document_frequency
E       AssertionError: assert {'signal': 1} == {'signal': 2}

FAILED tests\test_concepts.py::test_document_frequencies_aggregates_ngrams_across_documents
E         Differing items:
E         {'motion': 1} != {'motion': 2}

FAILED tests\test_concepts.py::test_document_frequencies_counts_duplicates_once_per_document
E         Differing items:
E         {'swarm': 1} != {'swarm': 2}
```

The handwritten first test (`test_document_frequency`) detects this mutation.

## M4 — off-by-one in the `min_docs` filter

Line 112:

```diff
-        if len(ids) < min_docs:
+        if len(ids) <= min_docs:
```

Result: `6 failed, 17 passed`, exit code 1.

```text
FAILED tests\test_concepts.py::test_candidate_terms_scores_and_ranks_by_formula
E       AssertionError: assert [] == ['alpha', 'beta']

FAILED tests\test_concepts.py::test_candidate_terms_breaks_score_ties_alphabetically
E       AssertionError: assert [] == ['alpha', 'beta']

FAILED tests\test_concepts.py::test_candidate_terms_min_docs_boundary_and_missing_df_default
E       AssertionError: assert [] == [{'term': 'al...['p1', 'p2']}]

FAILED tests\test_concepts.py::test_candidate_terms_excludes_query_words_with_plural_folding
E       AssertionError: assert [] == ['dynamics']

FAILED tests\test_concepts.py::test_candidate_terms_suppresses_components_of_selected_phrase
E       AssertionError: assert [] == ['collective motion']

FAILED tests\test_concepts.py::test_candidate_terms_top_limits_results_to_best_ranked
E       AssertionError: assert ['gamma'] == ['alpha', 'gamma']
```

Terms found in exactly two hits are now dropped. In the `top` test, only `gamma`
(present in three hits) survives.

## M5 — ranking order inverted

Line 116:

```diff
-    scored.sort(key=lambda t: (-t["score"], t["term"]))
+    scored.sort(key=lambda t: (t["score"], t["term"]))
```

Result: `3 failed, 20 passed`, exit code 1.

```text
FAILED tests\test_concepts.py::test_candidate_terms_scores_and_ranks_by_formula
E       AssertionError: assert ['beta', 'alpha'] == ['alpha', 'beta']

FAILED tests\test_concepts.py::test_candidate_terms_suppresses_components_of_selected_phrase
E       AssertionError: assert ['collective'...ctive motion'] == ['collective motion']

FAILED tests\test_concepts.py::test_candidate_terms_top_limits_results_to_best_ranked
E       AssertionError: assert ['gamma', 'alpha'] == ['alpha', 'gamma']
```

With ascending order, the component words are selected before the phrase, so
phrase suppression no longer removes them.

## Restoration

After M5 the source was restored with `git checkout`. `git status` showed no
source changes and `py -m pytest -q tests/` reported `23 passed`.
