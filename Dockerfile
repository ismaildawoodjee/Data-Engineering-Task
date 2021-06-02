FROM python:3.9.5
WORKDIR /src/app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "./ethprice.py"]
