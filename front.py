import streamlit as st
from PIL import Image
import os
import re
import pandas as pd
import datetime as dt

class Sample():
    def __init__(self, path) -> None:
        self.name = path
        self.files = os.listdir(f'data/{path}')
    
    def return_images(self):
        return [Image.open(f'data/{self.name}/{file}') for file in self.files]
    



def main():
    st.set_page_config(layout='wide')
    st.title('内視鏡 類似画像供覧ツール')

    if 'samples' not in st.session_state: 
        st.session_state.samples = [path for path in os.listdir('data') if os.path.isdir(os.path.join('data', path))]
        st.session_state.counter = 0
        st.session_state.df = pd.DataFrame({'Sample name': [], 'Person 1': [], 'Person 2':[], 'Person 3':[]})

    sample = Sample(st.session_state.samples[st.session_state.counter])
    pictures = sample.return_images()
    st.write(f'Query file is: {sample.name}')

    for row in range(-(-len(pictures)) // 3):
        for i, col in enumerate(st.columns(3)):
            k = row * 3 + i
            col.subheader(re.findall(r'(?<=\d_).+(?=\=Proc)', sample.files[k])[0])
            col.image(pictures[k])

    with st.form('供覧結果', clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            person1 = st.number_input('Person 1', step = 1, min_value = 0, max_value = 5, value = 3)
        with c2:
            person2 = st.number_input('Person 2', step = 1, min_value = 0, max_value = 5, value = 3)
        with c3:
            person3 = st.number_input('Person 3', step = 1, min_value = 0, max_value = 5, value = 3)
        with c4:
            push = st.form_submit_button(label = '供覧結果を転機')
    
    def minus_counter():
        st.session_state['counter'] -= 1

    def plus_counter():
        st.session_state['counter'] += 1

    col1, col2 =st.columns(2)
    with col1:
        st.button('<< 前の画像へ', on_click=minus_counter)
    with col2:
        st.button('次の画像へ >>', on_click=plus_counter)

    write_bt = st.button(label = 'Export to excel file')

    if push:
        df_var = pd.DataFrame({'Sample name': [sample.name],
                               'Person 1': [person1],
                               'Person 2': [person2],
                               'Person 3': [person3]})
        st.session_state.df = pd.concat([df_var, st.session_state.df])

    edited_df = st.data_editor(st.session_state.df, num_rows='dynamic')

    if write_bt:
        fname = 'output/' + dt.datetime.now().strftime('%Y%m%d_%H%M%S') + '.xlsx'
        edited_df.to_excel(fname)

if __name__ == '__main__':
    main()