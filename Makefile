ARCHITECTURE = $(shell uname -m)
OS = $(shell uname -s)

ifeq ($(ARCHITECTURE),arm64)
	ARM = true
	IMG_ARCH = arm64
else
	ARM = false
	IMG_ARCH = amd64
endif

.PHONY: dev
dev:
	uv run -- manage.py runserver


arch_env:
	@echo ARCHITECTURE=$(ARCHITECTURE) OS=$(OS) ARM=$(ARM)

dev_full:
	ARM=$(ARM) OS=$(OS) IMG_ARCH=$(IMG_ARCH) docker compose up mailhog
