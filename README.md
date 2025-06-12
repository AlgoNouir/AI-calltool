# EasyPoint Generator

EasyPoint Generator is a powerful framework designed to simplify the integration and usage of AI functions in your applications. Built on top of LangChain, it provides a streamlined way to create, manage, and execute AI-powered tools.

## 🌟 Features

- Easy tool definition using decorators
- Seamless integration with Ollama models
- JSON-based tool invocation
- Type-safe tool execution
- Built-in prompt management
- Flexible configuration options

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Ollama server running locally (default: http://localhost:11434)
- Virtual environment (recommended)

### Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd generator
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## 💡 Usage

### Defining Tools

Tools are defined using the `@tool` decorator. Here's a simple example:

```python
from langchain.tools import tool

@tool
def say_hello(name: str) -> str:
    """Say hello to someone"""
    return f"Hello {name}!"
```

### Setting Up the Chain

The framework uses LangChain to create a processing chain:

```python
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Initialize the LLM
llm = OllamaLLM(
    model="gemma3:12b",
    base_url="http://localhost:11434",
)

# Create the chain
chain = prompt | llm | JsonOutputParser() | invoke_tool
```

### Executing Tools

Tools can be executed through the chain:

```python
response = chain.invoke({"question": "Say hello to Alice"})
print(response)
```

## 🛠️ Project Structure

- `tools.py`: Core functionality for tool definition and execution
- `requirements.txt`: Project dependencies
- Additional modules can be added as needed

## ⚙️ Configuration

The framework supports various configuration options:

- Custom model selection
- Custom Ollama server URL
- Tool-specific configurations
- Custom prompt templates

## 📝 Dependencies

Key dependencies include:

- langchain
- langchain-ollama
- pydantic
- typing-extensions
- and more (see requirements.txt for full list)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.
