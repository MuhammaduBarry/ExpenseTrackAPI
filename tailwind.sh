#!/bin/bash

echo 'Starting tailwindcss....'
npx @tailwindcss/cli -i ./app/static/css/input.css -o ./app/static/css/output.css --watch