"""
clewcrew-recovery

Recovery engine framework for the clewcrew portfolio.
This package provides automated recovery engines for fixing various types of
code issues including syntax errors, indentation problems, import issues, and type annotations.
"""

__version__ = "0.1.0"
__author__ = "Lou Springer"
__email__ = "lou@example.com"

from .base_recovery_engine import BaseRecoveryEngine, RecoveryResult
from .syntax_recovery_engine import SyntaxRecoveryEngine

__all__ = [
    "BaseRecoveryEngine",
    "RecoveryResult",
    "SyntaxRecoveryEngine",
]
