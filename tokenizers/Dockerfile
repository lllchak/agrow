FROM python:3-alpine3.6 as tokenizers   

WORKDIR /project
COPY . .

LABEL "project"="tokenizers_tests"
LABEL "author"="lllchak"

RUN apk add --no-cache --virtual .build-deps \
    build-base openssl-dev libffi-dev

COPY tokenizers_requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r tokenizers_requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "tests/tokenizers_tests.py" ]
