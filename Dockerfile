FROM node:20
WORKDIR /front-end/website
COPY website/ .
RUN npm install
RUN npm run build

FROM python:3.8
WORKDIR /back-end
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8080
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
CMD /wait && pipenv run uvicorn app.main:app --reload
