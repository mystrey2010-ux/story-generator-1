#!/bin/bash

# Run the story generator Flask application

echo "Starting Story Generator Flask Application..."

# Source conda to ensure it's initialized
source /home/mattwakeling/miniconda3/etc/profile.d/conda.sh

# Activate conda environment
conda activate story-generator-1

# Set Flask application
export FLASK_APP=app.py
export FLASK_ENV=development

# Run the application using the activated Python
python -m flask run --host=0.0.0.0 --port=5000