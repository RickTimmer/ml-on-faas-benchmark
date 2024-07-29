import wrapper
import joblib

forest = None
vectorizer = None

def lambda_handler(event, context):
  requestId = context.aws_request_id
  return wrapper.wrap(event, handler, initializer, requestId)

def handler(batch):
  batch_vectorized = vectorizer.transform(batch)
  results = forest.predict(batch_vectorized)
  return results.tolist()

def initializer():
  global forest, vectorizer
  opt_dir = "/opt/python"
  forest = joblib.load(f'{opt_dir}/model.joblib')
  vectorizer = joblib.load(f'{opt_dir}/vectorizer.joblib')
