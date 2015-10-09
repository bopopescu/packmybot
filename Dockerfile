FROM node:0.10-onbuild


COPY . /packbot

# replace this with your application's default port
EXPOSE 443

CMD ["node", "/packbot/app.js"]

