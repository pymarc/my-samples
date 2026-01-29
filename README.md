# Overview

This repository contains code snippets that showcase my coding style
and serve as handy notes for future reference.

# Docker run command

There are several applications that you can easily execute using Docker.
Thanks to that it's very easy to run them without installing anything.

* Url Fetcher run: `docker compose run --rm --build url_fetcher` with default parameters
  or `docker compose run --rm --build url_fetcher --help` for help
  or `docker compose run --rm --build url_fetcher --urls http://example.com --concurrency 3`
