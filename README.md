# Bitcoin Tracker

- A Python-based study/portfolio project designed to demonstrate the use of **FastAPI** for building RESTful APIs,
  integration with **PostgreSQL** for data storage, and deployment on **AWS** using Terraform. This project fetches
  Bitcoin prices
  every minute using the **CoinGecko API**, stores them in a database, computes daily summaries (min/max prices),
  and includes a cleanup job to manage storage by removing data older than 90 days.

### Project Goals

- Showcase **FastAPI** for creating modern, asynchronous RESTful APIs.
- Demonstrate Python best practices for data fetching, storage, and processing.
- Implement a real-world use case with **PostgreSQL**, **AWS**, and **Terraform**.
- Provide a fully testable codebase with unit and integration tests.
- Serve as a portfolio piece for learning and experimentation.

### Features

- **Real-time Data Collection:** Fetches Bitcoin prices every minute using the CoinGecko API.
- **Daily Summaries:** Computes and stores the minimum and maximum Bitcoin prices per day.
- **Data Cleanup:** Automatically deletes data older than 90 days to manage storage.
- **API Endpoints:** Exposes endpoints to query Bitcoin prices and summaries.
- **Testing:** Includes unit tests (logic) and integration tests (API + database).
- **Infrastructure as Code:** Deploys the application to AWS (EC2, API Gateway, RDS) using Terraform.

### Tech Stack

- **Python 3.11:** Core programming language.
- **FastAPI:** Web framework for building APIs.
- **PostgreSQL:** Database for storing Bitcoin prices and summaries.
- **CoinGecko API:** Source of Bitcoin price data.
- **SQLAlchemy:** ORM for database interactions.
- **Pytest:** Framework for unit and integration tests.
- **Terraform:** Infrastructure provisioning on AWS.
- **AWS Services:**
    - **EC2:** Hosts the FastAPI application.
    - **API Gateway:** Exposes the API endpoints.
    - **RDS:** Managed PostgreSQL database.

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Terraform 1.5+
- AWS account with credentials configured
- CoinGecko API access (free tier, no key required)
- Docker (optional, for local development)

### Email Notifications

The application includes an automated email notification system that alerts users when Bitcoin's price experiences significant dips.
Specifically:

- Monitors Bitcoin price movements in real-time
- Sends email notifications when the current price drops below 10% of the historic maximum price
- Uses SMTP for sending emails (configured for Gmail by default)
- Customizable threshold through environment variables

### Environment Setup

To run the project, you need to create a `.env` file in the root directory with the following configuration:

```env
# Bitcoin API Configuration
BITCOIN_API_URL=https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd
ALLOWED_ORIGINS=

# Database Configuration
# For PostgreSQL (uncomment and configure as needed):
# DATABASE_URL=postgresql://admin:password@localhost:5432/bitcoin_tracker
# For SQLite in-memory (development/testing):
DATABASE_URL=sqlite:///:memory:

# Email Configuration
SENDER_EMAIL=your.email@gmail.com
DESTINATION_EMAIL=destination.email@example.com
SENDER_EMAIL_PASSWORD='your-app-specific-password'  # Gmail App Password
SMTP_ADDRESS=smtp.gmail.com
SMTP_PORT=587

# Price Alert Configuration
BITCOIN_PRICE_DIP_MIN_THRESHOLD=0.1  # 10% threshold for price dip alerts
```

Notes for email setup:
1. For Gmail, you need to use an App Password instead of your regular password
2. To generate an App Password:
   - Enable 2-Step Verification in your Google Account
   - Go to Security → App Passwords
   - Generate a new App Password for the application
3. Use the generated App Password in the `SENDER_EMAIL_PASSWORD` field


### API Endpoints

The API is prefixed with _/bitcoin_ and provides the following endpoints:

- **Get Latest Bitcoin Price**
    - Endpoint: **GET /bitcoin/prices/latest**
    - Description: Retrieves the most recent Bitcoin price stored in the database.
    - Response:
    - 200 OK: Returns the latest price data.

  ```
  {
    "id": 1,
    "price": 50000.0,
    "timestamp": "2025-04-06 12:00:00"
  }
  ```
    - 404 Not Found: If no prices are available.

    - ```{"detail": "No prices found"}```
    - 500 Internal Server Error: If an error occurs while fetching the data.


- **Get Daily Bitcoin Price Summary**
    - Endpoint: **GET /bitcoin/prices/summary/{date}**
    - Description: Retrieves a summary of Bitcoin prices for a specific day, including the maximum and minimum prices.
      The date parameter must be in YYYY-MM-DD format.
        - Parameters:
            - date (path): The date for which to retrieve the summary (e.g., 2025-04-06).
    - Response:
      200 OK: Returns the summary for the specified date.

    ```
  {
        "id": 1,
        "max_price": 51000.0,
        "min_price": 49000.0,
        "date": "2025-04-06"
    }
  ```

    - 404 Not Found: If no summary is available for the given date.


- **Get All Bitcoin Price Summaries**
    - Endpoint: GET /bitcoin/prices/summaries/
    - Description: Retrieves a list of all daily Bitcoin price summaries stored in the database.
    - Response:
      200 OK: Returns a list of summaries.

  ```
  [
    {
      "id": 1,
      "max_price": 51000.0,
      "min_price": 49000.0,
      "date": "2025-04-06"
    },
    {
      "id": 2,
      "max_price": 52000.0,
      "min_price": 50000.0,
      "date": "2025-04-07"
    }
  ]
