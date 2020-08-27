import pytest

url = "http://localhost:8000"


@pytest.mark.functional
def test_html(chrome):
    chrome.get(f"{url}/")
    assert "Avengers" in chrome.title
    assert "Progress" in chrome.page_source
    assert "/s/style.css" in chrome.page_source
    assert "/i/ima.jpg" in chrome.page_source
    assert (
        """<progress id="progress" value="9" max="26">34%</progress>"""
        in chrome.page_source
    )


@pytest.mark.functional
def test_images_jpg(chrome):
    chrome.get(f"{url}/i/ima.jpg")
    assert "jpg" in chrome.page_source
    assert "Avengers" in chrome.page_source


@pytest.mark.functional
def test_style_css(chrome, main_css):
    chrome.get(f"{url}/s/style.css")
    assert main_css in chrome.page_source