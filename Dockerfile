FROM python:3.12-slim

# Installa Playwright e Browser Use
RUN pip install playwright browser-use
RUN playwright install chromium
RUN playwright install-deps

WORKDIR /app

COPY login.py .

CMD ["python", "-u", "login.py"]