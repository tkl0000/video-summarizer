from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib.request
import time

def downloadVideo(video_url):
    filename = "video1.mp4"
    urllib.request.urlretrieve(video_url, filename)

def getHtml(canvas_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=0,0")
    service = Service(chrome_options=chrome_options)
    browser=webdriver.Chrome(service=service)
    browser.get(canvas_url)
    html = browser.page_source
    browser.close()
    return html

def transcribe_video(canvas_url):
    html = getHtml(canvas_url)
    soup = BeautifulSoup(html, "html.parser")
    video_url = soup.find_all("source")[0].get("src")
    

def main():
    url = "https://hcpss.instructuremedia.com/embed/f7c70668-3ace-430c-946b-0d8be1034e6e"
    transcribe_video(url)

if (__name__ == "__main__"):
    main()