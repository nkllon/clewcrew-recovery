"""
Tests for the SyntaxRecoveryEngine.
"""

import pytest

from clewcrew_recovery.syntax_recovery_engine import SyntaxRecoveryEngine


class TestSyntaxRecoveryEngine:
    """Test the SyntaxRecoveryEngine class."""

    @pytest.fixture
    def syntax_engine(self):
        """Create a test syntax recovery engine."""
        return SyntaxRecoveryEngine()

    def test_engine_initialization(self, syntax_engine):
        """Test engine initialization."""
        assert syntax_engine.engine_type == "SyntaxRecoveryEngine"
        assert syntax_engine.logger is not None

    def test_get_recovery_actions(self, syntax_engine):
        """Test getting available recovery actions."""
        actions = syntax_engine.get_recovery_actions()
        assert "fix_syntax_error" in actions
        assert "validate_syntax" in actions
        assert "auto_format_code" in actions
        assert len(actions) == 3

    def test_validate_action_valid(self, syntax_engine):
        """Test action validation with valid action."""
        action = {
            "target_files": ["test.py", "main.py"],
            "action_type": "fix_syntax_error",
        }
        assert syntax_engine.validate_action(action) is True

    def test_validate_action_invalid_no_target_files(self, syntax_engine):
        """Test action validation with missing target_files."""
        action = {"action_type": "fix_syntax_error"}
        assert syntax_engine.validate_action(action) is False

    def test_validate_action_invalid_file_extension(self, syntax_engine):
        """Test action validation with non-Python files."""
        action = {
            "target_files": ["test.py", "main.txt"],
            "action_type": "fix_syntax_error",
        }
        assert syntax_engine.validate_action(action) is False

    @pytest.mark.asyncio
    async def test_execute_recovery_valid_syntax(self, syntax_engine, tmp_path):
        """Test recovery execution with valid syntax."""
        # Create a Python file with valid syntax
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
def hello():
    print("Hello, World!")

if __name__ == "__main__":
    hello()
"""
        )

        action = {"target_files": [str(test_file)], "action_type": "validate_syntax"}

        result = await syntax_engine.execute_recovery(action)

        assert result.success is True
        assert result.engine_name == "SyntaxRecoveryEngine"
        assert result.files_fixed == []  # No files needed fixing
        assert result.errors == []
        assert result.confidence > 0.8

    @pytest.mark.asyncio
    async def test_execute_recovery_invalid_syntax(self, syntax_engine, tmp_path):
        """Test recovery execution with invalid syntax."""
        # Create a Python file with invalid syntax
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
def hello(
    print("Hello, World!")  # Missing closing parenthesis

if __name__ == "__main__":
    hello()
"""
        )

        action = {"target_files": [str(test_file)], "action_type": "fix_syntax_error"}

        result = await syntax_engine.execute_recovery(action)

        assert result.success is True  # Engine handled the error gracefully
        assert result.engine_name == "SyntaxRecoveryEngine"
        assert str(test_file) in result.files_fixed
        assert len(result.warnings) > 0  # Should have syntax warnings
        assert result.confidence < 0.9  # Lower confidence due to warnings

    @pytest.mark.asyncio
    async def test_execute_recovery_nonexistent_file(self, syntax_engine):
        """Test recovery execution with nonexistent file."""
        action = {"target_files": ["nonexistent.py"], "action_type": "fix_syntax_error"}

        result = await syntax_engine.execute_recovery(action)

        assert result.success is True  # Engine handled the error gracefully
        assert result.engine_name == "SyntaxRecoveryEngine"
        assert len(result.errors) > 0  # Should have file not found error

    def test_calculate_confidence(self, syntax_engine):
        """Test confidence calculation."""
        # Test with no errors or warnings
        confidence = syntax_engine.calculate_confidence([], [])
        assert confidence == 0.8

        # Test with warnings
        confidence = syntax_engine.calculate_confidence([], ["warning1", "warning2"])
        assert confidence < 0.8

        # Test with errors
        confidence = syntax_engine.calculate_confidence(["error1"], [])
        assert confidence < 0.8

        # Test with both errors and warnings
        confidence = syntax_engine.calculate_confidence(["error1"], ["warning1"])
        assert confidence < 0.8


if __name__ == "__main__":
    pytest.main([__file__])
