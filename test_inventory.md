# PyVisionAI Test Inventory

## Overview
Total Tests: 134

## Categories
1. Interface Tests (I)
   - Tests that verify the public API contract
   - Would survive complete internal refactoring
   - Focus on parameter validation, types, and error conditions

2. Implementation Tests (M)
   - Tests that verify specific implementation details
   - Would need updates if implementation changes
   - Focus on business logic and specific behaviors

3. Integration Tests (T)
   - Tests that verify integration with external systems
   - Depend on external services or file system
   - Focus on end-to-end functionality

## Test Inventory

### CLI Tests (`tests/test_cli.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_model_parameter | I | Verifies --model parameter handling |
| test_use_case_parameter | I | Verifies --use-case parameter handling |
| test_source_parameter | I | Verifies --source parameter handling |
| test_source_image_precedence | I | Verifies mutual exclusivity of --source and --image |
| test_no_source_or_image_parameter | I | Verifies required parameter validation |
| test_parameter_precedence | I | Verifies parameter precedence rules |
| test_default_model | I | Verifies default model behavior |
| test_model_specific | M | Tests specific model implementations |
| test_prompts | M | Tests custom prompt handling |
| test_error_cases | I | Tests error handling scenarios |
| test_invalid_model | I | Tests invalid model validation |
| test_verbose_output | M | Tests verbose output formatting |

### Core Tests (`tests/core/test_extractor.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_concrete_implementation | M | Tests concrete extractor implementation |
| test_extract_method_interface | I | Verifies extract method contract |
| test_extract_method_documentation | I | Verifies method documentation |

### Describer Tests (`tests/describers/test_claude.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_init | M | Tests Claude model initialization |
| test_validate_config_with_key | M | Tests config validation with API key |
| test_validate_config_without_key | M | Tests config validation without API key |
| test_retry_rate_limit | M | Tests rate limit retry behavior |
| test_retry_server_error | M | Tests server error retry behavior |
| test_retry_overloaded | M | Tests overload retry behavior |
| test_max_retries_exceeded | M | Tests max retries behavior |
| test_empty_response | M | Tests empty response handling |
| test_real_api_call | T | Tests actual API integration |

### Base Describer Tests (`tests/describers/test_base.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_model_registration | M | Tests model registration |
| test_model_factory | M | Tests model factory pattern |
| test_describe_image | M | Tests basic image description |
| test_describe_image_with_nonexistent_file | I | Tests file not found handling |

### Extraction Library Tests (`tests/test_extraction_lib.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_file_extraction_lib | M | Tests file extraction functionality |
| test_pdf_extraction | M | Tests PDF extraction |
| test_docx_extraction | M | Tests DOCX extraction |
| test_pptx_extraction | M | Tests PPTX extraction |
| test_html_extraction | M | Tests HTML extraction |

### Benchmark Tests (`tests/test_benchmarks.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_benchmark_log_structure | M | Tests benchmark logging |
| test_benchmark_metrics | M | Tests metric calculations |
| test_performance_thresholds | M | Tests performance requirements |

### Custom Prompt Tests (`tests/test_custom_prompts.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_technical_documentation | M | Tests technical doc prompts |
| test_business_presentation | M | Tests presentation prompts |
| test_data_analysis | M | Tests data analysis prompts |
| test_custom_prompt_validation | I | Tests prompt validation |

### Batch Processing Tests (`tests/test_batch_processing.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_process_file_success | M | Tests successful file processing |
| test_process_file_unsupported | I | Tests unsupported file handling |
| test_process_file_error | M | Tests error handling |
| test_process_directory | M | Tests directory processing |
| test_process_directory_empty | I | Tests empty directory handling |
| test_process_directory_filtered | M | Tests file filtering |
| test_parallel_processing | M | Tests parallel processing |

### API Retry Tests (`tests/describers/test_api_retry.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_retry_strategy | M | Tests retry strategy implementation |
| test_exponential_backoff | M | Tests exponential backoff |
| test_linear_backoff | M | Tests linear backoff |
| test_constant_backoff | M | Tests constant backoff |
| test_max_retries | M | Tests maximum retry limit |

### Integration Tests (`tests/test_integration.py`)
| Test Name | Category | Description |
|-----------|----------|-------------|
| test_end_to_end_pdf | T | Tests end-to-end PDF processing |
| test_end_to_end_docx | T | Tests end-to-end DOCX processing |
| test_end_to_end_pptx | T | Tests end-to-end PPTX processing |
| test_end_to_end_html | T | Tests end-to-end HTML processing |

## Summary
- Interface Tests (I): 15 tests
- Implementation Tests (M): 110 tests
- Integration Tests (T): 9 tests

## Notes
1. Interface Tests (I) are the most valuable for maintaining stability during refactoring
2. Implementation Tests (M) are important for ensuring correct behavior but may need updates during refactoring
3. Integration Tests (T) verify system boundaries but are the most fragile and expensive to maintain
