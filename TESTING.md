# Testing — Tests as Guardrails

This is my report on adding unit tests, mutation testing, CI, and an AI verifier
experiment to Problem-Solving Lab.

## 1. Starting Point

Before testing, I cleaned up the project structure. The core logic moved into
`problem_solving_lab/`, utilities moved into `scripts/`, and documentation moved
into `docs/`. `app.py` and `cli.py` stayed at the root, and the database path is
still `data/chroma/`. A small root `concepts.py` keeps the old `import concepts`
working, so tests and older code reach the same module.

I chose `problem_solving_lab/concepts.py` for testing because it holds the
transparent heuristics behind the Discovery Card, and it only needs the Python
standard library. The tests don't need ChromaDB, Streamlit, an API key, or a
network connection.

## 2. What I Tested

All tests are in [`tests/test_concepts.py`](tests/test_concepts.py). I wrote the
first one, `test_document_frequency`, by hand. Claude Code added the remaining
tests from my prompt. The expected values are worked out from the documented
rules, not produced by calling the function being tested.

| Function | What the tests check |
|---|---|
| `document_frequencies()` | Each term is counted once per document, n-grams are aggregated across documents, stopwords/numbers/short words are excluded, empty input returns `{}` |
| `candidate_terms()` | The score formula `hits × ln(N / df)`, ranking, alphabetical tie-breaking, the `min_docs` cutoff, excluding query words (with plural folding), suppressing words already inside a selected phrase, the `top` limit |
| `match_label()` | Exact thresholds and the nearest floating-point values around `0.60` and `0.70` |

One extra test checks that `import concepts` and `problem_solving_lab.concepts`
are the same module after the restructuring.

Result: **23 passed** (15 test functions; parameterized cases bring the total to 23).

```powershell
py -m pytest -q tests/
```

## 3. Mutation Testing

To check whether the tests actually catch bugs, I made five one-line changes to
the source, one at a time, and ran the suite after each one. All five were caught.

| # | Change | Failing tests |
|---|---|---|
| M1 | `match_label`: `<` → `<=` at 0.60 | 1 |
| M2 | `match_label`: `<=` → `<` at 0.70 | 1 |
| M3 | `document_frequencies`: count replaced with `1` | 3, including my handwritten test |
| M4 | `candidate_terms`: `min_docs` check `<` → `<=` | 6 |
| M5 | `candidate_terms`: ranking order reversed | 3 |

The exact diffs and failure messages are in
[`docs/HW9_MUTATION_EVIDENCE.md`](docs/HW9_MUTATION_EVIDENCE.md).

The boundary mutations (M1, M2) were only caught by the tests that use values
exactly at the threshold. Without those tests, an off-by-one change in the match
labels would have passed silently.

## 4. GitHub Actions

[`.github/workflows/tests.yml`](.github/workflows/tests.yml) runs the suite on
every push and pull request with Python 3.13. It only runs `tests/`, so
`scripts/smoke_test.py` (which needs ChromaDB and a local database) isn't collected.

| Run | Commit | Result |
|---|---|---|
| [First CI run](https://github.com/1h-barryy/2026-10-26_problem-solving-lab/actions/runs/43769468358) | `929db0a` | Passed |
| [Deliberate bug (M1)](https://github.com/1h-barryy/2026-10-26_problem-solving-lab/actions/runs/43769566482) | `37ee481` | Failed: `test_match_label_strong_moderate_boundary[0.6-moderate]` |
| [Verifier fix](https://github.com/1h-barryy/2026-10-26_problem-solving-lab/actions/runs/43772053722) | `850a466` | Passed |

## 5. AI Verifier Experiment

I put mutation M1 back into the source on the `faulty-test` branch and gave a
separate AI session a neutral prompt: the suite is failing, find the problem,
don't weaken or skip tests, and don't look at the mutation notes or Git history.

The verifier reproduced the failure (1 failed, 22 passed), found that exactly
`0.60` returned `strong` instead of `moderate`, and changed `<=` back to `<`.
It didn't touch any tests, and the suite went back to 23 passed.

The prompt, response excerpts, and test output are in
[`docs/HW9_VERIFIER_EVIDENCE.md`](docs/HW9_VERIFIER_EVIDENCE.md), and the diff is in
[`docs/HW9_VERIFIER_DIFF.patch`](docs/HW9_VERIFIER_DIFF.patch).

## 6. What I Learned

Passing tests only mean something if they would fail when the code is wrong.
Mutation testing showed me that, and the boundary tests turned out to be the
most valuable ones. CI made the deliberate bug visible as a red run without
me running anything locally.

## 7. Limitations

- The tests only cover `concepts.py`. Retrieval, ChromaDB, the Discovery Card
  rendering, and the Streamlit app are not unit tested.
- The mutations were chosen by hand. This was not a full mutation-testing tool run.
- No separate fake-test experiment is recorded in this repository.
- The verifier knew the suite was failing, so the experiment shows it can
  diagnose a known failure, not find bugs without a failing test.

## 8. AI Usage

I used Codex to clean up and restructure the repository, Claude Code (Claude
Opus 5.5) to complete the tests, run the mutations, and set up CI, and a
separate AI session for the verifier. The HW9 prompts are in
[`prompt_log.md`](prompt_log.md).
