from playwright.sync_api import Page,  expect, TimeoutError
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

def test_dynamic_table(page: Page):
    page.get_by_role("link", name="Dynamic Table").click()

    label = page.locator("p.bg-warning").inner_text()
    percentage = label.split()[-1]

    colum_headers = page.get_by_role("columnheader")
    cpu_column = None

    for index in range(colum_headers.count()):
        colum_header = colum_headers.nth(index)

        if colum_header.inner_text() == "CPU":
            cpu_column = index
            break

    assert cpu_column != None

    row_group = page.get_by_role("rowgroup").last
    chrome_row = row_group.get_by_role("row").filter(
        has_text="Chrome"
    )

    chrome_cpu = chrome_row.get_by_role("cell").nth(cpu_column)
    expect(chrome_cpu).to_have_text(percentage)

def test_verify_test(page: Page):
    page.get_by_role("link", name="Verify Text").click()

    text = page.locator("div.bg-primary").get_by_text("Welcome", exact=False)

    expect(text).to_have_text("Welcome UserName!")

def test_progress_bar(page: Page):
    page.get_by_role("link", name="Progress Bar").click()

    progress_bar = page.get_by_role("progressbar")

    start_btn = page.locator("button#startButton")
    stop_btn = page.locator("button#stopButton")

    start_btn.click()
    while True:
        progress = progress_bar.get_attribute("aria-valuenow")
        if(int(progress) >= 75):
            break
        else:
            print(f"value now is {progress}")

    stop_btn.click()
    page.screenshot(path="bar.jpg")
    assert int(progress) >= 75

def test_visibility(page: Page):
    page.get_by_role("link", name="Visibility").click()
    
    hide_btn = page.get_by_role("button", name="HIde")
    removed_btn = page.get_by_role("button", name="Removed")
    zero_btn = page.get_by_role("button", name="Zero Width")
    overlapped_btn = page.get_by_role("button", name="Overlapped")
    opacity_btn = page.get_by_role("button", name="Opacity 0")
    visibility_hide_btn = page.get_by_role("button", name="Visibility Hidden")
    display_none_btn = page.get_by_role("button", name="Display None")
    offscreen_btn = page.get_by_role("button", name="Offscreen")

    hide_btn.click()

    expect(removed_btn).to_be_hidden()
    expect(zero_btn).to_have_css("width", "0px")
    
    with pytest.raises(TimeoutError):
        overlapped_btn.click(timeout=2000)
                             
    expect(opacity_btn).to_have_css("opacity", "0")
    expect(visibility_hide_btn).to_be_hidden()
    expect(display_none_btn).to_be_hidden()
    expect(offscreen_btn).not_to_be_in_viewport()

def test_sample_app(page: Page):
    page.get_by_role("link", name="Sample App").click()
    user = "Will"
    psw = "pwd"
    
    user_field = page.get_by_placeholder("User Name")
    user_field.fill(user)

    password_field = page.get_by_placeholder("********")
    password_field.fill(psw)

    login_btn = page.get_by_role("button", name="Log In")
    login_btn.click()

    expected_msg = f"Welcome, {user}!"
    login_msg = page.locator("label#loginstatus")

    expect(login_msg).to_have_text(expected_msg)

