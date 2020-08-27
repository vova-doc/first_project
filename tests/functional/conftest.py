import pytest
from selenium import webdriver

import settings


@pytest.yield_fixture(scope="function", autouse=True)
def chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)

    try:
        yield browser
    finally:
        browser.close()
        browser.quit()


@pytest.yield_fixture(scope="function", autouse=True)
def style_css():
    path = settings.STATIC_DIR / "styles" / "style.css"
    with path.open("r") as src:
        yield src.read()


@pytest.yield_fixture(scope="function", autouse=True)
def images_jpg():
    path = settings.STATIC_DIR / "images" / "ima.jpg"
    with path.open("r") as src:
        yield src.read()