# frontend
FROM node:20
WORKDIR /front-end/website
COPY . .
RUN npm install
RUN npm run build
# backend
FROM python:3.9
WORKDIR /back-end
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8080
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
WORKDIR /back-end
CMD /wait && uvicorn app.main:app
