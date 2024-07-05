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
    fig1.update_layout(
        title='Open Branches Over Time',
        xaxis_title='Date',
        yaxis_title='Number of Branches',
        annotations=[
            dict(
                x=0,  # Adjust x and y coordinates as needed for optimal placement
                y=1.05,
                xref='paper',
                yref='paper',
                text='This graph shows the number of branches that were not yet merged on each day.',
                showarrow=False,
            )
        ]
    )
   
    fig2 = go.Figure(data=[go.Scatter(x=timestamps, y=avg_branch_lifetimes, mode='lines', name='Avg Branch Lifetime')])
    fig2.update_layout(
        title='Average Branch Lifetime Over Time',
        xaxis_title='Date',
        yaxis_title='Days',
        annotations=[
            dict(
                x=0,
                y=1.05,
                xref='paper',
                yref='paper',
                text='This graph shows the average time (in days) it took for branches to be merged, calculated for branches merged on each day.',
                showarrow=False,
            )
        ]
    )

    fig3 = go.Figure(data=[go.Scatter(x=timestamps, y=avg_pr_lifetimes, mode='lines', name='Avg PR Lifetime')])
    fig3.update_layout(
        title='Average Pull Request Lifetime Over Time',
        xaxis_title='Date',
        yaxis_title='Days',
        annotations=[
            dict(
                x=0,
                y=1.05,
                xref='paper',
                yref='paper',
                text='This graph shows the average time (in days) between a pull request being opened and merged, calculated for PRs merged on each day.',
                showarrow=False,
            )
        ]
    )

    fig4 = go.Figure(data=[go.Scatter(x=timestamps, y=avg_branch_pr_gaps, mode='lines', name='Avg Branch-PR Gap')])
    fig4.update_layout(
        title='Average Time Between Branch Creation and PR Opening',
        xaxis_title='Date',
        yaxis_title='Days',
        annotations=[
            dict(
                x=0,
                y=1.05,
                xref='paper',
                yref='paper',
                text='This graph shows the average time (in days) between a branch being created and its associated pull request being opened, calculated for branches created and PRs opened on each day.',
                showarrow=False,
            )
        ]
    )

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