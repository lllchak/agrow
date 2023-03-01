FROM python:3-alpine3.6 as tokenizers

WORKDIR /project
COPY . .

LABEL "project"="tokenizers_tests"
LABEL "author"="lllchak"

RUN apk add --no-cache --virtual .build-deps \
    build-base openssl-dev libffi-dev

RUN pip install --upgrade pip
RUN pip install -r tokenizers_requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "tecode/tokenizers/tokenizers_tests.py" ]

FROM python:3-alpine3.6 as vectorizers

WORKDIR /project
COPY . .

LABEL "project"="vectorizers_tests"
LABEL "author"="lllchak"

RUN apk add --no-cache --virtual .build-deps \
    build-base openssl-dev libffi-dev

RUN pip install --upgrade pip
RUN pip install -r vectorizers_requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "tecode/tokenizers/vectorizers_tests.py" ]
