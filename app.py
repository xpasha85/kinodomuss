import datetime
import random
import ttlock

import streamlit as st
from datetime import date, timedelta, datetime
import time

st.set_page_config(page_title='Пароли для KINODOMUSS', page_icon='🎥')
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.subheader('Создание паролей для KINODOMUSS')
pass_name = ''
# st.caption('Начало действия пароля')
col1, col2 = st.columns(2)
with col1:
    date_start = st.date_input(label='Начало действия пароля', min_value=date.today(),
                               max_value=date.today() + timedelta(days=14), format='DD.MM.YYYY')
with col2:
    time_start = st.time_input(label='', label_visibility='hidden',
                               step=timedelta(minutes=15))
col1, col2 = st.columns(2)
with col1:
    date_end = st.date_input(label='Окончание действия пароля', value=date_start, min_value=date.today(),
                             max_value=date.today() + timedelta(days=14), format='DD.MM.YYYY')
with col2:
    time_end = st.time_input(label='', label_visibility='hidden',
                             step=timedelta(minutes=15), key='re')
is_random = st.checkbox(label='Случайный пароль', value=True)
password_expander = st.expander('Ввод пароля', expanded=False)
with password_expander:
    password = str(st.number_input('', disabled=is_random, min_value=1000, value=None, placeholder=768458, format='%d'))

pass_name = st.text_input(label='Название пароля', placeholder='например, Марина')
if st.button('Создать'):
    start_date_time = datetime(date_start.year, date_start.month, date_start.day,
                               time_start.hour, time_start.minute) - timedelta(hours=10)
    end_date_time = datetime(date_end.year, date_end.month, date_end.day,
                             time_end.hour, time_end.minute) - timedelta(hours=10)
    if end_date_time.timestamp() - start_date_time.timestamp() < 0:
        st.error('Дата окончания действия должна быть больше даты начала')
        st.stop()
    if not pass_name:
        st.error('Введите название пароля')
        st.stop()
    if is_random:
        password = format(random.randint(0, 9999), '04d')
    with st.spinner('Подожите. Пароль формируется...'):
        result = ttlock.set_custom_pass(start_date_time, end_date_time, pass_name, False, password)
    if result.get('status') == 'ok':
        st.text(f'Пароль успешно создан. Действие пароля c\n'
                f'{(start_date_time - timedelta(hours=10)).strftime("%d.%m.%Y %H:%M")} до \n'
                f'{(end_date_time - timedelta(hours=10)).strftime("%d.%m.%Y %H:%M")}. Пароль:')
        st.header(result.get('password'))
    if result.get('status') == 'err':
        st.error(result.get('description'))