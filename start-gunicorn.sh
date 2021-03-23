#!/bin/bash

gunicorn app:app -b localhost:9898 --timeout=600 --daemon
