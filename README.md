# Innowise Internship Tasks

This repository contains solutions to internship tasks completed during the Innowise Group program.  
It includes PostgreSQL SQL queries and Python 3.12 scripts that:

- Load data from JSON files into a PostgreSQL database, execute database queries and save the output results into both JSON and XML formats
- Execute database queries

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL server running locally or remotely
- Access to a database and user credentials

### Installation

1. Clone the repository:

```bash
git clone https://github.com/anastainty/innowise_tasks.git
cd innowise_tasks
```

2.Set up a virtual environment (optional but recommended):

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### ⚙️ Configuration
Update database connection settings in the Python scripts (e.g., host, port, database, user, password) according to your environment.

### 📥 Data Loading & Query Execution
Each Python script is responsible for a specific part of the workflow:

Load data from JSON into PostgreSQL
Execute SQL queries from .sql files
Export results to JSON and XML
You can run scripts like this:

```bash
python scripts/load_data.py
python scripts/run_queries.py
```

Output files will be saved in the output/ directory.

### 📦 Dependencies

All required Python packages are listed in requirements.txt.

### 📚 License

This project is intended for educational and evaluation purposes during the internship. No license is applied.
