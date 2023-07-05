# 内視鏡画像供覧用 Viewer

`data`ディレクトリに入れた画像群をタイル状に表示させながら、表示画像の評価を最大3人の評価者で行うためのツールです。  
`png`, `jpeg`, `tiff`などの一般的な画像に対応しています。

----------

## "はじめから解析する"
![demo_1](https://github.com/hamamoto-lab/imageViewer/assets/7193590/72532b5b-efeb-4feb-9052-9351b863515b)

## "途中から解析を再開する"
![demo_2](https://github.com/hamamoto-lab/imageViewer/assets/7193590/43570a53-c1ca-445f-a334-00de1fc803f1)



# Installation

1. `git clone` or [Release](https://github.com/hamamoto-lab/imageViewer/releases)から最新版をダウンロードする

   ```
   # git cloneの場合
   git clone git@github.com:hamamoto-lab/imageViewer.git
   ```
2. `git clone` or ダウンロード&解凍したディレクトリに移動する
3. `conda create`する

   ```
   conda create -f env.yml
   ```



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
     |
     |– sample02/
     |	|– ︙

   ```
   - 必ず上記のような`data/サンプル名/画像ファイル`というディレクトリ構造にして下さい。サンプル名に命名規則はありません。
   - ファイル名は必ず、`数字_任意の文字列1=Proc任意の文字列2.拡張子`にして下さい。`任意の文字列1`は表示画像名として使用されます。`任意の文字列2`はなくても実行に影響はありません。
   - ファイル拡張子には、`png`, `jpeg`, `tiff`が利用可能です。

2. 以下のスクリプトを実行

   ```
   streamlit run front.py
   ```
3. [localhost:8501](http://localhost:8501)にブラウザからアクセスする


# Featurs
- 左上に各フォルダ内に含まれる一番最初のデータ（`0_xxxxx.png`など, Query画像）が表示されます
- 一度に表示可能な画像数に制限はありません（5–6枚は確認済み）
- 解析結果（.xlsx）と解析ログファイル（.log）をzipファイルでダウンロード可能です
- ダウンロードしたzipファイルの中身を読み込ませることで、途中から解析を再開することが可能です

# Tips
- 画像ファイル名は`数字_任意の文字列1=Proc任意の文字列2.拡張子`として下さい
- 画像名として表示されるのは、`任意の文字列1`の部分になります

# License
GPLv3

------------

## 開発履歴

- 未修正のバグがある場合があります。詳しくは `issues`をご確認下さい

### 2023.07.05
- `data`ディレクトリに正しくファイルが置かれていない場合のエラーメッセージを出力するように変更（issues: [#11](https://github.com/hamamoto-lab/imageViewer/issues/11)）
- ラジオボタンからセレクトボックスに変更（issues: [#12](https://github.com/hamamoto-lab/imageViewer/issues/12)）
- ダウンロードファイルをcsvからexcelファイルに変更（issues: [#14](https://github.com/hamamoto-lab/imageViewer/issues/14)）

### 2023.07.04

- 近藤さんからのリクエスト部分を機能追加（issues: [#9](https://github.com/hamamoto-lab/imageViewer/issues/9)）

### 2023.06.30

- データテーブルを編集した時の結果が保存されないバグを修正（issues: [#1](https://github.com/hamamoto-lab/imageViewer/issues/1)）
