Passos para conversão dos arquivos xml do Lattes para RDF

1) No servidor, entrar na pasta /home/cloud-di/lattes_novos

2) Copiar os arquivos recebidos para as respectivas pastas /home/cloud-di/lattes_novos/lattes_alunos-zip e /home/cloud-di/lattes_novos/lattes_professores-zip

3) Limpar as pastas lattes-alunos-rdf, lattes-alunos-xml, lattes-professores2-rdf, lattes-professores-rdf e lattes-professores2-rdf

4) Executar os scripts zip2xml_alunos.sh e xml2rdf_alunos.sh

5) Conferir o conteúdo das pastas lattes-alunos-rdf e lattes-alunos-xml. 
Se a quantidade de arquivos é igual e se os arquivos não estão vazios

6) Executar os scripts zip2xml_professores.sh e xml2rdf_professores.sh

7) Conferir o conteúdo das pastas lattes-professores-rdf, lattes-professores2-rdf e lattes-professores-xml. 
Se a quantidade de arquivos é igual e se os arquivos não estão vazios

Comandos de carga (revisar o nome do repositório em caso de teste)

~/ag-6.4.2/bin/agtool load --port 10035 --input rdfxml lattes-alunos lattes-alunos-rdf/*.rdf
~/ag-6.4.2/bin/agtool load --port 10035 --input rdfxml lattes-professores lattes-professores-rdf/*.rdf
~/ag-6.4.2/bin/agtool load --port 10035 --input rdfxml lattes-professores2 lattes-professores2-rdf/*.rdf

Verificar a quantidade de triplas carregadas em cada repositório e o tempo de carga

A cada carga executada é importante registrar no Blog do NIMA com um post como esse

https://biobdnima.blogspot.com/2020/02/revisao-da-conversao-e-carga-do-lattes.html
