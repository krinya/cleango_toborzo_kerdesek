import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.custom_functions import *
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from PIL import Image
from datetime import datetime
import ssl
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context

def add_picture_to_streamlit(image_path, caption = None):
    image = Image.open(image_path)
    st.image(image, caption=caption)

    hide_img_fs = '''
        <style> 
            button[title="View fullscreen"]{
                visibility: hidden;}
        </style>
    '''

    st.markdown(hide_img_fs, unsafe_allow_html=True)

def send_email(recipient_address, subject, body):
    # create a message object
    msg = MIMEMultipart()
    msg['From'] = st.secrets['email']['smtp_username']
    msg['To'] = recipient_address
    msg['Subject'] = subject

    # add some text to the email body allow use html
    msg.attach(MIMEText(body, 'html'))
    #msg.attach(MIMEText(body, 'plain'))

    # create a SMTP client session
    smtp_server = 'smtp.eu.mailgun.org'
    smtp_port = 587
    smtp_username = st.secrets['email']['smtp_username']
    smtp_password = st.secrets['email']['smtp_password']
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)

def session_counter():
    # st.sesson counter intialization
    if 'session_counter' not in st.session_state:
        st.session_state.session_counter = 1
    st.session_state.session_counter = 1
    return st.session_state.session_counter

def create_toborzo_form():

    email_list_to_us = ["menyhert.kristof@cleango.hu"] #ez az email cimre fogja elkuldeni a rendeles adatait

    with st.form(key='toborzo_form'):

        # kerdesek_csv = pd.read_csv('data/moso_toborzas_kerdesek.csv')
        # st.dataframe(kerdesek_csv)

        col1, col2, col3 = st.columns([6, 1, 1])

        st.markdown('### Szemelyes adatok')
        name = st.text_input("Név", key='name')
        email_user = st.text_input("Email", key='email_user')
        phone_number = st.text_input("Telefonszám", key='phone_number')
        # create list with numbers from 1900 to 2020 and also incude blank option
        blank_list = ["Valassz szuletesi evet"]
        birth_year_list = blank_list + list(range(1900, 2021))
        birth_year = st.selectbox("Születési ev", key='birth_year', options=birth_year_list)
        
        st.markdown('### Kerdesek')
        lakhely_options = ["", "Budapest", "Pest megye", "Egyeb"]
        lakhely = st.radio("Hol laksz? Honnan jarnal be dolgozni?", key='lakhely', options = lakhely_options, horizontal=True)
        mellek_vagy_foallas = st.radio("Mellék, vagy főállásban dolgoznál nálunk?", key='mellek_vagy_foallas', options = ["", "Mellekallasban", "Foallasban"], horizontal=True)
        tapasztalat = st.radio("Van tapasztalatod autómosás, vagy autókozmetika területén? - nem kizáró ok ha nincs", key='tapasztalat', options = ["", "Igen", "Valamennyi van", "Nem"], horizontal=True)
        motor = st.radio("Rendelkezel kismotor/motor, vagy B kategóriás jogosítvánnyal?", key='motor', options = ["", "Igen", "Nem"], horizontal=True)
        robogo = st.radio("Rendelkezel tapasztalattal motorozás/robogózás terén? - nem kizáró ok ha nem", key='robogo', options = ["", "Igen", "Nem"], horizontal=True,)
        auto = st.radio("Rendelkezel saját autóval? - nem kizáró ok ha nem", key='auto', options = ["", "Igen", "Nem"], horizontal=True)

        submitted = st.form_submit_button("Jelentkezem", on_click=session_counter)

        col1, col2 = st.columns([2, 2])

        with col1:

            st.markdown("Nyomja meg a gombot, hogy a jelentkezését elküldje nekünk.")
            #st.markdown("Ha megnyomja a gombot, és nem lát semmilyen egyéb üzenetet, ez alatt a mondat alatt, akkor nyomja meg a gombot újra.")
        with col2:
            st.write("Ha valami kérdése van, kérjük keressen minket bizalommal a következő elérhetőségeken:")
            st.write("Email: info@cleango.hu")
            st.write("Telefon: +36 30 141 5100")

        if submitted:
            print("submitted")
        if 'session_counter' not in st.session_state:
            st.session_state.session_counter = 0
        if st.session_state.session_counter == 1:
            st.session_state.session_counter = 0
            with col1:
                # some checks
                error_counter = 0

                if name == "":
                    st.warning("Kerjuk adja meg a nevet.")
                    error_counter += 1
                if email_user == "" or "@" not in email_user:
                    st.warning("Kerjuk adja meg az email cimet.")
                    error_counter += 1
                if phone_number == "":
                    st.warning("Kerjuk adja meg a telefonszamat.")
                    error_counter += 1
                if birth_year == "Valassz szuletesi evet":
                    st.warning("Kerjuk valassza ki a szuletesi evet.")
                    error_counter += 1
                if lakhely == "":
                    st.warning("Kerjuk valassza ki a lakhelyet.")
                    error_counter += 1
                if mellek_vagy_foallas == "":
                    st.warning("Kerjuk valassza ki hogy mellek, vagy foallasban szeretne dolgozni.")
                    error_counter += 1
                if tapasztalat == "":
                    st.warning("Kerjuk valassza ki hogy van-e tapasztalata autómosás, vagy autókozmetika területén.")
                    error_counter += 1
                if motor == "":
                    st.warning("Kerjuk valassza ki hogy rendelkezik-e kismotor/motor, vagy B kategóriás jogosítvánnyal.")
                    error_counter += 1
                if robogo == "":
                    st.warning("Kerjuk valassza ki hogy rendelkezik-e tapasztalattal motorozás/robogózás terén.")
                    error_counter += 1
                if auto == "":
                    st.warning("Kerjuk valassza ki hogy rendelkezik-e saját autóval.")
                    error_counter += 1
                
                
                if error_counter == 0:

                    # evalauate the answers
                    # if year < 1970
                    kizaro_ok = "Nem"
                    if int(birth_year) < 1970:
                        kizaro_ok = "Igen"
                    if lakhely != "Budapest":
                        kizaro_ok = "Igen"
                    
                    
                    email_subject_to_us = "CleanGo - Moso toborzas"
                    email_body_to_us = 'Email szovege a cleangonak'
                    if kizaro_ok == "Igen":
                        email_subject_to_us = "CleanGo - Moso toborzas - Sajnaljuk"
                        email_body_to_us = 'Email szovege a cleangonak - Sajnaljuk'
                    if kizaro_ok == "Nem":
                        email_subject_to_user = "CleanGo - Gratulalunk"
                        email_body_to_user = 'Email szovege a usernek - Granulalunk'
                        
                    # send the email to CleanGo
                    for email_adress_to_us in email_list_to_us:
                        try:
                            send_email(email_adress_to_us, email_subject_to_us, email_body_to_us)
                            st.write("A jelentkezest a CleanGo megkapta. A jelentkezest a lehető leghamarabb feldolgozzuk, es visszajelzunk.")
                        except:
                            st.write("Hoppá valami hiba történt. A jelentezest a CleanGo nem kapta meg.")
                        
                    # send the email to the user
                    try:
                        send_email(email_user, email_subject_to_user, email_body_to_user)
                        st.write("A további teendőket az alábbi emailcímre küldtük el:")
                        st.write(" {}".format(email_user))
                        st.write("Kérjük ellenőrizd a spam mappát is!")
                    except:
                        st.write("Hoppá valami hiba történt. A további teendőket nem tudtuk elküldeni az alábbi emailcímre:")
                        st.write("{}".format(email_user))
