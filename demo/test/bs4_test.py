import re

from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
<a href="http://www.baodu.com" class="sister" id="link4">baidu</a>,
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, "html.parser")

# print(soup.prettify())
# print(soup.title)
# print(soup.title.string)
#
# print(soup.findAll("a"))
# print(soup.find_all("a"))
# print(soup.find(id="link1").string)
# print(soup.find(id="link1").get_text())
print(soup.find("p"))
# print(soup.find("p", {"class": "story"}).get_text())
# print(soup.find_all("a", href=re.compile(r"example")))
# for tag in soup.find_all(re.compile("a")):
    # print("tag_name = ", tag.name)
for tag in soup.find_all("a",class_="sister"):
    print(tag.get_text())