"""

Confirmation Agent: Wires the confirmation agent node into a LangGraph StateGraph. This graph is responsible for sending appointment confirmation emails to patients after their booking is confirmed. It uses the Gmail tool to send the email with all the necessary details about the appointment, including the patient's name, doctor, date and time of the appointment, clinic address, cancellation policy, and contact information. The email should be professional and friendly, ensuring that patients have all the information they need for their upcoming appointment."""

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition            
from agents.confirmation_agent import create_confirmation_node
from tools.mcp_tools import get_mcp_client, get_gmail_tools

async def build_confirmation_graph():
    """Build and return the confirmation graph with MCP Gmail tools."""
    client = get_mcp_client()
    gmail_tools = await get_gmail_tools(client)

    if not gmail_tools:
        raise RuntimeError("No Gmail tools found. Is Composio MCP server running?")

    confirmation_node, tools = create_confirmation_node(gmail_tools)

    builder = StateGraph(MessagesState)
    builder.add_node("confirmation_agent", confirmation_node)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "confirmation_agent")
    builder.add_conditional_edges("confirmation_agent", tools_condition)
    builder.add_edge("tools", "confirmation_agent")

    return builder.compile(), client