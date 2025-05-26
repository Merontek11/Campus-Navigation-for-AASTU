# AASTU GO

AASTU GO is a campus navigation app for AASTU students, providing features to explore places (dorms, cafes, classrooms), events, and navigation routes using GraphHopper.

## Project Structure
- **Backend**: `campus_nav_backend` (Django)
- **Frontend**: `ustogo` (React Native with Expo)

## Features
- User authentication (register, login) with JWT.
- Explore places by category (dorm, cafe, classroom, etc.).
- Navigation between locations using GraphHopper.
- Event listings and gallery.

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- GraphHopper (for navigation)
- Expo CLI (for React Native)

## Setup Instructions

### Backend (Django)
1. Clone the repository:
git clone <repository-url>
cd campus_nav_backend</repository-url>

text

Copy
2. Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

text

Copy
3. Set up environment variables:
- Copy `.env.example` to `.env` and fill in the values (e.g., `SECRET_KEY`, database credentials).
4. Run migrations:
python manage.py makemigrations
python manage.py migrate

text

Copy
5. Create a superuser (for admin access):
python manage.py createsuperuser

text

Copy
6. Start the Django server:
python manage.py runserver

text

Copy

### Frontend (React Native)
1. Navigate to the frontend directory:
cd ustogo

text

Copy
2. Install dependencies:
npm install

text

Copy
3. Start the Expo development server:
npm start

text

Copy
- Open the app on an emulator, device, or browser via Expo Go.

### GraphHopper (Navigation)
1. Download GraphHopper (version 9.1 recommended).
2. Start the GraphHopper server:
java -jar graphhopper-web-9.1.jar server config.yml

text

Copy
- Ensure it’s running at `http://localhost:8989`.

## API Endpoints
- **Auth**:
- `POST /api/auth/register/` - Register a user
- `POST /api/auth/login/` - Login and get tokens
- **Places**:
- `GET /api/places/?category=<category>` - List places by category
- **Categories**:
- `GET /api/categories/` - List all categories
- **Navigation**:
- `GET /api/route/?start=<lat>,<lon>&end=<lat>,<lon>&vehicle=foot` - Get a route

## Database Setup
- Database: PostgreSQL
- Name: `campus_nav_db`
- Create the database:
psql -U postgres
CREATE DATABASE campus_nav_db;
\q

text

Copy

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m "Add YourFeature"`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
MIT License