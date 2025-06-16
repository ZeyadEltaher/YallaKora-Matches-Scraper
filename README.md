# YallaKora Match Scraper

This Python project scrapes football match data from the YallaKora website over a specified date range and stores the results in a MySQL database.

---

## Features

- Scrapes match information including teams, scores, status, date, time, championship title, round number, and TV channel.
- Supports scraping matches for any date range you specify.
- Automatically creates the necessary database table if it doesn't exist.
- Uses environment variables to securely manage database credentials.
- Handles errors gracefully and continues scraping.

---

## Requirements

- Python 3.7 or higher
- MySQL server running and accessible
- The following Python packages:
  - requests
  - beautifulsoup4
  - python-dotenv
  - mysql-connector-python
  - lxml

---

## Setup Instructions

1. **Clone or download** this repository.

2. **Create a `.env` file** in the project root folder with the following content (replace with your actual database info):

   ```ini
   DB_HOST=your_database_host
   DB_USER=your_database_username
   DB_PASSWORD=your_database_password
   DB_NAME=your_database_name
3. **Install the required Python packages** by running:

   pip install -r requirements.txt

4. **Run the script and call the function with your desired date range**, for example:

    get_matches_info("6/10/2025", "6/19/2025")


## How It Works
- The script scrapes football match data from YallaKora’s match center page for each date in the specified range.

- It parses HTML using BeautifulSoup to extract relevant information.

- The data is inserted into a MySQL table called matches.

- If the table does not exist, it will be created automatically.

- Time is handled carefully and stored in 12-hour format along with AM/PM period.

- Errors during scraping of individual matches are logged but do not stop the entire process.

## Project Structure
```
/project_root
│
├── .env                   # Environment variables for DB credentials
├── main.py                # Your main Python script with scraping code
├── requirements.txt       # Required Python packages
└── README.md              # This file
