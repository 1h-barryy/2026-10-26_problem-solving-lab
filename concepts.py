"""Compatibility alias for existing callers using ``import concepts``.

New code should import ``problem_solving_lab.concepts``.
"""

import sys

from problem_solving_lab import concepts as _concepts

sys.modules[__name__] = _concepts
