import matplotlib.pyplot as plt
import seaborn as sns


def plot_advised_financial_overview(user_data, analysis_data):
    """
    Creates beautiful dark-themed financial visualization charts.
    """
    
    expenses = user_data.get("expenses", 0)
    savings = analysis_data.get("savings", 0)
    emergency_fund_monthly = analysis_data.get("emergency_fund_monthly", 0)

    investment_allocation = analysis_data.get("recommended_investment_allocation", {})

    high_interest = investment_allocation.get("High-Interest Savings / RD", 0)
    stocks = investment_allocation.get("Stocks / Equity Funds", 0)
    etfs = investment_allocation.get("ETFs / Balanced Funds", 0)
    bonds = investment_allocation.get("Debt Mutual Funds / Bonds", 0)

    total_investments = high_interest + stocks + etfs + bonds
    remaining_savings = max(0, savings - (emergency_fund_monthly + total_investments))

    labels_all = [
        "Expenses",
        "Emergency Fund",
        "High-Interest / RD",
        "Stocks / Equity",
        "ETFs / Balanced",
        "Debt / Bonds",
        "Unallocated"
    ]

    values_all = [
        expenses,
        emergency_fund_monthly,
        high_interest,
        stocks,
        etfs,
        bonds,
        remaining_savings
    ]

    labels = [l for l, v in zip(labels_all, values_all) if v > 0]
    values = [v for l, v in zip(labels_all, values_all) if v > 0]
    
    if not values or sum(values) == 0:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, 'No data to visualize\nPlease enter your financial information',
                ha='center', va='center', fontsize=16, color='white')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        fig.patch.set_facecolor('#0f172a')
        return fig

    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('#0f172a')
    
    colors = [
        '#7c3aed',
        '#06b6d4',  
        '#10b981',  
        '#f59e0b',  
        '#ef4444',  
        '#8b5cf6',  
        '#64748b'   
    ]

    colors = colors[:len(values)]

    ax[0].set_facecolor('#1e293b')
    
    wedges, texts, autotexts = ax[0].pie(
        values, 
        labels=labels, 
        autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
        colors=colors, 
        startangle=90,
        textprops={'color': 'white', 'fontsize': 10, 'weight': 'bold'},
        wedgeprops={'linewidth': 2, 'edgecolor': '#0f172a'}
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_weight('bold')
    
    ax[0].set_title(
        'Financial Distribution', 
        color='white', 
        fontsize=16, 
        weight='bold',
        pad=20
    )

    ax[1].set_facecolor('#1e293b')
    
    bars = ax[1].bar(
        range(len(labels)), 
        values, 
        color=colors,
        edgecolor='#0f172a',
        linewidth=2
    )
    
    for bar, color in zip(bars, colors):
        bar.set_alpha(0.9)
    
    ax[1].set_xticks(range(len(labels)))
    ax[1].set_xticklabels(labels, rotation=45, ha='right', color='white', fontsize=10)
    ax[1].set_ylabel('Amount (₹)', color='white', fontsize=12, weight='bold')
    ax[1].tick_params(colors='white')
    
    for i, (value, bar) in enumerate(zip(values, bars)):
        height = bar.get_height()
        ax[1].text(
            bar.get_x() + bar.get_width()/2., 
            height,
            f'₹{int(value):,}',
            ha='center', 
            va='bottom',
            color='white',
            fontsize=10,
            weight='bold'
        )
    
    ax[1].set_title(
        'Amount Breakdown', 
        color='white', 
        fontsize=16, 
        weight='bold',
        pad=20
    )

    ax[1].grid(axis='y', alpha=0.2, color='white', linestyle='--', linewidth=0.5)
    ax[1].set_axisbelow(True)
    
    for spine in ['top', 'right']:
        ax[1].spines[spine].set_visible(False)
    
    for spine in ['bottom', 'left']:
        ax[1].spines[spine].set_color('white')
        ax[1].spines[spine].set_linewidth(1.5)

    plt.tight_layout()
    
    return fig