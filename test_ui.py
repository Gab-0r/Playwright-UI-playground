from playwright.sync_api import Page,  expect
from fixtures import *
import time

def dialog_handler(dialog):
    dialog.accept()


def test_dynamic_id(page: Page):
    dynamic_id_section = page.get_by_role("link", name="Dynamic ID")
    dynamic_id_section.click()
    button = page.get_by_role("button", name="Button with Dynamic ID")
    expect(button).to_be_visible()

def test_class_attribute(page: Page):
    page.on("dialog", dialog_handler)
    class_attribute_section = page.get_by_role("link", name="Class Attribute")
    class_attribute_section.click()
    button = page.locator('button.btn-primary')
    button.click()


