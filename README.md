# Google OAuth Django REST API

This project implements a **backend-only Google OAuth 2.0 authentication system** using Django Rest Framework and PostgreSQL, designed with **Clean Architecture** and **Object-Oriented Programming** principles.

It enables OAuth login via Google, fetches access/refresh tokens, and generates an application-level auth token for use in secured API endpoints. All interactions are handled via **API-only routes** — no frontend involved.

---

## 🚀 API Endpoints

| Method | Route                                         | Description                                                |
|--------|-----------------------------------------------|------------------------------------------------------------|
| GET    | `/users/google_oauth_redirect/`              | Initiates Google OAuth 2.0 flow                            |
| GET    | `/users/google_oauth_callback/`              | Callback endpoint that handles the response and returns tokens |

---

## 🛠️ Tech Stack

- Python 3.10+
- Django 4.x
- Django Rest Framework
- PostgreSQL
- psycopg2-binary
- Clean Architecture + OOP

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/google_oauth_django_rest_api.git
cd google_oauth_django_rest_api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add the following:

```bash
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
DATABASE_URL=postgresql://__USER_NAME__:__PASSWORD__@localhost:5432/orderly_auth_db
APP_URL=http://127.0.0.1:8000
```

🔒 Replace placeholders with your actual credentials.

---

## 🧱 Database Setup

Ensure PostgreSQL is installed and running, and create the database:

```sql
CREATE DATABASE orderly_auth_db;
```

Then run the initial migrations:

```sql
python manage.py migrate
```

## 🧪 Running the Server

```bash
python manage.py runserver
```

## 🔐 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Create an OAuth 2.0 Client ID.
3. Set the Authorized redirect URIs as:

    ```bash
    http://localhost:8000
    http://localhost:8000/users/google_oauth_callback/
    ```

4. Copy the Client ID and Client Secret into your .env file.

---

## 🧪 Testing

1. Visit below url in browser:

    ```url
    http://localhost:8000/users/google_oauth_redirect/
    ```

    This redirects to Google login.

2. Google redirects to callback
    After login, Google redirects to:

    ```url
    http://localhost:8000/users/google_oauth_callback/?code=...&state=...
    ```

3. Response Example:

    ```json
    {
        "token_id": {
            "iss": "https://accounts.google.com",
            "azp": "123-abc.apps.googleusercontent.com",
            "aud": "123-abc.apps.googleusercontent.com",
            "sub": "123",
            "email": "user@gmail.com",
            "email_verified": true,
            "at_hash": "12c",
            "name": "Vivek Tripathi",
            "picture": "https://lh3.googleusercontent.com/a/abc123=s96-c",
            "given_name": "Vivek",
            "family_name": "Tripathi",
            "iat": 123,
            "exp": 456
        },
        "access_token": "ya29.adfs-asdf-asdf-sadf-Z-asdf",
        "refresh_token": "1//sadf-sdaf"
    }
    ```
