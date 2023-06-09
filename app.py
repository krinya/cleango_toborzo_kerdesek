import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.custom_functions import *
from utils.contact_form import *
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#set streamlit page name
st.set_page_config(page_title='CleanGo - Moso Jelentkezés', page_icon='data/cleango-logo-small.png', layout='centered')

col1, col2 = st.columns([2, 8])
with col1:
    add_picture_to_streamlit('data/cleango-logo-small.png', caption = None)

# create a Streamlit app

st.title("Cleango - Moso Jelentkezés")
st.markdown("Leíras: ")
st.markdown("Ide kene par sort irni hogy mi is ez a moso jelentkezes")

create_toborzo_form()
