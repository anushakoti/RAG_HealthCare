"""
Memory configuration file. This file dused to configure the memory settings for the application.
"""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

#short time memory configuration
checkpointer= InMemorySaver()

#long term memory configuration
store = InMemoryStore()

