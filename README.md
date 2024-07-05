# GitHub Performance Dashboard

This project provides a dashboard for monitoring key statistics about branches and pull requests (PRs) across GitHub repositories within an organization. It collects data from GitHub, stores it in a local database, and visualizes trends over time.

## Features

- Tracks the number of open branches.
- Calculates the average lifetime of branches (from creation to merge).
- Calculates the average lifetime of pull requests (from open to merge).
- Calculates the average time gap between branch creation and PR opening.
- Displays interactive plots of these statistics over time on a web-based dashboard.

## Architecture

The project consists of two main components:

1.  **Data Collector:** A Python script (`src/data_collector.py`) that periodically fetches data from the GitHub API and updates a SQLite database.
2.  **Dashboard:** A Flask web application (`src/dashboard.py`) that reads data from the database, calculates statistics, and presents them on a dashboard using Plotly.

## Getting Started

### Prerequisites

- **Docker:** Ensure you have Docker installed on your system.
- **GitHub Personal Access Token:** Generate a GitHub Personal Access Token with the necessary permissions to access repository data (read access to `repo`).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://your-repository-url.git
    ```

2.  **Set up environment variables:**
    - Copy the `.env.example` file to `.env`.
    - Fill in the values for `GITHUB_TOKEN` (your GitHub Personal Access Token), `ORG_NAME` (your GitHub organization name), and `REPOSITORIES` (a comma-separated list of the repositories you want to track).

3.  **Start the application:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Access the dashboard:**
    - Open your web browser and navigate to `http://localhost:8080` (or your server's IP/domain if deployed).

## Customization

- **Statistics:** You can modify the `StatsCalculator` class in `src/database/stats.py` to add or customize the statistics you want to track.
- **Dashboard:** The `src/dashboard.py` file and the `src/templates/index.html` template can be modified to change the appearance and functionality of the dashboard.

## Deployment

- **Docker:** The provided `Dockerfile` and `docker-compose.yml` files are designed to make it easy to deploy the application using Docker.
- **Production:** For production deployment, consider using a production-grade WSGI server (e.g., Gunicorn) for the Flask app and configuring a process manager (e.g., Supervisor) to keep the containers running.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

