# Determine the system architecture and operating system
ARCHITECTURE = $(shell uname -m)
OS = $(shell uname -s)

# Set variables based on the architecture
ifeq ($(ARCHITECTURE),arm64)
	ARM = true
	IMG_ARCH = arm64
else
	ARM = false
	IMG_ARCH = amd64
endif

# Define a phony target for development server
.PHONY: dev
dev:
	# Run the development server using uvicorn
	uv run -- manage.py runserver

# Print the architecture and OS environment variables
arch_env:
	@echo ARCHITECTURE=$(ARCHITECTURE) OS=$(OS) ARM=$(ARM)

# Bring up the mailhog service with the appropriate environment variables
dev_full:
	ARM=$(ARM) OS=$(OS) IMG_ARCH=$(IMG_ARCH) docker compose up mailhog

# Run database migrations and create a superuser
migrate:
	# Run migrations
	docker compose run nephele uv run -- manage.py migrate
	# Create a superuser with predefined credentials
	docker compose run -d \
	-e DJANGO_SUPERUSER_USERNAME=admin \
	-e DJANGO_SUPERUSER_PASSWORD=admin \
	-e DJANGO_SUPERUSER_EMAIL=admin@example.com \
	nephele \
	uv run -- manage.py createsuperuser --noinput