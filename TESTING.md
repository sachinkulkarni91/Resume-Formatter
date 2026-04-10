# Resume Formatter - Testing Guide

## Unit Tests

### Backend Tests

```bash
cd backend

# Install pytest
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Install testing libraries
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Run tests
npm run test

# With coverage
npm run test -- --coverage
```

## Integration Tests

### End-to-End Testing

```bash
# Start both services
docker-compose up

# Run E2E tests
npm run test:e2e
```

## Load Testing

### Using Apache Bench

```bash
# Install
sudo apt-get install apache2-utils

# Test parser endpoint
ab -n 100 -c 10 http://localhost:8000/api/parse-resume

# Test format endpoint (with file upload)
# Use wrk or similar for file uploads
```

### Using Locust

```bash
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class ResumeFormatterUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def parse_resume(self):
        with open('sample_resume.pdf', 'rb') as f:
            self.client.post('/api/parse-resume', files={'resume': f})

EOF

# Run
locust -f locustfile.py --host=http://localhost:8000
```

## Manual Testing Checklist

- [ ] Upload PDF resume
- [ ] Upload DOCX resume
- [ ] Upload template
- [ ] Format resume
- [ ] Download formatted document
- [ ] Verify formatting matches template
- [ ] Parse resume to JSON
- [ ] Check all sections are extracted
- [ ] Get improvement suggestions
- [ ] Extract template info
- [ ] Test with various file sizes
- [ ] Test with different template styles
- [ ] Test error handling (invalid files)
- [ ] Test CORS from frontend
- [ ] Test file cleanup (no orphaned files)

## Test Coverage

### Backend Coverage Target: 80%+

- [ ] Parser module
- [ ] Gemini service
- [ ] Document generator
- [ ] Template engine
- [ ] File handling

### Frontend Coverage Target: 70%+

- [ ] FileUpload component
- [ ] API client
- [ ] App state management
- [ ] Error handling

## Performance Benchmarks

### Backend

- Parse PDF: < 2s
- Parse DOCX: < 1s
- Format resume: < 20s (including Gemini call)
- Extract template: < 5s

### Frontend

- Initial load: < 3s
- Upload time: < 5s
- Format response display: < 2s

## Bug Reporting Template

```
**Bug Title:** Issue description

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Error Logs:**
```
Paste logs here
```

**Environment:**
- OS: Windows/Mac/Linux
- Browser: Chrome/Firefox/Safari
- Backend version: x.x.x
```

## Test Data

### Sample Resumes
- Located in `test_data/resumes/`
- Multiple formats and styles
- Different sections and layouts

### Test Templates
- Located in `test_data/templates/`
- KPMG style
- Simple format
- Complex format with logos

## CI/CD Testing

### GitHub Actions
- Runs on every push
- Automated linting
- Dependency scanning
- Docker image building
- Integration tests

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

