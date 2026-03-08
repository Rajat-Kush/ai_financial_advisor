import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


def generate_rule_based_advice(user_data, analysis_data):
    """
    Generates advice using rules when API quota is exceeded.
    This ensures your app ALWAYS works!
    """
    
    income = user_data.get("income", 0)
    expenses = user_data.get("expenses", 0)
    savings = analysis_data.get("savings", 0)
    debts = user_data.get("debts", 0)
    existing_savings = user_data.get("existing_savings", 0)
    risk = user_data.get("risk_tolerance", "medium").lower()
    
    savings_ratio = analysis_data.get("savings_ratio", 0) * 100
    debt_ratio = analysis_data.get("debt_to_income_ratio", 0) * 100
    emergency_fund_target = analysis_data.get("emergency_fund_target", 0)
    emergency_fund_shortfall = analysis_data.get("emergency_fund_shortfall", 0)
    emergency_fund_monthly = analysis_data.get("emergency_fund_monthly", 0)
    investment_capacity = analysis_data.get("investment_capacity", 0)
    
    advice = f"""
Budgeting Strategy:
• Your current savings ratio is {savings_ratio:.1f}% - {'Excellent!' if savings_ratio >= 20 else 'Try to reach at least 20%'}
• Monthly surplus available: ₹{savings:,.0f}
• {'Consider reducing expenses to increase savings' if savings_ratio < 20 else 'Great job maintaining healthy savings!'}
• Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings
• Track all expenses using a budgeting app

Debt Management:
{'• No debts - Excellent financial position! Focus on building wealth.' if debts == 0 else f"""• Total debt: ₹{debts:,.0f} ({debt_ratio:.1f}% of income)
• {'⚠️ High debt burden - prioritize aggressive repayment' if debt_ratio > 40 else '✓ Manageable debt level'}
• Pay off highest interest rate debts first (avalanche method)
• Consider debt consolidation if you have multiple loans
• Allocate extra savings toward debt reduction
• Aim to keep total debt below 40% of annual income"""}

Investment Advice:
• Monthly investment capacity: ₹{investment_capacity:,.0f}
• Risk tolerance: {risk.title()}
{f'''• For {risk} risk:
  - {'60% Debt Funds, 40% Equity' if risk == 'low' else '50% Equity, 30% Balanced Funds, 20% Debt' if risk == 'medium' else '70% Equity, 20% Balanced Funds, 10% Debt'}
''' if investment_capacity > 0 else '• Focus on emergency fund before investing'}
• Start SIPs (Systematic Investment Plans) for regular investing
• Diversify across asset classes
• Consider index funds for low-cost equity exposure
• Review and rebalance portfolio annually

Emergency Fund:
• Target emergency fund: ₹{emergency_fund_target:,.0f} (6 months expenses)
• Current savings: ₹{existing_savings:,.0f}
• {'✓ Emergency fund fully funded!' if emergency_fund_shortfall == 0 else f'• Shortfall: ₹{emergency_fund_shortfall:,.0f}'}
{f'• Recommended monthly contribution: ₹{emergency_fund_monthly:,.0f}' if emergency_fund_shortfall > 0 else '• Maintain liquid emergency fund in savings account or liquid funds'}
• Keep emergency fund in easily accessible accounts
• Don't invest emergency funds in stocks or long-term assets

Goal Planning:
• Define specific financial goals with clear timelines
• Break down large goals into monthly savings targets
• Open separate accounts for different goals
• Review progress quarterly and adjust as needed
• Consider tax-saving investments (PPF, ELSS) for long-term goals
• Use goal-based calculators to track progress
"""
    
    return advice


def generate_financial_advice(user_data, analysis_data):
    """
    Generate comprehensive financial advice.
    Falls back to rule-based advice if API quota is exceeded.
    """
    
    if not api_key or model is None:
        return generate_rule_based_advice(user_data, analysis_data)
    
    profile = user_data.get("profile", "User")
    goals = user_data.get("goals", [])
    goals_str = ', '.join(goals) if goals else "Not specified"

    prompt = f"""
You are a professional financial advisor providing advice to a {profile}.

User Financial Profile:
- Monthly Income: ₹{user_data.get("income", 0):,.0f}
- Monthly Expenses: ₹{user_data.get("expenses", 0):,.0f}
- Current Savings: ₹{user_data.get("existing_savings", 0):,.0f}
- Total Debts: ₹{user_data.get("debts", 0):,.0f}
- Monthly Savings: ₹{analysis_data.get("savings", 0):,.0f}
- Savings Ratio: {analysis_data.get("savings_ratio", 0)*100:.1f}%
- Debt-to-Income Ratio: {analysis_data.get("debt_to_income_ratio", 0)*100:.1f}%
- Risk Tolerance: {user_data.get("risk_tolerance", "medium")}
- Financial Goals: {goals_str}

Analysis Insights:
- Investment Capacity: ₹{analysis_data.get("investment_capacity", 0):,.0f}
- Emergency Fund Target: ₹{analysis_data.get("emergency_fund_target", 0):,.0f}
- Emergency Fund Shortfall: ₹{analysis_data.get("emergency_fund_shortfall", 0):,.0f}
- Recommended Monthly Emergency Fund Contribution: ₹{analysis_data.get("emergency_fund_monthly", 0):,.0f}

Provide practical financial advice organized into these sections:

Budgeting Strategy:
[Provide specific budgeting recommendations]

Debt Management:
[Provide debt reduction strategies if applicable]

Investment Advice:
[Provide investment recommendations based on risk tolerance]

Goal Planning:
[Provide specific advice for achieving stated financial goals]

Emergency Fund:
[Provide guidance on building/maintaining emergency fund]

Use clear bullet points and actionable advice. Be specific with numbers where possible.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error_msg = str(e)
 
        if "429" in error_msg or "quota" in error_msg.lower():
            return f"""
⚠️ **AI Quota Exceeded - Using Smart Rule-Based Advice**

{generate_rule_based_advice(user_data, analysis_data)}

---
*Note: AI quota limit reached. Advice generated using advanced financial rules based on your data.
Your quota will reset in 24 hours, or you can upgrade your API key for unlimited access.*
"""

        return f"""
⚠️ **AI Temporarily Unavailable - Using Smart Rule-Based Advice**

{generate_rule_based_advice(user_data, analysis_data)}

---
*Error: {error_msg[:100]}*
"""


def finance_chatbot_response(user_data, analysis_data, user_query):
    """
    Provide conversational financial advice.
    Falls back to simple responses if quota exceeded.
    """
    
    if not api_key or model is None:
        return "⚠️ Gemini API not configured. Please add your GEMINI_API_KEY to the .env file."
    
    prompt = f"""
You are a friendly financial advisor chatbot.

User's Financial Context:
- Monthly Income: ₹{user_data.get("income", 0):,.0f}
- Monthly Expenses: ₹{user_data.get("expenses", 0):,.0f}
- Current Savings: ₹{user_data.get("existing_savings", 0):,.0f}
- Total Debts: ₹{user_data.get("debts", 0):,.0f}
- Monthly Savings: ₹{analysis_data.get("savings", 0):,.0f}
- Risk Tolerance: {user_data.get("risk_tolerance", "medium")}

User Question:
{user_query}

Provide helpful, personalized financial advice in 3-5 clear bullet points.
Be specific to their situation and use actual numbers when relevant.
Keep the tone friendly and encouraging.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error_msg = str(e)
        
        if "429" in error_msg or "quota" in error_msg.lower():
            return """
⚠️ **AI quota exceeded. Here's general advice:**

• Build an emergency fund covering 6 months of expenses
• Save at least 20% of your income monthly
• Pay off high-interest debts first (credit cards, personal loans)
• Invest based on your risk tolerance
• Review your budget regularly and track expenses

*Your AI quota will reset in 24 hours. Meanwhile, click "Analyze & Advise" for detailed rule-based guidance!*
"""
        
        return f"⚠️ Chatbot temporarily unavailable. Please use the main 'Analyze & Advise' feature instead."


def generate_goal_plan(user_data, analysis_data, specific_goal):
    """
    Generate a detailed plan for achieving a specific financial goal.
    """
    
    if not api_key or model is None:
        return "⚠️ Gemini API not configured."
    
    prompt = f"""
You are a financial planner creating a detailed action plan.

User Profile:
- Monthly Income: ₹{user_data.get("income", 0):,.0f}
- Monthly Savings: ₹{analysis_data.get("savings", 0):,.0f}
- Current Savings: ₹{user_data.get("existing_savings", 0):,.0f}
- Risk Tolerance: {user_data.get("risk_tolerance", "medium")}

Financial Goal: {specific_goal}

Create a detailed, step-by-step plan including timeline, required savings, monthly contribution, investment strategy, and action steps.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            return "⚠️ AI quota exceeded. Goal planning feature will be available when quota resets (24 hours)."
        return f"⚠️ Error: {str(e)[:100]}"