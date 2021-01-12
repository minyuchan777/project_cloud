FROM python:3.7

WORKDIR /streamlit-project

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8080

COPY . /streamlit-project

CMD streamlit run first_app.py --server.port 8080
