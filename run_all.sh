#!/bin/bash

cd "$(dirname "$0")"

# Start all services    
parallel -u ::: 'sh -x ./backend/run_backend.sh' 'sh -x ./frontend/run_frontend.sh'