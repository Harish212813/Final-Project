import uuid

from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"


def login(page: Page):
    unique = uuid.uuid4().hex[:8]

    username = f"user_{unique}"
    email = f"user_{unique}@example.com"
    password = "Password123"

    page.goto(f"{BASE_URL}/register-page")

    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", password)
    page.fill("#confirm-password", password)

    page.click("button[type='submit']")

    expect(page.locator("#message")).to_have_text(
        "Registration successful."
    )

    page.goto(f"{BASE_URL}/login-page")

    page.fill("#email", email)
    page.fill("#password", password)

    page.click("button[type='submit']")

    page.wait_for_url(
        f"{BASE_URL}/calculations-page"
    )


def test_calculation_bread(page: Page):
    login(page)

    # Add
    page.fill("#number-a", "10")
    page.fill("#number-b", "5")
    page.select_option(
        "#calculation-type",
        "Add",
    )

    page.click("#submit-button")

    expect(
        page.locator(".calculation-item")
    ).to_contain_text("15")

    # Read
    page.locator(".view-button").click()

    expect(
        page.locator("#message")
    ).to_contain_text("15")

    # Edit
    page.locator(".edit-button").click()

    page.select_option(
        "#calculation-type",
        "Multiply",
    )

    page.click("#submit-button")

    expect(
        page.locator(".calculation-item")
    ).to_contain_text("50")

    # Delete
    page.on(
        "dialog",
        lambda dialog: dialog.accept(),
    )

    page.locator(".delete-button").click()

    expect(
        page.locator(".calculation-item")
    ).to_have_count(0)

    expect(
        page.locator("#calculation-list")
    ).to_contain_text(
        "No calculations found."
    )


def test_divide_by_zero_validation(page: Page):
    login(page)

    page.fill("#number-a", "10")
    page.fill("#number-b", "0")

    page.select_option(
        "#calculation-type",
        "Divide",
    )

    page.click("#submit-button")

    expect(
        page.locator("#message")
    ).to_have_text(
        "Cannot divide by zero."
    )


def test_redirect_without_token(page: Page):
    page.goto(
        f"{BASE_URL}/calculations-page"
    )

    expect(page).to_have_url(
        f"{BASE_URL}/login-page"
    )


def test_logout(page: Page):
    login(page)

    page.click("#logout-button")

    expect(page).to_have_url(
        f"{BASE_URL}/login-page"
    )