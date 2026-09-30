FROM public.ecr.aws/lambda/python:3.12
COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}" && python -c "import cv2; assert cv2.__version__.startswith('5.')"
COPY dialguard ${LAMBDA_TASK_ROOT}/dialguard
COPY web ${LAMBDA_TASK_ROOT}/web
CMD ["dialguard.aws_handler.handler"]
