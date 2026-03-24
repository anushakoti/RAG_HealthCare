"""MCP tools: connect to MCP server for Google Calendar"""

import os
from dotenv import load_dotenv
load_dotenv()


from langchain_mcp_adapters.client import MultiServerMCPClient

COMPOSIO_TOKEN  = os.environ.get("COMPOSIO_API_KEY", "")
COMPOSIO_MCP_URL = os.environ.get("COMPOSIO_MCP_URL", "")

def get_mcp_client():
    """Get MCP client for Composio MCP server"""
    client = MultiServerMCPClient(
        {
            "composio": {
            "transport": "streamable_http",
            "url": COMPOSIO_MCP_URL,
            "headers": {"x-api-key": COMPOSIO_TOKEN},
            }
        }
    )
    return client


async def get_calendar_tools(client: MultiServerMCPClient):
    """Get calendar tools from MCP Server"""
    tools = await client.get_tools()
    return [t for t in tools if "calendar" in t.name.lower()]

async def get_gmail_tools(client: MultiServerMCPClient):
    """Get Gmail tools from MCP Server"""
    tools = await client.get_tools()
    return [t for t in tools if "gmail" in t.name.lower()]

async def get_all_mcp_tools(client: MultiServerMCPClient):
    """Get all tools from MCP Server"""
    return await client.get_tools()