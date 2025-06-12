# Quick Start Guide

This guide will help you create your first AI-powered tool using EasyPoint Generator.

## 1. Basic Tool Creation

Here's a simple example of creating a tool that generates a greeting:

```python
from langchain.tools import tool
from typing import Optional

@tool
def generate_greeting(name: str, language: Optional[str] = "English") -> str:
    """Generate a greeting for a person in the specified language.

    Args:
        name: The name of the person to greet
        language: The language to use (default: English)

    Returns:
        A greeting string
    """
    return f"Hello {name}!"
```

## 2. Setting Up the Chain

```python
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Initialize Ollama LLM
llm = OllamaLLM(
    model="gemma3:12b",
    base_url="http://localhost:11434",
)

# Create prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template="""
    You are an assistant that helps users generate greetings.
    Available tools: {tools}

    User question: {question}
    """,
)

# Create the chain
chain = prompt | llm | JsonOutputParser() | invoke_tool
```

## 3. Using the Tool

```python
# Example usage
response = chain.invoke({
    "question": "Generate a greeting for Alice"
})
print(response)  # Output: "Hello Alice!"

response = chain.invoke({
    "question": "Say hi to Bob in Spanish"
})
print(response)  # Output: "¡Hola Bob!"
```

## 4. Adding More Complex Tools

Here's an example of a more complex tool that performs calculations:

```python
from typing import Dict, Union
from pydantic import BaseModel

class CalculationResult(BaseModel):
    result: float
    steps: list[str]

@tool
def calculate_expression(
    expression: str,
    show_steps: bool = False
) -> Union[float, CalculationResult]:
    """Calculate the result of a mathematical expression.

    Args:
        expression: The mathematical expression to evaluate
        show_steps: Whether to show calculation steps

    Returns:
        The calculation result or a CalculationResult object with steps
    """
    # Add your calculation logic here
    result = eval(expression)  # Note: Use safer evaluation in production

    if show_steps:
        return CalculationResult(
            result=result,
            steps=[f"Evaluated expression: {expression}", f"Result: {result}"]
        )
    return result
```

## 5. Error Handling

Always include proper error handling in your tools:

```python
from typing import Optional

@tool
def divide_numbers(
    dividend: float,
    divisor: float
) -> Optional[float]:
    """Safely divide two numbers.

    Args:
        dividend: The number to be divided
        divisor: The number to divide by

    Returns:
        The result of the division or None if division by zero
    """
    try:
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        return dividend / divisor
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
```

## 6. Async Tools

For operations that might take time, use async tools:

```python
from langchain.tools import tool
import aiohttp
import asyncio

@tool
async def fetch_data(url: str) -> dict:
    """Fetch data from a URL asynchronously.

    Args:
        url: The URL to fetch data from

    Returns:
        The fetched data as a dictionary
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## 7. Tool Configuration

You can configure your tools with additional metadata:

```python
@tool(
    name="text_analyzer",
    description="Analyzes text for various metrics",
    return_direct=True
)
def analyze_text(
    text: str,
    metrics: list[str] = ["length", "word_count"]
) -> dict:
    """Analyze text and return requested metrics.

    Args:
        text: The text to analyze
        metrics: List of metrics to calculate

    Returns:
        Dictionary of calculated metrics
    """
    results = {}
    if "length" in metrics:
        results["length"] = len(text)
    if "word_count" in metrics:
        results["word_count"] = len(text.split())
    return results
```

## 8. Next Steps

- Explore the technical documentation for advanced features
- Check out the example tools in the repository
- Join our community for support and discussions
- Contribute your own tools to the project

## Common Issues

1. **Tool Not Found**

   - Make sure your tool is properly decorated with `@tool`
   - Check that the tool is registered in your tools list

2. **Type Errors**

   - Verify your type hints are correct
   - Make sure return values match declared types

3. **LLM Connection**
   - Check if Ollama is running
   - Verify the base_url is correct
   - Ensure the model is available

## Tips and Tricks

1. **Documentation**

   - Write clear docstrings
   - Include example usage
   - Document all parameters

2. **Testing**

   - Write unit tests for your tools
   - Test edge cases
   - Use mock LLM for testing

3. **Performance**
   - Cache expensive operations
   - Use async where appropriate
   - Batch operations when possible
