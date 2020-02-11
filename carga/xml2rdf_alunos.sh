#!/bin/bash

cd lattes-alunos-xml/

echo "Iniciando o script:"

echo "Convertendo os xmls em rdfs..."
for f in *.xml
do
    newFile=${f/${f: -4}/} 

    # need to install libxml2, libxslt
    xsltproc --stringparam ID $newFile lattes_alunos.xsl $f > $newFile".rdf"
done


