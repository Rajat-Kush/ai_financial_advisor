def analyze_finances(user_data):

    income = user_data.get("income", 0)
    expenses = user_data.get("expenses", 0)
    debts = user_data.get("debts", 0)
    existing_savings = user_data.get("existing_savings", 0)

    savings = max(0, income - expenses)

    debt_to_income_ratio = debts / income if income > 0 else 0
    savings_ratio = savings / income if income > 0 else 0
    expense_ratio = expenses / income if income > 0 else 0
    debt_to_savings_ratio = debts / savings if savings > 0 else 0

    investment_capacity = savings * 0.5
    total_net_worth = existing_savings + savings - debts

    emergency_fund_target = expenses * 6
    emergency_fund_shortfall = max(0, emergency_fund_target - existing_savings)
    emergency_fund_monthly = emergency_fund_shortfall / 18 if emergency_fund_shortfall > 0 else 0

    risk = user_data.get("risk_tolerance", "medium").lower()

    if risk == "low":
        investment_allocation = {
            "High-Interest Savings / RD": investment_capacity * 0.4,
            "Debt Mutual Funds / Bonds": investment_capacity * 0.4,
            "ETFs / Balanced Funds": investment_capacity * 0.2
        }

    elif risk == "medium":
        investment_allocation = {
            "Stocks / Equity Funds": investment_capacity * 0.3,
            "ETFs / Balanced Funds": investment_capacity * 0.4,
            "Debt Mutual Funds / Bonds": investment_capacity * 0.3
        }

    elif risk == "high":
        investment_allocation = {
            "Stocks / Equity Funds": investment_capacity * 0.5,
            "ETFs / Balanced Funds": investment_capacity * 0.3,
            "Debt Mutual Funds / Bonds": investment_capacity * 0.2
        }

    else:
        investment_allocation = {
            "Stocks / Equity Funds": investment_capacity * 0.3,
            "ETFs / Balanced Funds": investment_capacity * 0.4,
            "Debt Mutual Funds / Bonds": investment_capacity * 0.3
        }

    high_debt_alert = debt_to_income_ratio > 0.4

    return {
        "savings": savings,
        "debt_to_income_ratio": debt_to_income_ratio,
        "savings_ratio": savings_ratio,
        "expense_ratio": expense_ratio,
        "debt_to_savings_ratio": debt_to_savings_ratio,
        "investment_capacity": investment_capacity,
        "emergency_fund_target": emergency_fund_target,
        "emergency_fund_shortfall": emergency_fund_shortfall,
        "emergency_fund_monthly": emergency_fund_monthly,
        "total_net_worth": total_net_worth,
        "existing_savings": existing_savings,
        "recommended_investment_allocation": investment_allocation,
        "high_debt_alert": high_debt_alert
    }