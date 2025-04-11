import streamlit as st
import datetime
import io
import zipfile
from agents import (
    UsecaseAgent, SchemaAgent, MappingAgent,
    CertifierAgent, ChatbotAgent, SentimentAgent
)
from tools import OllamaLLM as CustomTool
from multi_agent_framework import Memory

st.set_page_config(page_title="Veritas360", layout="wide")
st.title("🧠 Veritas360: Agentic Customer 360 Data Product System")

tools = [CustomTool() for _ in range(4)]
memory = Memory()
agents = {
    "UsecaseAgent": UsecaseAgent(tools, memory),
    "SchemaAgent": SchemaAgent(tools, memory),
    "MappingAgent": MappingAgent(tools, memory),
    "CertifierAgent": CertifierAgent(tools, memory),
    "SentimentAgent": SentimentAgent(tools, memory),
    "ChatbotAgent": ChatbotAgent(tools, memory)
}

with st.sidebar:
    st.header("📘 Agent Overview")
    st.markdown("- **UsecaseAgent**: Understands business goals")
    st.markdown("- **SchemaAgent**: Designs entity schema")
    st.markdown("- **MappingAgent**: Links source data to targets")
    st.markdown("- **CertifierAgent**: Verifies quality & governance")
    st.markdown("- **SentimentAgent**: Analyzes user feedback")
    st.markdown("- **ChatbotAgent**: Responds to user queries")
    st.markdown("---")
    st.caption("Powered by SQLite memory + Ollama LLM")


def extract_entities(text):
    entities = {}
    current = None
    for line in text.splitlines():
        if "Entity:" in line:
            current = line.split("Entity:")[1].strip()
            entities[current] = []
        elif current and "-" in line:
            attr = line.split("-")[0].strip()
            entities[current].append(attr)
    return entities

def render_mermaid(schema_text):
    schema = extract_entities(schema_text)
    mermaid_code = "erDiagram\n"
    for entity, attrs in schema.items():
        mermaid_code += f"  {entity} {{\n"
        for attr in attrs:
            mermaid_code += f"    string {attr}\n"
        mermaid_code += "  }\n"
    return mermaid_code


st.subheader("📥 Use Case Input")
use_case_input = st.text_area("Enter a Retail Banking Business Use Case:", height=200)


results = {}
if st.button("🚀 Run Veritas360"):
    if not use_case_input.strip():
        st.warning("Please provide a use case input.")
    else:
        with st.spinner("🤖 Agents at work..."):
            for key in ["UsecaseAgent", "SchemaAgent", "MappingAgent", "CertifierAgent"]:
                results[key] = agents[key].think(use_case_input)

        with st.expander("🧠 UsecaseAgent Output", expanded=True):
            st.write(results["UsecaseAgent"])

        with st.expander("📐 SchemaAgent Output", expanded=True):
            st.code(results["SchemaAgent"])
            st.subheader("📊 Visual Schema (Mermaid.js)")
            st.code(render_mermaid(results["SchemaAgent"]), language="mermaid")

        with st.expander("🔗 MappingAgent Output", expanded=True):
            st.code(results["MappingAgent"])

        with st.expander("✅ CertifierAgent Output", expanded=True):
            st.code(results["CertifierAgent"])

    
        final_report = "\n\n".join([f"### {k} Output\n{v}" for k, v in results.items()])
        filename = f"veritas360_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        st.download_button("⬇️ Download Full Report", final_report, file_name=filename)


st.markdown("---")
st.subheader("🧠 Sentiment Analysis")

feedback_input = st.text_area("Paste customer feedback (one per line)", placeholder="enter feedback")
feedbacks = [line.strip() for line in feedback_input.splitlines() if line.strip()]
sentiment_result = ""

if st.button("Analyze Sentiments"):
    if not feedbacks:
        st.warning("Please enter feedback lines.")
    else:
        sentiment_result = agents["SentimentAgent"].think(feedbacks)
        st.code(sentiment_result, language="text")
        st.download_button("⬇️ Download Sentiment Output", sentiment_result, file_name="sentiment_analysis.txt")


st.markdown("---")
st.subheader("💬 Ask Veritas360 Anything (Chatbot Agent)")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

query_input = st.text_input("Type your question about the data product:")

if st.button("Send"):
    response = agents["ChatbotAgent"].think([query_input])
    st.session_state.chat_history.append(("🧑 You", query_input))
    st.session_state.chat_history.append(("🤖 V360", response))

for speaker, message in reversed(st.session_state.chat_history[-6:]):
    st.markdown(f"**{speaker}:** {message}")


st.markdown("---")
if st.checkbox("🧾 Show Agent Memory Log"):
    for name in agents:
        st.markdown(f"### {name}")
        rows = memory.fetch(name)
        for row in rows:
            st.markdown(f"**Input:** `{row['input']}`")
            st.markdown(f"**Output:** {row['output']}`")
            st.markdown("---")


st.markdown("---")
if st.button("⬇️ Download All Outputs as ZIP"):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for name in agents:
            logs = memory.fetch(name)
            if logs:
                content = ""
                for log in logs:
                    content += f"Input: {log['input']}\nOutput: {log['output']}\n\n"
                zf.writestr(f"{name}.txt", content)
    zip_buffer.seek(0)
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📦 Download Agent Outputs (ZIP)",
        data=zip_buffer,
        file_name=f"veritas360_outputs_{now}.zip",
        mime="application/zip"
    )


st.markdown("---")
st.caption("⚙️ Veritas360 | Built with Ollama LLM, Streamlit, and modular multi-agent design.")
