FROM python

ENV PORT=5001
ENV PYTHONPATH=.:$PYTHONPATH

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app
COPY exceptions exceptions

CMD python -m app.api
