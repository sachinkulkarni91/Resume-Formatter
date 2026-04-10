# Contributing Guide

Thank you for interest in contributing to Resume Formatter!

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others succeed

## Getting Started

### 1. Fork the Repository
```bash
git clone https://github.com/yourusername/resume-formatter.git
cd resume-formatter
```

### 2. Set Up Development Environment

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
python -m venv venv && venv\Scripts\activate  # Windows

pip install -r requirements.txt
pip install -e .
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 3. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Making Changes

1. Make your changes
2. Add tests for new functionality
3. Update documentation
4. Follow code style guidelines

### Code Style

**Python (Backend):**
```bash
# Format with Black
pip install black
black backend/

# Lint with flake8
pip install flake8
flake8 backend/

# Type checking
pip install mypy
mypy backend/
```

**JavaScript (Frontend):**
```bash
# Format with Prettier
npx prettier --write frontend/src/

# Lint with ESLint
npm run lint
```

### Commit Guidelines

```
Type: Description

feat: Add new feature
fix: Bug fix
docs: Documentation
style: Code style
refactor: Code refactoring
test: Adding tests
chore: Maintenance
```

**Example:**
```
feat: Add multi-template support

- Allow users to upload multiple templates
- Select template during formatting
- Store templates for reuse

Closes #123
```

## Testing

### Run Tests

```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test

# E2E
npm run test:e2e
```

### Minimum Coverage

- Backend: 80%
- Frontend: 70%

### Writing Tests

**Backend (pytest):**
```python
# tests/test_parser.py
import pytest
from parser import ResumeParser

def test_parse_pdf():
    text = ResumeParser.parse_pdf('test_data/resume.pdf')
    assert 'John Doe' in text
    
def test_parse_docx():
    text = ResumeParser.parse_docx('test_data/resume.docx')
    assert len(text) > 0
```

**Frontend (vitest):**
```javascript
// src/__tests__/FileUpload.test.jsx
import { render, screen } from '@testing-library/react'
import { FileUpload } from '../FileUpload'

describe('FileUpload', () => {
  it('displays upload area', () => {
    render(<FileUpload onFileSelect={() => {}} />)
    expect(screen.getByText(/drag and drop/i)).toBeInTheDocument()
  })
})
```

## Documentation

### Update README if you:
- Add new features
- Change API endpoints
- Update dependencies
- Fix known issues

### Document your code:
```python
def format_resume(target_path: str, template_path: str) -> bytes:
    """
    Format a resume to match template.
    
    Args:
        target_path: Path to target resume (PDF/DOCX)
        template_path: Path to template (DOCX)
    
    Returns:
        Formatted DOCX as bytes
    
    Raises:
        ValueError: If file format unsupported
        IOError: If file not found
    """
    pass
```

## Pull Request Process

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages clear
- [ ] No unrelated changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
- [ ] Unit tests added
- [ ] Integration tests pass
- [ ] Manual testing done

## Checklist
- [ ] Code style followed
- [ ] No new warnings
- [ ] Documentation updated
- [ ] Tests pass locally

## Related Issues
Closes #123
```

### Review Process

1. Automated checks must pass
2. Code review by maintainer
3. Address feedback
4. Final approval
5. Merge to develop
6. Release in next version

## Reporting Bugs

### Bug Report Template

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. First step
2. Second step
3. Third step

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows 10
- Python: 3.11
- Node: 18.x
- Browser: Chrome

## Error Logs
(Paste relevant logs)

## Additional Context
Any other relevant information
```

## Feature Requests

### Feature Request Template

```markdown
## Summary
Brief summary of requested feature

## Motivation
Why is this feature needed?

## Proposed Solution
How should this work?

## Alternatives
Other possible approaches

## Additional Context
Links, examples, references
```

## Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [React Best Practices](https://react.dev/learn)
- [Git Documentation](https://git-scm.com/doc)
- [Issue Templates](.github/ISSUE_TEMPLATE/)

## Development Tips

### Useful Commands

**Backend:**
```bash
# Watch for changes and reload
pip install python-dotenv watchdog[watchmedo]
watchmedo auto-restart -d backend -p '*.py' -- python main.py

# Run with debug output
PYTHONUNBUFFERED=1 python main.py

# Interactive debugging
python -m pdb main.py
```

**Frontend:**
```bash
# Fast refresh
npm run dev -- --port 5173

# Build and preview
npm run build && npm run preview

# Debug in VS Code
# Add .vscode/launch.json with Chrome debugger
```

## Getting Help

- Check existing issues
- Read documentation
- Ask in discussions
- Contact maintainers

## Appreciation

Thank you for contributing! Your work helps make Resume Formatter better for everyone.

### Recognition

Contributors are acknowledged in:
- README.md contributors section
- Release notes
- GitHub contributors graph

---

**Happy coding!** 🚀

