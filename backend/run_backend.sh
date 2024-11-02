#!/bin/bash

cd "$(dirname "$(realpath "$0")")"
source $(pwd)/../.env

uvicorn main:app --reload --port $FASTAPI_PORT --host $FASTAPI_HOST