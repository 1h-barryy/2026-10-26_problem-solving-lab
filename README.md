# Problem-Solving Lab

*A tool for discovering academic concepts through everyday questions.*

## 1. About the Project

I built this project because sometimes we know what problem we're facing, but don't know the right terms to search for or technical term to express it.

Problem-Solving Lab lets users describe a problem in natural language and find related research, technical terminology, and possible connections across different fields.

Instead of just searching for papers, I wanted to help users better understand what their problem might actually be called.

## 2. Dataset

I used the arXiv API to collect **399 real research papers** across several fields, including human-computer interaction, cognitive science, robotics, and collective behavior.

Each document contains a paper's title and abstract, along with its category and source information.

The papers are stored in a persistent ChromaDB collection using the `all-MiniLM-L6-v2` embedding model.

Each database item represents one paper, using its title and abstract as searchable text. The metadata includes the paper ID, academic categories, publication date, and source URL.

I did not split the papers into smaller chunks in this version. Some longer abstracts are truncated by the embedding model.

## 3. How It Works

Users can enter a question in everyday language, and the app searches for semantically related research.

The results are organized into a Discovery Card showing:

- Related technical terms
- Relevant academic fields
- Possible cross-disciplinary connections
- Research papers and their sources

Users can also add their own notes, search for them immediately, and find them again after restarting the app.

## 4. Why Semantic Search?

I wanted to test whether a vector database could connect everyday descriptions with academic language, even when they don't use the same words.

**Example 1 — Collective Motion**

Query: "My stars move like they are following the same invisible clock; how could they behave more naturally as a group?"

Result: *Intermittent Flocking and Fractal Collective Order Induced by Time-Varying Delays*

Rank 1 · Cosine distance: 0.582

**Example 2 — Task Interruptions**

Query: "Every time a notification pops up I get distracted and it takes ages to focus again."

Result: *Mitigating the Effects of Reading Interruptions by Providing Reviews and Previews*

Rank 3 · Cosine distance: 0.537

Neither matched paper shares exact non-stopword terms with its query in our evaluation. A simple exact-keyword search would miss these connections, while semantic search was able to retrieve them.

## 5. Setup and Run

The application runs locally using Python, ChromaDB, and Streamlit.

**Requirements:** Python 3.13

### Installation

Create a virtual environment and install dependencies:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Build the Database

Download the research papers from arXiv:

```powershell
.\.venv\Scripts\python.exe -m scripts.fetch_arxiv
```

On a fresh database, create the smoke-test collection used by the ingestion
configuration comparison, then generate embeddings and store the papers:

```powershell
.\.venv\Scripts\python.exe -m scripts.smoke_test
.\.venv\Scripts\python.exe -m scripts.ingest
```

The database is stored locally in `data/chroma/`.

The initial dataset is not included in GitHub. These setup commands allow users to build their own local database. They only need to do this once unless they want to rebuild it.

### Run the Web App

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

The app has two main sections:

- **Explore:** Ask a question, discover related academic terminology, and explore research through Discovery Cards.
- **Add Knowledge:** Save personal notes and retrieve them through semantic search.

The original CLI is also available:

```powershell
.\.venv\Scripts\python.exe cli.py
```

## 6. Technical Details

- **Vector Database:** ChromaDB 1.5.9, using persistent local storage
- **Embedding Model:** all-MiniLM-L6-v2 (384 dimensions)
- **Distance Metric:** Cosine
- **Dataset:** 399 arXiv papers at the time of development
- **Frontend:** Streamlit
- **Search Results:** Candidate terminology, academic categories, related papers, and potential connections

The embedding model downloads automatically on first use. Once downloaded, it runs locally.

The current version does not use an LLM or RAG.

### Repository Map

Run the commands in this README from the repository root. The two application
entry points remain there; shared modules and utilities are grouped below.
Paths in `problem_solving_lab/lab_common.py` remain anchored to the repository
root, not the package directory or the shell's working directory.

| Files | Role |
|---|---|
| `app.py`, `cli.py` | Streamlit and interactive CLI entry points; both use the shared retrieval and Discovery Card modules. |
| `problem_solving_lab/retrieval.py` | Opens the persistent `papers` collection, searches, adds notes, and reports counts. |
| `problem_solving_lab/concepts.py`, `problem_solving_lab/card.py` | Extract candidate terms and build/render Discovery Cards from retrieval results. |
| `problem_solving_lab/lab_common.py` | Shared data paths, collection configuration, embedding function, and text helpers. |
| `concepts.py` | Compatibility alias for callers that still use `import concepts`. |
| `scripts/fetch_arxiv.py`, `scripts/ingest.py` | Fetch/cache/deduplicate arXiv records, then embed and upsert them into ChromaDB. |
| `scripts/preview_arxiv.py` | Standalone metadata preview; does not save records. |
| `scripts/smoke_test.py` | Existing persistence/semantic-search check; writes sample notes to `smoke_test_notes` in the same database. |
| `scripts/eval_queries.py`, `scripts/case_evidence.py` | Existing corpus evaluation and supporting-evidence scripts. |
| `.streamlit/config.toml` | Local server settings and UI theme. |
| `requirements.txt`, `.gitignore` | Pinned application dependencies and exclusions for local artifacts. |
| `docs/PROJECT_NOTES.md`, `docs/prompt_log.md` | Historical Phase 1 planning notes and development prompts, preserved as written; see this README for current paths and commands. |
| `tests/` | Pytest unit tests for `concepts.py` and their dependency file; see `tests/README.md`. |
| `.github/workflows/tests.yml` | GitHub Actions: runs `tests/` with Python 3.13 on every push and pull request. |
| `TESTING.md`, `prompt_log.md` | HW9 testing report and HW9 prompt log. |
| `docs/HW9_MUTATION_EVIDENCE.md`, `docs/HW9_VERIFIER_EVIDENCE.md`, `docs/HW9_VERIFIER_DIFF.patch` | Mutation-testing and AI verifier evidence. |

Data flows from arXiv through `fetch_arxiv.py` into `data/raw/arxiv/` (cached feeds)
and `data/processed/arxiv_papers.jsonl` (deduplicated records). `ingest.py` reads
those records and writes embeddings and metadata to `data/chroma/`. Both interfaces
query that database through `retrieval.py`, then use `concepts.py` and `card.py`
to present results. Added notes go directly into the same `papers` collection;
CLI exports go into `cards/`. These generated directories are Git-ignored.

**Existing setup dependency:** `ingest.py` currently reads the `smoke_test_notes`
collection for a configuration comparison before ingesting papers. On a fresh
database, run `python -m scripts.smoke_test` with the project environment first to create
that collection. This script writes sample data; `--reset` deletes and rebuilds
only that collection.

### Utility Commands and Import Compatibility

Utilities now run as modules from the repository root (instead of commands such
as `python ingest.py` or `python scripts/ingest.py`):

```powershell
.\.venv\Scripts\python.exe -m scripts.preview_arxiv --help
.\.venv\Scripts\python.exe -m scripts.fetch_arxiv --help
.\.venv\Scripts\python.exe -m scripts.smoke_test --help
.\.venv\Scripts\python.exe -m scripts.eval_queries
.\.venv\Scripts\python.exe -m scripts.case_evidence
```

New Python code should import from `problem_solving_lab`, for example
`from problem_solving_lab.concepts import candidate_terms`. The root `concepts.py`
aliases the same module, including private helpers, so existing HW9 imports such
as `import concepts` continue to work when the repository root is on `sys.path`.
Other old core imports (`card`, `retrieval`, `lab_common`) must use the package
prefix.

### Running the Tests

The unit tests need only pytest, not the full app dependencies or a database:

```powershell
py -m pip install -r tests/requirements-dev.txt
py -m pytest -q tests/
```

Pass `tests/` explicitly so `scripts/smoke_test.py` is not collected. See
`TESTING.md` for the testing report.

## 7. Limitations and Future Work

This is an early prototype with a relatively small research dataset.

Some abstracts exceed the embedding model's input limit, and terminology extraction still relies on heuristics. Cross-disciplinary connections are exploratory rather than verified solutions.

I'd like to improve this by adding better document chunking, expanding the research database, and eventually exploring AI and RAG to provide more useful explanations and connections.

## 8. AI Usage

I used ChatGPT for brainstorming and refining the project idea, Claude.ai for additional planning and prompt drafting, and Claude Code for implementation, debugging, and testing.

After completing the CLI, I also used Claude Code to develop a simple Streamlit interface.

The main development prompts are documented separately in `docs/prompt_log.md`.
Prompts for the HW9 testing work are in `prompt_log.md`.
