from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page, expect


def assert_screenshot_created(path: Path) -> None:
    assert path.exists(), f"Expected screenshot at {path}"
    assert path.stat().st_size > 0, f"Expected screenshot {path} to be non-empty"


def open_authenticated_path(page: Page, base_url: str, path: str) -> None:
    page.goto(f"{base_url}{path}", wait_until="domcontentloaded")


def test_dashboard_overview_shows_core_widgets(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page

    expect(page.get_by_text("Access Manager")).to_be_visible()
    expect(page.get_by_text("Web Access").first).to_be_visible()
    expect(page.get_by_text("Micro Tunnel").first).to_be_visible()
    expect(page.get_by_text("Pending Access Requests").first).to_be_visible()
    expect(page.get_by_role("button", name="Disconnect All")).to_be_visible()
    expect(page.get_by_text(str(settings["username"]))).to_be_visible()

    screenshot = save_screenshot("dashboard-overview")
    assert_screenshot_created(screenshot)


def test_primary_navigation_links_route_to_core_sections(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    base_url = str(settings["base_url"])

    page.get_by_role("link", name="Devices").click()
    expect(page).to_have_url(f"{base_url}/devices/overview/cards")

    page.get_by_role("link", name="Files").click()
    expect(page).to_have_url(f"{base_url}/files")

    page.get_by_role("link", name="User Management").click()
    expect(page).to_have_url(f"{base_url}/user-management")

    page.get_by_role("link", name="Settings").click()
    expect(page).to_have_url(f"{base_url}/settings/deployment")

    page.get_by_role("link", name="Home").click()
    expect(page).to_have_url(f"{base_url}/")

    screenshot = save_screenshot("primary-navigation")
    assert_screenshot_created(screenshot)


def test_devices_cards_view_lists_available_devices(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/devices/overview/cards")

    expect(page).to_have_url(str(settings["base_url"]) + "/devices/overview/cards")
    expect(page.get_by_role("link", name="Overview")).to_be_visible()
    expect(page.get_by_role("link", name="Cards")).to_be_visible()
    expect(page.get_by_text("Sort by:")).to_be_visible()
    expect(page.get_by_role("button", name="Add Device")).to_be_visible()
    expect(page.get_by_text("Connect").first).to_be_visible()
    expect(page.get_by_text("STATUS").first).to_be_visible()

    screenshot = save_screenshot("devices-cards")
    assert_screenshot_created(screenshot)


def test_devices_table_view_exposes_device_inventory(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/devices/overview/table")

    expect(page).to_have_url(str(settings["base_url"]) + "/devices/overview/table")
    expect(page.get_by_role("link", name="Overview")).to_be_visible()
    expect(page.get_by_role("button", name="Export")).to_be_visible()
    expect(page.get_by_role("button", name="Add Device")).to_be_visible()
    expect(page.get_by_text("ACCESS POINT")).to_be_visible()
    expect(page.get_by_text("DEVICE ID")).to_be_visible()
    expect(page.get_by_text("DEVICE NAME")).to_be_visible()

    screenshot = save_screenshot("devices-table")
    assert_screenshot_created(screenshot)


def test_files_page_exposes_upload_and_listing_controls(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/files")

    expect(page).to_have_url(str(settings["base_url"]) + "/files")
    expect(page.get_by_text("All Files")).to_be_visible()
    expect(page.get_by_role("button", name="Create Folder")).to_be_visible()
    expect(page.get_by_role("button", name="Upload File")).to_be_visible()
    expect(page.get_by_text("NAME").first).to_be_visible()
    expect(page.get_by_text("TYPE").first).to_be_visible()
    expect(page.get_by_text("OWNER").first).to_be_visible()
    expect(page.get_by_text("SCAN STATUS").first).to_be_visible()

    screenshot = save_screenshot("files-page")
    assert_screenshot_created(screenshot)


def test_user_management_users_view_exposes_admin_actions(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/user-management")

    expect(page).to_have_url(str(settings["base_url"]) + "/user-management")
    expect(page.get_by_text("User Management")).to_be_visible()
    expect(page.get_by_text("Users").first).to_be_visible()
    expect(page.get_by_role("button", name="Export")).to_be_visible()
    expect(page.get_by_role("button", name="Download Report")).to_be_visible()
    expect(page.get_by_role("button", name="Add User")).to_be_visible()
    expect(page.get_by_text("USERNAME").first).to_be_visible()
    expect(page.get_by_text("USER ROLE").first).to_be_visible()
    expect(page.get_by_text("STATUS").first).to_be_visible()

    screenshot = save_screenshot("user-management-users")
    assert_screenshot_created(screenshot)


def test_user_management_groups_view_exposes_group_inventory(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/user-management")
    page.locator('[data-testid="groups-panel-tab"]').click()

    expect(page.get_by_role("button", name="Add Group")).to_be_visible()
    expect(page.get_by_text("GROUP NAME")).to_be_visible()
    expect(page.get_by_text("GROUP TYPE")).to_be_visible()
    expect(page.get_by_text("LAST UPDATED")).to_be_visible()

    screenshot = save_screenshot("user-management-groups")
    assert_screenshot_created(screenshot)


def test_settings_deployment_page_lists_access_points(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/settings/deployment")

    expect(page).to_have_url(str(settings["base_url"]) + "/settings/deployment")
    expect(page.get_by_text("Settings / Deployment Management")).to_be_visible()
    expect(page.get_by_text("Access Points").first).to_be_visible()
    expect(page.get_by_role("button", name="Get Access Key")).to_be_visible()
    expect(page.get_by_text("Headquarters")).to_be_visible()
    expect(page.get_by_text("Chicago")).to_be_visible()

    screenshot = save_screenshot("settings-deployment")
    assert_screenshot_created(screenshot)


def test_settings_authentication_page_exposes_password_policy(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/settings/authentication")

    expect(page).to_have_url(str(settings["base_url"]) + "/settings/authentication")
    expect(page.get_by_text("Settings / Authentication Settings")).to_be_visible()
    expect(page.get_by_text("Password and Login Policy")).to_be_visible()
    expect(page.get_by_text("Password Complexity").first).to_be_visible()
    expect(page.get_by_role("button", name="Force Password Reset")).to_be_visible()
    expect(page.get_by_role("button", name="Save")).to_be_visible()

    screenshot = save_screenshot("settings-authentication")
    assert_screenshot_created(screenshot)


def test_settings_identity_providers_page_lists_configuration_options(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/settings/identity-providers")

    expect(page).to_have_url(str(settings["base_url"]) + "/settings/identity-providers")
    expect(page.get_by_text("Settings / Identity Providers")).to_be_visible()
    expect(page.get_by_text("Active Directory").first).to_be_visible()
    expect(page.get_by_text("SAML Authentication")).to_be_visible()
    expect(page.get_by_text("OIDC Authentication")).to_be_visible()
    expect(page.get_by_role("button", name="Add Domain")).to_be_visible()

    screenshot = save_screenshot("settings-identity-providers")
    assert_screenshot_created(screenshot)


def test_settings_login_page_exposes_notice_controls(
    authenticated_page: Page,
    settings: dict[str, str | bool],
    save_screenshot,
) -> None:
    page = authenticated_page
    open_authenticated_path(page, str(settings["base_url"]), "/settings/login-page")

    expect(page).to_have_url(str(settings["base_url"]) + "/settings/login-page")
    expect(page.get_by_text("Settings / Login Page Settings")).to_be_visible()
    expect(page.get_by_text("Login Page Message")).to_be_visible()
    expect(page.get_by_text("Enable custom admin notice")).to_be_visible()
    expect(page.get_by_role("button", name="Save")).to_be_visible()

    screenshot = save_screenshot("settings-login-page")
    assert_screenshot_created(screenshot)
