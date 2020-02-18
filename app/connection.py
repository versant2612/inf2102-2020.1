import os
AGRAPH_HOST = os.environ.get('AGRAPH_HOST')
AGRAPH_PORT = int(os.environ.get('AGRAPH_PORT', '10035'))
AGRAPH_USER = os.environ.get('AGRAPH_USER')
AGRAPH_PASSWORD = os.environ.get('AGRAPH_PASSWORD')

from franz.openrdf.connect import ag_connect
lattes = ag_connect('carga-lattes-alunos')
lattes21 = ag_connect('carga-lattes-professores') 
lattes22 = ag_connect('carga-lattes-professores2')