import csv
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# CCのメールアドレス
# cc_address = "ouji@kotonaru.co.jp"

# CSVファイルのパス
csv_file_path = "/Users/yutokohata/Desktop/chores/extra_students/filtered_student.csv"

# SMTPサーバー情報
smtp_server = os.getenv('SMTP_SERVER')  # SMTPサーバーアドレスを設定
smtp_port = os.getenv('SMTP_PORT')  # SMTPポート番号を設定
smtp_username = os.getenv('SMTP_USERNAME')  # SMTPユーザー名を設定
smtp_password = os.getenv('SMTP_PASSWORD')  # SMTPパスワードを設定

print(f"smtp_server: {smtp_server}")
print(f"smtp_port: {smtp_port}")
print(f"smtp_username: {smtp_username}")
print(f"smtp_password: {smtp_password}")

# メール送信者情報
from_address = "yuto@kotonaru.co.jp"
from_name = "Kotonaru 木幡雄斗"

def send_mail(to_address, get_name):
    # メール内容
    subject = "【星野リゾート代表登壇】観光クロスオーバーサミット2024のご紹介！25歳以下参加費無料！"
    body = f"""
{get_name}さま

こんにちは。
株式会社Kotonaruインターン生の木幡です。
いつも完全オンライン長期インターン検索サイト「コトナル」をご利用いただき、ありがとうございます。

今回、コトナルを活用いただく観光系スタートアップ「たびふぁん」様が運営する、観光や地方創生、起業などに興味のある方におすすめのイベントを紹介します。
※株式会社たびふぁん様の過去求人はこちら（https://kotonaru.co.jp/internship-detail/390/tabifun2）

以下、正式なイベント概要になります。

ーーーーー
星野リゾート代表星野佳路氏も登壇する「観光クロスオーバーサミット2024」の参加募集！（U25 無料）

星野リゾート代表星野佳路氏による登壇や観光や地方創生で活躍するキーマンのセッション、観光に特化したビジネスコンテストのファイナリストによるプレゼンなどを行う「観光クロスオーバーサミット2024」への参加を募集しています。

観光や地方創生、起業などに興味のある方には絶好の機会なので、ぜひご参加ください！

【観光クロスオーバーサミット2024の概要】
観光産業で新たに挑戦するスタートアップや学生などを応援するきっかけの場として開催するイベントです。

【詳細】
日時：2024年7月04日（木）12:45〜18:45（開場12:00〜）
会場：東京証券会館 ホール（〒103-0025 東京都中央区日本橋茅場町１丁目５−８）
参加者：観光事業者、地方自治体、若手起業家やスタートアップ
参加費：U25 無料

【イベントホームページURL】※お申し込みはこちらから！
https://kankou-xoversummit2024.com

【主なプログラム】
・オープニング （12:45〜13:10）
・来賓挨拶 （13:10〜13:20）
　衆議院議員からのご挨拶 ※公務により変更あり

・基調講演 （13:30〜14:30）
　星野リゾート代表 星野佳路 氏による「観光の未来」について 講演

・観光クロスオーバーコンテスト 2024 （14:40〜16:10）
　ファイナリストによるプレゼンテーション

・観光クロスオーバーセッション１ （16:20〜17:10）
　株式会社 BEYOND 道越氏、観光庁担当者、株式会社おてつたび 永岡氏、
　リクルートじゃらんリサーチセンター 森戸氏、株式会社 POI 清水氏

・観光クロスオーバーサミットセッション２ （17:30〜18:00）
　観光庁観光戦略課長 河田氏、JTIC.SWISS 代表/観光カリスマ 山田氏

・クロージング （18:00〜18:45）
　東京都議会議員: 入江のぶこ氏からのご挨拶
　コモンズ投信株式会社取締役会長/シブサワ・アンド・カンパニー株式会社代表取締役: 渋澤健氏からのご挨拶
　コンテストの表彰式
　運営代表からのクロージング挨拶

ぜひ、ご参加お待ちしております！
また、「観光クロスオーバーサミット2024」の当日運営スタッフも募集しています。
ご興味のある方はこちらからご応募ください。
https://forms.gle/iyQrnH4tL2LKeDjVA

ーーーーー

なお、本メールに関わるご質問などがありましたら、お気軽にご連絡くださいませ。


ーーーーー
株式会社Kotonaru
木幡雄斗（Kohata Yuto）
Mail: yuto@kotonaru.co..jp
Mobile: +1 925 448 6990 105-0013
東京都港区浜松町2丁目2番15号 浜松町ダイヤビル2F

    """

    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header(from_name, 'utf-8')), from_address))
    msg['To'] = to_address
    # msg['Cc'] = cc_address
    msg['Subject'] = subject

    text = MIMEText(body, 'plain', 'utf-8')
    msg.attach(text)

    # SMTPサーバーに接続してメール送信
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(from_address, [to_address], msg.as_string())
        print(f"メールを {to_address} に送信しました")
    except Exception as e:
        print(f"メール送信エラー: {str(e)}")

# CSVファイルからメールアドレス読み込み
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # ヘッダー行をスキップ

    sent_count = 0
    for row in csv_reader:
        email_address = row[0] # メールアドレスの列の位置を適切に設定
        name = row[1]
        if email_address:
            send_mail(email_address, name)
            # 1秒待ってから次のメールを送信
            time.sleep(1)
            sent_count += 1
            if sent_count == 30:
                print("30件送信しました。次は61秒待機します。")
                time.sleep(61)  # 61秒待機
                sent_count = 0  # カウンターをリセット