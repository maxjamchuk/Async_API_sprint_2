FROM node:alpine

ENV HOME_APP=/elastic

RUN mkdir $HOME_APP
RUN apk --no-cache add curl
RUN npm install elasticdump -g elasticdump

WORKDIR $HOME_APP

COPY entrypoint.sh entrypoint.sh
COPY . $HOME_APP

RUN chmod +x entrypoint.sh

CMD ["/elastic/entrypoint.sh"]