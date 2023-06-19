import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.custom_functions import *
from utils.contact_form import *
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#set streamlit page name
st.set_page_config(page_title='CleanGo - Mosó Jelentkezés"', page_icon='data/cleango-logo-small.png', layout='centered')

col1, col2 = st.columns([2, 8])
with col1:
    add_picture_to_streamlit('data/cleango-logo-small.png', caption = None)

# create a Streamlit app

st.title("CleanGo - Mosó Jelentkezés")
st.markdown(f"""Szia! \n\n Ha autómosónak szeretnél jelentkezeni a CleanGo-ba, akkor jó helyen jársz.\n\nTöltsd ki az alábbi űrlapot, és mi hamarosan felveszünk veled kapcsolatot.\n\nKöszönjük, hogy jelentkezel, reméljük hamarosan találkozunk!""")
st.markdown(f"""Ha elakadtál vagy kérdésed van, kérjük keressen minket bizalommal az info@cleango.hu email címen.""")

create_toborzo_form()
