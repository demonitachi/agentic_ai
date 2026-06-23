from agents import Agent, ModelSettings
import requests
import os
from agents import function_tool
from dotenv import load_dotenv


INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)
load_dotenv(override=True)
serp_api_key = os.getenv("SERPER_API_KEY")

@function_tool
async def serper_web_search(query: str) -> str:
    """Search for current information using SERP API and return short results."""
    url = "https://google.serper.dev/search"

    payload = {
        "q": query
    }
    headers = {
        'X-API-KEY': serp_api_key,  # Serper playground default
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=payload)
    
    # 2. ADD THIS DIAGNOSTIC PRINT
    # If something is wrong (unauthorized, out of credits), this will print the exact reason.
    if response.status_code != 200:
        print(f"API Error ({response.status_code}): {response.text}")
        return "Search failed due to API error."

    data = response.json()
    organic = data.get("organic", [])[:5]
    if not organic:
        return "No search results found."
    lines = []
    for item in organic:
        title = item.get("title", "No title")
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        lines.append(f"{title}\n{link}\n{snippet}")
    return "\n\n".join(lines)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[serper_web_search],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)