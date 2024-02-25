# FROM public.ecr.aws/lambda/python:3.11

# COPY requirements.txt ${LAMBDA_TASK_ROOT}

# RUN pip install -r requirements.txt

# COPY src/__init__.py ${LAMBDA_TASK_ROOT}
# COPY src/email_build.py ${LAMBDA_TASK_ROOT}
# COPY src/github.py ${LAMBDA_TASK_ROOT}
# COPY src/lambda_function.py ${LAMBDA_TASK_ROOT}

# CMD ["lambda_function.lambda_handler"]

# Define custom function directory
ARG FUNCTION_DIR="/function"

FROM python:3.11 as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
COPY src/__init__.py ${FUNCTION_DIR}
COPY src/email_build.py ${FUNCTION_DIR}
COPY src/github.py ${FUNCTION_DIR}
COPY src/lambda_function.py ${FUNCTION_DIR}
COPY requirements.txt ${FUNCTION_DIR}
# Install the function's dependencies
RUN pip install \
    --target ${FUNCTION_DIR} \
    awslambdaric
RUN pip install \
    --target ${FUNCTION_DIR} \
    -r ${FUNCTION_DIR}/requirements.txt

# Use a slim version of the base Python image to reduce the final image size
FROM python:3.11-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "lambda_function.lambda_handler" ]