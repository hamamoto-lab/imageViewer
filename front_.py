import streamlit as st
from PIL import Image
import os
import re
import pandas as pd
import datetime as dt
import json
from enum import Enum
import shutil

class Sample():
    def __init__(self, path) -> None:
        self.name = path
        self.files = sorted([f for f in os.listdir(f'data/{path}') if not f.startswith('.')],
                            key=lambda x: int(re.findall(r'^\d+(?=_)', x)[0]))
        self.suggestion = [re.findall(r'(?<=\d_).+?(?==Proc)', f)[0] for f in self.files]
                                 
    def return_images(self):
        return [Image.open(f'data/{self.name}/{file}') for file in self.files]

class Mode(Enum):
    BLI = 0
    Indigo = 1
    LCI = 2
    NBI = 3
    WLI = 4

Mode2 = {
    "0-I(Is, Ip, Isp)" : 0,
    '0-IIa' : 1,
    '0-IIc' : 2,
    'LST-G' : 3,
    'LST-NG' : 4,
    'Type2' : 5,
    'Type3' : 6,
}

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
                                  f"{st.session_state['name_person1']}": [None],
                                  f"{st.session_state['name_person2']}": [None],
                                  f"{st.session_state['name_person3']}": [None]})
            st.session_state['df'] = pd.concat([df, d_new]).reset_index(drop=True)
            st.session_state.data['added_rows'] = []

    def push_tbl():
        df_var = pd.DataFrame({'Query name': [sample.name for _ in range(len(sample.suggestion) - 1)],
                               'Suggested file': sample.suggestion[1:],
                               f"{st.session_state['name_person1']}": [v for k, v in sorted(st.session_state.items()) if 'p1' in k],
                               f"{st.session_state['name_person2']}": [v for k, v in sorted(st.session_state.items()) if 'p2' in k],
                               f"{st.session_state['name_person3']}": [v for k, v in sorted(st.session_state.items()) if 'p3' in k],
                               '撮像モード': [v for k, v in sorted(st.session_state.items()) if 'mode1_' in k],
                               '肉眼型': [v for k, v in sorted(st.session_state.items()) if 'mode2_' in k]})
        st.session_state.df = pd.concat([df_var, st.session_state.df]).reset_index(drop=True)
        st.session_state.log[st.session_state.counter] = 1
        plus_counter()

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

    def start_1():
        st.session_state['name_project'] = '氏名' if st.session_state['f1'] == '' else st.session_state['f1']
        st.session_state['name_person1'] = '色が似ている' if st.session_state['f2'] == '' else st.session_state['f2']
        st.session_state['name_person2'] = '形が似ている' if st.session_state['f3'] == '' else st.session_state['f3']
        st.session_state['name_person3'] = '模様が似ている' if st.session_state['f4'] == '' else st.session_state['f4']
        st.session_state['init'] = 1

    def move_query():
        st.session_state['counter'] = st.session_state['query_slider'] - 1

    def load_logfile(json):
        try:
            if st.session_state['samples'] == json['samples']:
                st.session_state.update(log)
                st.session_state['init'] = 1
            else:
                st.error('選択したログファイルとdataディレクトリにあるクエリ画像フォルダリストが一致しません！dataディレクトリに正しいクエリ画像フォルダを置いて下さい。')
        except KeyError:
            st.error('選択したログファイルにはクエリリストに関する情報が含まれていません！')
        except TypeError:
            st.error('選択したログファイルが壊れています！JSON形式のログファイルを選択して下さい。')
        
    def create_zip():
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame({'Query name': [], 
                                                'Suggested file': [],
                                                f"{st.session_state['name_person1']}": [], 
                                                f"{st.session_state['name_person2']}": [], 
                                                f"{st.session_state['name_person3']}": [],
                                                '撮像モード': [],
                                                '肉眼型': []})
        os.mkdir('results')
        fname = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        with open('results/' + fname + '.log', 'w') as f:
            json.dump({k: v for k, v in st.session_state.items() if k in ['counter', 'samples', 'log',
                                                                                        'name_project', 'name_person1', 
                                                                                        'name_person2', 'name_person3']}, 
                                                                                        f, indent=4)
        st.session_state['df'].to_excel('results/' + fname + '.xlsx', index=False)
        shutil.make_archive('results', format='zip', root_dir = 'results')
        shutil.rmtree('results')
        
    # ========= Initializing app state =========
    try:
        if 'samples' not in st.session_state: 
            st.session_state['samples'] = sorted([path for path in os.listdir('data') if os.path.isdir(os.path.join('data', path))])
            st.session_state['log'] = [0 for _ in range(len(st.session_state['samples']))]
            st.session_state['counter'] = 0
            st.session_state["error_massage"] = None
            st.session_state['init'] = 0

        sample = Sample(st.session_state.samples[st.session_state['counter']])
        pictures = sample.return_images()


        # ======== Viewer =========
        ## >>>> Page setting <<<<<
        st.set_page_config(layout='wide')

        ## >>>> Side bar <<<<
        with st.sidebar:
            # ====== Subheader ======
            st.subheader('内視鏡 類似画像供覧ツール')

            # ====== Project information form ======
            if st.session_state['init'] == 0:
                st.radio('start', ['新規解析', '途中から解析'], label_visibility='hidden', key='radio_start')
                if st.session_state['radio_start'] == '新規解析':
                    with st.form('プロジェクト情報'):
                        st.text_input('お名前と日付', placeholder='お名前と日付を入力して下さい', key='f1')
                        #st.text_input('色が似ている', placeholder='何も入れないで下さい', key='f2', disabled=True)
                        #st.text_input('形が似ている', placeholder='何も入れないで下さい', key='f3', disabled=True)
                        #st.text_input('模様が似ている', placeholder='何も入れないで下さい', key='f4', disabled=True)
                        st.session_state['f2'] = '色が似ている'
                        st.session_state['f3'] = '形が似ている'
                        st.session_state['f4'] = '模様が似ている'
                        st.form_submit_button('プロジェクト開始', on_click=start_1)
                else:
                    files = st.file_uploader('ログファイルから解析を再開', accept_multiple_files=True, help='\~.log(必須)と\~.xlsxの最大2つのファイルを選択することが可能です。')
                    if files is not None:
                        for f in files:
                            if 'xlsx' in f.name:
                                st.session_state['df'] = pd.read_excel(f)
                            if 'log' in f.name:
                                log = json.load(f)
                                load_logfile(log)
                        st.experimental_rerun()
            else:
                # ====== Slide bar =====
                st.write(f"{sum(st.session_state['log'])}枚のクエリ画像リストを供覧済みです")
                with st.form('query state'):
                    st.slider('Query number', min_value=1, max_value=len(st.session_state['samples']), 
                            step = 1, value = st.session_state['counter'] + 1, key='query_slider')
                    st.form_submit_button('Queryを移動する', on_click=move_query)
                
                ## >>>> Query name <<<<
                if st.session_state.log[st.session_state.counter]:
                    st.markdown('**Query file is**')
                    st.info(sample.name)
                    st.error('供覧済みです!')
                else:
                    st.markdown('**Query file is**')
                    st.info(sample.name)

                ## >>>> PopUp Error Massage <<<<
                error_empty = st.empty()
                if st.session_state.error_massage is not None:
                    error_empty.error(st.session_state.error_massage)
                    
                ## >>>> Move next and previous buttons <<<<
                col1, col2 =st.columns(2)
                with col1:
                    st.button('<< 前の画像へ', on_click=minus_counter)
                with col2:
                    st.button('次の画像へ >>', on_click=plus_counter)

                ## >>>> Download button <<<<
                create_zip()
                with open('results.zip', 'rb') as fp:
                    st.download_button(label = 'Download ZIP',
                                    data = fp,
                                    file_name='results.zip',
                                    mime = 'application/zip')
                os.remove('results.zip')

        if st.session_state['init']:
            ## >>>> Ttitle <<<<
            st.title('内視鏡 類似画像供覧ツール')

            ## >>>> Pictures with tile-like viewing <<<<
            for row in range((len(pictures) + 2) // 3):
                for i, col in enumerate(st.columns(3)):
                    k = row * 3 + i
                    if k == 0:
                        col.subheader(f"Query: {sample.suggestion[k]}")
                        col.image(pictures[k])
                    elif k < len(pictures):
                        col.subheader(f"{str(k)}: {sample.suggestion[k]}")
                        col.image(pictures[k])

            ## >>>> Input form <<<<
            with st.form('供覧結果', clear_on_submit=True):
                if st.session_state['log'][st.session_state['counter']]:
                    df_inputed_prev = st.session_state['df'][st.session_state['df']['Query name'] == sample.name].to_dict()
                    radio_defaults1 = [vv for k, v in df_inputed_prev.items() for vv in v.values() if st.session_state['name_person1'] in k]
                    radio_defaults2 = [vv for k, v in df_inputed_prev.items() for vv in v.values() if st.session_state['name_person2'] in k]
                    radio_defaults3 = [vv for k, v in df_inputed_prev.items() for vv in v.values() if st.session_state['name_person3'] in k]
                    radio_defaults4 = [vv for k, v in df_inputed_prev.items() for vv in v.values() if '撮像モード' in k]                 
                    radio_defaults5 = [vv for k, v in df_inputed_prev.items() for vv in v.values() if '肉眼型' in k]
                else:
                    radio_defaults1 = ['3' for _ in range(1, len(pictures))]
                    radio_defaults2 = ['3' for _ in range(1, len(pictures))]
                    radio_defaults3 = ['3' for _ in range(1, len(pictures))]
                    radio_defaults4 = ['BLI' for _ in range(1, len(pictures))]
                    radio_defaults5 = ['0-I(Is, Ip, Isp)' for _ in range(1, len(pictures))]
                radio_defaults1 = [int(value) - 1 for value in radio_defaults1]
                radio_defaults2 = [int(value) - 1 for value in radio_defaults2]
                radio_defaults3 = [int(value) - 1 for value in radio_defaults3]
                radio_defaults4 = [Mode[value].value for value in radio_defaults4]
                radio_defaults5 = [Mode2[value] for value in radio_defaults5]
                c1, c2, c3, c4, c5, c6 = st.columns(6)
                with c1:
                    c1.subheader(f"{st.session_state['name_person1']}")
                    for i in range(1, len(pictures)):
                        c1.radio(f"{str(i)}:   {sample.suggestion[i]}", ('1', '2', '3', '4', '5'), key = f'p1{i}', horizontal=True, index=radio_defaults1[i - 1])
                with c2:
                    c2.subheader(f"{st.session_state['name_person2']}")
                    for i in range(1, len(pictures)):
                        c2.radio(f"{str(i)}:   {sample.suggestion[i]}", ('1', '2', '3', '4', '5'), key = f'p2{i}', horizontal=True, index=radio_defaults2[i - 1])
                with c3:
                    c3.subheader(f"{st.session_state['name_person3']}")
                    for i in range(1, len(pictures)):
                        c3.radio(f"{str(i)}:   {sample.suggestion[i]}", ('1', '2', '3', '4', '5'), key = f'p3{i}', horizontal=True, index=radio_defaults3[i - 1])
                with c4:
                    c4.subheader('撮像モード')
                    for i in range(1, len(pictures)):
                        c4.selectbox(f"{str(i)}:   {sample.suggestion[i]}", ('BLI', 'Indigo', 'LCI', 'NBI', 'WLI'), key = f'mode1_{i}', index=radio_defaults4[i - 1])                        
                with c5:
                    c5.subheader('肉眼型')
                    for i in range(1, len(pictures)):
                        c5.selectbox(f"{str(i)}:   {sample.suggestion[i]}", ("0-I(Is, Ip, Isp)", "0-IIa", '0-IIc', 'LST-G', 'LST-NG', 'Type2', 'Type3'), key = f'mode2_{i}', index=radio_defaults5[i - 1])                        
                with c6:
                    st.form_submit_button(label = '供覧結果を転記', on_click = push_tbl)
            
            ## >>>> Data table of reviewing results <<<<
            st.data_editor(st.session_state.df, num_rows='dynamic', on_change=edit_tbl, key='data')
    except AttributeError:
        st.error('dataディレクトリに正しくファイルが置かれていません！！正しくファイルを置いて画面をReloadして下さい。')
        code_message_for_error = '''# 正しいディレクトリ構成
        data/
          |– サンプル名_1/
          |     |– 0_任意の文字列=Proc.jpeg
          |     |– 1_任意の文字列=Proc.jpeg
          |     |– 2_任意の文字列=Proc.jpeg
          |     |– 3_任意の文字列=Proc.jpeg
          |     |– 4_任意の文字列=Proc.jpeg
          |     |– 5_任意の文字列=Proc.jpeg
          |
          |– サンプル名_2/
          |     |– 0_任意の文字列=Proc.jpeg
          |     |–     ︙'''
        st.code(code_message_for_error)

if __name__ == '__main__':
    main()