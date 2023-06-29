import streamlit as st
from PIL import Image
import os
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
        st.session_state.samples = [Sample(path) for path in os.listdir('data') if os.path.isdir(os.path.join('data', path))]
        st.session_state.counter = 0
        st.session_state.df = pd.DataFrame({'Sample name': [], 'Person 1': [], 'Person 2':[], 'Person 3':[]})

    cols = st.columns(3)
    cols[0].image(st.session_state.samples[st.session_state.counter].return_images()[0])
    cols[1].image(st.session_state.samples[st.session_state.counter].return_images()[1])
    cols[2].image(st.session_state.samples[st.session_state.counter].return_images()[2])

    cols = st.columns(3)
    cols[0].image(st.session_state.samples[st.session_state.counter].return_images()[3])
    cols[1].image(st.session_state.samples[st.session_state.counter].return_images()[4])
    cols[2].image(st.session_state.samples[st.session_state.counter].return_images()[5])

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
    
    col1, col2 =st.columns(2)
    with col1:
        prev_bt = st.button('<< 前の画像へ', key = 'prev_bt')
    with col2:
        next_bt = st.button('次の画像へ >>', key = 'next_bt')

    write_bt = st.button(label = 'Export to excel file')

    if next_bt:
        st.session_state.counter += 1
    if prev_bt:
        st.session_state.counter += 0
    if push:
        df_var = pd.DataFrame({'Sample name': [st.session_state.samples[st.session_state.counter].name],
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