# biobd-nima

## FLASK

All commands must be executed in the command line or anaconda command line (windows). All commands should be executed inside the project folder unless stated otherwise.

# Environment 

## Create 
```
conda create --name nima python
```
## Activate

### Linux
```
source activate nima
```

### Windows
```
activate nima
```

## Install packages (after activating the environment)

```
pip install -r requirements.txt
```

# Configuring development environment variables

## Linux

```
export FLASK_APP=run.py
export FLASK_CONFIG=development
```

## Windows

```
SET FLASK_APP=run.py
SET FLASK_CONFIG=development
```

# Run in development

```
flask run
```

# Suggested 'IDE'

[Visual studio code](https://code.visualstudio.com/)

[Sublime](https://www.sublimetext.com/3)

[Notepad ++](https://notepad-plus-plus.org/)

# Tutorial flask - windows

O primeiro passo para começar a usar o python é instalar o [anaconda](https://repo.continuum.io/archive/Anaconda3-4.4.0-Windows-x86_64.exe).

Agora você deve criar uma pasta para o projeto do tutorial (flask_tutorial) e
adicionar um arquivo requirements.txt com os pacotes necessários à pasta criada.

Feito isso abra o command line anaconda, vá até a pasta criada com cd
e dir e acesse o ambiente com
```
activate nima
```

Agora basta instalar os pacotes do tutorial com 
```
pip install -r requirements.txt
``` 

e seguir os 3 tutoriais abaixo, substituindo export
por SET e podendo pular os pip install.

[Parte "0" (Começar do Say "Hello World!" with Flask)](https://scotch.io/tutorials/getting-started-with-flask-a-python-microframework), 
[Parte 1](https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one), 
[Parte 2]( https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-two)
