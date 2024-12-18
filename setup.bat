@echo off
:: Ensure Python is installed and available
python --version

:: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

:: Inform the user the installation is complete
echo Installation complete!

:: Pause to keep the window open
pause
