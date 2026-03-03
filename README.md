# Ace Perez - Personal Portfolio

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/ace-perez/ace-perez-portfolio)

This repository contains the source code for my personal portfolio website. It is a modern, containerized web application built with Python and Flask, showcasing my work experience, education, hobbies, and a travel map. The project is designed for easy deployment and scaling using Docker, with a complete CI/CD pipeline for automated testing and deployment.

## Features

*   **Dynamic Content**: Easily update work experience, education, and hobbies by modifying data structures in the main application file.
*   **Interactive Travel Map**: A world map powered by Leaflet.js that displays markers for all the places I have visited.
*   **Timeline API**: A RESTful API that allows visitors to post, view, and delete messages on a public timeline.
*   **Responsive Design**: A clean, sidebar-based navigation that adapts to different screen sizes.
*   **Containerized**: Fully containerized using Docker and Docker Compose for both development and production environments.
*   **Automated Deployment**: CI/CD pipeline with GitHub Actions to automatically run tests and deploy the latest version to a live server.
*   **Secure Production Setup**: Production environment uses Nginx as a reverse proxy with SSL certificates from Let's Encrypt for HTTPS.

## Tech Stack

*   **Backend**: Flask, Peewee ORM, Gunicorn
*   **Frontend**: HTML, CSS, JavaScript, Jinja2, Leaflet.js
*   **Database**: MySQL (Production), SQLite (Testing)
*   **DevOps**: Docker, Docker Compose, Nginx, GitHub Actions

## Repository Structure

```
├── .github/workflows/    # GitHub Actions for CI/CD
├── app/                  # Main Flask application
│   ├── static/           # Static assets (CSS, images)
│   ├── templates/        # Jinja2 HTML templates
│   └── tests/            # Unit and integration tests
├── scripts/              # Helper scripts for testing and deployment
├── Dockerfile            # Docker image definition for the Flask app
├── docker-compose.yml    # Docker Compose for local development
└── docker-compose.prod.yml # Docker Compose for production
```

## Getting Started

### Prerequisites

*   Docker
*   Docker Compose

### Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ace-perez/ace-perez-portfolio.git
    cd ace-perez-portfolio
    ```

2.  **Create an environment file:**
    Create a `.env` file in the root directory and add the following variables. These are used by the local `docker-compose.yml` to set up the database.

    ```env
    # Database Configuration
    MYSQL_DATABASE=myportfolio_db
    MYSQL_USER=user
    MYSQL_PASSWORD=password
    MYSQL_ROOT_PASSWORD=root_password
    MYSQL_HOST=mysql
    ```

3.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

4.  **Access the application:**
    Open your web browser and navigate to `http://localhost:5001`.

## Testing

The project includes unit tests for the Flask application and database models, along with an end-to-end testing script for the API.

### Running Unit Tests

A GitHub Actions workflow automatically runs tests on every push and pull request to the `main` branch. To run the tests locally:

1.  Ensure you have the dependencies from `requirements.txt` installed.
2.  Run the test script:
    ```bash
    ./scripts/run_test.sh
    ```

### End-to-End API Testing

The `curl-test.sh` script performs an end-to-end test of the timeline API by creating, retrieving, and then deleting a post.

```bash
./scripts/curl-test.sh
```

## API Endpoints

The application exposes a REST API for managing timeline posts. While the frontend page (`/timeline`) is currently disabled in the application routes, the API endpoints are fully functional.

| Method   | Endpoint                      | Description                               |
| :------- | :---------------------------- | :---------------------------------------- |
| `POST`   | `/api/timeline_post`          | Creates a new timeline post.              |
| `GET`    | `/api/timeline_posts`         | Retrieves all timeline posts.             |
| `DELETE` | `/api/timeline_post/<post_id>`| Deletes a specific timeline post by its ID. |

#### `POST /api/timeline_post`

Creates a new timeline post.

*   **Form Data:**
    *   `name` (string, required): The author's name.
    *   `email` (string, required): The author's email (used for Gravatar).
    *   `content` (string, required): The content of the post.
*   **Success Response (200 OK):** A JSON object representing the created post.
*   **Error Response (400 Bad Request):** An error message if input is invalid.

## Deployment

Deployment is automated via a GitHub Actions workflow defined in `.github/workflows/deploy.yml`. On every push to the `main` branch, the workflow securely connects to a Virtual Private Server (VPS) via SSH and executes the `redeploy-site.sh` script.

The `redeploy-site.sh` script performs the following actions:
1.  Pulls the latest changes from the `main` branch.
2.  Shuts down the existing production containers using `docker-compose.prod.yml`.
3.  Rebuilds the application image and restarts all services in detached mode.

This process ensures a zero-downtime update of the live site. The production setup uses `docker-compose.prod.yml`, which includes an Nginx container configured to act as a reverse proxy and handle SSL termination with certificates from Let's Encrypt.
