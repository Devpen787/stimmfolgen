FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir pymupdf==1.28.2
COPY track_2b /app/track_2b
RUN python track_2b/src/gate0/source_probe.py --out /tmp/source.json --pdf-out /app/booklet.pdf
RUN useradd --uid 10001 --create-home stimmfolgen
USER 10001
EXPOSE 8770
CMD ["python", "track_2b/src/app/backend.py", "--source-pdf", "/app/booklet.pdf", "--host", "0.0.0.0", "--port", "8770"]
