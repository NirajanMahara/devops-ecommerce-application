# E-commerce Web Application with CI/CD

A Flask-based e-commerce platform with automated CI/CD pipeline and AWS deployment.

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

- Backend: Flask
- Database: SQLAlchemy with SQLite
- Frontend: Bootstrap 5
- Testing: pytest
- CI/CD: GitHub Actions
- Deployment: AWS EC2, Nginx, Gunicorn

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-app
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

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
python run.py
```

## Testing

Run the test suite:
```bash
pytest
```

## AWS Deployment

1. Install AWS CLI and configure credentials:
```bash
aws configure
# Enter your AWS Access Key ID and Secret Access Key
```

2. Run AWS setup script:
```bash
chmod +x deployment/aws_setup.sh
./deployment/aws_setup.sh
```

3. Configure GitHub Secrets:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- EC2_SSH_KEY (contents of ecommerce-key.pem)
- EC2_HOST (EC2 instance public IP)
- EC2_USER (ubuntu)

4. Push to main branch to trigger deployment:
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

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

- Email: admin@example.com
- Password: admin123

## CI/CD Pipeline

The GitHub Actions workflow:
1. Runs tests on every push and pull request
2. Deploys to AWS EC2 on successful merge to main
3. Automatically sets up the production environment

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License

## Authors

[Your Name] and contributors

## Acknowledgments

- Flask documentation
- Bootstrap documentation
- AWS documentation 