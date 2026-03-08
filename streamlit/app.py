import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st

from core.finance_analysis import analyze_finances
from core.ai_advisor import generate_financial_advice, finance_chatbot_response
from core.visualization import plot_advised_financial_overview
from core.utils import split_advice_sections

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
try:
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("styles.css not found. Using default styling.")

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<div class="hero-container">
    <div class="hero-title">💰 AI Financial Advisor</div>
    <div class="hero-subtitle">
        Your Personal AI-Powered Financial Planning Assistant
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("User Financial Details")

profile = st.sidebar.selectbox(
    "Select Profile",
    ["Student", "Professional"]
)

if profile == "Student":
    income = st.sidebar.number_input("Monthly Income", min_value=0, value=0)
    
    part_time = st.sidebar.selectbox(
        "Do you have part-time income?",
        ["No", "Yes"]
    )
    
    if part_time == "Yes":
        extra_income = st.sidebar.number_input("Part-time income", min_value=0, value=0)
        income += extra_income
else:
    income = st.sidebar.number_input("Monthly Salary", min_value=0, value=0)

expenses = st.sidebar.number_input("Monthly Expenses", min_value=0, value=0)

existing_savings = st.sidebar.number_input("Current Savings", min_value=0, value=0)

debts = st.sidebar.number_input("Total Debts", min_value=0, value=0)

goals_input = st.sidebar.text_area(
    "Financial Goals (comma separated)",
    "buy house, travel, emergency fund"
)

risk_tolerance = st.sidebar.selectbox(
    "Risk Tolerance",
    ["Low", "Medium", "High"]
)

analyze = st.sidebar.button("Analyze & Advise")

if not analyze:
    st.info("Enter your financial details in the sidebar and click **Analyze & Advise** to generate your financial report.")

if analyze:
    
    if income == 0:
        st.warning("Please enter your income before analyzing.")
        st.stop()

    goals = [g.strip() for g in goals_input.split(",") if g.strip()]

    user_data = {
        "profile": profile,
        "income": income,
        "expenses": expenses,
        "existing_savings": existing_savings, 
        "debts": debts,
        "risk_tolerance": risk_tolerance,
        "goals": goals
    }

    with st.spinner("Analyzing financial data..."):
        analysis = analyze_finances(user_data)
        advice_text = generate_financial_advice(user_data, analysis)
        
    advice = split_advice_sections(advice_text)

    savings_ratio = analysis["savings_ratio"]
    monthly_savings = analysis["savings"]

    st.markdown('<p class="section-title">Financial Overview</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1.metric("Monthly Income", f"₹{income:,.0f}")
    col2.metric("Monthly Expenses", f"₹{expenses:,.0f}")
    col3.metric("Current Savings", f"₹{existing_savings:,.0f}")
    col4.metric("Total Debts", f"₹{debts:,.0f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.subheader("Financial Health Indicators")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Savings Ratio**")
        st.progress(min(max(savings_ratio, 0), 1))
        st.caption(f"{savings_ratio*100:.1f}% of income saved monthly")

    with col2:
        st.write("**Debt Level**")
        if debts > existing_savings:
            st.error("⚠️ Debt exceeds savings")
        elif debts > income * 3:
            st.warning("⚠️ High debt burden")
        else:
            st.success("✅ Debt is manageable")

    with col3:
        st.write("**Monthly Surplus**")
        st.metric("Available", f"₹{monthly_savings:,.0f}")

    st.divider()

    st.markdown('<p class="section-title">Financial Distribution</p>', unsafe_allow_html=True)
    fig = plot_advised_financial_overview(user_data, analysis)
    st.pyplot(fig)

    st.divider()

    st.markdown('<p class="section-title">Goal-Oriented Planning</p>', unsafe_allow_html=True)

    if goals:
        for g in goals:
            st.write("🎯", g.title())
    else:
        st.info("No financial goals specified.")

    st.divider()

    st.markdown('<p class="section-title">AI Financial Advice</p>', unsafe_allow_html=True)

    for section, content in advice.items():
        with st.expander(f"📊 {section}", expanded=True):
            st.write(content)

    st.session_state.user_data = user_data
    st.session_state.analysis = analysis

st.divider()

st.markdown('<p class="section-title">💬 AI Financial Chatbot</p>', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Ask a financial question", key="chat_input")
send = st.button("Send")

if send and user_query:
    
    if "user_data" not in st.session_state or "analysis" not in st.session_state:
        st.warning("⚠️ Please click 'Analyze & Advise' first to get personalized responses.")
    else:
        with st.spinner("AI is thinking..."):
            answer = finance_chatbot_response(
                st.session_state.user_data,
                st.session_state.analysis,
                user_query
            )

        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("AI", answer))

for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")

st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <small>AI Financial Advisor | Powered by Gemini AI</small>
</div>
""", unsafe_allow_html=True)