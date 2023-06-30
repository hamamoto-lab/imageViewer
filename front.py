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
        self.suggestion = [re.findall(r'(?<=\d_).+(?=\=Proc)', f)[0] for f in self.files]
    
    def return_images(self):
        return [Image.open(f'data/{self.name}/{file}') for file in self.files]
    



def main():
    st.set_page_config(layout='wide')
    st.title('内視鏡 類似画像供覧ツール')

    if 'samples' not in st.session_state: 
        st.session_state.samples = [path for path in os.listdir('data') if os.path.isdir(os.path.join('data', path))]
        st.session_state.counter = 0
        st.session_state.df = pd.DataFrame({'Query name': [], 
                                            'Suggested file': [],
                                            'Person 1': [], 
                                            'Person 2':[], 
                                            'Person 3':[]})

    sample = Sample(st.session_state.samples[st.session_state.counter])
    pictures = sample.return_images()
    st.write(f'Query file is: {sample.name}')

    for row in range(-(-len(pictures)) // 3):
        for i, col in enumerate(st.columns(3)):
            k = row * 3 + i
            col.subheader(sample.suggestion[k])
            col.image(pictures[k])

    with st.form('供覧結果', clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            c1.subheader('Preson 1')
            for i in range(1, len(pictures)):
                c1.radio(sample.suggestion[i], ("OK", 'Bad'), key = f'p1{i}', horizontal=True, args=[1, 0])
        with c2:
            c2.subheader('Preson 2')
            for i in range(1, len(pictures)):
                c2.radio(sample.suggestion[i], ("OK", 'Bad'), key = f'p2{i}', horizontal=True, args=[1, 0])

        with c3:
            c3.subheader('Preson 3')
            for i in range(1, len(pictures)):
                c3.radio(sample.suggestion[i], ("OK", 'Bad'), key = f'p3{i}', horizontal=True, args=[1, 0])

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

    if push:
        df_var = pd.DataFrame({'Query name': [sample.name for _ in range(len(sample.suggestion) - 1)],
                               'Suggested file': sample.suggestion[1:],
                               'Person 1': [v for k, v in st.session_state.items() if 'p1' in k],
                               'Person 2': [v for k, v in st.session_state.items() if 'p2' in k],
                               'Person 3': [v for k, v in st.session_state.items() if 'p3' in k]})
        st.session_state.df = pd.concat([df_var, st.session_state.df])

    edited_df = st.data_editor(st.session_state.df, num_rows='dynamic')

    st.download_button(label = 'Download csv file',
                       data = edited_df.to_csv().encode('shift-jis'),
                       mime = 'text/csv',
                       file_name = 'output/' + dt.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv')

if __name__ == '__main__':
    main()