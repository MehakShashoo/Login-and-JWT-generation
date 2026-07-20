A simple FastAPI authentication project that integrates with Supabase to authenticate users using email and password, verify hashed passwords with Argon2 (pwdlib), and generate secure JWT access tokens for successful logins.
## Run the Project

```bash
fastapi dev main.py
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

## Endpoint

**POST** `/auth/login`

Returns:

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```
