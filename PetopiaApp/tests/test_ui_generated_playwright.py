from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://petopia.pythonanywhere.com/")
    page.get_by_role("link", name="Login").click()
    page.get_by_label("Username").click()
    page.get_by_label("Username").fill("janedoe")
    page.get_by_label("Username").press("Tab")
    page.get_by_label("Password").fill("zaq1@WSX")
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("link", name="Hamster").click()
    page.get_by_text("Long Hamster Cage").click()
    page.get_by_role("link", name="Add to cart ").click()
    page.get_by_role("cell", name="Long Hamster Cage").click()
    page.get_by_role("link", name="Continue to checkout").click()
    page.get_by_role("heading", name="Checkout form").click()
    page.get_by_placeholder("1234 Main St").click()
    page.get_by_placeholder("1234 Main St").fill("1234 Main St")
    page.get_by_placeholder("Apartment or suite").click()
    page.get_by_placeholder("Apartment or suite").fill("10")
    page.locator("#id_country").select_option("MK")
    page.locator("#id_zip").click()
    page.locator("#id_zip").fill("1000")
    page.get_by_text("Stripe").click()
    page.get_by_role("button", name="Continue to payment").click()
    page.get_by_role("heading", name="Payment with stripe").click()
    page.get_by_placeholder("4242 4242 4242 4242").fill("4242424242424242")
    page.get_by_placeholder("12/25").click()
    page.get_by_placeholder("12/25").fill("12/25")
    page.get_by_placeholder("222").click()
    page.get_by_placeholder("222").fill("222")
    page.get_by_role("button", name="Pay").click()
    page.get_by_text("Your order was successful! ×").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
