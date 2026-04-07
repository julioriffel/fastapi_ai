# Test-Driven Development (TDD) Orientation

This document outlines the mandatory TDD flow for all agents when implementing new features or fixing bugs. Following this process ensures code quality, reliability, and maintainability.

---

## The TDD Cycle: Red-Green-Refactor

1.  **RED**: Write a failing test for the next bit of functionality you want to add.
2.  **GREEN**: Write the minimum amount of code necessary to make the test pass.
3.  **REFACTOR**: Clean up the code you just wrote, ensuring it follows best practices while keeping the tests green.

---

## Detailed TDD Workflow

### 1. Pre-Implementation (Red Phase)
- **Identify the Requirement**: Clearly understand the feature or bug.
- **Define the Interface**: Decide how the new code will be called (API endpoint, function signature).
- **Create a Test Case**: Use `pytest` to write a test that describes the expected behavior.
- **Run the Test**: Confirm it fails (Red). If it passes, the test is either incorrect or the feature already exists.

### 2. Implementation (Green Phase)
- **Minimum Code**: Write only enough code to satisfy the test. Avoid over-engineering.
- **Run the Test**: Confirm it passes (Green).
- **Run Existing Tests**: Ensure no regressions were introduced.

### 3. Improvement (Refactor Phase)
- **Code Quality**: Improve naming, remove duplication, and simplify logic.
- **Architecture**: Ensure the code follows the project's architectural patterns (e.g., Repository pattern, Dependency Injection).
- **Type Safety**: Add or refine Pydantic models and type hints.
- **Final Check**: Ensure tests are still Green.

---

## Checklists

### ✅ Start-of-Work Checklist
Before writing any production code, ensure:
- [ ] I have a clear understanding of the "Definition of Done" for this task.
- [ ] I have identified the specific file(s) where the tests should reside.
- [ ] I have written at least one failing test (Unit or Integration).
- [ ] I have verified the test fails with a relevant error (not just a syntax error).
- [ ] For bugs: I have a reproduction test that fails due to the reported issue.

### ✅ End-of-Work Checklist
Before submitting the task, ensure:
- [ ] All new tests pass (Green).
- [ ] All existing tests in the project pass (No regressions).
- [ ] The code is properly typed (Mypy/Pydantic).
- [ ] Code style follows project standards (Ruff/Linting).
- [ ] I have removed any temporary debugging code or print statements.
- [ ] For FastAPI: Async/await patterns are correctly used and dependencies are mocked where appropriate.
- [ ] Coverage for the new/fixed functionality is adequate.

---

## FastAPI Specific Tips
- **Async Testing**: Use `pytest-asyncio` for testing async endpoints and functions.
- **Dependency Overrides**: Use `app.dependency_overrides` to mock databases or external services during integration tests.
- **TestClient**: Use `fastapi.testclient.TestClient` or `httpx.AsyncClient` for end-to-end API testing.
- **Pydantic Validation**: Write tests to verify that invalid data is correctly rejected with a `422 Unprocessable Entity` status.
