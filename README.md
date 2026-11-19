# Overview

This repository contains code snippets that showcase my coding style
and serves as a handy reference for the future.

## Applications

In the repository there are these applications:

- **URL Fetcher** (`samples/url_fetcher`) - asynchronously fetch basic information about specified URLs
- **Web Images Checker** (`samples/web_images_checker`) - a FastAPI service that queues image analysis jobs
  using Celery and Redis
- **Events API** (`samples/events_api`) - an async FastAPI service backed by PostgreSQL
  to handle hypothetical events
- **AI demos** (`samples/ai`) - tokenization and OpenAI embeddings
- **Time Machine Helpdesk** (`samples/time_machine_helpdesk`) - an LLM chat which gives answers
  based on the attached documentation

The Docker Compose configuration currently supports the URL Fetcher and Web Images Checker.
The other samples are run locally.

# Docker run commands

There are several applications that you can easily execute using Docker.
Thanks to that it's very easy to run them without installing anything.

- **Url Fetcher run app**: `docker compose run --rm --build url_fetcher` with default parameters
  or `docker compose run --rm --build url_fetcher --help` for help
  or `docker compose run --rm --build url_fetcher --urls http://example.com --concurrency 3`
- **Url Fetcher run tests**: `docker compose run --rm --build url_fetcher_tests`
- **Web Images Checker start the service**: `docker compose up --build api-web_images_checker`
