import os
AGRAPH_HOST = os.environ.get('AGRAPH_HOST')
AGRAPH_PORT = int(os.environ.get('AGRAPH_PORT', '10035'))
AGRAPH_USER = os.environ.get('AGRAPH_USER')
AGRAPH_PASSWORD = os.environ.get('AGRAPH_PASSWORD')

from franz.openrdf.connect import ag_connect
lattes_alunos = ag_connect('carga-lattes-alunos')
lattes_profs1 = ag_connect('carga-lattes-professores') 
lattes_profs2 = ag_connect('carga-lattes-professores2')
matriculas_puc =  ag_connect('matriculas_puc_etl')