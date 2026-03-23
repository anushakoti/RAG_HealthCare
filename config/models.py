from langchain_aws import BedrockEmbeddings , ChatBedrockConverse
from dotenv import load_dotenv

load_dotenv()
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
llm = ChatBedrockConverse(model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0")

