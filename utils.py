import streamlit as st
from openai import OpenAI
#import openai
import datetime
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")


#openai.api_key = api_key

client = OpenAI(api_key=api_key)


def history_teller(city):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system",
                "content": (
                    "Sen, Türkiye'deki bir şehir hakkında detaylı bilgi veren bir yardımcı asistansın. Şehir hakkında şu bilgileri sağla:\n"
                    "- Tarihsel Hava Durumu: Geçmişte sıcaklık, yağış, nem gibi verilerdeki değişimler.\n"
                    "- İklim değişikliğinin etkileri: Tarih boyunca iklim değişikliklerinin bölgenin coğrafi ve kültürel yapısına olan etkileri.\n"
                    "- Modern iklim verileri: Şehrin günümüzdeki iklim durumu ve gelecekteki olası değişimler.\n"
                    "- Bölgesel iklim modelleri: Bölgedeki sıcaklık ve yağış değişimlerini simüle eden veriler.\n"
                    "- Çevresel değişimlerin doğal yapıya etkileri: Bitki örtüsü ve toprak üzerindeki etkiler.\n\n"
                    "- Önemli tarihi olaylar\n"
                    "Bilgileri başlıklar, bir müze rehberi gibi ve uygun yerlerde emoji kullanarak kısa ve dinlendirici bir şekilde sun. Markdown formatını kullan."
                )
            },
            {"role": "user", "content": f"{city} hakkında bilgi ver."},
        ]
    )
    history_of_location = response.choices[0].message.content
    return history_of_location

