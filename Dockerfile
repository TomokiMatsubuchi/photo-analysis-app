FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get -y install \
    tesseract-ocr \
    tesseract-ocr-jpn
RUN apt-get clean
WORKDIR /Photo-analysis
COPY requirements.txt /Photo-analysis
RUN pip install -r requirements.txt
COPY . /Photo-analysis