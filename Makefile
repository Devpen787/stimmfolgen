.PHONY: build run check
IMAGE ?= stimmfolgen:local
PORT ?= 8770
build:
	docker build -t $(IMAGE) .
run: build
	docker run --rm --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m -p 127.0.0.1:$(PORT):8770 $(IMAGE)
check: build
	docker run --rm --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m $(IMAGE) python track_2b/src/app/backend.py --source-pdf /app/booklet.pdf --check

# Apple Silicon local inference. Setup downloads weights only when explicitly requested.
LOCAL_PYTHON ?= .local/runtime/bin/python
APERTUS_PYTHON ?= $(LOCAL_PYTHON)
APP_PORT ?= 8770
MODEL_DIR ?= .local/models/apertus-v1.5-8b-mlx-4bit
SOURCE_PDF ?= .local/local/booklet.pdf
.PHONY: local-setup local-download local-run
local-setup:
	python3 track_2b/tools/local_setup.py
local-download:
	python3 track_2b/tools/local_setup.py --download
local-run:
	$(LOCAL_PYTHON) track_2b/tools/local_run.py --model-python $(APERTUS_PYTHON) --model-dir $(MODEL_DIR) --source-pdf $(SOURCE_PDF) --port $(APP_PORT)
