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

    # ========= Define functions =========
    def edit_tbl():
        data_dict = st.session_state.data
        if len(data_dict['edited_rows'].keys()):
            d = pd.DataFrame.from_dict(data_dict['edited_rows'], orient='index')
            st.session_state['df'].update(d)
            
        if len(data_dict['deleted_rows']):
            for idx in data_dict['deleted_rows']:
                st.session_state['df'].drop(idx, inplace = True)
            st.session_state['df'].reset_index(drop=True, inplace=True)
            st.session_state.data['deleted_rows'] = []
        
        if len(data_dict['added_rows']):
            df = st.session_state['df']
            d_new = pd.DataFrame({'Query name': [None],
                                  'Suggested file': [None],
                                  'Person 1': [None],
                                  'Person 2': [None],
                                  'Person 3': [None]})
            st.session_state['df'] = pd.concat([df, d_new]).reset_index(drop=True)
            st.session_state.data['added_rows'] = []

    def push_tbl():
        df_var = pd.DataFrame({'Query name': [sample.name for _ in range(len(sample.suggestion) - 1)],
                               'Suggested file': sample.suggestion[1:],
                               'Person 1': [v for k, v in st.session_state.items() if 'p1' in k],
                               'Person 2': [v for k, v in st.session_state.items() if 'p2' in k],
                               'Person 3': [v for k, v in st.session_state.items() if 'p3' in k]})
        st.session_state.df = pd.concat([df_var, st.session_state.df]).reset_index(drop=True)
        st.session_state.log[st.session_state.counter] = 1

    def minus_counter():
        if st.session_state.counter:
            st.session_state['counter'] -= 1
            st.session_state["error_massage"] = None
        else:
            st.session_state["error_massage"] = "最初のクエリです"

    def plus_counter():
        if (st.session_state.counter + 1) < len(st.session_state.samples):
            st.session_state['counter'] += 1
            st.session_state["error_massage"] = None
        else:
            st.session_state["error_massage"] = "最後のクエリです"

    # ========= Initializing app state =========
    if 'samples' not in st.session_state: 
        st.session_state.samples = [path for path in os.listdir('data') if os.path.isdir(os.path.join('data', path))]
        st.session_state.log = [0 for _ in range(len(st.session_state.samples))]
        st.session_state.counter = 0
        st.session_state.df = pd.DataFrame({'Query name': [], 
                                            'Suggested file': [],
                                            'Person 1': [], 
                                            'Person 2':[], 
                                            'Person 3':[]})
        st.session_state["error_massage"] = None
    sample = Sample(st.session_state.samples[st.session_state.counter])
    pictures = sample.return_images()


    # ======== Viewer =========
    ## >>>> Page setting <<<<<
    st.set_page_config(layout='wide')

    ## >>>> Ttitle <<<<
    st.title('内視鏡 類似画像供覧ツール')

    ## >>>> Query name <<<<
    if st.session_state.log[st.session_state.counter]:
        st.markdown(f'Query file is: {sample.name} **:red[供覧済みです!]**')
    else:
        st.markdown(f'Query file is: {sample.name}')

    ## >>>> Pictures with tile-like viewing <<<<
    for row in range((len(pictures) + 2) // 3):
        for i, col in enumerate(st.columns(3)):
            k = row * 3 + i
            if k < len(pictures):
                col.subheader(sample.suggestion[k])
                col.image(pictures[k])

    ## >>>> Input form <<<<
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
            st.form_submit_button(label = '供覧結果を転機', on_click = push_tbl)

    ## >>>> Move next and previous buttons <<<<
    col1, col2 =st.columns(2)
    with col1:
        st.button('<< 前の画像へ', on_click=minus_counter)
    with col2:
        st.button('次の画像へ >>', on_click=plus_counter)
    
    ## >>>> PopUp Error Massage <<<<
    error_empty = st.empty()
    if st.session_state.error_massage is not None:
        error_empty.error(st.session_state.error_massage)
    
    ## >>>> Data table of reviewing results <<<<
    edited_df = st.data_editor(st.session_state.df, num_rows='dynamic', on_change=edit_tbl, key='data')

    ## >>>> Download button <<<<
    st.download_button(label = 'Download csv file',
                       data = edited_df.to_csv().encode('shift-jis'),
                       mime = 'text/csv',
                       file_name = dt.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv')

if __name__ == '__main__':
    main()