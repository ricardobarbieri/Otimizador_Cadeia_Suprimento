# Easy Transportation Calculator 🚚
A user-friendly web application built with Python and Streamlit to optimize transportation costs using linear programming. Input shipping costs, supply, and demand to find the cheapest way to move goods from factories to cities. Results are displayed in a table and an interactive Plotly chart.

# Features
Interactive Interface: Enter costs (€) and quantities with tooltips and emojis for a smooth experience.
Optimization: Uses PuLP to minimize total shipping costs based on user inputs.
Visualizations: Displays results in a table and an animated bar chart.
Custom Styling: Clean design with CSS, including a ~800x600px layout and styled buttons/messages.

# How to Use
Clone the repo: git clone https://github.com/yourusername/easy-transport-calculator.git
Install dependencies: pip install -r requirements.txt
Run the app: streamlit run app.py
Open your browser, input costs and quantities, then click "Calculate Best Plan" to see the results!

# Requirements
Python 3.x
Libraries: streamlit, pulp, pandas, plotly

# Example
Inputs: Costs (e.g., Factory 1 → City 2: €4), Supply (e.g., Factory 1: 100), Demand (e.g., City 2: 80)
Output: Total cost and quantities shipped per route (e.g., Factory 1 → City 2: 80 units).
