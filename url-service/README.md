# URL Management Service

The URL Management Service is a RESTful API that allows users to manage shortened URLs. It provides functionality for creating, retrieving, updating, and deleting shortened URLs.

## Technologies Used

- **Python**: Programming language used for backend development.
- **Flask**: Web framework used for building the RESTful API.
- **Flask-Smorest**: Extension for building RESTful APIs with Flask.
- **SQLAlchemy**: ORM (Object-Relational Mapping) library for interacting with the database.
- **Marshmallow**: Library for object serialization and deserialization.
- **SQLite**: Lightweight relational database used for storing URL data.

## Installation

1. Clone the repository:

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Configure the environment variables, database connection, and any other settings as needed.

4. Run the application:

    ```
    python app.py
    ```

## API Endpoints

- **GET /**: Retrieve a list of all shortened URLs.
- **POST /**: Create a new shortened URL.
- **GET /{url_key}**: Retrieve information about a specific shortened URL.
- **PUT /{url_key}**: Update an existing shortened URL.
- **DELETE /{url_key}**: Delete a shortened URL.
