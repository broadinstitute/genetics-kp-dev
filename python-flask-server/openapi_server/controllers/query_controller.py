import connexion
import six
import pymysql
# import mysql.connector

from openapi_server.models.response import Response  # noqa: E501
# from openapi_server.models.message import Message  # noqa: E501
from openapi_server import util


def queryOld(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: dict | bytes

    :rtype: Message
    """
    return 'do some magic!'

def query(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: Response
    """
    # cnx = mysql.connector.connect(database='Translator', user='mvon')
    cnx = pymysql.connect(host='localhost', port=3306, database='Translator', user='mvon')
    # cnx = pymysql.connect(host='localhost', port=3306, database='tran_genepro', user='root', password='this aint no password')
    cursor = cnx.cursor()

    if connexion.request.is_json:
        body = connexion.request.get_json()
        print("got {}".format(body))
        takenNodes = {}
        takenEdges = {}

        body['results'] = []
        body['knowledge_graph'] = {}
        body['knowledge_graph']['nodes'] = []
        body['knowledge_graph']['edges'] = []
 
        for edge in body['message']['query_graph']['edges']:
            if 'type' not in edge or edge['type'] != 'associated' or 'source_id' not in edge or 'target_id' not in edge:
                continue
            
            sourceNode = 0;
            for node in body['message']['query_graph']['nodes']:
                if 'id' in node and node['id'] == edge['source_id']:
                    sourceNode = node
                    break

            if sourceNode == 0 or 'type' not in sourceNode or 'curie' not in sourceNode:
                continue

            targetnode = 0;
            for node in body['message']['query_graph']['nodes']:
                if 'id' in node and node['id'] == edge['target_id']:
                    targetNode = node
                    break

            if targetNode == 0 or 'type' not in targetNode:
                continue
        
            qeID       = edge['id']
            sourceID   = sourceNode['curie']
            qn0ID      = sourceNode['id']
            qn1ID      = targetNode['id']
            sourceType = sourceNode['type']
            targetType = targetNode['type']

            # N = 0
            info    = []
            queries = []

            # log
            print("running query for source type: {} and source_id: {} and target type: {}".format(sourceType, sourceID, targetType))

            # queries
            if (sourceType == 'disease' or sourceType == 'phenotypic_feature') and targetType == 'gene':
                # N = 2
                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["Richards-effector-genes", "higher_is_better"],\
                        ["ABC-genes", "not_displayed"],\
                        ["Genetics-quantile", "higher_is_better"]]
                queries = ["select GENE,ID,PVALUE from MAGMA_GENES where DISEASE='{}' and CATEGORY='{}' and PVALUE<2.5e-6 ORDER by PVALUE  ASC".format(sourceID,sourceType),\
                           "select gene, id, probability from richards_gene where phenotype='{}' and category='{}' ORDER by probability desc".format(sourceID,sourceType),\
                           "select gene_ncbi_id, edge_id, null from abc_gene_phenotype where phenotype_efo_id='{}' and category='{}' and gene_ncbi_id is not null order by edge_id".format(sourceID,sourceType),\
                           "select GENE,ID,SCORE  from SCORE_GENES where DISEASE='{}' and CATEGORY='{}' and SCORE >0.95   ORDER by SCORE  DESC".format(sourceID,sourceType)]

            elif (sourceType == 'disease' or sourceType == 'phenotypic_feature') and targetType == 'pathway':
                # N = 1
                info = [["MAGMA-pvalue", "smaller_is_better"]]
                queries = ["select PATHWAY,ID,PVALUE from MAGMA_PATHWAYS where DISEASE='{}' and CATEGORY='{}' and PVALUE<2.0e-6 ORDER by PVALUE ASC".format(sourceID,sourceType)]

            elif sourceType == 'gene' and (targetType == 'disease' or targetType == 'phenotypic_feature'):
                # N = 2
                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["Richards-effector-genes", "higher_is_better"],\
                        ["ABC-genes", "not_displayed"],\
                        ["Genetics-quantile", "higher_is_better"]]
                queries = ["select DISEASE,ID,PVALUE from MAGMA_GENES where GENE='{}' and CATEGORY='{}' and PVALUE<0.05 ORDER by PVALUE ASC".format(sourceID,targetType),\
                           "select phenotype, id, probability from richards_gene where gene='{}' and category='{}' ORDER by probability desc".format(sourceID,targetType),\
                           "select phenotype_efo_id, edge_id, null from abc_gene_phenotype where gene_ncbi_id='{}' and category='{}' and phenotype_efo_id is not null order by edge_id".format(sourceID,targetType),\
                           "select DISEASE,ID,SCORE  from SCORE_GENES where GENE='{}' and CATEGORY='{}' and SCORE >0.80 ORDER by SCORE DESC".format(sourceID,targetType)]

            elif sourceType == 'pathway' and (targetType == 'disease' or targetType == 'phenotypic_feature'):
                # N = 1
                info = [["MAGMA-pvalue", "smaller_is_better"]]
                queries = ["select DISEASE,ID,PVALUE from MAGMA_PATHWAYS where PATHWAY='{}' and CATEGORY='{}' and PVALUE<0.05 ORDER by PVALUE ASC".format(sourceID,targetType)]

            if len(queries) > 0:
                for i in range(0, len(queries)):
                    print("running query: {}".format(queries[i]))
                    cursor.execute(queries[i])
                    results = cursor.fetchall()
                    if results:
                        for record in results:
                            targetID  = record[0]
                            edgeID    = record[1]
                            score     = record[2]

                            if sourceID not in takenNodes:
                                body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : sourceType})
                                takenNodes[sourceID] = 1

                            if targetID not in takenNodes:
                                body['knowledge_graph']['nodes'].append({"id" : targetID, "type" : targetType})
                                takenNodes[targetID] = 1

                            if edgeID not in takenEdges: 
                                if score is not None:
                                    body['knowledge_graph']['edges'].append({"id" : edgeID, "source_id": sourceID, "target_id" : targetID, "score_name" : info[i][0], "score" : score, "score_direction" : info[i][1], "type" : "associated"})
                                else:
                                    body['knowledge_graph']['edges'].append({"id" : edgeID, "source_id": sourceID, "target_id" : targetID, "score_name" : info[i][0], "type" : "associated"})
                                takenEdges[edgeID] = 1

                            body['results'].append({"edge_bindings": [ {"kg_id": edgeID, "qg_id": qeID} ], "node_bindings": [ { "kg_id": sourceID, "qg_id": qn0ID }, { "kg_id": targetID, 'qg_id': qn1ID } ] })

        body['query_graph'] = body['message']['query_graph']
        del body['message']
        return body

    cnx.close() 
    return({"status": 400, "title": "body content not JSON", "detail": "Required body content is not JSON", "type": "about:blank"}, 400)
