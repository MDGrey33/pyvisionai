# Test Suite Refactoring Plan

## Current Issues

1. **API Quota Errors**: Many tests are making real OpenAI API calls and hitting quota limits
2. **Poor Test Isolation**: Tests depend on external services and aren't properly mocked
3. **Inconsistent Markers**: Tests lack proper categorization (unit vs integration vs e2e)
4. **Slow Execution**: Real API calls and file operations make tests slow
5. **Mock Issues**: subprocess.run mocking conflicts between different test types

## Test Classification Strategy

### 1. Unit Tests (70%)
- **Characteristics**: Fast, isolated, fully mocked
- **Markers**: `@pytest.mark.unit`
- **Examples**:
  - Model initialization tests
  - Configuration validation tests
  - Error handling tests
  - Business logic tests
- **Mocking**: All external dependencies (APIs, file I/O, subprocess)

### 2. Integration Tests (20%)
- **Characteristics**: Test component integration, some mocking
- **Markers**: `@pytest.mark.integration`
- **Examples**:
  - CLI command execution (with mocked APIs)
  - File extraction flow (with test data)
  - Model factory integration
- **Mocking**: External APIs only

### 3. E2E Tests (10%)
- **Characteristics**: Real API calls, full system tests
- **Markers**: `@pytest.mark.e2e`
- **Examples**:
  - Real OpenAI API tests
  - Real Ollama tests
  - Full extraction pipeline
- **Requirements**: API keys, services running

## Implementation Steps

### Phase 1: Fix Immediate Issues (Critical)
1. [ ] Add proper markers to all existing tests
2. [ ] Fix subprocess.run mocking conflicts
3. [ ] Mock all OpenAI API calls in non-e2e tests
4. [ ] Create test fixtures for common scenarios

### Phase 2: Improve Test Structure
1. [ ] Reorganize tests by feature/module
2. [ ] Create shared fixtures in conftest.py
3. [ ] Implement proper test data management
4. [ ] Add parameterized tests for better coverage

### Phase 3: Performance Optimization
1. [ ] Mock time.sleep globally for unit tests
2. [ ] Create lightweight test data
3. [ ] Implement parallel test execution
4. [ ] Add test result caching

### Phase 4: Documentation and CI
1. [ ] Document test running strategies
2. [ ] Create CI-specific test configurations
3. [ ] Add test coverage reporting
4. [ ] Create developer testing guide

## Specific Test Fixes Needed

### test_extraction_lib.py
- [ ] Mock OpenAI API calls
- [ ] Mock LibreOffice subprocess calls
- [ ] Add proper test markers
- [ ] Create minimal test files

### test_image_description.py
- [ ] Mock all vision model API calls
- [ ] Create unit test variants
- [ ] Separate e2e tests

### test_cli.py
- [ ] Fix subprocess mocking
- [ ] Add unit test class
- [ ] Properly categorize tests

### test_extraction_cli.py
- [ ] Mock file-extract CLI calls
- [ ] Use test fixtures
- [ ] Add integration markers

## Running Tests

### Development (Fast)
```bash
# Run only unit tests (fast, mocked)
poetry run pytest -m "unit"

# Run unit and integration tests
poetry run pytest -m "not e2e"
```

### Full Test Suite
```bash
# Run all tests including e2e
poetry run pytest

# Run specific model tests
poetry run pytest -m "openai and e2e"
poetry run pytest -m "ollama and e2e"
```

### CI Configuration
```bash
# CI should run unit and integration tests
poetry run pytest -m "not e2e" --cov=pyvisionai

# E2E tests in separate CI job with secrets
poetry run pytest -m "e2e" --env-file=.env.test
```

## Success Metrics
- [ ] All unit tests run in < 10 seconds
- [ ] No real API calls in unit tests
- [ ] Test coverage > 80%
- [ ] All tests pass in CI
- [ ] Clear test documentation
