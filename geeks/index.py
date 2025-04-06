import streamlit as st
import concurrent.futures
st.set_page_config(page_title="Customer 360 Multi-Agent System", layout="wide")

from agents import UsecaseAgent, SchemaAgent, MappingAgent, CertifierAgent, SentimentAgent, ChatbotAgent
from tools import OllamaLLM, WebScraperTool, APIClientTool, CustomMLModel
from embedding_db import MemoryDB

tools = [WebScraperTool(), APIClientTool(), CustomMLModel(), OllamaLLM()]
db = MemoryDB()

agents = {
    "UsecaseAgent": UsecaseAgent(tools, db),
    "SchemaAgent": SchemaAgent(tools, db),
    "MappingAgent": MappingAgent(tools, db),
    "CertifierAgent": CertifierAgent(tools, db),
    "SentimentAgent": SentimentAgent(tools, db),
    "ChatbotAgent": ChatbotAgent(tools, db)
}

st.title("🤖 Customer 360 Multi-Agent System for Retail Banking")

# Input fields
task = st.text_area("Enter business use case")
feedback_input = st.text_area("Enter customer feedback (comma-separated)")
query_input = st.text_area("Enter customer queries (comma-separated)")

# Convert inputs
feedbacks = [fb.strip() for fb in feedback_input.split(',')]
queries = [q.strip() for q in query_input.split(',')]

# Result placeholders
usecase_result = schema_result = mapping_result = certifier_result = sentiment_result = chatbot_result = ""

# Run All Agents button (parallelized)
if st.button("▶️ Run All Agents"):
    with st.spinner("Running all agents..."):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                "UsecaseAgent": executor.submit(agents["UsecaseAgent"].think, task),
                "SchemaAgent": executor.submit(agents["SchemaAgent"].think, task),
                "MappingAgent": executor.submit(agents["MappingAgent"].think, task),
                "CertifierAgent": executor.submit(agents["CertifierAgent"].think, task),
                "SentimentAgent": executor.submit(agents["SentimentAgent"].think, feedbacks),
                "ChatbotAgent": executor.submit(agents["ChatbotAgent"].think, queries)
            }
            results = {name: future.result() for name, future in futures.items()}
        usecase_result = results["UsecaseAgent"]
        schema_result = results["SchemaAgent"]
        mapping_result = results["MappingAgent"]
        certifier_result = results["CertifierAgent"]
        sentiment_result = results["SentimentAgent"]
        chatbot_result = results["ChatbotAgent"]
    st.success("✅ All agents executed.")

# Tabs layout
tabs = st.tabs(["Usecase", "Schema", "Mapping", "Certifier", "Sentiment", "Chatbot"])

with tabs[0]:
    st.subheader("🔍 Usecase Agent")
    if st.button("Run Usecase Agent"):
        usecase_result = agents["UsecaseAgent"].think(task)
    st.text_area("Usecase Agent Output", value=usecase_result, height=300)

with tabs[1]:
    st.subheader("📊 Schema Agent")
    if st.button("Run Schema Agent"):
        schema_result = agents["SchemaAgent"].think(task)
    st.text_area("Schema Agent Output", value=schema_result, height=300)

with tabs[2]:
    st.subheader("🔗 Mapping Agent")
    if st.button("Run Mapping Agent"):
        mapping_result = agents["MappingAgent"].think(task)
    st.text_area("Mapping Agent Output", value=mapping_result, height=300)

with tabs[3]:
    st.subheader("✅ Certifier Agent")
    if st.button("Run Certifier Agent"):
        certifier_result = agents["CertifierAgent"].think(task)
    st.text_area("Certifier Agent Output", value=certifier_result, height=300)

with tabs[4]:
    st.subheader("🧠 Sentiment Agent")
    if st.button("Run Sentiment Agent"):
        sentiment_result = agents["SentimentAgent"].think(feedbacks)
    st.text_area("Sentiment Analysis Output", value=sentiment_result, height=200)

with tabs[5]:
    st.subheader("💬 Chatbot Agent")
    if st.button("Run Chatbot Agent"):
        chatbot_result = agents["ChatbotAgent"].think(queries)
    st.text_area("Chatbot Responses", value=chatbot_result, height=200)
