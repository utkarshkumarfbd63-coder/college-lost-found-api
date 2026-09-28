# College Lost & Found API

A small REST API for students to report campus items that are lost or found, update their details and status, and search reports by status or category. Reports are stored in a local SQLite database.

## Technologies

- Python
- FastAPI and Pydantic
- SQLModel
- SQLite
- Uvicorn

## Features

- Create, list, retrieve, update, and delete item reports
- Filter reports by status or category
- Validate required text fields and the allowed status values
- Automatically create the SQLite table at application startup
- Interactive API documentation with Swagger UI

## Project Structure

```text
college-lost-found-api/
|-- database.py
|-- main.py
|-- models.py
|-- requirements.txt
|-- README.md
|-- .gitignore
`-- screenshots/
```

## Installation

Open a terminal in the project directory and create a virtual environment:

```powershell
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Application

```powershell
uvicorn main:app --reload
```

The API runs at <http://127.0.0.1:8000>. Swagger UI is available at <http://127.0.0.1:8000/docs> and ReDoc at <http://127.0.0.1:8000/redoc>.

The root endpoint (`GET /`) returns a message confirming that the API is running.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/items` | Create an item report (`201 Created`) |
| `GET` | `/items` | List all item reports |
| `GET` | `/items/{item_id}` | Get one report by ID |
| `PUT` | `/items/{item_id}` | Update one or more supplied fields |
| `DELETE` | `/items/{item_id}` | Delete a report |
| `GET` | `/items/status/{status}` | List reports by status |
| `GET` | `/items/category/{category}` | List reports by category |

### Valid Status Values

Status is case-sensitive and must be one of `Lost`, `Found`, or `Returned`. For example, use `GET /items/status/Lost`.

### Example Request

```json
{
  "title": "Black Wallet",
  "description": "Black leather wallet containing college ID card",
  "category": "Accessories",
  "location": "Central Library",
  "reported_by": "Rahul Sharma",
  "status": "Lost"
}
```

## Database

The application uses SQLModel with SQLite and `create_engine()`. On startup, the FastAPI lifespan creates the `item` table if it does not exist. The database file is `lost_found.db` in the working directory and is excluded from Git so local reports are not submitted.

## Validation and Error Handling

- Required text fields cannot be empty or whitespace-only; surrounding whitespace is trimmed.
- Descriptions must contain at least three characters after trimming.
- Status accepts only `Lost`, `Found`, or `Returned`.
- Invalid request data returns FastAPI's `422 Unprocessable Entity` response.
- Requests for missing item IDs return `404 Not Found` with `{"detail": "Item not found"}`.

## API Testing

Use Swagger UI at <http://127.0.0.1:8000/docs> to try each operation, or send HTTP requests with a local API client. Create a few reports first to demonstrate listing, status filtering, and category filtering. The sample requests in the assessment can be entered through Swagger; they are not preloaded by the application.

## Screenshots / Proof

The following screenshots were captured from the running Swagger UI and show the submitted request (when applicable), HTTP status, and response body:

- [01_post_item.png](screenshots/01_post_item.png) - successful `POST /items` (`201 Created`)
- [02_get_items.png](screenshots/02_get_items.png) - `GET /items` with the four sample reports
- [03_get_item.png](screenshots/03_get_item.png) - successful `GET /items/{item_id}`
- [04_put_item.png](screenshots/04_put_item.png) - successful partial `PUT /items/{item_id}`
- [05_delete_item.png](screenshots/05_delete_item.png) - successful `DELETE /items/{item_id}`
- [06_status_filter.png](screenshots/06_status_filter.png) - `GET /items/status/Lost`
- [07_category_filter.png](screenshots/07_category_filter.png) - `GET /items/category/Accessories`
- [08_validation_error.png](screenshots/08_validation_error.png) - invalid `POST /items` (`422 Unprocessable Entity`)