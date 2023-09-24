import logging
import pytest
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)
log_file_path = 'PetopiaApp/tests/logs.txt'
file_handler = logging.FileHandler(log_file_path, mode='a')

logger.setLevel(logging.INFO)
logger.propagate = False

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(log_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    return browser.new_page()


def login(page, username, password):
    try:
        page.goto("http://petopia.pythonanywhere.com/")
        page.click("a:has-text('Login')")
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        assert page.is_visible('main > div.container')
        logger.info("Logged in as %s", username)
    except Exception as e:
        logger.error("Login Test failed: %s", str(e))


def navigate_to_product(page, product_url):
    try:
        page.goto(product_url)
        logger.info("Navigated to product page: %s", product_url)
    except Exception as e:
        logger.error("Navigate to product Test failed %s", str(e))


def add_product_to_cart(page):
    try:
        page.click("a:has-text('Add to cart')")
        assert "Your Shopping Cart" in page.locator('h2').text_content()
        logger.info("Added product to the cart")
    except Exception as e:
        logger.error("Add product to card Test failed %s", str(e))


def checkout_and_pay(page, street_address, country, zip_code, payment_option, card_number, expiration, cvc):
    try:
        page.click("a:has-text('Continue to checkout')")
        assert "Checkout form" in page.locator('h2').text_content()

        page.fill("input[name='street_address']", street_address)
        page.select_option("select[name='country']", country)
        page.fill("input[name='zip']", zip_code)
        page.evaluate('''(selector) => {
            const radioBtn = document.querySelector(selector);
            if (radioBtn) {
                radioBtn.checked = true;
                radioBtn.click();
            }
        }''', f"input[name='payment_option'][value='{payment_option}']")

        page.click("button:has-text('Continue to payment')")
        assert "Payment with stripe" in page.locator('h2').text_content()

        page.fill("input[id='card-number']", card_number)
        page.fill("input[id='expiration']", expiration)
        page.fill("input[id='cvc']", cvc)

        page.click("button:has-text('Pay')")
        assert "Your order was successful!" in page.locator('div.alert').text_content()
        logger.info("Payment successful")
    except Exception as e:
        logger.error("Checkout and Pay Test failed %s", str(e))


def test_test_complete(page, username, password, product_url, street_address, country, zip_code, payment_option,
                       card_number,
                       expiration, cvc):
    try:
        logger.info("Test started")
        login(page, username, password)
        navigate_to_product(page, product_url)
        add_product_to_cart(page)
        checkout_and_pay(page, street_address, country, zip_code, payment_option, card_number, expiration, cvc)
        logger.info("Completed payment successfully")
    except Exception as e:
        logger.error("Complete payment Test failed: %s", str(e))


if __name__ == "__main__":
    pytest.main()


@pytest.fixture
def username():
    return 'johndoe'


@pytest.fixture
def password():
    return 'zaq1@WSX'


@pytest.fixture
def product_url():
    return 'http://petopia.pythonanywhere.com/product/dog/adult-rottweiler-1'


@pytest.fixture
def street_address():
    return '1234 Main St'


@pytest.fixture
def country():
    return 'North Macedonia'


@pytest.fixture
def zip_code():
    return '1000'


@pytest.fixture
def payment_option():
    return 'S'


@pytest.fixture
def card_number():
    return '4242 4242 4242 4242'


@pytest.fixture
def expiration():
    return '12/25'


@pytest.fixture
def cvc():
    return '222'
