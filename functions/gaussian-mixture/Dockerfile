FROM ml-on-faas:base

COPY requirements.txt .
RUN mkdir /opt/python
RUN pip3 install -r requirements.txt -t /opt/python

COPY model.joblib /opt/python
COPY vectorizer.joblib /opt/python

COPY config.py ${LAMBDA_TASK_ROOT}
COPY handler.py ${LAMBDA_TASK_ROOT}

ENV HF_HOME=/tmp

CMD [ "handler.lambda_handler" ]
