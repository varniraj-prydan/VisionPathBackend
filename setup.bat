@echo off
echo Setting up Voice Learning Tutor Backend...

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete!
echo.
echo Next steps:
echo 1. Set your Google Cloud credentials in .env file
echo 2. Run: python main.py
echo 3. API will be available at http://localhost:8000