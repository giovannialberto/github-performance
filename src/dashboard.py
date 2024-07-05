from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template
from database.database import DatabaseManager
from database.stats import StatsCalculator
    
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    db_manager = DatabaseManager()
    stats_calculator = StatsCalculator(db_manager)

    timestamps = []
    open_branches = []
    avg_branch_lifetimes = []
    avg_pr_lifetimes = []
    avg_branch_pr_gaps = []

    now = datetime.now()
    for i in range(30):  # Get data for the past 30 days
        date = now - timedelta(days=i)
        timestamps.append(date.strftime("%Y-%m-%d"))
        open_branches.append(stats_calculator.calculate_open_branches(date))
        avg_branch_lifetimes.append(stats_calculator.calculate_average_branch_lifetime(date))
        avg_pr_lifetimes.append(stats_calculator.calculate_average_pr_lifetime(date))
        avg_branch_pr_gaps.append(stats_calculator.calculate_average_branch_pr_gap(date))

    # Create separate Plotly figures for each metric
    fig1 = go.Figure(data=[go.Scatter(x=timestamps, y=open_branches, mode='lines', name='Open Branches')])
    fig1.update_layout(title='Open Branches Over Time', xaxis_title='Date', yaxis_title='Number of Branches')

    fig2 = go.Figure(data=[go.Scatter(x=timestamps, y=avg_branch_lifetimes, mode='lines', name='Avg Branch Lifetime')])
    fig2.update_layout(title='Average Branch Lifetime Over Time', xaxis_title='Date', yaxis_title='Days')

    fig3 = go.Figure(data=[go.Scatter(x=timestamps, y=avg_pr_lifetimes, mode='lines', name='Avg PR Lifetime')])
    fig3.update_layout(title='Average PR Lifetime Over Time', xaxis_title='Date', yaxis_title='Days')

    fig4 = go.Figure(data=[go.Scatter(x=timestamps, y=avg_branch_pr_gaps, mode='lines', name='Avg Branch-PR Gap')])
    fig4.update_layout(title='Average Branch-PR Gap Over Time', xaxis_title='Date', yaxis_title='Days')

    # Convert figures to JSON for rendering in HTML
    graphJSON1 = fig1.to_json()
    graphJSON2 = fig2.to_json()
    graphJSON3 = fig3.to_json()
    graphJSON4 = fig4.to_json()

    return render_template('index.html', graphJSON1=graphJSON1, graphJSON2=graphJSON2,
                           graphJSON3=graphJSON3, graphJSON4=graphJSON4)


def main():
    app.run(host='0.0.0.0', port=8080, debug=True) 

if __name__ == "__main__":
    main()