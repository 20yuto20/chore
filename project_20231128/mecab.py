import MeCab
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# MeCabの初期化
tagger = MeCab.Tagger()

# CSVファイルの読み込み
df = pd.read_csv("")

# NaNや空の文字列を含む行を除去
df = df.dropna(subset=['ページ タイトルとスクリーン クラス'])
df = df[df['ページ タイトルとスクリーン クラス'] != ""]

# 名詞、動詞、形容詞、形容動詞を抽出する関数
def extract_words(text):
    nodes = tagger.parse(text).split("\n")
    words = []
    for node in nodes[:-2]:
        parts = node.split("\t")
        if len(parts) >= 2:
            word = parts[0]
            # 数字を無視
            if word.isnumeric():
                continue
            pos = parts[1].split(",")[0]
            if pos in ["名詞", "動詞", "形容詞", "形容動詞"]:
                words.append(word)
    return " ".join(words)

# 各タイトルに関数を適用
df['words'] = df['ページ タイトルとスクリーン クラス'].apply(extract_words)

# トレーニングデータとテストデータに分割
X = df['words']
y = df['ユーザーあたりのビュー']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# トークンのカウントのマトリックスに変換
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ランダムフォレストのトレーニング
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_vec, y_train)

# テストデータでの評価
y_pred = rf.predict(X_test_vec)
mse = mean_squared_error(y_test, y_pred)
print(f"Random Forest MSE: {mse}")

# 重要な特徴量の表示
feature_importances = rf.feature_importances_
coeffs = pd.Series(feature_importances, index=vectorizer.get_feature_names_out()).sort_values(ascending=False)
print(coeffs.head(10))
