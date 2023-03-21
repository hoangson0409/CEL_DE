FROM python:3.9.4

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' CEL

WORKDIR /opt/BE

ARG PIP_EXTRA_INDEX_URL

ADD ./BE /opt/BE
RUN pip install --upgrade pip
RUN pip install -r /opt/BE/requirements.txt



USER CEL

EXPOSE 8001

CMD ["uvicorn", "app:app"]
