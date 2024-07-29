import wrapper
import torch
from transformers import pipeline

pipe = None

def lambda_handler(event, context):
  requestId = context.aws_request_id
  return wrapper.wrap(event, handler, initializer, requestId)

def handler(batch):
  results = []
  for item in batch:
    messages = build_messages(item)
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    results.append(outputs[0]["generated_text"])
  return results

def initializer():
  global pipe
  pipe = pipeline("text-generation", model="Maykeye/TinyLLama-v0", torch_dtype=torch.bfloat16)

def build_messages(question):
    return [
      {
          "role": "system",
          "content": "You are a chatbot trying to answer a multiple choice question.",
      },
      {"role": "user", "content": question},
    ]
