# Build stage
FROM public.ecr.aws/lambda/python:3.12 as builder

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM public.ecr.aws/lambda/python:3.12

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy only necessary files from builder stage
COPY --from=builder ${LAMBDA_TASK_ROOT}/lib/python3.12/site-packages ${LAMBDA_TASK_ROOT}/lib/python3.12/site-packages

# Copy your application code
COPY main.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["main.lambda_handler"]