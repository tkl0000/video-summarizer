from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib.request
import time
import whisper
import openai

def get_key():
    with open("key.txt", "r") as r:
        return r.read()

#returns file name
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
    filename = (soup.find_all({"property" : "og:title"})[0].get("content")) + ".mp3"
    urllib.request.urlretrieve(video_url, filename)
    return filename

def transcribe_audio(filename):
    model = whisper.load_model("medium.en")
    result = model.transcribe(filename)
    text = result["text"]
    segments = result["segments"]
    language = result["language"]
    return text

def summarize(text):
    openai_key = get_key()

    return text

def main():
    url = "https://hcpss.instructuremedia.com/embed/f7c70668-3ace-430c-946b-0d8be1034e6e"
    audio_file = download_audio(url)
    text = transcribe_audio("cigs.mp3")
    summarized_text = summarize(text)
    print(summarized_text)

if (__name__ == "__main__"):
    main()