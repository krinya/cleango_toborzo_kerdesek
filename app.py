import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.custom_functions import *
from utils.contact_form import *
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#set streamlit page name
st.set_page_config(page_title='CleanGo - Moso Toborzas', page_icon='data/cleango-logo-small.png', layout='wide')

col1, col2 = st.columns([2, 8])
with col1:
    add_picture_to_streamlit('data/cleango-logo-small.png', caption = None)

# create a Streamlit app

st.title("Cleango - Moso Toborzas")
st.markdown("Leiras")

create_toborzo_form()
