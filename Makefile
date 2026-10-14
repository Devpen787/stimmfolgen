.PHONY: build run check
IMAGE ?= stimmfolgen:local
PORT ?= 8770
build:
	docker build -t $(IMAGE) .
run: build
	docker run --rm --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m -p 127.0.0.1:$(PORT):8770 $(IMAGE)
check: build
	docker run --rm --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m $(IMAGE) python track_2b/src/app/backend.py --source-pdf /app/booklet.pdf --check
