# Website Automated Tests

This project contains a Python + Playwright automated browser test suite for `https://demo.xsa.claroty.com/`.

## What it covers

- Successful login flow
- Login page visual capture
- Empty form submission validation behavior
- Invalid password validation behavior
- HTML reporting
- Full-page screenshots for each test
- Failure screenshots captured automatically

## Project structure

- `tests/test_login.py`: login flow and validation tests
- `tests/conftest.py`: browser setup, environment loading, screenshots, reports
- `.env.example`: configuration template
- `artifacts/screenshots/`: screenshots created during runs
- `artifacts/reports/report.html`: generated test report

## Setup

1. Create a local environment file:

```bash
cp .env.example .env
```

2. Update `.env` with the real password.

3. Create and activate the virtual environment if needed:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the tests

```bash
.venv/bin/python -m pytest
```

## Run in Jenkins

Add two Jenkins secret text credentials before running the pipeline:

- `claroty-login-username`
- `claroty-login-password`

The pipeline uses the local Chrome binary at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, so the Jenkins agent should have Google Chrome installed at that path or you should update `BROWSER_EXECUTABLE_PATH` in [`Jenkinsfile`](/Users/doronnuni/Documents/Playground/Jenkinsfile).

## Configuration

Environment variables supported in `.env`:

- `BASE_URL`
- `LOGIN_USERNAME`
- `LOGIN_PASSWORD`
- `HEADLESS`
- `BROWSER_EXECUTABLE_PATH`

By default the suite uses the local macOS Chrome binary at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. If you want to use a different browser binary, update `BROWSER_EXECUTABLE_PATH`.

## Notes

- The site currently shows a generic invalid-credentials banner even when the login form is submitted empty. The validation test reflects that live behavior.
- Screenshots are saved on every test run so you can inspect the visual state without opening the site manually.
