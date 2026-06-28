import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from dotenv import load_dotenv

load_dotenv(override=True)

# 1. Wrap the async code inside an async function
async def main():
    # Get the fetch tool from mcp-server-fetch.
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"], read_timeout_seconds=30)
    fetcher = await mcp_server_tools(fetch_mcp_server)

    # Create an agent that can use the fetch tool.
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    agent = AssistantAgent(name="fetcher", model_client=model_client, tools=fetcher, reflect_on_tool_use=True)

    # Let the agent fetch the content of a URL and summarize it.
    result = await agent.run(task="Review edwarddonner.com and summarize what you learn. Reply in Markdown.")
    print(result.messages[-1].content)

# 2. Use asyncio to kick off the event loop and run the function
if __name__ == "__main__":
    asyncio.run(main())