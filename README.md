# Bitcoin Tracker
- A Python-based study/portfolio project designed to demonstrate the use of **FastAPI** for building RESTful APIs,
integration with **PostgreSQL** for data storage, and deployment on **AWS** using Terraform. This project fetches Bitcoin prices 
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