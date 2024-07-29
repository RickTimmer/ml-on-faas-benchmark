import wrapper
import joblib

logreg = None
vectorizer = None

def lambda_handler(event, context):
  requestId = context.aws_request_id
  return wrapper.wrap(event, handler, initializer, requestId)

def handler(batch):
  batch_vectorized = vectorizer.transform(batch)
  results = logreg.predict(batch_vectorized)
  return results.tolist()

def initializer():
  global logreg, vectorizer
  opt_dir = "/opt/python"
  logreg = joblib.load(f'{opt_dir}/model.joblib')
  vectorizer = joblib.load(f'{opt_dir}/vectorizer.joblib')
