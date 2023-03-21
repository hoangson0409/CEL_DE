FROM python:3.9.4

WORKDIR /opt/FE

ADD ./FE /opt/FE
RUN pip install --upgrade pip
RUN pip install -r /opt/FE/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "stl.py"]