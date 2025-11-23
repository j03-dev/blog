# Project Overview

This project is a blog application built with a Python backend using the Oxapy web server. Oxapy is a high-performance HTTP library written in Rust. The application uses SQLAlchemy for database interaction with a libSQL-compatible database (like Turso) and Jinja2 for templating. The frontend appears to use htmx for some dynamic interactions.

The project is structured into a `core` directory containing the main application logic, a `static` directory for static assets, and a `templates` directory for Jinja2 templates.

## Building and Running

To run this project, you need to have Python and the dependencies installed.

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: A `requirements.txt` file is not present. You can generate one from `pyproject.toml` using a tool like `pip-tools`.*

2.  **Set up the database:**
    The project uses a libSQL-compatible database. You will need to set up a database and provide the connection details in the `settings.py` file.

3.  **Run the application:**
    ```bash
    python main.py
    ```
    The application will be available at `http://0.0.0.0:8000`.

## Development Conventions

*   **Routing:** Routes are defined in `core/routers.py` and are separated into public and secure routers.
*   **Views:** View functions are located in `core/views.py` and are responsible for handling requests and rendering templates.
*   **Services:** Business logic is encapsulated in `core/services.py`.
*   **Repositories:** Database interactions are handled by functions in `core/repositories.py` using SQLAlchemy.
*   **Models:** SQLAlchemy database models are defined in `core/models.py`.
*   **Templates:** Jinja2 templates are stored in the `templates` directory.
*   **Static Files:** Static files like CSS and JavaScript are served from the `static` directory.
