from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import asyncio
import os


load_dotenv(override=True)

fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}

async def main():
    # async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=60) as server:
    #     fetch_tools = await server.session.list_tools()

    # print(fetch_tools.tools)

    playwright_params = {"command": "npx","args": [ "@playwright/mcp@latest"]}

    # async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as server:
    #     playwright_tools = await server.session.list_tools()

    # print(playwright_tools)
    
    sandbox_path = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))
    os.makedirs(sandbox_path, exist_ok=True)
    print(f"Using sandbox directory: {sandbox_path}")

    # # 2. Windows-compatible npx parameter schema
    files_params = {
        "command": "cmd", 
        "args": [
            "/c", 
            "npx", 
            "-y", 
            "@modelcontextprotocol/server-filesystem", 
            sandbox_path
        ]
    }

    # print("Connecting to MCP filesystem server...")
    # async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as server:
    #     # Access the server tools list
    #     file_tools = await server.session.list_tools()

    # print("\nAvailable Tools:")
    # print(file_tools)

    instructions = """
    You browse the internet to accomplish your instructions.
    You are highly capable at browsing the internet independently to accomplish your task, 
    including accepting all cookies and clicking 'not now' as
    appropriate to get to the content you need. If one website isn't fruitful, try another. 
    Be persistent until you have solved your assignment,
    trying different options and sites as needed.
    When you need to write files, you do that inside the sandbox folder only.
    """


    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=60) as mcp_server_files:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=60) as mcp_server_browser:
            agent = Agent(
                name="investigator", 
                instructions=instructions, 
                model="gpt-4o-mini",
                mcp_servers=[mcp_server_files, mcp_server_browser]
                )
            with trace("investigate"):
                result = await Runner.run(agent, "Find a great recipe for Banoffee Pie, then summarize it in markdown to banoffee.md")
                print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())