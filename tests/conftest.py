from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright


ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = ROOT / "artifacts"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
FAILURES_DIR = SCREENSHOTS_DIR / "failures"
REPORTS_DIR = ARTIFACTS_DIR / "reports"
DEFAULT_BROWSER_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def _load_dotenv() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return

    for raw_line in env_file.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def pytest_configure(config: pytest.Config) -> None:
    for directory in (SCREENSHOTS_DIR, FAILURES_DIR, REPORTS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def settings() -> dict[str, str | bool]:
    return {
        "base_url": os.getenv("BASE_URL", "https://demo.xsa.claroty.com").rstrip("/"),
        "username": os.getenv("LOGIN_USERNAME", ""),
        "password": os.getenv("LOGIN_PASSWORD", ""),
        "headless": os.getenv("HEADLESS", "true").lower() != "false",
        "browser_executable_path": os.getenv("BROWSER_EXECUTABLE_PATH", DEFAULT_BROWSER_PATH),
    }


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: dict[str, str | bool]) -> Browser:
    executable_path = str(settings["browser_executable_path"])
    launch_options = {"headless": bool(settings["headless"])}

    if Path(executable_path).exists():
        launch_options["executable_path"] = executable_path

    browser = playwright_instance.chromium.launch(**launch_options)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(
        viewport={"width": 1440, "height": 1200},
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page


@pytest.fixture()
def authenticated_page(page: Page, settings: dict[str, str | bool]) -> Page:
    username = str(settings["username"])
    password = str(settings["password"])

    assert username, "LOGIN_USERNAME is required for authenticated tests"
    assert password, "LOGIN_PASSWORD is required for authenticated tests"

    page.goto(f"{settings['base_url']}/login", wait_until="domcontentloaded")
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    page.wait_for_url(str(settings["base_url"]) + "/")
    yield page


@pytest.fixture()
def screenshot_path(request: pytest.FixtureRequest) -> Callable[[str], Path]:
    test_name = request.node.name

    def _build(name: str) -> Path:
        filename = f"{test_name}__{name}.png"
        return SCREENSHOTS_DIR / filename

    return _build


@pytest.fixture()
def save_screenshot(page: Page, screenshot_path: Callable[[str], Path]) -> Callable[[str], Path]:
    def _save(name: str) -> Path:
        path = screenshot_path(name)
        page.screenshot(path=str(path), full_page=True)
        return path

    return _save


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def capture_failure_screenshot(request: pytest.FixtureRequest, page: Page):
    yield
    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        failure_file = FAILURES_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(failure_file), full_page=True)
