import wrapper
import joblib

svm = None
vectorizer = None

def lambda_handler(event, context):
  requestId = context.aws_request_id
  return wrapper.wrap(event, handler, initializer, requestId)

def handler(batch):
  batch_vectorized = vectorizer.transform(batch)
  results = svm.predict(batch_vectorized)
  return results.tolist()

def initializer():
  global svm, vectorizer
  opt_dir = "/opt/python"
  svm = joblib.load(f'{opt_dir}/model.joblib')
  vectorizer = joblib.load(f'{opt_dir}/vectorizer.joblib')
