import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
import joblib

data = pd.read_csv('../datasets/sentiment.csv')

X = data['Text']
y = data['Emotion']

vectorizer = CountVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

# Train SVM 
svm = LinearSVC(random_state=42, max_iter=5000)
svm.fit(X_vectorized, y)

joblib.dump(svm, '../functions/svm/model.joblib')
joblib.dump(vectorizer, '../functions/svm/vectorizer.joblib')
