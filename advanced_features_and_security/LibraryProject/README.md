This is the initial setup for a Django-based web application named LibraryProject. It serves as the foundation for building scalable, database-driven systems—ideal for managing books, users, and other library-related features.
## Security Measures Implemented

- CSRF protection via {% csrf_token %} in all forms
- Secure cookie settings in production
- Content Security Policy headers via django-csp
- Input validation using Django forms
- ORM-based queries to prevent SQL injection