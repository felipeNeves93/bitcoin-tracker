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

Below is an example of how you can update your project's README.md file to include descriptions of the endpoints from
app/api/endpoints.py. I’ll assume your project is called "Bitcoin Tracker" and provide a clear, concise description of
each endpoint, including their purpose, request format, and response format. You can adjust this based on your existing
README.md content or project details.

Example README.md
markdown

Collapse

Wrap

Copy

# Bitcoin Tracker

Bitcoin Tracker is a FastAPI-based application that fetches, stores, and provides insights into Bitcoin price data. It
uses a background job to periodically fetch the latest Bitcoin price from an external API (e.g., CoinGecko) and stores
it in a database. The application exposes RESTful endpoints to retrieve the latest price, daily summaries, and
historical summary data.

## Features

- Fetches Bitcoin prices every 60 seconds and stores them in a database.
- Provides endpoints to retrieve the latest price, daily price summaries, and all summaries.
- Built with FastAPI, SQLAlchemy, and Python threading for background tasks.

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
