from playwright.sync_api import Page
import pytest

URL = "https://uitestingplayground.com/"

@pytest.fixture(autouse=True, scope="function")
def playwright_page(page: Page):
    page.goto(URL)
    yield
    page.close()
