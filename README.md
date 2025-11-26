# Crowdfund Console Django Project

This is a Django web application for a crowd-funding platform, implementing user authentication with email activation and project management (CRUD).

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the repository (if applicable)

```bash
# git clone https://github.com/Magdyowies/iti_django_final/
# cd crowdfund_console
```

### 2. Create a Python Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

-   **On Linux/macOS:**
    ```bash
    source .venv/bin/activate
    ```
-   **On Windows (Command Prompt):**
    ```bash
    .venv\Scripts\activate.bat
    ```
-   **On Windows (PowerShell):**
    ```bash
    .venv\Scripts\Activate.ps1
    ```

### 4. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 5. Environment Variables

Create a `.env` file in the project root directory (same level as `manage.py`) based on the `.env.example` file. This file will store your `SECRET_KEY` and `DEBUG` settings.

```bash
cp .env.example .env
```

Open the newly created `.env` file and replace the placeholder for `SECRET_KEY` with a strong, randomly generated key. You can generate one using Django:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Then add `SECRET_KEY=<your_generated_key_here>` to your `.env` file. `DEBUG=True` should be present for local development.

Example `.env` file:
```
SECRET_KEY=your_super_secret_key_here
DEBUG=True
```

### 6. Run Database Migrations

Apply the database migrations to create the necessary tables:

```bash
python manage.py migrate
```

### 7. Create a Superuser (Optional)

You can create an administrator account to access the Django admin panel:

```bash
python manage.py createsuperuser
```
Follow the prompts to set up your superuser account. Remember that the `USERNAME_FIELD` is email.

### 8. Create Sample Data (Optional, for Development)

Populate the database with some sample users and projects:

```bash
python manage.py create_sample_data
```

This command will create two active users (`user1@example.com`, `user2@example.com` with password `password123`) and a few sample projects.

### 9. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.

---

## Usage

### User Registration and Email Activation

1.  Navigate to `http://127.0.0.1:8000/users/register/` in your browser.
2.  Fill out the registration form.
3.  Upon submission, an activation email will be sent. Since the `EMAIL_BACKEND` is set to `console.EmailBackend` in development, **the activation link will be printed directly to your console where the `runserver` command is running.**
    Example console output for activation link:
    ```
    Content-Type: text/plain; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit
    Subject: Activate your account.
    From: webmaster@localhost
    To: test@example.com
    Date: Wed, 26 Nov 2025 10:00:00 -0000
    Message-ID: <...>

    Hi testuser,

    Please click on the link below to confirm your registration:

    http://127.0.0.1:8000/users/activate/MjA/b732d80d2432a10523b1/
    ```
4.  Copy the full activation link (e.g., `http://127.0.0.1:8000/users/activate/MjA/b732d80d2432a10523b1/`) and paste it into your browser to activate the account.
5.  Once activated, you can log in using your registered email and password.

### Login / Logout

-   **Login:** Navigate to `http://127.0.0.1:8000/users/login/`. Use your email and password.
-   **Logout:** Click the "Logout" button in the navigation bar.

### Project Management (CRUD)

-   **View All Projects:** Go to the home page `http://127.00.0.1:8000/`.
-   **View My Projects:** If logged in, click "My Projects" in the navigation bar.
-   **Create Project:** If logged in, click "Create Project" in the navigation bar.
-   **View Project Details:** Click on a project title from the list.
-   **Edit/Delete Project:** On the project detail page, if you are the owner, you will see "Edit" and "Delete" links.

### Search Projects by Date

On the home page (project list), use the date input field to filter projects that are active on the selected date.

---

## Testing

To run the unit tests:

```bash
python manage.py test
```

---

## Commands to test email activation and project CRUD (using `curl` or `httpie`)

**Assumptions:**
-   Server is running on `http://127.0.0.1:8000/`.
-   You have `httpie` installed (`pip install httpie`). If not, `curl` commands are also provided.

### 1. Register a User (and get activation link from console)

```bash
# Using httpie
http POST http://127.0.0.1:8000/users/register/ first_name='Test' last_name='User' email='cli_test@example.com' mobile_phone='01012345678' password='cli_password123' password2='cli_password123'

# Using curl
curl -X POST -d "first_name=Test&last_name=User&email=cli_test@example.com&mobile_phone=01012345678&password=cli_password123&password2=cli_password123" http://127.0.0.1:8000/users/register/
```
**ACTION REQUIRED:** After running this, look for the activation link in your terminal where `python manage.py runserver` is executing. Copy the link.

### 2. Activate User Account

```bash
# Assuming the activation link you copied from the console is:
# http://127.0.0.1:8000/users/activate/BASE64_UID/TOKEN/

# Using httpie (replace BASE64_UID and TOKEN)
http GET http://127.0.0.1:8000/users/activate/BASE64_UID/TOKEN/

# Using curl (replace BASE64_UID and TOKEN)
curl http://127.0.0.1:8000/users/activate/BASE64_UID/TOKEN/
```

### 3. Login a User

You need to capture the `csrftoken` from a GET request to the login page first.

```bash
# Using httpie
http --session=session.json GET http://127.0.0.1:8000/users/login/
# Look for 'csrftoken' in session.json or response headers

# Then login
http --session=session.json POST http://127.0.0.1:8000/users/login/ username='cli_test@example.com' password='cli_password123'
# The session.json will now contain the sessionid (auth cookie)

# Using curl (more complex to manage sessions/cookies)
# First, get CSRF token and cookies
CSRF_TOKEN=$(curl -s -c cookies.txt http://127.0.0.1:8000/users/login/ | grep -o 'name="csrfmiddlewaretoken" value="[^"]*"' | cut -d'"' -f4)

# Then login
curl -X POST -b cookies.txt -c cookies.txt -d "username=cli_test@example.com&password=cli_password123&csrfmiddlewaretoken=$CSRF_TOKEN" http://127.0.0.1:8000/users/login/
```

### 4. Create a Project (after login)

You need to be logged in and have the session cookie.

```bash
# Using httpie (session.json from previous login step)
http --session=session.json POST http://127.0.0.1:8000/projects/create/ title='CLI Project' details='Project created via CLI' target_amount:=2500 start_date='2025-11-26' end_date='2025-12-26'

# Using curl (more complex, requires manual handling of CSRF and session cookie)
# 1. Get CSRF token from project creation page while logged in
CSRF_TOKEN=$(curl -s -b cookies.txt http://127.0.0.1:8000/projects/create/ | grep -o 'name="csrfmiddlewaretoken" value="[^"]*"' | cut -d'"' -f4)

# 2. Post to create project
curl -X POST -b cookies.txt -c cookies.txt -d "title=CLI Project&details=Project created via CLI&target_amount=2500&start_date=2025-11-26&end_date=2025-12-26&csrfmiddlewaretoken=$CSRF_TOKEN" http://127.0.0.1:8000/projects/create/
```

### 5. Logout

```bash
# Using httpie
http --session=session.json POST http://127.0.0.1:8000/users/logout/

# Using curl (requires CSRF and session cookie)
# 1. Get CSRF token from a page while logged in (e.g., home page)
CSRF_TOKEN=$(curl -s -b cookies.txt http://127.0.0.1:8000/ | grep -o 'name="csrfmiddlewaretoken" value="[^"]*"' | cut -d'"' -f4)

# 2. Post to logout
curl -X POST -b cookies.txt -c cookies.txt -d "csrfmiddlewaretoken=$CSRF_TOKEN" http://127.0.0.1:8000/users/logout/
```
