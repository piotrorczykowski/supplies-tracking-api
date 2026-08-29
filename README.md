# Supply Tracking API

A REST API for tracking and managing supplies.

## Prerequisites

* Python 3.12+
* Package manager [uv](https://github.com/astral-sh/uv)

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Install Git Hooks (pre-commit)
uv run pre-commit install

# 3. Apply database migrations
uv run python manage.py migrate

# 4. Start the development server
uv run python manage.py runserver
