# 🌆 City & Temperature Management API

## 📌 How to Run the Project

1. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Run migrations**
```bash
alembic upgrade head
```
4**Run migrations**
```bash
uvicorn main:app --reload
```
## 🗺️ API Endpoints

### Cities

| Method | Endpoint       | Description         |
|--------|----------------|-------------------|
| GET    | /city/         | Get all cities     |
| GET    | /city/{id}     | Get a single city by ID |
| PATCH  | /city/{id}     | Update a city by ID |

### Temperatures

| Method | Endpoint                  | Description                               |
|--------|---------------------------|-------------------------------------------|
| GET    | /temperatures             | Get all temperature records               |
| GET    | /temperatures?city_id=    | Get temperature records for a specific city |
| POST   | /temperatures/update      | Fetch and store temperature for all cities |
