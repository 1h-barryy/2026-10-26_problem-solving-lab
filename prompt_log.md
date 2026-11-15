# HW9 — Tests as Guardrails: Prompt Log

This log records user prompts visible verbatim in the current conversation.
The first two concern preparation of this repository for HW9; the third requests
the final documentation. Entries 4–7 (Claude Code) cover implementing the tests,
mutation testing, CI, and preparing the verifier experiment.

Tool for these three entries: **Codex** (this conversation).
Exact model/version for each entry: **[MISSING — supply the model shown in the
original session; an exact model identifier is not available in this transcript.]**
Individual prompt timestamps: **[MISSING — supply from the original conversation
export if needed.]** The entries below follow their observed conversation order.

The HW6 log remains separately preserved at `docs/prompt_log.md`.

## 1. Repository inspection and minimal cleanup

Verbatim user prompt:

```text
We are working in my existing Problem-Solving Lab repository.

Before starting testing, I want to clean up the project structure and make the codebase easier to maintain.

### Step 1 — Inspect
- Review the entire repository structure, source files, dependencies, and entry points.
- Identify how Streamlit, ChromaDB, semantic retrieval, data processing, and CLI components connect.
- Check for redundant files, unused code, confusing organization, or unnecessary generated files.
- Check the current Git status and preserve all existing uncommitted changes.

### Step 2 — Safe Cleanup
- Make only small, low-risk structural improvements that do not change application behavior.
- Improve organization and remove unnecessary clutter where clearly safe.
- Preserve all working features, imports, database paths, configuration, and existing connections.
- Do not move or rename core modules if doing so could break dependencies.
- Do not delete project data, database files, or existing documentation.

### Step 3 — Verification
- Verify that the Streamlit app, CLI, and retrieval pipeline still work.
- Run available checks and report what was actually verified.
- Compare the project structure before and after cleanup.

### Constraints
- No new features or functional changes.
- No testing implementation, mutation testing, or CI setup yet.
- Do not copy or create HW9 test files. I will do that manually later.
- Do not commit or push.
- If a structural change is risky or cannot be verified, leave it unchanged and explain why.

Keep the cleanup minimal, reversible, and focused on maintainability.

At the end, summarize all changes, verification results, and anything that still needs attention.
```

## 2. Folder restructuring before HW9 test transfer

Verbatim user prompt:

```text
I want to improve the folder structure of my existing Problem-Solving Lab repository.

The goal is a cleaner, more readable, and maintainable Python project without changing any existing application behavior.

### Proposed Structure
- Keep `app.py` and `cli.py` as root entry points.
- `problem_solving_lab/` — core modules such as concepts, retrieval, card generation, and shared utilities.
- `scripts/` — data ingestion, evaluation, and development utilities.
- `docs/` — project documentation.
- `tests/` — reserved for HW9 tests that I will transfer manually later.

### Step 1 — Audit
Inspect all imports, module dependencies, entry points, database paths, scripts, and configuration.

Check the current Git status and preserve all uncommitted changes.

### Step 2 — Establish Baseline
Before moving anything, run existing available verification checks and record their results. Identify checks that cannot be performed.

### Step 3 — Safe Restructuring
Reorganize files into logical folders, updating imports and execution paths as necessary.

Critical constraints:
- Preserve Streamlit, CLI, ChromaDB, embeddings, semantic retrieval, and existing functionality.
- Keep all existing database and data paths unchanged.
- Do not move or delete databases, datasets, secrets, or generated assets.
- Keep the same application behavior and outputs.
- Avoid unnecessary code rewrites.
- Do not modify or add HW9 tests yet.
- Existing tests will initially import `concepts` directly; flag any compatibility changes needed.
- Keep documentation accurate, including setup and execution commands.

Apply changes incrementally. If a change is risky or cannot be verified, leave it unchanged and explain why.

### Step 4 — Verification
Verify imports, CLI execution, Streamlit startup, and the retrieval pipeline wherever dependencies and data are available.

Compare verification results with the baseline and report all changes.

Do not commit or push.

At the end, provide the final folder tree, modified files, verification results, and any remaining risks.
```

## 3. Final HW9 documentation request

Verbatim user prompt:

```text
We are preparing the final documentation for Tests as Guardrails.

Please prepare the following:

### 1. TESTING.md
- Create an EMPTY `TESTING.md` file at the repository root.

containing verified factual evidence I can use when writing my report:
- Starting project and refactoring evidence
- Functions tested and test results
- Five mutation results from the existing evidence file
- Any documented fake tests
- Green and red GitHub Actions URLs
- Outstanding verifier evidence
- Any missing information I still need to supply

Distinguish verified facts from missing evidence. Do not invent results.

### 2. prompt_log.md
Create a separate HW9-specific `prompt_log.md` at the repository root.

- Preserve the existing HW6 prompt log in `docs/prompt_log.md`.
- Record only actual, verifiable HW9 prompts, verbatim, including their tool and model where known.
- Use clearly marked placeholders for prompts or model information you cannot access.


### Constraints
- Documentation only.
- Do not modify tests, source code, workflows, or existing documentation.
- Do not commit, merge, or push.
- Do not use the ongoing verifier's incomplete results as completed evidence.

At the end, report the files created, evidence collected, and what I still need to provide myself.
```

Tool for entries 4–7: **Claude Code** (CLI). Model: **Claude Opus 5.5
(`claude-opus-5-5`)**. Prompts were copied verbatim from the session transcript
(session `747b6a2c-ef51-4a23-a158-693df7ab153c`, 2026-11-15, 22:13–22:56 UTC) and
follow their conversation order.

## 4. Complete the unit test suite

Verbatim user prompt:

```text
We are working in my project repo. I am currently running a test for this project. First inspect the repo.
We are continuing the testing: Tests as Guardrails in the Problem-Solving Lab repository.

I have written my first unit test manually in `tests/test_concepts.py`.

Please complete the remaining unit tests using pytest.

 Preserve my handwritten first test unchanged.
 Add at least 7 additional meaningful tests, covering:
   - `document_frequencies()` — aggregation, counting, duplicates, empty inputs.
   - `candidate_terms()` — scoring accuracy, ranking, filtering, edge cases.
   - `match_label()` — threshold classification and boundary conditions.
Use deterministic, in-memory test data without ChromaDB, Streamlit, or external APIs.
 Run the complete suite using `py -m pytest -q tests/`.
 Make sure the tests validate actual expected behavior, not just whether functions execute.
Report each test's purpose and the actual PASS/FAIL results.
 Ensure the tests import the actual application logic after the recent folder restructuring.

Do not modify application logic or weaken assertions to make tests pass.

Do not start mutation testing, GitHub Actions, or AI Verifier yet.

Do not commit or push anything.

Stop after completing and verifying the test suite. I will review the results before the next phase.
```

## 5. Mutation testing, GitHub Actions, and intentional failure

Verbatim user prompt:

```text
The baseline test suite is complete and already pushed to GitHub: 23 tests passing across 3 functions.


### Part 1 — Mutation Testing
1. Make 5 different one-line mutations to the actual source code, one at a time.
2. For each mutation, run `py -m pytest -q tests/`.
3. Record the exact source change, failing test name, and actual failure message.
4. Restore the original source before the next mutation.
5. Confirm all 23 tests pass again afterward.
6. Save factual mutation evidence in `docs/HW9_MUTATION_EVIDENCE.md`.

Do not change test assertions or weaken the tests.

### Part 2 — GitHub Actions
1. Create `.github/workflows/tests.yml` using Python 3.13 and pytest.
2. Run only `tests/` to avoid collecting `scripts/smoke_test.py`.
3. Configure CI to run automatically on push and pull requests.
4. Commit and push the working CI configuration on a dedicated `hw9-testing` branch.
5. Confirm that GitHub Actions passes and record the workflow run URL.

### Part 3 — Prepare the AI Verifier Experiment
1. Select one of the five verified mutations that reliably fails an existing test.
2. Apply that one-line source mutation again.
3. Commit and push the broken source code to `faulty test`, never to main.
4. Confirm GitHub Actions fails and record the red workflow URL.
5. Leave the failing source code in place for a fresh Claude session.

Important:
- Preserve the existing application and database connections.
- Do not modify the test suite.
- Do not write `TESTING.md`; I must write it myself.
- Do not attempt to fix the final deliberate bug.
- Do not begin the AI Verifier Experiment in this session.
- Report both CI URLs, the mutation evidence, the commits, and the remaining failing test.

Stop after the red CI run is confirmed.
```

## 6. Consolidate branches into faulty-test

Verbatim user prompt:

```text
can you merge the hw9-testing to the branch as faulty-test and finally make it one branch called faulty-test
```

## 7. Record the HW9 prompt log

Verbatim user prompt:

```text
now there is another agent working so do not change any more of the structure file and help me record the prompt_log and Testing.md.
```

## Missing prompt records — placeholders, not reconstructed prompts

- **[MISSING: fake-test prompts or records, if any, and their tool/model.]** No
  explicit fake-test documentation was found in the inspected repository files.
- **Verifier prompt: recorded.** The separate verifier's original prompt and
  selected verbatim responses are in `docs/HW9_VERIFIER_EVIDENCE.md`. Its exact
  tool/model is **[MISSING — not recorded in that evidence file.]**

Replace these placeholders only with original, verifiable records. Do not infer
prompt wording, model names, or completion from source code or commit messages.
