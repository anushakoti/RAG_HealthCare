""" 
Booking Graph: This graph manages the entire booking process.wires the booking agent node into langgraph stategraph
"""
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode,tools_condition
from agents.booking_agent import create_booking_node
from tools.mcp_tools import get_mcp_client, get_calendar_tools


async def build_booking_graph():
   client= get_mcp_client()
   calendar_tools = await get_calendar_tools(client)

   if not calendar_tools:
       raise RuntimeError("No calendar tools found in MCP client. Please check your MCP setup.")  
   
   booking_node,tools = create_booking_node(calendar_tools)

   builder = StateGraph(MessagesState)

   builder.add_node("booking_agent", booking_node)
   builder.add_node("tools", ToolNode(tools))

   builder.add_edge(START, "booking_agent")
   builder.add_conditional_edges("booking_agent", tools_condition)
   builder.add_edge("tools", "booking_agent")

   booking_graph = builder.compile()

   return booking_graph, client