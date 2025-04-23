# Next Gen Student Management System

A Django-based student management system with role-based access control.

## Development Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp env.template .env
   # Edit .env with your actual values
   # Never commit the .env file to version control
   ```
5. Run database migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run development server:
   ```bash
   python manage.py runserver
   ```

## Security Considerations

### Rate Limiting
The application implements rate limiting to protect against brute force attacks:
- Login attempts: 5 per minute
- Password reset attempts: 3 per hour
- Customizable via settings.py:
  ```python
  RATELIMIT_ENABLE = True
  LOGIN_RATELIMIT = '5/m'  # 5 attempts per minute
  PASSWORD_RESET_RATELIMIT = '3/h'  # 3 attempts per hour
  ```

### Production Deployment
- Set `DEBUG=False` in production
- Use HTTPS with valid certificates
- Set all security-related environment variables to `True`:
  ```
  CSRF_COOKIE_SECURE=True
  SESSION_COOKIE_SECURE=True 
  SECURE_SSL_REDIRECT=True
  ```
- Rotate `SECRET_KEY` regularly
- Use a dedicated database user with minimal privileges
- Keep dependencies updated

### Environment Variables
Never commit your `.env` file to version control. The following sensitive values must be configured:

- Database credentials
- Email service credentials  
- Django secret key
- All security-related settings

## Testing
Run tests with:
```bash
python manage.py test
```

## Contributing
Pull requests are welcome. Please follow the existing code style and include tests.
