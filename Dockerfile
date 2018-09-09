FROM python:3.6 as builder

# RUN apk update && apk add build-base python-dev libffi-dev openssl-dev git

RUN mkdir /build
WORKDIR /build

# COPY requirements.txt /build/
# RUN pip install -r requirements.txt

COPY . /build
# RUN pytest -v

RUN pip install --install-option="--prefix=/install" .

FROM python:3.6-alpine

COPY --from=builder /install /usr/local
