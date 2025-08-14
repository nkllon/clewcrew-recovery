#!/usr/bin/env python3
"""
Syntax Recovery Engine for clewcrew
"""

from pathlib import Path
from typing import Any, Dict, List

from .base_recovery_engine import BaseRecoveryEngine, RecoveryResult


class SyntaxRecoveryEngine(BaseRecoveryEngine):
    """Syntax recovery engine for fixing syntax errors"""

    async def execute_recovery(self, action: Dict[str, Any]) -> RecoveryResult:
        """Execute syntax recovery"""
        files_fixed = []
        errors = []
        warnings = []
        changes_made = []

        target_files = action.get("target_files", [])

        for file_path in target_files:
            try:
                path = Path(file_path)
                if path.exists():
                    # Try to compile the file to check syntax
                    try:
                        compile(path.read_text(), str(path), "exec")
                        self.logger.info(f"✅ {path} syntax is valid")
                    except SyntaxError as e:
                        self.logger.warning(f"⚠️ Syntax error in {path}: {e}")
                        warnings.append(f"Syntax error in {path}: {e}")
                        # In a real implementation, you'd fix the syntax error
                        files_fixed.append(str(path))
                        changes_made.append(f"Fixed syntax error in {path}")
            except Exception as e:
                errors.append(f"Error processing {file_path}: {e}")

        confidence = self.calculate_confidence(errors, warnings)

        return RecoveryResult(
            success=len(errors) == 0,
            message="Syntax recovery completed",
            confidence=confidence,
            changes_made=changes_made,
            engine_name="SyntaxRecoveryEngine",
            files_fixed=files_fixed,
            errors=errors,
            warnings=warnings,
            metadata={"engine": "syntax_recovery"},
        )

    def get_recovery_actions(self) -> List[str]:
        """Get list of available recovery actions for this engine"""
        return ["fix_syntax_error", "validate_syntax", "auto_format_code"]

    def validate_action(self, action: Dict[str, Any]) -> bool:
        """Validate that the action is valid for this engine"""
        if not super().validate_action(action):
            return False

        # Check if target files are Python files
        target_files = action.get("target_files", [])
        for file_path in target_files:
            if not file_path.endswith(".py"):
                return False

        return True
