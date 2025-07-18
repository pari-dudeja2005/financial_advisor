import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    st.error("⚠️ Please set OPENROUTER_API_KEY in your .env")
    st.stop()
os.environ["OPENAI_API_KEY"] = API_KEY

# App UI config
st.set_page_config(page_title="Yabx Smart Financial Advisor", layout="centered")
st.title("🌍 Smart Financial Advisor")
st.markdown("""
We're helping bridge financial access using your digital profile—with smart, data-driven advice.
""")

# Input form
with st.form("info_form"):
    income = st.number_input("📥 Monthly Income (₹)", min_value=0, step=500)
    age = st.number_input("🎂 Age", min_value=18, max_value=100, step=1)
    savings = st.number_input("💰 Current Savings (₹)", min_value=0, step=500)
    debt = st.number_input("📉 Existing Debt (₹)", min_value=0, step=500)
    risk = st.selectbox("⚖️ Risk Appetite", ["Low", "Medium", "High"])
    phone_usage = st.selectbox(
        "📱 Primary Mobile Usage",
        ["Voice & SMS only", "Basic internet (2G/3G)", "Smartphone data & apps"]
    )
    financial_service = st.selectbox(
        "✅ Desired Service",
        ["Savings", "Credit/Loans", "Insurance", "All"]
    )
    region = st.selectbox(
        "🌐 Region",
        ["Rural/Underbanked", "Urban / Banked"]
    )
    submitted = st.form_submit_button("💡 Get Advice")

if submitted:
    st.spinner("Generating advice…")
    template = """
You are a smart financial advisor working with underserved users in emerging markets. Based on the following profile, give practical, tailored recommendations:

- Monthly Income: ₹{income}
- Age: {age}
- Savings: ₹{savings}
- Debt: ₹{debt}
- Risk Appetite: {risk}
- Mobile Usage: {phone_usage}
- Desired Service: {financial_service}
- Region: {region}

Keep advice short, actionable, and culturally relevant.
"""
    prompt = PromptTemplate.from_template(template)

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        base_url="https://openrouter.ai/api/v1",
    )
    chain = prompt | llm  # RunnableSequence

    response = chain.invoke({
        "income": income,
        "age": age,
        "savings": savings,
        "debt": debt,
        "risk": risk,
        "phone_usage": phone_usage,
        "financial_service": financial_service,
        "region": region,
    })
    st.markdown("### 🧠 Personalized Advice")
    st.write(response.content)


    









