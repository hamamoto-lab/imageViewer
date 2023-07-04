# 内視鏡画像供覧用 Viewerです

## 開発状況

- 未修正のバグがあります。詳しくは `issues`をご確認下さい

### 2023.07.04

- 近藤さんからのリクエスト部分を機能追加（issues: [#9](https://github.com/hamamoto-lab/imageViewer/issues/9)）

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
![demo_1](https://github.com/hamamoto-lab/imageViewer/assets/7193590/580572c5-0289-4ff4-83df-d91569b0afc8)

## `途中から解析を再開する`
![demo_2](https://github.com/hamamoto-lab/imageViewer/assets/7193590/40c35c6b-2cef-4ca1-ba13-110187b355db)

# How to use

1. `data`ディレクトリに供覧したいデータを入れます

   ```
   data/
     |– sample01/
     |	|– 0_file_01=ProcXXXXX.png
     |	|– 1_file_02=ProcXXXXX.png
     |	|– 2_file_03=ProcXXXXX.png
     |	|– 3_file_04=ProcXXXXX.png
     |	|– 4_file_05=ProcXXXXX.png
     |	|– 5_file_06=ProcXXXXX.png
     |– sample02/
     |	|– ︙

   ```
2. 以下のスクリプトを実行

   ```
   streamlit run front.py
   ```
3. [localhost:8501](http://localhost:8501)にブラウザからアクセスする

# Tips
- ファイル名は`数字_任意の文字列1=Proc任意の文字列2.拡張子`として下さい
- 画像名として表示されるのは、`任意の文字列1`の部分になります