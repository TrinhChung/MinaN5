from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the WebDriver
driver = webdriver.Chrome()

for i in range(1, 51):
    # Open a webpage
    driver.get(
        "https://www.vnjpclub.com/minna-no-nihongo/bai-" + str(i) + "-kiem-tra.html"
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
    questionHtml = question.get_attribute("innerHTML")
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

    scriptHtml = scriptHtml.replace(
        "$(function () { $(",
        "jQuery(function () { jQuery(",
    )

    with open("test" + str(i) + ".html", "w", encoding="utf-8") as myFile:
        myFile.write(
            """
<link rel="stylesheet" href="./test.css" type="text/css" />
<script src="media/jui/js/jquery.min.js" type="text/javascript"></script>
<script src="media/jui/js/jquery-noconflict.js" type="text/javascript"></script>
<script src="media/jui/js/jquery-migrate.min.js" type="text/javascript"></script></script>"""
        )
        myFile.write(
            """<div style="display: flex; gap: 10px;">
			<a href="./home.html">Home</a>
			<a href="./choukai-list.html">Nghe</a>
		</div>"""
        )
        myFile.write(styleCssHtml)
        myFile.write('<div id="tracnghiemdiv">' + questionHtml + "</div>")
        myFile.write('<script type="text/javascript">var question_count=30;</script>')
        myFile.write(scriptHtml)

# Close the browser
driver.quit()
