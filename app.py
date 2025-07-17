import os
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Get API key from environment variable
openai_api_key = os.getenv("OPENROUTER_API_KEY")

# Validate API key
if not openai_api_key:
    st.error("❌ OPENAI_API_KEY not found in .env file!")
    st.stop()

# Initialize LLM using OpenRouter
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    base_url="https://openrouter.ai/api/v1",
    openai_api_key=openai_api_key
)

# Define the prompt
template = """
You are a helpful AI financial advisor.

The user provides:
- Their monthly income
- Monthly expenses
- Any existing loans (type and amount)
- Financial goal (e.g., buying a house, saving for education, etc.)

Based on this information, provide a detailed and friendly financial advice plan. Suggest:
- Budgeting improvements
- Investment strategies
- Loan suggestions or caution
- Savings tips

### USER DATA ###
Income: {income}
Expenses: {expenses}
Loan Details: {loan_details}
Financial Goal: {goal}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt)

# Streamlit UI
st.set_page_config(page_title="💸 Financial Advisor", layout="centered")
st.title("💬 Financial Advisor ")

with st.form("advisor_form"):
    income = st.text_input("Your Monthly Income (in ₹)", placeholder="e.g., 50000")
    expenses = st.text_input("Your Monthly Expenses (in ₹)", placeholder="e.g., 20000")
    loan_details = st.text_area("Existing Loans (type and amount)", placeholder="e.g., Education Loan ₹5,00,000")
    goal = st.text_area("Your Financial Goal", placeholder="e.g., Buy a house in 5 years")

    submitted = st.form_submit_button("Get Advice")

    if submitted:
        if not income or not expenses or not goal:
            st.warning("Please fill in all required fields.")
        else:
            with st.spinner("Generating your financial advice..."):
                response = chain.invoke({
                    "income": income,
                    "expenses": expenses,
                    "loan_details": loan_details,
                    "goal": goal
                })
                st.success("✅ Here's your personalized financial advice:")
                st.markdown(response["text"])
