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


def test_hidden_layer(page: Page):
    page.get_by_role("link", name="Hidden Layers").click()
    green_btn = page.locator("button#greenButton")
    green_btn.click()

    with pytest.raises(TimeoutError):
        green_btn.click(timeout=2000)

def test_load_delays(page: Page):
    load_link = page.get_by_role("link", name="Load Delay")
    load_link.click()

    button = page.get_by_role("button", name="Button Appearing After Delay")
    button.wait_for(timeout=10_000)
    expect(button).to_be_visible()

def test_ajax_data(page: Page):
    ajax_button = page.get_by_role("link", name="AJAX Data")
    ajax_button.hover()
    ajax_button.click()
    button = page.locator("button#ajaxButton")
    button.click()
    content = page.locator("p.bg-success")
    content.wait_for(timeout=20_000)
    expect(content).to_be_visible()

def test_click_action(page: Page):
    click_btn = page.get_by_role('link', name="Click")
    click_btn.hover()
    click_btn.click()

    btn = page.locator('button#badButton')
    btn.click()

    expect(btn).to_have_class("btn btn-success")

def test_text_input(page: Page):
    section_btn = page.get_by_role("link", name="Text Input")
    section_btn.hover()
    section_btn.click()

    text = "This is an input test"

    input_field = page.get_by_label("Set New Button Name")
    input_field.fill(text)

    btn = page.locator("button.btn-primary")
    btn.click()

    expect(btn).to_have_text(text)

def test_scrollbars(page: Page):
    section_btn = page.get_by_role('link', name="Scrollbars")
    section_btn.hover()
    section_btn.click()

    btn = page.get_by_role("button", name="Hiding Button")

    btn.scroll_into_view_if_needed()
    page.screenshot(path='test-scrollbars.jpg')