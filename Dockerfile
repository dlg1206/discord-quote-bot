FROM python:3-alpine
# Build project
WORKDIR /app
COPY src .
RUN pip install -r requirements.txt
# Launch bot
ENTRYPOINT ["python3", "quotebot"]