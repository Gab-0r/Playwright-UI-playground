from playwright.sync_api import Page,  expect
from fixtures import *


def test_dynamic_id(page: Page):
    dynamic_id_section = page.get_by_role("link", name="Dynamic ID")
    dynamic_id_section.click()
    button = page.get_by_role("button", name="Button with Dynamic ID")
    expect(button).to_be_visible()