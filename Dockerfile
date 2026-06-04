FROM python:3.12-slim

RUN pip install playwright
RUN playwright install chromium
RUN playwright install-deps

WORKDIR /app
COPY login.py .

CMD ["python", "-u", "login.py"]
