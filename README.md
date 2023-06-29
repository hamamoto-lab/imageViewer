# 内視鏡画像供覧用 Viewerです

# Installation
1. `git clone`する
   ```
   git clone git@github.com:hamamoto-lab/imageViewer.git
   ```
2. git cloneしたディレクトリに移動する
3. `conda create`する
   ```
   conda create -f env.yml
   ```


# How to use

1. `data`ディレクトリに供覧したいデータを入れます

   ```
   data/
     |– sample01/
     |	|– file_01.png
     |	|– file_02.png
     |	|– file_03.png
     |	|– file_04.png
     |	|– file_05.png
     |	|– file_06.png
     |– sample02/
     |	|– ︙

   ```
2. 以下のスクリプトを実行
   ```
   streamlit run front.py
   ```

3. [localhost:8501](localhost:8501)にブラウザからアクセスする