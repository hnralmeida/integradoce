## Prefixo do namespace esta sendo alterado para ns2 (??)

## Função de mesclagem não está funcionando devidamente

from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from datetime import datetime
from rdflib.namespace import XSD

doce = URIRef("http://purl.org/nemo/doce#")
DOCE = Namespace(doce)
ex = URIRef("http://purl.org/nemo/integradoce#")
DOCEEX = Namespace(ex)
wgs = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#")
WGS = Namespace(wgs)
owl = URIRef("http://www.w3.org/2002/07/owl#")
OWL = Namespace(owl)
gufo = URIRef("http://purl.org/nemo/gufo#")
GUFO = Namespace(gufo)
xsd = URIRef("http://www.w3.org/2001/XMLSchema#")
XSD = Namespace(xsd)

# =================================== TEMPO ===================================
#
#
## Função 1 - Medições por período de tempo
def pesqTempo (graph, ini, fin):
    x = Graph()
    for s1, p1, o1 in graph.triples((None, RDF.type, DOCE.Measurement)) :
        for s2, p2, o2 in graph.triples((s1, GUFO.hasBeginPointInXSDDateTimeStamp, None)) :
            dateo2 = str(o2)
            dateo2 = dateo2.replace('-0200', '') # sufixo com significado desconhecido pelos autores
            dateo2 = dateo2.replace('-0300', '') # sufixo com significado desconhecido pelos autores
            dateComp = datetime.fromisoformat(dateo2)
            if ((dateComp.year >= ini.year) and (dateComp.year <= fin.year) and (dateComp.month >= ini.month) and 
                (dateComp.month <= fin.month) and (dateComp.day >= ini.day) and (dateComp.day <= fin.day)) :
                for s21, p21, o21 in graph.triples((s1, GUFO.hasEndPointInXSDDateTimeStamp, None)) :
                    dateo2 = str(o21)
                    dateo2 = dateo2.replace('-0200', '') # sufixo com significado desconhecido pelos autores
                    dateo2 = dateo2.replace('-0300', '') # sufixo com significado desconhecido pelos autores
                    dateComp = datetime.fromisoformat(dateo2)
                    if ((dateComp.year >= ini.year) and (dateComp.year <= fin.year) and (dateComp.month >= ini.month) and 
                (dateComp.month <= fin.month) and (dateComp.day >= ini.day) and (dateComp.day <= fin.day)) :
                        x.add((s1, p1, o1))
                        for s3, p3, o3 in graph.triples((None, GUFO.participatedIn, s1)) :
                            x.add((s3, p3, o3))
                        for s3, p3, o3 in graph.triples((s1, DOCE.locatedIn, None)) :
                            x.add((s3, p3, o3))
                        for s3, p3, o3 in graph.triples((s1, DOCE.measured, None)) :
                            x.add((s3, p3, o3))
                        for s3, p3, o3 in graph.triples((s1, DOCE.measuredQualityKind, None)) :
                            x.add((s3, p3, o3))
                        for s3, p3, o3 in graph.triples((s1, DOCE.expressedIn, None)) :
                            x.add((s3, p3, o3))
                        for s3, p3, o3 in graph.triples((s1, GUFO.hasQualityValue, None)) :
                            x.add((s3, p3, o3))
                    x.add((s21, p21, o21))
                    x.add((s2, p2, o2))

    return x

#  =================================== REGIÃO ===================================
#
#
## Função 2 - Medições por região geográfica
## Problema com comparação de wgs.lat e wgs.long
def pesqLocalizacao(graph, latMin, latMax, longMin, longMax):
    x = Graph()
    flag = 1
    for s1, p1, o1 in graph.triples((None, None, DOCE.GeographicPoint)) :
        for s2, p2, o2 in graph.triples((s1, WGS.lat, None)) :
            lat = Literal(o2, datatype=XSD.float)
            print(lat, lat < latMax)
            print(type(lat), lat > latMin)
            print("____")
            if lat < latMax and lat > latMin :
                for s3, p3, o3 in graph.triples((s1, WGS.long, None)) :
                    if o3 < longMax and o3 > longMin :
                        for s4, p4, o4 in graph.triples((None, DOCE.locatedIn, s1)) :
                            for s5, p5, o5 in graph.triples((s4, RDF.type, DOCE.Measurement)) :
                                x.add((s5, p5, o5))
                                flag=0
                                for s6, p6, o6 in graph.triples((None, GUFO.participatedIn, s5)) :
                                    x.add((s6, p6, o6))
                                x.add((s1, p1, o1))
                                for s6, p6, o6 in graph.triples((s5, DOCE.measuredQualityKind, None)) :
                                    x.add((s6, p6, o6))
                                    for s7, p7, o7 in graph.triples((s5, DOCE.expressedIn, None)) :
                                        x.add((s7, p7, o7))
                                    for s3, p3, o3 in graph.triples((s1, DOCE.measured, None)) :
                                        x.add((s3, p3, o3))
                                    for s7, p7, o7 in graph.triples((s5, DOCE.hasQualityValue, None)) :
                                        x.add((s7, p7, o7))
                                    for s7, p7, o7 in graph.triples((s5, DOCE.hasBeginPointInXSDDateTimeStamp, None)) :
                                        x.add((s7, p7, o7))

    if flag :
        print("\nNão foram encontrados resultados")
    return x

#  =================================== QUALIDADE ===================================
#
#
## Função 3 - Medições por tipo de qualidade
def pesqQualidade(exampleTriple, qualk):
    x = Graph()
    for s1, p1, o1 in exampleTriple.triples((None, RDF.type, DOCE.Measurement)) :
        for s2, p2, o2 in exampleTriple.triples((s1, DOCE.measuredQualityKind, None)) :
            med = str(o2)
            med = med.replace(str(DOCE),"")
            if qualk in med :
                x.add((s1, p1, o1))
                for s3,p3,o3 in exampleTriple.triples((None, GUFO.participatedIn, s1)) :
                    x.add((s3, p3, o3))
                for s3,p3,o3 in exampleTriple.triples((s1, DOCE.locatedIn, None)) :
                    x.add((s3, p3, o3))
                x.add((s2, p2, o2))
                for s3,p3,o3 in exampleTriple.triples((s1, DOCE.expressedIn, None)) :
                    x.add((s3, p3, o3))
                for s3, p3, o3 in exampleTriple.triples((s1, DOCE.measured, None)) :
                    x.add((s3, p3, o3))
                for s3,p3,o3 in exampleTriple.triples((s1, GUFO.hasQualityValue, None)) :
                    x.add((s3, p3, o3))
                for s3,p3,o3 in exampleTriple.triples((s1, GUFO.hasBeginPointInXSDDateTimeStamp, None)) :
                    x.add((s3, p3, o3))
    return x

# =================================== AGENTE ===================================
#
#
## Função 4 - Medições por agente responsável
def PesqAgent(exampleTriple, pesquisa):
    x= Graph()
    for s1, p1, o1 in exampleTriple.triples((None, RDF.type , DOCE.Agent)) :
        lab = str(s1)
        lab = lab.replace(str(DOCEEX),"")
        if pesquisa in lab :
            for s2, p2, o2 in exampleTriple.triples((s1, GUFO.participatedIn, None)) :
                med = str(o2)
                med = med.replace(str(DOCEEX),"")
                x.add((o2, RDF.type, DOCE.Measurement))
                x.add((s2, p2, o2))
                for s3, p3, o3 in exampleTriple.triples((o2, DOCE.locatedIn, None)) :
                    x.add((s3, p3, o3))
                for s3, p3, o3 in exampleTriple.triples((o2, DOCE.measuredQualityKind, None)) :
                    x.add((s3, p3, o3))
                for s3, p3, o3 in exampleTriple.triples((s1, DOCE.measured, None)) :
                    x.add((s3, p3, o3))
                for s3, p3, o3 in exampleTriple.triples((o2, DOCE.expressedIn, None)) :
                    x.add((s3, p3, o3))
                for s3, p3, o3 in exampleTriple.triples((o2, GUFO.hasQualityValue, None)) :
                    x.add((s3, p3, o3))
                for s3, p3, o3 in exampleTriple.triples((o2, GUFO.hasBeginPointInXSDDateTimeStamp, None)) :
                    x.add((s3, p3, o3))
    return x


x= Graph()
y= Graph()
x.parse("unespInst.ttl", format = "ttl")
ini= datetime.fromisoformat("2016-01-01")
fin= datetime.fromisoformat("2016-12-31")
y= pesqTempo(x, ini,fin)
y= pesqQualidade(x, "Aluminium")
y.serialize(destination="pesqMesc.ttl")
