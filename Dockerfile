FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m flaskuser

RUN chown -R flaskuser:flaskuser /app

USER flaskuser

EXPOSE 8000

CMD ["gunicorn","--bind","0.0.0.0:8000","app:app"]

