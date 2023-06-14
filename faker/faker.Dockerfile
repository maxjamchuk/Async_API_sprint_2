FROM python:3.10

ENV HOME_APP=/faker

RUN mkdir $HOME_APP
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

WORKDIR $HOME_APP

COPY faker/entrypoint.sh entrypoint.sh
COPY . $HOME_APP

RUN chmod +x entrypoint.sh

CMD ["/faker/entrypoint.sh"]