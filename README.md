# Course Selection Optimizer

何か問題やご質問がございましたら、下記のメールアドレスまでご連絡ください。  
* yankawadev@gmail.com

## 概要

Pythonを利用したツールです。  
このツールは、課題研究の選択割り当ての省力化のために制作されました。

## ライブラリのインストール

> [!IMPORTANT]
> ライブラリが正常に行われていない場合正常に動作しない可能性があります

**当プログラムに必要なライブラリの方法**
```bash:install library
pip install -r requirements.txt
```

## 使用方法

> [!NOTE]
> 分類数などによって処理時間が非常に長くなる可能性があります。

1. *app.py*を実行します。[^1]
2. ファイルの入力は*GUI*を通じて行うことができます。[^2]
3. 出力は*output/selected_courses.csv*に出力されます。

***

[^1]: *app.py*は以下のようにして実行することができます。
```bash:execution app.py
python app.py
```
[^2]: 現在入力されるファイルの形式はcsvに限定されています。


## 各関数の説明

read_course_preferences(csv_path): CSV ファイルからコース設定データを読み取り、辞書を返します。  
read_course_capacities(csv_path): CSV ファイルからコース定員データを読み取り、辞書を返します。  
save_to_csv(selected_courses_per_student, csv_path): 学生ごとに選択したコースを CSV ファイルに保存します。  
analyze_hope_and_assignment_data(selected_courses_per_student): 各学生の満たされた優先レベルを分析し、辞書を返します。  
Lot_fulfilled_preference_levels(fulfilled_preference_data): 嗜好を満たすレベルの分布をプロットします。  
Decide_courses(): 線形計画法を使用して各学生のコースを決定し、辞書を返します。  
get_file_paths(): Tkinter ファイル ダイアログを開き、ユーザーがコース設定とコース容量の CSV ファイルを選択できるようにします。  

main(): get_file_paths 関数を呼び出してファイル パスを取得し、CourseSelectionOptimizer インスタンスを作成し、そのメソッドを呼び出してコース選択の最適化と分析を実行します。  