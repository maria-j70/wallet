FROM python:3.9
COPY . .
RUN --mount=type=cache,target=/root/.cache pip install -r req.txt
