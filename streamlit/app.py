import streamlit as st
import pandas as pd
import plotly.express as px
from finance_utils import analyze_finances, generate_financial_advice
from gemini_chat import ask_gemini

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Financial Advisor")
st.subheader("Your Personal AI-Powered Financial Planning Assistant")

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("User Financial Details")

profile = st.sidebar.selectbox(
    "Select Profile",
    ["Student", "Professional"]
)

if profile == "Student":

    income = st.sidebar.number_input("Monthly Income", min_value=0)

    part_time = st.sidebar.selectbox(
        "Do you have part-time income?",
        ["No", "Yes"]
    )

    if part_time == "Yes":
        extra_income = st.sidebar.number_input("Part-time income", min_value=0)
        income += extra_income

else:

    income = st.sidebar.number_input("Monthly Salary", min_value=0)

expenses = st.sidebar.number_input("Monthly Expenses", min_value=0)

savings = st.sidebar.number_input("Current Savings", min_value=0)

debts = st.sidebar.number_input("Total Debts", min_value=0)

goals_input = st.sidebar.text_area(
    "Financial Goals (comma separated)",
    "buy house, travel, emergency fund"
)

risk = st.sidebar.selectbox(
    "Risk Tolerance",
    ["Low", "Medium", "High"]
)

analyze = st.sidebar.button("Analyze & Advise")

# ---------------- MAIN ANALYSIS ---------------- #

if analyze:

    user_data = {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "debts": debts,
        "risk": risk
    }

    analysis = analyze_finances(user_data)

    advice = generate_financial_advice(user_data, analysis)

    remaining = analysis["remaining_income"]
    savings_ratio = analysis["savings_ratio"]

    st.header("Financial Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Income", income)
    col2.metric("Expenses", expenses)
    col3.metric("Savings", savings)
    col4.metric("Debts", debts)

    st.divider()

    st.subheader("Financial Health Indicators")

    col1, col2 = st.columns(2)

    with col1:

        st.write("Savings Ratio")

        st.progress(min(max(savings_ratio, 0), 1))

    with col2:

        st.write("Debt Level")

        if debts > savings:
            st.error("Debt is higher than savings")
        else:
            st.success("Debt is manageable")

    st.divider()

    data = pd.DataFrame({
        "Category": ["Income", "Expenses", "Savings"],
        "Amount": [income, expenses, savings]
    })

    fig = px.bar(
        data,
        x="Category",
        y="Amount",
        title="Financial Distribution"
    )

    st.plotly_chart(fig)

    st.divider()

    st.header("Goal-Oriented Planning")

    goals = [g.strip() for g in goals_input.split(",")]

    for g in goals:
        st.write("•", g)

    st.divider()

    st.subheader("AI Financial Advice")

    for tip in advice:
        st.write("•", tip)

# ---------------- CHATBOT ---------------- #

st.divider()

st.header("💬 AI Financial Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Ask a financial question")

send = st.button("Send")

if send and user_query:

    prompt = f"""
User Financial Data:

Income: {income}
Expenses: {expenses}
Savings: {savings}
Debts: {debts}
Risk tolerance: {risk}

User Question:
{user_query}

Provide helpful financial advice.
"""

    answer = ask_gemini(prompt)

    st.session_state.chat_history.append(("You", user_query))
    st.session_state.chat_history.append(("AI", answer))

for sender, message in st.session_state.chat_history:

    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**AI:** {message}")