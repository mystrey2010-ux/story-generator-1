# Run the story generator Flask application

echo "Starting Story Generator Flask Application..."

# Source conda to ensure it's initialized
source /home/mattwakeling/miniconda3/etc/profile.d/conda.sh

# Activate conda environment
conda activate story-generator-1

# Run the application directly (no flask run = no dotenv tip)
python app.py