rem CALL C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3
CALL C:\Users\Vika\anaconda3\Scripts\activate.bat C:\Users\Vika\anaconda3
CALL conda activate nima
SET FLASK_APP=run.py
SET FLASK_CONFIG=development
SET FLASK_DEBUG=1
SET AGRAPH_HOST=localhost
SET AGRAPH_PORT=10035
SET AGRAPH_USER=nima
SET AGRAPH_PASSWORD=nima2019
flask run
pause