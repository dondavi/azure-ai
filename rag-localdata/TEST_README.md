# RAG Implementation Tests

This directory contains comprehensive unit tests for the RAG (Retrieval-Augmented Generation) implementation using Azure OpenAI and Azure Search.

## Test Framework

- **Framework**: pytest (Python testing framework)
- **Mocking**: unittest.mock for mocking external dependencies
- **Coverage**: Comprehensive test coverage including happy paths, edge cases, and error conditions

## Test Structure

### TestOwnDataRAGImplementation

Main test class covering:

- Azure OpenAI client initialization
- Chat completion request structure
- Response handling and JSON serialization
- Various question input types
- Error handling (API, authentication, rate limit errors)
- Environment variable loading

### TestRAGDataSourceValidation

Tests for Azure Search data source configuration:

- Data source type validation
- Required parameters presence
- Authentication structure validation
- Complete parameter structure validation

### TestMessageFormatValidation

Tests for OpenAI message format:

- Message structure validation
- Role validation
- Content type handling
- Messages array structure

### TestEnvironmentVariableHandling

Tests for environment variable management:

- Missing variable handling
- Required variable presence
- Variable access methods

## Running Tests

### Prerequisites

Install testing dependencies:

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
pytest test_ownData_comprehensive.py -v
```

### Run Specific Test Class

```bash
pytest test_ownData_comprehensive.py::TestOwnDataRAGImplementation -v
```

### Run with Coverage

```bash
pytest test_ownData_comprehensive.py --cov=. --cov-report=html
```

### Using the Test Runner

```bash
python run_tests.py
```

## Test Coverage

The test suite covers:

- ✅ Environment variable handling and validation
- ✅ Azure OpenAI client initialization
- ✅ Chat completion API calls
- ✅ Azure Search data source configuration
- ✅ Message format validation
- ✅ Response handling and JSON serialization
- ✅ Error handling (API, authentication, rate limits)
- ✅ Edge cases (empty input, long input, special characters)
- ✅ Parametrized testing for multiple scenarios
- ✅ Mock external dependencies to avoid actual API calls

## Key Features Tested

1. **Configuration Management**: Tests ensure all required environment variables are properly loaded and validated.
2. **API Integration**: Validates the structure of API calls to Azure OpenAI with proper data source configuration.
3. **Error Resilience**: Tests various error conditions and ensures proper exception handling.
4. **Input Validation**: Tests various types of user input including edge cases.
5. **Response Processing**: Validates proper handling and serialization of API responses.

## Notes

- Tests use mocking to avoid actual API calls to Azure services.
- All tests are isolated and don't depend on external state.
- Parametrized tests cover multiple scenarios efficiently.
- Tests follow pytest best practices and conventions.