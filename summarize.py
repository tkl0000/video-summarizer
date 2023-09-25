from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib.request
import time
import whisper
import openai
from pytube import YouTube
import os

def get_key():
    with open("key.txt", "r") as r:
        return r.read()

def download_youtube_audio(youtube_url):
    try:
        yt = YouTube(youtube_url)
    except:
        print("Connection Error!")
    audio_stream = yt.streams.get_audio_only()
    filename = yt.title + ".mp4"
    audio_stream.download(output_path=os.getcwd())
    return filename

def download_canvas_audio(canvas_url):
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
    filename = (soup.find_all(attrs={"property" : "og:title"})[0].get("content")) + ".mp3"
    urllib.request.urlretrieve(video_url, filename)
    return filename

#returns file name
def download_audio(url):
    if ("youtube.com" in url):
        return download_youtube_audio(url)
    elif ("instructuremedia" in url):
        return download_canvas_audio(url)
    else:
        return "Invalid URL!"

def transcribe_audio(filename):
    model = whisper.load_model("medium.en")
    result = model.transcribe(filename)
    text = result["text"]
    segments = result["segments"]
    language = result["language"]
    return text

def summarize(text):
    openai_key = get_key()
    openai.api_key = openai_key
    prompt = "Convert this into notes optimal for studying: \n" + text
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    response_text = response['choices'][0]['message']['content']
    return response_text

#test url: "https://hcpss.instructuremedia.com/embed/f7c70668-3ace-430c-946b-0d8be1034e6e"
def main():
    start_time = time.time()
    url = input("Enter Video URL: ")
    audio_file = download_audio(url)
    text = transcribe_audio(audio_file)
    summarized_text = summarize(text)
    end_time = time.time()
    print(f'Elapsed: {end_time - start_time} s')
    print(summarized_text)

if (__name__ == "__main__"):
    main()