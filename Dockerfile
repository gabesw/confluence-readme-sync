FROM python:3-slim
# Tells pipenv to create virtualenvs in /root rather than $HOME/.local/share.
# We do this because GitHub modifies the HOME variable between `docker build` and
# `docker run`
ENV WORKON_HOME /root

# Tells pipenv to use this specific Pipfile rather than the Pipfile in the 
# current working directory (the working directory changes between `docker build` 
# and `docker run`, this ensures we always use the same Pipfile)
ENV PIPENV_PIPFILE /Pipfile
ADD . /action

WORKDIR /action

COPY ./Pipfile* ./
RUN pip install pipenv && \
  pipenv install --system --deploy && \
  pipenv --clear

COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]