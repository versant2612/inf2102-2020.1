rem CALL C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3
CALL C:\Users\Vika\anaconda3\Scripts\activate.bat C:\Users\Vika\anaconda3
CALL conda create --name nima python
CALL conda activate nima
CD docs
CALL pip install -r requirements.txt
pause