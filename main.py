import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI  # ✅ Updated import
from langchain_core.runnables import RunnableSequence  # ✅ New method

def main():
    print("✅ Smart Financial Advisor Started!\n")

    # Take user inputs
    income = input("💬 Enter your monthly income in ₹: ")
    age = input("💬 Enter your age: ")
    savings = input("💬 Enter your current savings in ₹: ")
    debt = input("💬 Enter your existing debt in ₹ (0 if none): ")
    risk = input("💬 What is your risk appetite? (Low / Medium / High): ")

    print("\n💡 Generating personalized financial advice...\n")

    # Prompt template
    template = """
    You are a financial advisor. Based on the following user's financial data:
    - Monthly Income: ₹{income}
    - Age: {age}
    - Current Savings: ₹{savings}
    - Existing Debt: ₹{debt}
    - Risk Appetite: {risk}
    
    Provide actionable and personalized financial advice in bullet points.
    """

    prompt = PromptTemplate(
        input_variables=["income", "age", "savings", "debt", "risk"],
        template=template
    )

    # ✅ Updated usage with langchain-openai
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        base_url="https://openrouter.ai/api/v1",
        api_key="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",  
        temperature=0.7
    )

    # ✅ Replace LLMChain with RunnableSequence
    chain: RunnableSequence = prompt | llm

    # Invoke
    response = chain.invoke({
        "income": income,
        "age": age,
        "savings": savings,
        "debt": debt,
        "risk": risk
    })

    print("💬 Advice:\n")
    print(response.content)

if __name__ == "__main__":
    main()

