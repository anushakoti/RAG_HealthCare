"""
Streamlit UI for MediCare Plus Medical Center
Imports the LangGraph graph directly (no API calls).
Run: streamlit run app.py
"""
import asyncio
import uuid
import streamlit as st
from langchain_core.messages import AIMessage
from graph.workflow import build_faq_only_workflow, build_workflow


def _extract_text(messages) -> str:
    """Extract text from the last AI message, handling Bedrock's list content format."""
    for msg in reversed(messages):
        if not isinstance(msg, AIMessage):
            continue
        content = msg.content
        # String content — return directly if non-empty
        if isinstance(content, str) and content.strip():
            return content
        # List of content blocks (Bedrock format) — extract text parts
        if isinstance(content, list):
            parts = [b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text"]
            if parts:
                return "\n".join(parts)
    return "I'm sorry, I couldn't generate a response. Please try again."

# --- Page Config ---
st.set_page_config(
    page_title="MediCare Plus Medical Center",
    page_icon="🏥",
    layout="centered",
)

# --- Session State Init ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]
if "user_id" not in st.session_state:
    st.session_state.user_id = "demo_user"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "faq_only"
if "graph" not in st.session_state:
    st.session_state.graph = build_faq_only_workflow()
if "mcp_client" not in st.session_state:
    st.session_state.mcp_client = None


def connect_full_system():
    """Try to connect to Composio MCP and build the full multi-agent graph."""
    try:
        graph, client = asyncio.run(build_workflow())
        st.session_state.graph = graph
        st.session_state.mcp_client = client
        st.session_state.mode = "full"
        return True
    except Exception as e:
        st.error(f"Could not connect to MCP server: {e}")
        return False


# --- Sidebar ---
with st.sidebar:
    st.title("MediCare Plus")
    st.caption("Intelligent Healthcare Assistant")

    st.divider()

    # Mode selector
    st.subheader("System Status")
    if st.session_state.mode == "faq_only":
        st.info("📋 Basic Information Mode")
        if st.button("🔌 Enable Full Services"):
            with st.spinner("Connecting to healthcare services..."):
                if connect_full_system():
                    st.success("✅ Full services activated!")
                    st.rerun()
    else:
        st.success("🚀 Full Service Mode Active")
        st.caption("All healthcare services available")

    st.divider()

    # User ID
    st.subheader("Patient Information")
    new_user = st.text_input("Patient ID", value=st.session_state.user_id)
    if new_user != st.session_state.user_id:
        st.session_state.user_id = new_user

    st.divider()

    # Session info
    st.subheader("Session Details")
    st.text(f"Session ID: {st.session_state.thread_id}")
    st.text(f"Patient: {st.session_state.user_id}")

    if st.button("🔄 Start New Session"):
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("💡 Quick Questions")
    if st.session_state.mode == "full":
        st.markdown("""
        - What are your operating hours?
        - I need to schedule an appointment
        - Which specialists are available?
        - What's your cancellation policy?
        - Book me with Dr. Chen tomorrow at 10 AM
        - How do I prepare for a consultation?
        """)
    else:
        st.markdown("""
        - What are your operating hours?
        - Which doctors are on staff?
        - What's the cancellation policy?
        - Do you accept my insurance?
        - Where is the medical center located?
        - How do I contact the clinic?
        """)

    st.divider()
    st.caption("Powered by AI Healthcare Assistant")

# --- Main Chat Area ---
st.title("🏥 MediCare Plus Medical Center")
if st.session_state.mode == "full":
    st.caption("✨ Full service mode active. Ask about appointments, doctor availability, medical services, or get assistance with scheduling.")
else:
    st.caption("📋 Basic information mode. Ask about clinic hours, doctors, policies, and general medical services.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your healthcare question here..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id,
            "user_id": st.session_state.user_id,
        }
    }

    graph = st.session_state.graph

    with st.chat_message("assistant"):
        with st.spinner("MediCare AI is thinking..."):
            if st.session_state.mode == "full":
                result = asyncio.run(graph.ainvoke(
                    {"messages": [("user", prompt)]},
                    config,
                ))
            else:
                result = graph.invoke(
                    {"messages": [("user", prompt)]},
                    config,
                )
            response = _extract_text(result["messages"])
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})