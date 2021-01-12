FROM python:3.7.8-slim

WORKDIR /streamlit-project

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8080

COPY . /streamlit-project

CMD streamlit run --server.port 8080 --server.enableCORS false first_app.py