FROM node:0.12


COPY . /packbot

# replace this with your application's default port
EXPOSE 8080

CMD ["node", "/packbot/app.js"]

