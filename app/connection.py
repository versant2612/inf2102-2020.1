import os
import logging

# Inicialização da variável que guarda o logger do módulo
logger = logging.getLogger(__name__)

AGRAPH_HOST = os.environ.get('AGRAPH_HOST')
AGRAPH_PORT = int(os.environ.get('AGRAPH_PORT', '10035'))
AGRAPH_USER = os.environ.get('AGRAPH_USER')
AGRAPH_PASSWORD = os.environ.get('AGRAPH_PASSWORD')

from franz.openrdf.connect import ag_connect
try:
    lattes_alunos = ag_connect('carga-lattes-alunos')
    lattes_profs1 = ag_connect('carga-lattes-professores') 
    lattes_profs2 = ag_connect('carga-lattes-professores2')
    matriculas_puc =  ag_connect('matriculas_puc_etl')
except Exception as e:
    print("Exception : ", e)
    logger.error('Aconteceu alguma excecao na conexao com o banco: %s', e)