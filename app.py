import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from utils import history_teller
# Load environment variables from .env file
load_dotenv(override=True)

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")


# Load environment variables from .env file

client = OpenAI(api_key=api_key)

# Set page configuration
st.set_page_config(page_title="Türkiye'yi Keşfet", page_icon="🌍", layout="centered")

# Display a banner image (ensure 'turkey_banner.jpg' is in your directory)
#st.image('turkey_banner.jpg', use_column_width=True)

# Title
st.title("Bulunduğunuz Şehrin Tarihini Keşfedin🌟")


# List of cities in Turkey
cities = [
    "Istanbul", "Ankara", "Izmir", "Antalya", "Bursa",
    "Adana", "Konya", "Gaziantep", "Kayseri", "Mersin",
    "Diyarbakır", "Erzurum", "Eskişehir", "Samsun", "Trabzon"
]

# Markdown with list of cities
st.markdown("## Bulunduğunuz Şehri Seçiniz:")
#st.markdown(", ".join(cities))

# Dropdown to select a city
selected_city = st.selectbox("Şehirler:", options=["Seç"] + cities)

# Check if a valid city is selected
if selected_city != "Seç":
    # Call the history_teller function with a loading spinner
    with st.spinner(f"{selected_city} için Geçmişin İzleri Toplanıyor ..."):
        output = history_teller(selected_city)
    
    # Display the output
    st.markdown("### Şehirler İlgili Bilgiler:")
    st.markdown(output, unsafe_allow_html=True)
else:
    st.info("Lütfen Bir Şehir Seçiniz.")

# Footer
st.markdown("---")
