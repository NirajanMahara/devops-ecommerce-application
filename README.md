# E-commerce Web Application with CI/CD

A Flask-based e-commerce platform with automated CI/CD pipeline and AWS deployment.

## Live Demo
http://35.182.246.144

## Features

- User Authentication and Authorization
  - User registration and login
  - Admin dashboard
  - Role-based access control

- Product Management
  - Product catalog with search
  - Stock management
  - Category organization

- Shopping Cart
  - Add/remove items
  - Update quantities
  - Persistent cart storage

- Order Processing
  - Secure checkout
  - Order history
  - Order status tracking

- Admin Features
  - Sales dashboard
  - Order management
  - Product inventory
  - User management

## Technical Stack

- Backend: Flask 2.x
- Database: SQLAlchemy with SQLite
- Frontend: Bootstrap 5
- Testing: pytest
- CI/CD: GitHub Actions
- Deployment: AWS EC2, Nginx, Gunicorn
- OS: Amazon Linux 2

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/NirajanMahara/devops-ecommerce-application.git
cd devops-ecommerce-application
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

5. Run the application:
```bash
python run.py
```

## Testing

Run the test suite:
```bash
pytest
```

## AWS Deployment

The application is deployed on AWS EC2 with:
- Amazon Linux 2
- Python 3.9
- Nginx as reverse proxy
- Gunicorn as application server

### Required GitHub Secrets:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION (ca-central-1)
- EC2_SSH_KEY
- EC2_HOST
- EC2_USER (ec2-user)

### Deployment Process
1. Push to main branch
2. GitHub Actions runs tests
3. If tests pass, deploys to EC2
4. Sets up Python environment
5. Configures Nginx and Gunicorn
6. Starts the application

## Project Structure

```
ecommerce-app/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   ├── templates/      # HTML templates
│   └── static/         # Static files
├── deployment/         # Deployment configurations
├── tests/             # Test files
├── .github/           # GitHub Actions workflow
└── requirements.txt   # Python dependencies
```

## Default Admin Account

- Email: admin@ecommerce.com
- Password: Admin@123

## Monitoring and Maintenance

1. View application logs:
```bash
sudo journalctl -u ecommerce
```

2. Restart application:
```bash
sudo systemctl restart ecommerce
```

3. Check Nginx status:
```bash
sudo systemctl status nginx
```

## Security Features

- Password hashing with bcrypt
- CSRF protection
- Secure session handling
- Role-based access control
- Input validation and sanitization

## Authors

Nirajan Mahara
Santosh Khanal
Kshitij Chaudhary

## License

MIT License 
