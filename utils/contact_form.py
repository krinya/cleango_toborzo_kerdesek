import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.custom_functions import *
from utils.sql_functions import *
from PIL import Image
from datetime import datetime
import ssl
import pandas as pd
import pymysql

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

    email_list_to_us = ["menyhert.kristof@gmail.com"] #ez az email cimre fogja elkuldeni a rendeles adatait

    with st.form(key='toborzo_form'):

        # kerdesek_csv = pd.read_csv('data/moso_toborzas_kerdesek.csv')
        # st.dataframe(kerdesek_csv)

        col1, col2, col3 = st.columns([6, 1, 1])

        st.markdown('### Személyes adatok')
        name = st.text_input("Név", key='name')
        email_user = st.text_input("Email cimed", key='email_user')
        phone_number = st.text_input("Telefonszámod", key='phone_number')
        default_szuletesi_ev = "Válassz ki hogy melyik évben születtél"
        birth_year = st.selectbox("Születési éved", key='birth_year', options=[default_szuletesi_ev] + list(range(1900, 2021)))
        
        st.markdown('### Kérdések')
        blank_valasztas = "Kérjük válassz:"
        horizontal = True

        lakhely = st.radio("Hol laksz? (Honnan járnál be dolgozni?)", key='lakhely', options = [blank_valasztas, "Budapest", "Pest megyei település", "Egyéb"], horizontal=horizontal)
        mellek_vagy_foallas = st.radio("Mellék, vagy főállásban dolgoznál nálunk?", key='mellek_vagy_foallas', options = [blank_valasztas, "Mellékallasban", "Főállásban"], horizontal=horizontal)
        van_auto = st.radio("Rendelkezel saját autóval?", key='van_auto', options = [blank_valasztas, "Igen", "Nem"], horizontal=horizontal)
        tapasztalat = st.radio("Van tapasztalatod autómosás, vagy autókozmetika területén?", key='tapasztalat', options = [blank_valasztas, "Igen", "Valamennyi van", "Nem"], horizontal=horizontal)
        jogositvany = st.radio("Rendelkezel kismotor/motor, vagy B kategóriás jogosítvánnyal?", key='motor', options = [blank_valasztas, "Igen", "Nem"], horizontal=horizontal)
        robogo = st.radio("Rendelkezel tapasztalattal motorozás/robogózás terén?", key='robogo', options = [blank_valasztas, "Igen", "Nem"], horizontal=horizontal)
        
        submitted = st.form_submit_button("Jelentkezem", on_click=session_counter)

        col1, col2 = st.columns([2, 2])

        with col1:
            st.markdown("Nyomja meg a gombot, hogy a jelentkezését elküldje nekünk.")
        with col2:
            st.write("Ha valami kérdése van, kérjük keressen minket bizalommal a következő elérhetőségeken:")
            st.write("Email: info@cleango.hu")

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
                    st.warning("Kerjük adja meg a nevét.")
                    error_counter += 1
                if email_user == "" or "@" not in email_user or "." not in email_user:
                    st.warning("Kerjük adjon meg helyes email címet.")
                    error_counter += 1
                if phone_number == "":
                    st.warning("Kerjük adja meg a telefonszámat helyesen.")
                    error_counter += 1
                if birth_year == default_szuletesi_ev:
                    st.warning("Kerjük válassza ki a születesi évét.")
                    error_counter += 1
                if lakhely == blank_valasztas:
                    st.warning("Kerjük válassza ki a lakhelyet.")
                    error_counter += 1
                if mellek_vagy_foallas == blank_valasztas:
                    st.warning("Kerjük válassza ki hogy mellek, vagy foallasban szeretne dolgozni.")
                    error_counter += 1
                if van_auto == blank_valasztas:
                    st.warning("Kerjük válassza ki hogy van-e sajat autoja.")
                    error_counter += 1
                if tapasztalat == blank_valasztas:
                    st.warning("Kerjük válassza ki hogy van-e tapasztalata autómosás, vagy autókozmetika területén.")
                    error_counter += 1
                if jogositvany == blank_valasztas:
                    st.warning("Kerjük válassza ki hogy rendelkezik-e kismotor/motor, vagy B kategóriás jogosítvánnyal.")
                    error_counter += 1
                if robogo == blank_valasztas:
                    st.warning("Kerjük válassza ki hogy rendelkezik-e tapasztalattal motorozás/robogózás terén.")
                    error_counter += 1

                
                
                if error_counter == 0:
                    # create a string with the answers
                    questiions_and_answers = f""" <br><br>
                        Név: {name} <br><br>
                        Email: {email_user} <br><br>
                        Telefonszám: {phone_number} <br><br>
                        Születési év: {birth_year} <br><br>
                        Hol laksz: {lakhely} <br><br>
                        Mellék, vagy főállásban dolgoznál: {mellek_vagy_foallas} <br><br>
                        Van saját autód: {van_auto} <br><br>
                        Van tapasztalatod autómosás, vagy autókozmetika területén: {tapasztalat} <br><br>
                        Rendelkezel kismotor/motor, vagy B kategóriás jogosítvánnyal: {jogositvany} <br><br>
                        Rendelkezel tapasztalattal motorozás/robogózás terén: {robogo}
                    """

                    questiions_and_answers_dictionary = {
                        "name": name,
                        "email": email_user,
                        "tel_number": phone_number,
                        "dob": birth_year,
                        "location": lakhely,
                        "job": mellek_vagy_foallas,
                        "own_car": van_auto,
                        "experience": tapasztalat,
                        "motor_licence": jogositvany,
                        "motor_experience": robogo
                    }
                    # convert dict to a string
                    questiions_and_answers_dictionary = str(questiions_and_answers_dictionary)

                    conn = create_connection()
                    cursor = conn.cursor()
                    # I have these columns in the table: id, name, email, telephone_number, dob, questions, created_at, updated_at.
                    # The id and the created_at and updated_at columns are automatically filled by the database.
                    insert_query = """INSERT INTO cleango.bi_job_applications (name, email, telephone_number, dob, questions) VALUES ('{}', '{}', '{}', '{}', '{}')""".format(
                        name, email_user, phone_number, birth_year, questiions_and_answers_dictionary)
                    print(insert_query)
                    cursor.execute(insert_query)
                    # Commit the changes and close the cursor and the database connection
                    conn.commit()
                    cursor.close()
                    conn.close()

                    kizaro_ok = 0
                    if int(birth_year) < 1970:
                        kizaro_ok = kizaro_ok + 1
                    if lakhely == "Pest megye" and van_auto == "Nem":
                        kizaro_ok = kizaro_ok + 1
                    if lakhely == "Egyéb":
                        kizaro_ok = kizaro_ok + 1
                    if jogositvany == "Nem":
                        kizaro_ok = kizaro_ok + 1
                    if robogo == "Nem" and van_auto == "Nem":
                        kizaro_ok = kizaro_ok + 1
                    
                    if kizaro_ok > 0:
                        # Ha a kizaro ok miatt nem tud jelentkezni ezt rakjuk az emailbe
                        email_subject_to_us = "CleanGo - Moso Jelentkezes - Nem sikeres"
                        email_body_to_us = f"""Moso jelentkezes erkezett. A jelentkezes NEM sikeres <br><br> 
                            A jelentkezo az alabbi valaszokat adta : {questiions_and_answers}"""
                        email_subject_to_user = "CleanGo - Moso toborzas - Sajnáljuk"
                        email_body_to_user = f"""Szia {name}! <br><br>
                        Sajnáljuk a jelentkezésed most nem volt sikeres. :( <br><br> Ez lehet azért, mert nem felelt meg a feltételeknek, vagy mert jelenleg nincs szabad kapacításunk fogadni Téged. <br><br> 
                        Köszönjük, hogy jelentkeztél, és ha változik a helyzet, akkor felvesszük veled a kapcsolatot. <br><br> Üdvözlettel, <br> CleanGo csapata <br><br>"""

                    if kizaro_ok == 0:
                        # Ha nincs kizaro ok
                        foglalasi_link = "https://calendly.com/cleango/interju"
                        email_subject_to_us = "CleanGo - Moso toborzas"
                        email_body_to_us = f"""Moso jelentkezes erkezett. A jelentkezes SIKERES. <br><br> 
                            A jelentkezo az alabbi valaszokat adta : {questiions_and_answers}"""
                        email_subject_to_user = "CleanGo - Gratulálunk"
                        email_body_to_user = f"""Szia {name}! <br><br>
                        Gratulálunk, a válaszaid alapján kiválasztásra kerültél. Az első lépést megtetted a CleanGo csapatába való bekerüléshez. <br><br> 
                        A masodik lépéshez foglalj időpontot a következő linken: {foglalasi_link} <br><br> Üdvözlettel, <br> CleanGo csapata <br><br>"""
                        
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
