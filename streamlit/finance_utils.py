def analyze_finances(data):

    income = data["income"]
    expenses = data["expenses"]
    savings = data["savings"]
    debts = data["debts"]

    remaining = income - expenses

    savings_ratio = 0
    if income > 0:
        savings_ratio = remaining / income

    debt_ratio = 0
    if income > 0:
        debt_ratio = debts / income

    analysis = {
        "remaining_income": remaining,
        "savings_ratio": savings_ratio,
        "debt_ratio": debt_ratio
    }

    return analysis


def generate_financial_advice(data, analysis):

    advice = []

    if analysis["savings_ratio"] < 0.2:
        advice.append("Try to save at least 20% of your income.")

    if data["debts"] > data["income"]:
        advice.append("Focus on reducing debts before investing.")

    if data["risk"] == "Low":
        advice.append("Consider fixed deposits or government bonds.")

    elif data["risk"] == "Medium":
        advice.append("Mutual funds can be a balanced investment.")

    elif data["risk"] == "High":
        advice.append("Stocks or ETFs may suit your risk appetite.")

    return advice