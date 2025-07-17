import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# 🔐 Set your OpenRouter API Key here
os.environ["OPENAI_API_KEY"] = "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"  # Replace with your actual key

# Streamlit App UI
st.set_page_config(page_title="Smart Financial Advisor 💰", layout="centered")
st.title("💬 Smart Financial Advisor")

st.markdown("Get personalized financial advice based on your profile.")

# Input fields
income = st.number_input("📥 Monthly Income (₹)", min_value=0)
age = st.number_input("🎂 Age", min_value=18, max_value=100)
savings = st.number_input("💰 Current Savings (₹)", min_value=0)
debt = st.number_input("📉 Existing Debt (₹)", min_value=0)
risk = st.selectbox("⚖️ Risk Appetite", ["Low", "Medium", "High"])

# Submit button
if st.button("💡 Get Financial Advice"):
    with st.spinner("Generating personalized financial advice..."):

        # Create LangChain prompt
        template = """
        You are a smart financial advisor. Based on the following user profile, give personalized financial advice:
        - Monthly Income: ₹{income}
        - Age: {age}
        - Current Savings: ₹{savings}
        - Existing Debt: ₹{debt}
        - Risk Appetite: {risk}

        Respond in clear bullet points with practical suggestions.
        """
        prompt = PromptTemplate.from_template(template)

        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            base_url="https://openrouter.ai/api/v1",
        )

        chain = prompt | llm  # RunnableSequence

        # Run chain with user input
        response = chain.invoke({
            "income": income,
            "age": age,
            "savings": savings,
            "debt": debt,
            "risk": risk,
        })

        # Display the result
        st.markdown("### 🧠 Advice:")
        st.write(response.content)
