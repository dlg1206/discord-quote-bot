FROM python:3.13-alpine3.22
WORKDIR /app
# install quotebot dependencies
COPY --chown=quotebot:quotebot requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# copy code
COPY --chown=quotebot:quotebot quotebot quotebot
# create user
RUN adduser -H -D quotebot
USER quotebot
# launch bot
ENTRYPOINT ["python3", "quotebot"]