# 🔧 clewcrew-recovery

**Recovery engine framework for the clewcrew portfolio.**

clewcrew-recovery provides automated recovery engines for fixing various types of code issues including syntax errors, indentation problems, import issues, and type annotations. Each recovery engine specializes in resolving specific types of code problems.

## 🚀 Quick Start

### Installation

```bash
# Install with pip
pip install clewcrew-recovery

# Install with UV
uv add clewcrew-recovery
```

### Basic Usage

```python
from clewcrew_recovery import SyntaxRecoveryEngine, RecoveryResult

# Initialize a syntax recovery engine
syntax_engine = SyntaxRecoveryEngine()

# Execute syntax recovery
action = {
    "target_files": ["problematic_file.py"],
    "action_type": "fix_syntax_error"
}

result = await syntax_engine.execute_recovery(action)

# Check results
if result.success:
    print(f"✅ Recovery successful: {result.message}")
    print(f"Files fixed: {result.files_fixed}")
    print(f"Confidence: {result.confidence}")
else:
    print(f"❌ Recovery failed: {result.errors}")
```

## 🏗️ Architecture

### Core Components

- **BaseRecoveryEngine**: Abstract base class for all recovery engines
- **RecoveryResult**: Standardized result format for all recovery actions
- **SyntaxRecoveryEngine**: Specialized engine for syntax error recovery

### Recovery Engine Capabilities

Each recovery engine provides:

- **Issue Detection**: Identify specific types of code problems
- **Automated Fixes**: Apply fixes to resolve issues
- **Confidence Scoring**: Assess the reliability of recovery actions
- **Action Validation**: Ensure recovery actions are valid
- **Comprehensive Reporting**: Detailed results of recovery operations

## 🔧 Dependencies

- **clewcrew-common**: Shared utilities and patterns
- **clewcrew-framework**: Base classes and abstractions
- **pydantic**: Data validation and settings management

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/clewcrew_recovery --cov-report=html
```

## 📚 Documentation

- [API Reference](https://github.com/louspringer/clewcrew-recovery#readme)
- [Recovery Engine Development Guide](https://github.com/louspringer/clewcrew-recovery#engine-development)
- [Examples](https://github.com/louspringer/clewcrew-recovery#examples)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/louspringer/clewcrew-recovery/blob/main/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to recover from code issues with the clewcrew revolution!** 🔧✨






