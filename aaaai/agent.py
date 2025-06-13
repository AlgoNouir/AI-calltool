from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.tools import tool as langToolDecorator
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tools import render_text_description
from typing import Any, Dict, Optional, TypedDict
from langchain_core.runnables import RunnableConfig

toolsPrompt = """\
system_prompt:
    You are an assistant that has access to the following set of tools. 
    Here are the names and descriptions for each tool:

    {rendered_tools}

    Given the user input, return the name and input of the tool to use. 
    Return your response as a JSON blob with 'name' and 'arguments' keys.

    The `arguments` should be a dictionary, with keys corresponding 
    to the argument names and the values corresponding to the requested values.
"""

mainPrompt = """\
system_prompt:
    {mainText}

plan:

"""


class ToolCallRequest(TypedDict):
    """A typed dict that shows the inputs into the invoke_tool function."""

    name: str
    arguments: Dict[str, Any]


class Agent:
    def __init__(
        self,
        mainText: str,
        modelName: str,
        maxRetray=3,
        baseUrl="http://localhost:11434",
    ):
        self.system_prompt = ""
        self.modelName = modelName
        self.baseUrl = baseUrl
        self.maxRetray = maxRetray

        ignoreFuncs = ["message", "select"]

        self.tools = {
            tool: langToolDecorator(self.__getattribute__(tool))
            for tool in self.__dir__()
            if (
                tool.strip("_") == tool
                and tool not in self.__dict__.keys()
                and tool not in ignoreFuncs
            )
        }

        # generate tools from method
        if len(self.tools):
            rendered_tools_text = render_text_description(self.tools.values()).replace(
                "\n", "\n\t"
            )
            self.system_prompt += toolsPrompt.format(rendered_tools=rendered_tools_text)

        # add system prompts
        self.system_prompt += mainPrompt.format(mainText=mainText)

        # create LLM model
        llm = OllamaLLM(
            model=self.modelName,
            base_url=self.baseUrl,
        )

        prompt = PromptTemplate(
            input_variables=["question"],
            template=self.system_prompt + "{question}",
        )

        # set tools of chain in agent
        self.chain = prompt | llm
        if len(self.tools):
            self.chain = self.chain | JsonOutputParser() | self._invoke_tool

    # -------------------------------------------------------- MAIN FUNCTIONS

    def _invoke_tool(
        self,
        tool_call_request: ToolCallRequest,
        config: Optional[RunnableConfig] = None,
    ):
        """A function that we can use the perform a tool invocation.

        Args:
            tool_call_request: a dict that contains the keys name and arguments.
                The name must match the name of a tool that exists.
                The arguments are the arguments to that tool.
            config: This is configuration information that LangChain uses that contains
                things like callbacks, metadata, etc.See LCEL documentation about RunnableConfig.

        Returns:
            output from the requested tool
        """
        name = tool_call_request["name"]

        for funcName, requested_tool in self.tools.items():
            if funcName in name:
                break
        else:
            return "function not found"

        return requested_tool.invoke(tool_call_request["arguments"], config=config)

    # -------------------------------------------------------- DEFAULT TOOLS

    def message(self, message):
        return self.chain.invoke({"question": message})

    def select(self, text: str, options: list[str], freq=0, think=False):
        """Choose exactly one of the options based on the text."""
        # create prompt and
        question = f"text: {text} | plan: Choose exactly one of the options based on the text. | options : {', '.join(options)} "
        print(question)
        response = self.chain.invoke({"question": question})

        # check exact option
        for opt in options:
            if opt.lower() in response.lower():
                return opt

        # if option not in response
        print("response not found")

        if freq >= self.maxRetray:
            return None

        # if not think
        if not think:
            return None

        # retray on anwsering
        return self.select(response, options, freq + 1, think=True)
