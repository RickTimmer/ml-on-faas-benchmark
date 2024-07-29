import wrapper
import joblib

gaussian_mixture = None
vectorizer = None

def lambda_handler(event, context):
  requestId = context.aws_request_id
  return wrapper.wrap(event, handler, initializer, requestId)

def handler(batch):
  batch_vectorized = vectorizer.transform(batch)
  batch_vectorized_dense = batch_vectorized.toarray()
  results = gaussian_mixture.predict(batch_vectorized_dense)
  return results.tolist()

def initializer():
  global gaussian_mixture, vectorizer
  opt_dir = "/opt/python"
  gaussian_mixture = joblib.load(f'{opt_dir}/model.joblib')
  vectorizer = joblib.load(f'{opt_dir}/vectorizer.joblib')
