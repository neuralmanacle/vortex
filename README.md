# FastAPI CRUD Assignment

## Overview
This application performs CRUD operations for **Items** and **User Clock-In Records** using FastAPI and MongoDB.

## Setup and Installation

### Prerequisites
- Python 3.7+
- MongoDB Atlas account or local MongoDB instance
- Git

### Installation Steps
1. **Clone the Repository**
    ```bash
    git clone https://github.com/your_username/fastapi-crud-assignment.git
    cd fastapi-crud-assignment
    ```

2. **Create and Activate Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**
    - Create a `.env` file in the project root.
    - Add your MongoDB URI:
        ```
        MONGO_URI=your_mongodb_connection_uri
        ```

5. **Run the Application**
    ```bash
    uvicorn main:app --reload
    ```

6. **Access Swagger UI**
    - Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view and interact with the API documentation.

## API Endpoints

### Items API
- **POST /items**: Create a new item.
- **GET /items/{id}**: Retrieve an item by ID.
- **GET /items/filter**: Filter items based on query parameters.
- **GET /items/aggregate/count-by-email**: Get count of items grouped by email.
- **DELETE /items/{id}**: Delete an item by ID.
- **PUT /items/{id}**: Update an item's details by ID.

### Clock-In Records API
- **POST /clock-in**: Create a new clock-in entry.
- **GET /clock-in/{id}**: Retrieve a clock-in record by ID.
- **GET /clock-in/filter**: Filter clock-in records based on query parameters.
- **DELETE /clock-in/{id}**: Delete a clock-in record by ID.
- **PUT /clock-in/{id}**: Update a clock-in record's details by ID.

## Hosted Application
Access the live API documentation [here](https://your-hosted-app-url/docs).

