import pandas as pd

# 応募情報を読み込む
application_info = pd.read_csv('')

# 指定された学校名のリスト
school_name = [
    '東京大学', '京都大学', '一橋大学', '東京工業大学', '早稲田大学',
    '慶應大学', '上智大学', '東京理科大学', '学習院大学', '明治大学',
    '青山学院大学', '立教大学', '中央大学', '法政大学', '関西大学',
    '関西学院大学', '同志社大学', '立命館大学', '筑波大学', '横浜国立大学',
    '千葉大学', '神戸大学', '大阪公立大学', '北海道大学', '東北大学',
    '名古屋大学', '大阪大学', '九州大学', '広島大学', 'お茶の水女子大学'
]

# 学校名が指定された学校名のリストに含まれる行のみを残す
# 注意: カラム名が '大学名' に修正されている
filtered_application_info = application_info[application_info['大学名'].isin(school_name)]

# 学生情報を読み込む
student_info = pd.read_csv('')

# 学生IDと内部IDが一致し、一言アピールが空白でない行を抽出
matched_students = pd.merge(filtered_application_info, student_info, left_on='学生ID', right_on='内部ID')
non_empty_appeals = matched_students[matched_students['一言アピール'].notna() & (matched_students['一言アピール'] != '')]

# 内部IDが重複している場合は最初の行を残して他を削除
unique_non_empty_appeals = non_empty_appeals.drop_duplicates(subset=['内部ID'], keep='first')

# get_feedback_students.csv を読み込む
feedback_students = pd.read_csv('get_feedback_students.csv')

# unique_non_empty_appeals から feedback_students に存在する内部IDの行を削除
# isin を使って一致するIDを見つけ、~ でその条件を反転させて一致しないものだけを選択
final_students = unique_non_empty_appeals[~unique_non_empty_appeals['内部ID'].isin(feedback_students[''])]

# 結果をプリント
print(final_students)

# 結果をCSVファイルとして出力
final_students.to_csv('final_filtered_student_info.csv', index=False)