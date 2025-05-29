

# 🔐 Flask JWT Authentication with Docker & PostgreSQL

A secure Flask application that implements JWT-based user authentication and authorization. Fully containerized using Docker, connected to a PostgreSQL database, and monitored through pgAdmin.

---

## 🗂️ Table of Contents

- [📌 Overview](#-overview)
- [🧠 Project Architecture](#-project-architecture)
- [🚀 Getting Started](#-getting-started)
- [⚙️ Services & Ports](#️-services--ports)
- [📦 Tech Stack](#-tech-stack)
- [📁 Directory Structure](#-directory-structure)
- [🔐 API Endpoints](#-api-endpoints)
- [🔌 Port Mapping](#-port-mapping)
- [📃 License](#-license)

---

## 📌 Overview

This project demonstrates how to:

- Build a modular Flask app with JWT Auth (access + refresh tokens)
- Use PostgreSQL for user/token storage
- Monitor and manage the database via pgAdmin
- Containerize the entire stack using Docker Compose

---

## 🧠 Project Architecture

The architecture includes three main Docker containers:

- `Flask App`: Provides the RESTful authentication API.
- `PostgreSQL`: Stores users and JWT-related token data.
- `pgAdmin`: A web-based UI to manage PostgreSQL.

![Project Architecture](images/poridhi.drawio%20(1).svg)

---


## 📁 Project Structure

![Project Structure](images/pic.png)


## ⚙️ Configuration Files
- app/routes/config.py: Contains application configuration settings
- app/routes/auth.py: Handles authentication routes (login, register, etc.)
- app/routes/user.py: Manages user-related endpoints
- app/models.py: Database models for user information
- app/utils.py: Helper functions for the application
- run.py: Entry point for the Flask application
## Database Tables
- users
- refresh_tokens
- revoked_tokens
- reset_tokens

# 🚀 Getting Started
## Prerequisites

- Docker 
- Docker Compose
## Clone the Repository


git clone https://github.com/Towshin05/FLASK_JWT_AUTH.git
- cd FLASK_JWT_AUTH
 

## Run with Docker Compose
 docker-compose up --build

 ## Access the service
| Service    | URL                     | Description               |
| ---------- | ----------------------- | ------------------------- |
| Flask App  | `http://localhost:5000` | API Endpoints             |
| PostgreSQL | `localhost:5432`        | DB Server (internal only) |
| pgAdmin    | `http://localhost:5050` | DB GUI                    |
 pgAdmin Login:

 - Email: admin@example.com
 - Pass: poridhi25
## Create a .env file with the following variables:
 - Flask_APP=run.py
 - FLASK_ENV=development
 - JWT_SECRET_KEY=your_secret_key
 - POSTGRES_USER=postgres
 - POSTGRES_PASSWORD=yourpassword
 - POSTGRES_DB=flask_jwt_auth


## Tech Stack
- Backend: Flask
- Database: PostgreSQL
- Authentication: JWT(Access & Refresh Token)
- Containerization: Docker , Docker compose
- DB Admin: pgAdmin
## 🔐 API Endpoints
| Method | Endpoint     | Description                      |
| ------ | ------------ | -------------------------------- |
| POST   | `/register`  | Register a new user              |
| POST   | `/login`     | Authenticate and get JWT tokens  |
| POST   | `/refresh`   | Get a new access token           |
| POST   | `/logout`    | Revoke access and refresh tokens |
| GET    | `/protected` | Protected route (JWT required)   |

## 🧪 API Testing
You can test the API endpoints using the test_api.sh script included in the project.
- 🔄 Logout Endpoint Example (from test_api.sh)
curl -X POST http://127.0.0.1:5000/api/logout \
 -  -H "Content-Type: application/json" \
 -  -H "Authorization: Bearer <your_access_token_here>"

  - bash test_api.sh (run in terminal)
## 🔌 Port Mapping Guide
- Port Mapping (also known as port forwarding) is the process of forwarding network packets from one network address and port number combination to another. It's commonly used to allow external devices to access services on private networks.

- In a load-balanced environment, port mapping helps distribute traffic efficiently across multiple instances of an application or service.

📍 Get the  private ip address.
- ifconfig
 <div align="center"> <img src="images/ifconfig.drawio.png" alt="ifconfig output" width="500"/> </div>

⚙️ Create load balancer
 <div align="center"> <img src="images/load.drawio.png" alt="load balancer" width="500"/> </div>

🔍 Getting the Ports
<div align="center"> <img src="images/port.png" alt="port information" width="600"/> </div>

## Port mapping example
| Load Balancer Port | Backend IP  | Backend Port | Protocol |
| ------------------ | ----------- | ------------ | -------- |
| 80 (HTTP)          | 192.168.1.2 | 8080         | TCP      |
| 80 (HTTP)          | 192.168.1.3 | 8080         | TCP      |
| 443 (HTTPS)        | 192.168.1.4 | 8443         | TCP      |

# Running the Application
## Start all services
docker-compose up -d

## View logs
docker-compose logs -f app

## Stop all services
docker-compose down
## Stop the running terminal 
CTRL+C

# 🛠  Troubleshooting

## Database Connection Issues:

- Ensure PostgreSQL is running: docker-compose ps
- Check the check_pg_connection.sh script is working correctly
- Check database logs: docker-compose logs db


# 🔑 JWT Token Issues:

- Verify JWT_SECRET_KEY is set correctly in .env
- Check token expiration settings


# 🐳 Docker Issues:

- Rebuild containers: docker-compose up --build
- Clean Docker system: docker system prune

# 📃 License
This project is licensed under the MIT License.

# 🤝 Contributing
Contributions are welcome!
Feel free to fork the repository and open a pull request.
- Contributed by: Towshin05