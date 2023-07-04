# 内視鏡画像供覧用 Viewerです

## 開発状況

- 未修正のバグがあります。詳しくは `issues`をご確認下さい

### 2023.06.30

- データテーブルを編集した時の結果が保存されないバグを修正（issues: [#1](https://github.com/hamamoto-lab/imageViewer/issues/1)）

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


# Demonstration
## `はじめから解析する`
![demo_1](https://github.com/hamamoto-lab/imageViewer/assets/7193590/47c83f22-c865-4907-9fce-9b344873f3c3)

## `途中から解析を再開する`
![demo_2](https://github.com/hamamoto-lab/imageViewer/assets/7193590/655972e0-b289-4c0e-b261-94f893172ea1)


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
3. [localhost:8501](http://localhost:8501)にブラウザからアクセスする
