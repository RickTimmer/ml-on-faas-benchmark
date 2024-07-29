import wrapper
import joblib

pca = None
vectorizer = None

def lambda_handler(event, context):
  requestId = context.aws_request_id
  return wrapper.wrap(event, handler, initializer, requestId)

def handler(batch):
  batch_vectorized = vectorizer.transform(batch)
  batch_pca = pca.transform(batch_vectorized.toarray())
  return batch_pca.tolist()

def initializer():
  global pca, vectorizer
  opt_dir = "/opt/python"
  pca = joblib.load(f'{opt_dir}/model.joblib')
  vectorizer = joblib.load(f'{opt_dir}/vectorizer.joblib')
