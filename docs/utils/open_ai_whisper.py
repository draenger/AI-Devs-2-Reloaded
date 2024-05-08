import requests
import os
from openai import OpenAI
from utils.downloader import Downloader

class OpenAIWhisper:
    def __init__(self, mode_name = "whisper-1",):
        self.client = OpenAI()
        self.mode_name = mode_name
        self.downloader = Downloader()

    def transcribe_audio(self, audio_url):
        audio_file_name = downloader.download_file(audio_url)
        try:
            with open(audio_file_name, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcription.text
        finally:
            os.remove(audio_file_name)
