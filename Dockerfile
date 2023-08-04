FROM python:3-slim
ADD . /action

WORKDIR /action

COPY ./Pipfile* ./
RUN pip install pipenv && \
  pipenv install --system --deploy && \
  pipenv --clear

COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]