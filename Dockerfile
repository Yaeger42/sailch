FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY src/__init__.py ${LAMBDA_TASK_ROOT}
COPY src/email_build.py ${LAMBDA_TASK_ROOT}
COPY src/github.py ${LAMBDA_TASK_ROOT}
COPY src/lambda_function.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.lambda_handler"]