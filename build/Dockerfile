FROM python:3.9

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY templates/ templates/

COPY app.py .

EXPOSE 5000

ENV FLASK_APP=app.py

LABEL org.opencontainers.image.source=https://github.com/granolaameobi/fresko

CMD ["flask", "run", "--host=0.0.0.0"]