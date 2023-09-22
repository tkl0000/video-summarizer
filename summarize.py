from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib.request
import time
import whisper

def download_audio(canvas_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=0,0")
    service = Service(chrome_options=chrome_options)
    browser=webdriver.Chrome(service=service)
    browser.get(canvas_url)
    html = browser.page_source
    browser.close()
    soup = BeautifulSoup(html, "html.parser")
    video_url = soup.find_all("source")[0].get("src")
    filename = "video1.mp3"
    urllib.request.urlretrieve(video_url, filename)

def transcribe_audio():
    model = whisper.load_model("medium.en")
    result = model.transcribe("cigs.mp3")
    print(result["text"])

def main():
    url = "https://hcpss.instructuremedia.com/embed/f7c70668-3ace-430c-946b-0d8be1034e6e"
    # download_video(url)
    transcribe_audio()

if (__name__ == "__main__"):
    main()