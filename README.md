# Url shortner

## Description

This project is a comprehensive web application that provides URL management and user management functionalities, along with a frontend interface built using Angular and styled with Bootstrap. The URL service allows users to shorten URLs and manage their shortened URLs. The user service provides authentication, user registration, and user management features. The frontend interface provides a user-friendly way to interact with the services and manage URLs and user accounts.

## Disclaimer

This project serves as a test project for learning REST API and microservices architecture. The microservice structure implemented in this project may not be optimal for a small-scale application. 

## Features

- **URL Service**:
  - Shorten long URLs into easy-to-share shortened URLs.
  - Manage shortened URLs, including creating, updating, and deleting them.

- **User Service**:
  - User authentication with login/logout functionality.
  - User registration with email verification.
  - User management, including profile updates and password changes.

- **Frontend Interface**:
  - User-friendly interface built with Angular framework.
  - Responsive design using Bootstrap for seamless viewing on various devices.
  - Intuitive navigation and interaction for managing URLs and user accounts.

## Technologies Used

- **Backend**:
  - Flask (Python) for the URL service and user service.
  - SQLAlchemy for database management.
  - Flask-Smorest for building RESTful APIs.
  - Marshmallow for object serialization/deserialization.
  - Flask-CORS for Cross-Origin Resource Sharing.
  
- **Frontend**:
  - Angular framework for building the frontend interface.
  - Bootstrap framework for styling and layout.
  - TypeScript for frontend scripting.
  
- **Database**:
  - SQLite for storing URL and user data.

## Installation and Setup

1. **URL Service**:
   - Install dependencies using `pip install -r requirements.txt`.
   - Configure environment variables and database connection.
   - Run the Flask application using `python app.py`.

2. **User Service**:
   - Install dependencies using `pip install -r requirements.txt`.
   - Configure environment variables and database connection.
   - Run the Flask application using `python app.py`.

3. **Frontend Interface**:
   - Install Angular CLI globally using `npm install -g @angular/cli`.
   - Install dependencies using `npm install`.
   - Configure API endpoints in the Angular environment configuration.
   - Run the Angular development server using `ng serve`.
