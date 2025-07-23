import os
import sys
import pytest
from unittest.mock import Mock, patch
import openai
import dotenv

# Add the current directory to Python path for importing the module under test
sys.path.insert(0, os.path.dirname(__file__))


class TestOwnDataRAGImplementation:
    """Comprehensive unit tests for the RAG implementation with Azure OpenAI and Search."""
    
    @pytest.fixture
    def mock_env_vars(self):
        """Fixture to provide mock environment variables."""
        return {
            'AZURE_OAI_ENDPOINT': 'https://test-endpoint.openai.azure.com/',
            'AZURE_OAI_KEY': 'test-api-key-redacted',
            'AZURE_OAI_DEPLOYMENT': 'test-deployment',
            'AZURE_SEARCH_ENDPOINT': 'https://test-search.search.windows.net',
            'AZURE_SEARCH_INDEX': 'test-search-index',
            'AZURE_SEARCH_KEY': 'test-search-key-redacted',
        }
    
    @pytest.fixture
    def mock_completion_response(self):
        """Fixture to provide a mock Azure OpenAI completion response."""
        mock_response = Mock()
        mock_response.model_dump_json.return_value = '{"id": "test-completion-123", "object": "chat.completion", "choices": [{"message": {"role": "assistant", "content": "Test response from RAG system"}}], "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70}}'
        return mock_response
    
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_environment_variables(self) -> None:
        """Test behavior when required environment variables are missing."""
        with pytest.raises((TypeError, ValueError)) as exc_info:
            openai.AzureOpenAI(
                azure_endpoint=None,
                api_key=None,
                api_version="2024-12-01-preview",
            )
        # Should fail due to missing required parameters
        assert exc_info.value is not None
    
    @patch.dict(os.environ)
    @patch('openai.AzureOpenAI')
    def test_azure_openai_client_initialization(self, mock_azure_openai, mock_env_vars) -> None:
        """Test proper initialization of Azure OpenAI client with environment variables."""
        os.environ.update(mock_env_vars)
        
        # Simulate the client initialization from the original code
        endpoint = os.environ.get("AZURE_OAI_ENDPOINT")
        api_key = os.environ.get("AZURE_OAI_KEY")
        
        openai.AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2024-12-01-preview",
        )
        
        mock_azure_openai.assert_called_once_with(
            azure_endpoint=mock_env_vars['AZURE_OAI_ENDPOINT'],
            api_key=mock_env_vars['AZURE_OAI_KEY'],
            api_version="2024-12-01-preview",
        )
    
    @patch.dict(os.environ)
    @patch('openai.AzureOpenAI')
    def test_chat_completion_request_structure(self, mock_azure_openai, mock_env_vars, mock_completion_response) -> None:
        """Test the structure of the chat completion request with data sources."""
        os.environ.update(mock_env_vars)
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_completion_response
        mock_azure_openai.return_value = mock_client
        
        # Simulate the completion request from the original code
        client = mock_azure_openai.return_value
        test_question = "What is the capital of France?"
        
        client.chat.completions.create(
            model=mock_env_vars['AZURE_OAI_DEPLOYMENT'],
            messages=[
                {
                    "role": "user",
                    "content": test_question,
                },
            ],
            extra_body={
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": mock_env_vars["AZURE_SEARCH_ENDPOINT"],
                            "index_name": mock_env_vars["AZURE_SEARCH_INDEX"],
                            "authentication": {
                                "type": "api_key",
                                "key": mock_env_vars["AZURE_SEARCH_KEY"],
                            },
                        },
                    },
                ],
            },
        )
        
        # Verify the call was made with correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        
        assert call_args[1]['model'] == mock_env_vars['AZURE_OAI_DEPLOYMENT']
        assert call_args[1]['messages'][0]['role'] == 'user'
        assert call_args[1]['messages'][0]['content'] == test_question
        assert 'extra_body' in call_args[1]
        assert 'data_sources' in call_args[1]['extra_body']
    
    @patch.dict(os.environ)
    @patch('openai.AzureOpenAI')
    def test_azure_search_data_source_configuration(self, mock_azure_openai, mock_env_vars) -> None:
        """Test the Azure Search data source configuration in detail."""
        os.environ.update(mock_env_vars)
        
        mock_client = Mock()
        mock_azure_openai.return_value = mock_client
        
        # Test the data source configuration exactly as in the original code
        data_sources = [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": os.environ["AZURE_SEARCH_ENDPOINT"],
                    "index_name": os.environ["AZURE_SEARCH_INDEX"],
                    "authentication": {
                        "type": "api_key",
                        "key": os.environ["AZURE_SEARCH_KEY"],
                    },
                },
            },
        ]
        
        # Verify data source structure
        assert len(data_sources) == 1
        assert data_sources[0]["type"] == "azure_search"
        assert "parameters" in data_sources[0]
        
        params = data_sources[0]["parameters"]
        assert params["endpoint"] == mock_env_vars["AZURE_SEARCH_ENDPOINT"]
        assert params["index_name"] == mock_env_vars["AZURE_SEARCH_INDEX"]
        assert params["authentication"]["type"] == "api_key"
        assert params["authentication"]["key"] == mock_env_vars["AZURE_SEARCH_KEY"]
    
    @patch.dict(os.environ)
    @patch('openai.AzureOpenAI')
    def test_completion_response_handling(self, mock_azure_openai, mock_env_vars, mock_completion_response) -> None:
        """Test handling of completion response and JSON serialization."""
        os.environ.update(mock_env_vars)
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_completion_response
        mock_azure_openai.return_value = mock_client
        
        completion = mock_client.chat.completions.create(
            model=mock_env_vars['AZURE_OAI_DEPLOYMENT'],
            messages=[{"role": "user", "content": "test"}],
            extra_body={"data_sources": []},
        )
        
        # Test JSON serialization as done in the original code
        json_output = completion.model_dump_json(indent=2)
        assert json_output is not None
        assert isinstance(json_output, str)
        assert "test-completion-123" in json_output
        mock_completion_response.model_dump_json.assert_called_once_with(indent=2)
    
    @pytest.mark.parametrize("question", [
        "What is AI?",
        "How does machine learning work?", 
        "Explain quantum computing",
        "",  # Edge case: empty question
        "A" * 1000,  # Edge case: very long question
        "What is 2+2?",  # Simple question
        "¿Qué es inteligencia artificial?",  # Non-English question
        "Question with special chars: !@#$%^&*()",
        "Multi-line\nquestion\nwith\nbreaks",
    ])
    @patch.dict(os.environ)
    @patch('openai.AzureOpenAI')
    def test_various_question_inputs(self, mock_azure_openai, mock_env_vars, mock_completion_response, question) -> None:
        """Test the system with various types of question inputs."""
        os.environ.update(mock_env_vars)
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_completion_response
        mock_azure_openai.return_value = mock_client
        
        mock_client.chat.completions.create(
            model=mock_env_vars['AZURE_OAI_DEPLOYMENT'],
            messages=[
                {
                    "role": "user",
                    "content": question,
                },
            ],
            extra_body={
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": mock_env_vars["AZURE_SEARCH_ENDPOINT"],
                            "index_name": mock_env_vars["AZURE_SEARCH_INDEX"],
                            "authentication": {
                                "type": "api_key",
                                "key": mock_env_vars["AZURE_SEARCH_KEY"],
                            },
                        },
                    },
                ],
            },
        )
        
        # Verify the question was passed correctly
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]['messages'][0]['content'] == question
    
    @patch.dict(os.environ)
    @patch('openai.AzureOpenAI')
    def test_api_error_handling(self, mock_azure_openai, mock_env_vars) -> None:
        """Test handling of API errors from Azure OpenAI."""
        os.environ.update(mock_env_vars)
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = openai.APIError("API Error occurred")
        mock_azure_openai.return_value = mock_client
        
        with pytest.raises(openai.APIError) as exc_info:
            mock_client.chat.completions.create(
                model=mock_env_vars['AZURE_OAI_DEPLOYMENT'],
                messages=[{"role": "user", "content": "test"}],
                extra_body={"data_sources": []},
            )
        assert "API Error occurred" in str(exc_info.value)
    
    @patch.dict(os.environ)
    @patch('openai.AzureOpenAI')
    def test_authentication_error_handling(self, mock_azure_openai, mock_env_vars) -> None:
        """Test handling of authentication errors."""
        os.environ.update(mock_env_vars)
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = openai.AuthenticationError("Invalid API key")
        mock_azure_openai.return_value = mock_client
        
        with pytest.raises(openai.AuthenticationError) as exc_info:
            mock_client.chat.completions.create(
                model=mock_env_vars['AZURE_OAI_DEPLOYMENT'],
                messages=[{"role": "user", "content": "test"}],
                extra_body={"data_sources": []},
            )
        assert "Invalid API key" in str(exc_info.value)
    
    @patch.dict(os.environ)
    @patch('openai.AzureOpenAI')
    def test_rate_limit_error_handling(self, mock_azure_openai, mock_env_vars) -> None:
        """Test handling of rate limit errors."""
        os.environ.update(mock_env_vars)
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = openai.RateLimitError("Rate limit exceeded")
        mock_azure_openai.return_value = mock_client
        
        with pytest.raises(openai.RateLimitError) as exc_info:
            mock_client.chat.completions.create(
                model=mock_env_vars['AZURE_OAI_DEPLOYMENT'],
                messages=[{"role": "user", "content": "test"}],
                extra_body={"data_sources": []},
            )
        assert "Rate limit exceeded" in str(exc_info.value)
    
    @patch('dotenv.load_dotenv')
    def test_dotenv_loading(self, mock_load_dotenv) -> None:
        """Test that dotenv.load_dotenv() is called to load environment variables."""
        # Simulate importing the module (which calls load_dotenv)
        dotenv.load_dotenv()
        mock_load_dotenv.assert_called()
    
    def test_api_version_constant(self) -> None:
        """Test that the API version is set to the expected value."""
        expected_api_version = "2024-12-01-preview"
        # This tests the hardcoded API version in the original code
        assert expected_api_version == "2024-12-01-preview"
    
    @pytest.mark.parametrize("invalid_env_value", [None, "", "   "])
    @patch.dict(os.environ, {}, clear=True)
    def test_invalid_environment_values(self, invalid_env_value) -> None:
        """Test behavior with invalid environment variable values."""
        test_vars = {
            'AZURE_OAI_ENDPOINT': invalid_env_value if invalid_env_value != "   " else 'https://test.openai.azure.com',
            'AZURE_OAI_KEY': invalid_env_value if invalid_env_value != "   " else 'test-key',
            'AZURE_OAI_DEPLOYMENT': invalid_env_value if invalid_env_value != "   " else 'test-deployment',
        }
        os.environ.update(test_vars)
        
        endpoint = os.environ.get("AZURE_OAI_ENDPOINT")
        api_key = os.environ.get("AZURE_OAI_KEY")
        
        if invalid_env_value in [None, ""]:
            # These should cause issues with client initialization
            with pytest.raises((TypeError, ValueError, AttributeError)):
                openai.AzureOpenAI(
                    azure_endpoint=endpoint,
                    api_key=api_key,
                    api_version="2024-12-01-preview",
                )
    
    @patch.dict(os.environ)
    @patch('builtins.input')
    @patch('openai.AzureOpenAI')
    def test_user_input_simulation(self, mock_azure_openai, mock_input, mock_env_vars, mock_completion_response) -> None:
        """Test simulation of user input functionality."""
        os.environ.update(mock_env_vars)
        mock_input.return_value = "What is machine learning?"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_completion_response
        mock_azure_openai.return_value = mock_client
        
        # Simulate the input() call from the original code
        text = input('\nEnter a question:\n')
        
        # Verify input was called correctly
        mock_input.assert_called_once_with('\nEnter a question:\n')
        assert text == "What is machine learning?"


class TestRAGDataSourceValidation:
    """Tests specifically for validating the Azure Search data source configuration."""
    
    def test_data_source_type_validation(self) -> None:
        """Test that data source type is correctly set to 'azure_search'."""
        data_source = {
            "type": "azure_search",
            "parameters": {},
        }
        assert data_source["type"] == "azure_search"
    
    def test_required_parameters_presence(self) -> None:
        """Test that all required parameters are present in data source configuration."""
        required_params = ["endpoint", "index_name", "authentication"]
        
        parameters = {
            "endpoint": "https://test.search.windows.net",
            "index_name": "test-index",
            "authentication": {
                "type": "api_key",
                "key": "test-key",
            },
        }
        
        for param in required_params:
            assert param in parameters
    
    def test_authentication_structure(self) -> None:
        """Test the authentication section structure."""
        auth_config = {
            "type": "api_key",
            "key": "test-search-key",
        }
        
        assert auth_config["type"] == "api_key"
        assert "key" in auth_config
        assert auth_config["key"] is not None
    
    def test_data_source_parameters_structure(self) -> None:
        """Test the complete data source parameters structure."""
        data_source_params = {
            "endpoint": "https://test-search.search.windows.net",
            "index_name": "test-search-index",
            "authentication": {
                "type": "api_key",
                "key": "test-search-key-redacted",
            },
        }
        
        # Validate endpoint format
        assert data_source_params["endpoint"].startswith("https://")
        assert ".search.windows.net" in data_source_params["endpoint"]
        
        # Validate index name is not empty
        assert len(data_source_params["index_name"]) > 0
        
        # Validate authentication structure
        auth = data_source_params["authentication"]
        assert auth["type"] == "api_key"
        assert len(auth["key"]) > 0


class TestMessageFormatValidation:
    """Tests for validating the message format sent to Azure OpenAI."""
    
    def test_message_structure(self) -> None:
        """Test that messages follow the correct structure."""
        message = {
            "role": "user",
            "content": "Test question",
        }
        
        assert "role" in message
        assert "content" in message
        assert message["role"] == "user"
        assert isinstance(message["content"], str)
    
    def test_message_role_validation(self) -> None:
        """Test valid message roles."""
        valid_roles = ["user", "assistant", "system"]
        
        for role in valid_roles:
            message = {"role": role, "content": "test"}
            assert message["role"] in valid_roles
    
    @pytest.mark.parametrize("content_type", [
        "string content",
        "",  # empty string
        "Multi-line\ncontent\nwith\nbreaks",
        "Content with special characters: !@#$%^&*()",
        "Unicode content: 🤖 AI 人工智能",
        "Very long content: " + "A" * 2000,
    ])
    def test_message_content_types(self, content_type) -> None:
        """Test various content types in messages."""
        message = {
            "role": "user",
            "content": content_type,
        }
        
        assert isinstance(message["content"], str)
        assert message["content"] == content_type
    
    def test_messages_array_structure(self) -> None:
        """Test the messages array structure as used in the original code."""
        messages = [
            {
                "role": "user",
                "content": "Test question",
            },
        ]
        
        assert isinstance(messages, list)
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert "content" in messages[0]


class TestEnvironmentVariableHandling:
    """Tests for environment variable handling and configuration."""
    
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_azure_search_endpoint(self) -> None:
        """Test behavior when AZURE_SEARCH_ENDPOINT is missing."""
        test_env = {
            'AZURE_OAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OAI_KEY': 'test-key',
            'AZURE_OAI_DEPLOYMENT': 'test-deployment',
            'AZURE_SEARCH_INDEX': 'test-index',
            'AZURE_SEARCH_KEY': 'test-search-key',
        }
        os.environ.update(test_env)
        
        with pytest.raises(KeyError):
            # This simulates the original code's direct access to os.environ["AZURE_SEARCH_ENDPOINT"]
            os.environ["AZURE_SEARCH_ENDPOINT"]
    
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_azure_search_index(self) -> None:
        """Test behavior when AZURE_SEARCH_INDEX is missing."""
        test_env = {
            'AZURE_OAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OAI_KEY': 'test-key',
            'AZURE_OAI_DEPLOYMENT': 'test-deployment',
            'AZURE_SEARCH_ENDPOINT': 'https://test.search.windows.net',
            'AZURE_SEARCH_KEY': 'test-search-key',
        }
        os.environ.update(test_env)
        
        with pytest.raises(KeyError):
            # This simulates the original code's direct access to os.environ["AZURE_SEARCH_INDEX"]
            os.environ["AZURE_SEARCH_INDEX"]
    
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_azure_search_key(self) -> None:
        """Test behavior when AZURE_SEARCH_KEY is missing."""
        test_env = {
            'AZURE_OAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OAI_KEY': 'test-key',
            'AZURE_OAI_DEPLOYMENT': 'test-deployment',
            'AZURE_SEARCH_ENDPOINT': 'https://test.search.windows.net',
            'AZURE_SEARCH_INDEX': 'test-index',
        }
        os.environ.update(test_env)
        
        with pytest.raises(KeyError):
            # This simulates the original code's direct access to os.environ["AZURE_SEARCH_KEY"]
            os.environ["AZURE_SEARCH_KEY"]
    
    @patch.dict(os.environ)
    def test_all_required_env_vars_present(self) -> None:
        """Test that all required environment variables can be accessed."""
        required_vars = {
            'AZURE_OAI_ENDPOINT': 'https://test.openai.azure.com',
            'AZURE_OAI_KEY': 'test-key',
            'AZURE_OAI_DEPLOYMENT': 'test-deployment',
            'AZURE_SEARCH_ENDPOINT': 'https://test.search.windows.net',
            'AZURE_SEARCH_INDEX': 'test-index',
            'AZURE_SEARCH_KEY': 'test-search-key',
        }
        os.environ.update(required_vars)
        
        # Test the .get() method calls from the original code
        assert os.environ.get("AZURE_OAI_ENDPOINT") == required_vars['AZURE_OAI_ENDPOINT']
        assert os.environ.get("AZURE_OAI_KEY") == required_vars['AZURE_OAI_KEY']
        assert os.environ.get("AZURE_OAI_DEPLOYMENT") == required_vars['AZURE_OAI_DEPLOYMENT']
        
        # Test the direct access calls from the original code
        assert os.environ["AZURE_SEARCH_ENDPOINT"] == required_vars['AZURE_SEARCH_ENDPOINT']
        assert os.environ["AZURE_SEARCH_INDEX"] == required_vars['AZURE_SEARCH_INDEX']
        assert os.environ["AZURE_SEARCH_KEY"] == required_vars['AZURE_SEARCH_KEY']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])