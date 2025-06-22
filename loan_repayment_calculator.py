import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

st.title("📚 Education Loan Repayments Calculator")

st.write("### 🎓 Loan Input Details")

# Loan amount & APY
col1, col2 = st.columns(2)
loan_amount = col1.number_input("Total Education Loan Amount ($)", min_value=0, value=100000)
apy = col2.number_input("Annual Percentage Yield (APY %)", min_value=0.0, value=5.0)
monthly_interest_rate = (1 + (apy / 100)) ** (1 / 12) - 1

# Loan term
st.write("#### Loan Term")
term_col1, term_col2 = st.columns(2)
loan_term_years = term_col1.number_input("Years", min_value=0, value=10)
loan_term_months = term_col2.number_input("Months", min_value=0, max_value=11, value=0)
total_loan_months = loan_term_years * 12 + loan_term_months

# Grace and Interest-only
col3, col4 = st.columns(2)
grace_period = col3.number_input("Grace Period (months)", min_value=0, max_value=12, value=6)
interest_only_months = col4.number_input("Interest-Only Period (months)", min_value=0, max_value=60, value=6)
capitalize_interest = st.checkbox("Capitalize Interest from Grace Period?", value=True)

# Capitalize interest if chosen
if capitalize_interest:
    for _ in range(grace_period):
        loan_amount += loan_amount * monthly_interest_rate
    accrued_interest = 0  # already included
else:
    accrued_interest = loan_amount * monthly_interest_rate * grace_period

# Monthly EMI calculation
repayment_months = total_loan_months - grace_period - interest_only_months
monthly_payment_after = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** repayment_months)
    / ((1 + monthly_interest_rate) ** repayment_months - 1)
) if repayment_months > 0 else 0

# Build payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, total_loan_months + 1):
    if i <= grace_period:
        payment = 0
        interest = remaining_balance * monthly_interest_rate
        principal = 0
    elif i <= grace_period + interest_only_months:
        interest = remaining_balance * monthly_interest_rate
        payment = interest
        principal = 0
    else:
        interest = remaining_balance * monthly_interest_rate
        principal = monthly_payment_after - interest
        payment = monthly_payment_after
        remaining_balance -= principal

    year = math.ceil(i / 12)
    schedule.append([i, payment, principal, interest, remaining_balance, year])

# Convert to DataFrame
df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Summary
total_payment = df["Payment"].sum()
total_interest = df["Interest"].sum()

# Metrics
st.write("### 💰 Repayment Summary")
m1, m2, m3 = st.columns(3)
m1.metric("Monthly Payment After Grace", f"${monthly_payment_after:,.2f}")
m2.metric("Total Repayment Amount", f"${total_payment:,.0f}")
m3.metric("Total Interest Paid", f"${total_interest:,.0f}")

# Remaining balance chart
st.write("### 📉 Remaining Loan Balance Over Time")
balance_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(balance_df)

# Monthly Payment Composition
st.write("### 📊 Monthly Payment Composition: Interest vs Principal")

composition_df = df[["Month", "Principal", "Interest"]].copy()
composition_df.set_index("Month", inplace=True)

fig, ax = plt.subplots(figsize=(10, 4))
ax.stackplot(
    composition_df.index,
    composition_df["Principal"],
    composition_df["Interest"],
    labels=["Principal", "Interest"]
)
ax.set_title("Monthly Payment Breakdown")
ax.set_xlabel("Month")
ax.set_ylabel("Amount ($)")
ax.legend(loc="upper right")
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

# Monthly table
st.write("### 📋 Monthly Payment Schedule")
st.dataframe(df.style.format({
    "Payment": "${:,.2f}",
    "Principal": "${:,.2f}",
    "Interest": "${:,.2f}",
    "Remaining Balance": "${:,.2f}",
}))

# Download CSV
csv = df.to_csv(index=False)
st.download_button(
    label="📥 Download Payment Schedule as CSV",
    data=csv,
    file_name="education_loan_schedule.csv",
    mime="text/csv",
)
