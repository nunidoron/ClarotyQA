from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page, expect


LOGIN_ERROR = "Invalid username or password. Please contact your administrator."


def open_login(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/login", wait_until="domcontentloaded")
    expect(page).to_have_title("xDome Secure Access")
    expect(page.get_by_role("button", name="Login")).to_be_visible()


def fill_login_form(page: Page, username: str, password: str) -> None:
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)


def submit_login(page: Page) -> None:
    page.get_by_role("button", name="Login").click()


def assert_screenshot_created(path: Path) -> None:
    assert path.exists(), f"Expected screenshot at {path}"
    assert path.stat().st_size > 0, f"Expected screenshot {path} to be non-empty"


def test_login_page_visual_capture(
    page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    open_login(page, str(settings["base_url"]))

    expect(page.get_by_text("Access Manager | Headquarters")).to_be_visible()
    expect(page.get_by_text("Claroty Employee")).to_be_visible()

    screenshot = save_screenshot("login-page")
    assert_screenshot_created(screenshot)


def test_login_success_reaches_dashboard(
    page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    username = str(settings["username"])
    password = str(settings["password"])

    assert username, "LOGIN_USERNAME is required for the login success test"
    assert password, "LOGIN_PASSWORD is required for the login success test"

    open_login(page, str(settings["base_url"]))
    fill_login_form(page, username, password)
    submit_login(page)

    expect(page).to_have_url(str(settings["base_url"]) + "/")
    expect(page.get_by_text("ClarotySupportUser1")).to_be_visible()
    expect(page.get_by_text("Access Manager")).to_be_visible()
    expect(page.get_by_role("button", name="Disconnect All")).to_be_visible()
    expect(page.get_by_text("Pending Access Requests")).to_be_visible()

    screenshot = save_screenshot("dashboard")
    assert_screenshot_created(screenshot)


def test_login_empty_submit_shows_error_banner(
    page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    open_login(page, str(settings["base_url"]))
    submit_login(page)

    expect(page.get_by_text(LOGIN_ERROR)).to_be_visible()

    screenshot = save_screenshot("empty-submit-error")
    assert_screenshot_created(screenshot)


def test_login_invalid_password_shows_error_banner(
    page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    username = str(settings["username"])
    assert username, "LOGIN_USERNAME is required for the invalid password test"

    open_login(page, str(settings["base_url"]))
    fill_login_form(page, username, "definitely-not-the-right-password")
    submit_login(page)

    expect(page).to_have_url(str(settings["base_url"]) + "/login")
    expect(page.get_by_text(LOGIN_ERROR)).to_be_visible()

    screenshot = save_screenshot("invalid-password-error")
    assert_screenshot_created(screenshot)
