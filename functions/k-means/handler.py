import wrapper
import joblib

k_means = None
vectorizer = None

def lambda_handler(event, context):
  requestId = context.aws_request_id
  return wrapper.wrap(event, handler, initializer, requestId)

def handler(batch):
  batch_vectorized = vectorizer.transform(batch)
  results = k_means.predict(batch_vectorized)
  return results.tolist()

def initializer():
  global k_means, vectorizer
  opt_dir = "/opt/python"
  k_means = joblib.load(f'{opt_dir}/model.joblib')
  vectorizer = joblib.load(f'{opt_dir}/vectorizer.joblib')
