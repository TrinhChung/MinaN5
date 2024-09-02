from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from urllib.request import Request, urlopen

# Initialize the WebDriver
driver = webdriver.Chrome()

head = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
    "refere": "https://example.com",
    "cookie": """your cookie value ( you can get that from your web page) """,
}


def get_page_content(url, head):
    req = Request(url, headers=head)
    return urlopen(req).read()


def downloadImg(url, head):
    src = url.split("/")
    pathSaveFolder = "./" + "/".join(src[3:-1])
    pathSave = "./" + "/".join(src[3:])

    if not os.path.isdir(pathSaveFolder):
        os.makedirs(pathSaveFolder)
    with open(pathSave, "wb") as out_file:
        out_file.write(get_page_content(url, head))


def downloadAudio(url, head):
    src = url.split("/")
    pathSaveFolder = "./" + "/".join(src[3:-1])
    pathSave = "./" + "/".join(src[3:])
    if not os.path.isdir(pathSaveFolder):
        os.makedirs(pathSaveFolder)
    with open(pathSave, "wb") as out_file:
        out_file.write(get_page_content(url, head))


for i in range(1, 5):
    # Open a webpage
    driver.get(
        "https://www.vnjpclub.com/tanki-master-n5/choukai-mondai-" + str(i) + ".html"
    )

    driver.execute_script(
        """
    var elements = document.querySelectorAll("#tracnghiemdiv script");
    elements.forEach(function(element) {
       if (element)
            element.parentNode.removeChild(element);
    });
    """
    )

    styleCss = driver.find_element(
        By.XPATH, "//div[@id='tracnghiemdiv']/preceding-sibling::*[1]"
    )
    styleCssHtml = styleCss.get_attribute("outerHTML")

    question = driver.find_element(By.ID, "tracnghiemdiv")
    questionHtml = question.get_attribute("outerHTML")
    script = driver.find_element(
        By.XPATH, "//div[@id='tracnghiemdiv']/following-sibling::script"
    )
    scriptHtml = script.get_attribute("outerHTML")
    scriptHtml = scriptHtml.replace(
        '<img id="img_wrong" style="vertical-align:baseline" src="/jls/assets/img/favicons/wrong.png">',
        '<i style="color: red; display: inline-block;">&#10008;</i>',
    )
    scriptHtml = scriptHtml.replace(
        '<img id="img_correct" style="vertical-align:baseline" src="/jls/assets/img/favicons/correct.png">',
        '<i style="color: green; display: inline-block;">&#10004;</i>',
    )

    imgs = question.find_elements(By.TAG_NAME, "img")
    for img in imgs:
        url = img.get_attribute("src")
        # download the image
        # downloadImg(url, head)
        break

    audios = question.find_elements(By.XPATH, "//audio/source")
    for audio in audios:
        # downloadAudio(audio.get_attribute("src"), head)
        break

    questionHtml = questionHtml.replace(
        "http://www.vnjpclub.com/images/tankimastern5/",
        "./images/tankimastern5/",
    )

    questionHtml = questionHtml.replace(
        "/Audio/tankimastern5",
        "./Audio/tankimastern5",
    )

    with open("tanki-choukai" + str(i) + ".html", "w", encoding="utf-8") as myFile:
        myFile.write(
            """
<link rel="stylesheet" href="./test.css" type="text/css" />
<script src="http://code.jquery.com/jquery-1.10.2.js"></script>
<script src="http://code.jquery.com/ui/1.11.2/jquery-ui.js"></script>
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
<script type="text/javascript" src="choukai.js"></script>
"""
        )
        myFile.write(styleCssHtml)
        myFile.write(
            """<div style="display: flex; gap: 10px; height: 50px;">
			<a href="./home.html">Home</a>
			<a href="./test-list.html">Kiểm tra từ vựng</a>
		</div>"""
        )
        myFile.write(questionHtml)

# Close the browser
driver.quit()
