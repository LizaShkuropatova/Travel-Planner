# Travel Planner

Test assessment - [Link](https://develops.notion.site/Python-engineer-test-assessment-Travel-Planner-2ee0fe54b07b80a5851cf4e241045d15)

## Tech stack
- FastAPI
- SQLAlchemy (SQLite)
- Pydantic
- Requests
- Uvicorn

## Installation

1. Create and activate virtual environment
2. Install dependencies

`pip install -r requirements.txt`

Run locally: `uvicorn main:app --reload`

Server will start at: http://127.0.0.1:8000

## API Documentation

Swagger UI: http://127.0.0.1:8000/docs

## Example requests

Create a project with places

POST /projects

```
{
  "name": "Trip",
  "description": "Summer vacation",
  "start_date": "2026-06-06",
  "places": [
    { "external_id": "129883", "notes": "Place_1" },
    { "external_id": "129884", "notes": "Place_2" }
  ]
}
```

Add a place to an existing project

```
{
  "external_id": "129885",
  "notes": "I need to go there"
}
```

Update place

```
{
  "visited": true
}
```

