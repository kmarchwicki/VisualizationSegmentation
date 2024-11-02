#!/bin/bash

cd "$(dirname "$(realpath "$0")")"
source $(pwd)/../.env

# Start frontend application    
npm i && npm start