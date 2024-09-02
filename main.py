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
    pathSave = "./images/minnaln/" + src[-2] + "/" + src[-1]

    if not os.path.isdir("./images/minnaln/" + src[-2]):
        os.makedirs("./images/minnaln/" + src[-2])
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


for i in range(1, 51):
    # Open a webpage
    driver.get(
        "https://www.vnjpclub.com/minna-no-nihongo/bai-" + str(i) + "-luyen-nghe.html"
    )

    question = driver.find_element(By.CLASS_NAME, "tab_container")
    questionHtml = "<body>" + question.get_attribute("outerHTML") + "</body>"
    questionHtml = questionHtml.replace(
        "/images/minnaln",
        "./images/minnaln",
    )

    questionHtml = questionHtml.replace(
        "/Audio/minnaln/",
        "./Audio/minnaln/",
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

    with open("choukai" + str(i) + ".html", "w", encoding="utf-8") as myFile:
        myFile.write(
            """
	<link rel="stylesheet" href="./choukai.css" type="text/css" />
	<script src="media/jui/js/jquery.min.js" type="text/javascript"></script>
	<script src="media/jui/js/jquery-noconflict.js" type="text/javascript"></script>
	<script src="media/jui/js/jquery-migrate.min.js" type="text/javascript"></script>
	<script type="text/javascript" src="choukai.js"></script>
	"""
        )
        myFile.write(
            """<div style="display: flex; gap: 10px; height: 50px;">
			<a href="./home.html">Home</a>
			<a href="./test-list.html">Kiểm tra từ vựng</a>
		</div>"""
        )
        myFile.write(questionHtml)

# Close the browser
driver.quit()
