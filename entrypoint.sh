#!/bin/bash

alembic upgrade head

python runserver.py