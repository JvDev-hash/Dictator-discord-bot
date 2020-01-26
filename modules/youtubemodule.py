import requests
from bs4 import BeautifulSoup

def youtube_detect(content):

    foundedYTB = ""

    if "youtu" in content:
        foundedYTB = "Yes"
    else:
        foundedYTB = "No"

    print(foundedYTB)
    return foundedYTB

def youtube_webscrap(link):
    
    page = requests.get(link)

    soup = BeautifulSoup(page.text, 'html.parser')

    title = soup.find_all("span", id="eow-title")

    title2 = ""

    for titulo in title:
        title2 = titulo.get("title")

    print(title2)

    return title2