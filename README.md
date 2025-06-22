# Education Loan Repayments Calculator

This is a Streamlit-based web application that allows users to calculate and visualize their education loan repayment schedule. The tool supports flexible loan terms, APY-based interest, grace periods, interest-only repayment phases, and CSV export.

## Features

* Input loan amount, APY (Annual Percentage Yield), and loan term (in years and months)
* Grace period and interest-only period support
* Option to capitalize interest from the grace period
* Dynamic EMI calculation after deferment periods
* Line chart for remaining balance over time
* Stacked area chart for interest vs. principal breakdown
* Full monthly schedule table and CSV export

## How to Use

### 1. Install Dependencies

```
pip install streamlit pandas matplotlib
```

### 2. Run the App

```
streamlit run app.py
```

### 3. Fill Out the Form

* Enter your loan details (amount, interest rate as APY, term)
* Choose deferment and interest-only periods if applicable
* Toggle interest capitalization during the grace period

### 4. Review Outputs

* Repayment summary metrics
* Charts for balance and breakdown
* Downloadable payment schedule CSV

## Requirements

* Python 3.8+
* Streamlit
* Pandas
* Matplotlib

---

This tool helps students and financial planners understand how different loan structures affect long-term repayment costs and schedules.
