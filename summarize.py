from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


def getHtml(video_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=0,0")
    service = Service(chrome_options=chrome_options)
    browser=webdriver.Chrome(service=service)
    browser.get(video_url)
    html = browser.page_source
    browser.close()
    return html

def transcribe_video(video_url):
    html = getHtml(video_url)
    soup = BeautifulSoup(html, "html.parser")
    video = soup.find_all("source")[0].get("src")
    print(video)

def main():
    url = "https://hcpss.instructuremedia.com/embed/f7c70668-3ace-430c-946b-0d8be1034e6e"
    transcribe_video(url)

if (__name__ == "__main__"):
    main()