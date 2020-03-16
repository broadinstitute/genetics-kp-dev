import connexion
import six
import mysql.connector


from openapi_server.models.message import Message  # noqa: E501
from openapi_server import util


def query(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: dict | bytes

    :rtype: Message
    """
    cnx = mysql.connector.connect(database='Translator')
    cursor = cnx.cursor()

    if connexion.request.is_json:
        body = connexion.request.get_json()

        if len(body['message']['query_graph']['nodes'])==2 and len(body['message']['query_graph']['edges'])==1 and \
               'type' in body['message']['query_graph']['edges'][0] and body['message']['query_graph']['edges'][0]['type'] == 'associated' and\
               'type' in body['message']['query_graph']['nodes'][0] and 'curie' in body['message']['query_graph']['nodes'][0] and\
               'type' in body['message']['query_graph']['nodes'][1]:

            sourceID   = body['message']['query_graph']['nodes'][0]['curie']
            qeID       = body['message']['query_graph']['edges'][0]['id']
            qn0ID      = body['message']['query_graph']['nodes'][0]['id']
            qn1ID      = body['message']['query_graph']['nodes'][1]['id']
            sourceType = body['message']['query_graph']['nodes'][0]['type']
            targetType = body['message']['query_graph']['nodes'][1]['type']

            N = 0
            info    = []
            queries = []

            if (sourceType == 'disease' or sourceType == 'phenotype') and targetType == 'gene':
                N = 2
                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["Genetics-quantile", "higher_is_better"]]
                queries = ["select GENE,ID,PVALUE from MAGMA_GENES where DISEASE='{}' and PVALUE<2.5e-6 ORDER by PVALUE  ASC".format(sourceID),\
                           "select GENE,ID,SCORE  from SCORE_GENES where DISEASE='{}' and SCORE >0.95   ORDER by SCORE  DESC".format(sourceID)]

            elif (sourceType == 'disease' or sourceType == 'phenotype') and targetType == 'pathway':
                N = 1
                info = [["MAGMA-pvalue", "smaller_is_better"]]
                queries = ["select PATHWAY,ID,PVALUE from MAGMA_PATHWAYS where DISEASE='{}' and PVALUE<2.0e-6 ORDER by PVALUE ASC".format(sourceID)]

            elif sourceType == 'gene' and (targetType == 'disease' or sourceType == 'phenotype'):
                N = 2
                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["Genetics-quantile", "higher_is_better"]]
                queries = ["select DISEASE,ID,PVALUE from MAGMA_GENES where GENE='{}' and PVALUE<0.05 ORDER by PVALUE ASC".format(sourceID),\
                           "select DISEASE,ID,SCORE  from SCORE_GENES where GENE='{}' and SCORE >0.80 ORDER by SCORE DESC".format(sourceID)]

            elif sourceType == 'pathway' and (targetType == 'disease' or sourceType == 'phenotype'):
                N = 1
                info = [["MAGMA-pvalue", "smaller_is_better"]]
                queries = ["select DISEASE,ID,PVALUE from MAGMA_PATHWAY where PATHWAY='{}' and PVALUE<0.05 ORDER by PVALUE ASC".format(sourceID)]

            if N > 0:
                for i in range(0, N):
                    cursor.execute(queries[i])
                    results = cursor.fetchall()
                    if results:
                        for record in results:
                            targetID = record[0]
                            edgeID   = record[1]
                            score   = record[2]
                            if 'results' not in body:
                                body['results'] = []
                                body['knowledge_graph'] = {}
                                body['knowledge_graph']['nodes'] = []
                                body['knowledge_graph']['edges'] = []
                                body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : sourceType})
                            body['knowledge_graph']['nodes'].append({"id" : targetID, "type" : targetType})
                            body['knowledge_graph']['edges'].append({"id" : edgeID, "source_id": sourceID, "target_id" : targetID, "score_name" : info[i][0], "score" : score, "score_direction" : info[i][1], "type" : "associated"})
                            body['results'].append({"edge_bindings": [ {"kg_id": edgeID, "qg_id": qeID} ], "node_bindings": [ { "kg_id": sourceID, "qg_id": qn0ID }, { "kg_id": targetID, 'qg_id': qn1ID } ] })

        #explortory queries - only nodes are provided
        elif len(body['message']['query_graph']['edges'])==0:

            queryNodes={}
            for node in body['message']['query_graph']['nodes']:
                queryNodes[node['id']] = 1

            takenNodes={}
            takenSourceTarget={}
            for node in body['message']['query_graph']['nodes']:
                nodeID = node['id']

                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["MAGMA-pvalue", "smaller_is_better"],\
                        ["Genetics-quantile", "higher_is_better"]]


                #disease and phenotype to genes and pathways with magma and genetics score
                if nodeID[0:6] == "MONDO:" or node['id'][0:4] == "EFO:":
                    sourceID = nodeID
                    queries = ["select    GENE,ID,PVALUE from MAGMA_GENES    where DISEASE='{}' and PVALUE<2.5e-6 ORDER by PVALUE  ASC".format(sourceID),\
                               "select PATHWAY,ID,PVALUE from MAGMA_PATHWAYS where DISEASE='{}' and PVALUE<2.0e-6 ORDER by PVALUE  ASC".format(sourceID),\
                               "select    GENE,ID,SCORE  from SCORE_GENES    where DISEASE='{}' and SCORE >0.95  ORDER by SCORE  DESC".format(sourceID)]

                    for i in range(0, 3):
                        cursor.execute(queries[i])
                        results = cursor.fetchall()
                        if results:
                            for record in results:
                                targetID = record[0]
                                edgeID   = record[1]
                                pvalue   = record[2]
                                if sourceID + "-" + targetID in takenSourceTarget:
                                    continue
                                if 'results' not in body:
                                    body['results'] = {}
                                    body['results']['node_bindings'] = []
                                    body['knowledge_graph'] = {}
                                    body['knowledge_graph']['nodes'] = []
                                    body['knowledge_graph']['edges'] = []
                                body['knowledge_graph']['edges'].append({"id" : edgeID, "source_id": sourceID, "target_id" : targetID, "score_name" : info[i][0], "score" : pvalue, "score_direction" : info[i][1], "type" : "associated"})
                                takenSourceTarget[sourceID + "-" + targetID] = 1
                                if not sourceID in takenNodes:
                                    takenNodes[sourceID] = 1
                                    if sourceID[0:6] == "MONDO:":
                                        body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : "disease"})
                                    else:
                                        body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : "phenotype"})
                                    if sourceID in queryNodes:
                                        body['results']['node_bindings'].append({"qg_id" : sourceID, "kg_id" : sourceID})                
                                if not targetID in takenNodes:
                                    takenNodes[targetID] = 1
                                    if targetID[0:9] == "NCBIGene:":
                                        body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : "gene"})
                                    else:
                                        body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : "pathway"})
                                    if targetID in queryNodes:
                                        body['results']['node_bindings'].append({"qg_id" : targetID, "kg_id" : targetID})                
                                  
                #genes and pathways to disease and  phenotype with magma and genetics score
                elif node['id'][0:9] == "NCBIGene:" or node['id'][0:3] == "GO:":
                    targetID = nodeID
                    queries = ["select DISEASE,ID,PVALUE from MAGMA_GENES    where    GENE='{}' and PVALUE<0.05 ORDER by PVALUE  ASC".format(targetID),\
                               "select DISEASE,ID,PVALUE from MAGMA_PATHWAYS where PATHWAY='{}' and PVALUE<0.05 ORDER by PVALUE  ASC".format(targetID),\
                               "select DISEASE,ID,SCORE  from SCORE_GENES    where    GENE='{}' and SCORE> 0.80 ORDER by SCORE  DESC".format(targetID)]

                    for i in range(0, 3):
                        cursor.execute(queries[i])
                        results = cursor.fetchall()
                        if results:
                            for record in results:
                                sourceID = record[0]
                                edgeID   = record[1]
                                pvalue   = record[2]
                                if sourceID + "-" + targetID in takenSourceTarget:
                                    continue
                                if 'results' not in body:
                                    body['results'] = {}
                                    body['results']['node_bindings'] = []
                                    body['knowledge_graph'] = {}
                                    body['knowledge_graph']['nodes'] = []
                                    body['knowledge_graph']['edges'] = []
                                body['knowledge_graph']['edges'].append({"id" : edgeID, "source_id": sourceID, "target_id" : targetID, "score_name" : info[i][0], "score" : pvalue, "score_direction" : info[i][1] })
                                takenSourceTarget[sourceID + "-" + targetID] = 1
                                if not sourceID in takenNodes:
                                    takenNodes[sourceID] = 1
                                    if sourceID[0:9] == "NCBIGene:":
                                        body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : "gene"})
                                    else:
                                        body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : "pathway"})
                                    if sourceID in queryNodes:
                                        body['results']['node_bindings'].append({"qg_id" : sourceID, "kg_id" : sourceID})                
                                if not targetID in takenNodes:
                                    takenNodes[targetID] = 1
                                    if targetID[0:6] == "MONDO:":
                                        body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : "disease"})
                                    else:
                                        body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : "phenotype"})
                                    if targetID in queryNodes:
                                        body['results']['node_bindings'].append({"qg_id" : targetID, "kg_id" : targetID})                
                else:
                    continue
            
        else:
            #Add gene edges with Magma score
            takenNodes = {}
            for edge in body['message']['query_graph']['edges']:
                if (edge['source_id'][0:6] == "MONDO:" or edge['source_id'][0:4] == "EFO:") and edge['target_id'][0:9] == "NCBIGene:":
                    diseaseID = edge['source_id']
                    geneID = edge['target_id']
                elif edge['source_id'][0:9] == "NCBIGene:" and (edge['target_id'][0:6] == "MONDO:" or edge['target_id'][0:4] == "EFO:"):
                    diseaseID = edge['source_id']
                    geneID = edge['target_id']
                else:
                    continue
                cursor.execute("select ID,PVALUE from MAGMA_GENES where GENE='{}' and DISEASE='{}'".format(geneID,diseaseID))
                result = cursor.fetchall()
                if not result:
                    continue
                ksID   = result[0][0]
                pvalue = result[0][1]
                if 'results' not in body:
                    body['results'] = {}
                    body['results']['node_bindings'] = []
                    body['results']['edge_bindings'] = []
                    body['knowledge_graph'] = {}
                    body['knowledge_graph']['nodes'] = []
                    body['knowledge_graph']['edges'] = []
                body['knowledge_graph']['edges'].append({"id" : ksID, "source_id": diseaseID, "target_id" : geneID, "score_name" : "P-value", "score" : pvalue, "score_direction": "smaller_is_better", "type": "associated"})
                body['results']['edge_bindings'].append({"qg_id" : edge['id'], "kg_id" : ksID})
                takenNodes[edge['source_id']] = 1;
                takenNodes[edge['target_id']] = 1;
    
            #Add gene edges with Genomics score
            for edge in body['message']['query_graph']['edges']:
                if (edge['source_id'][0:6] == "MONDO:" or edge['source_id'][0:4] == "EFO:") and edge['target_id'][0:9] == "NCBIGene:":
                    diseaseID = edge['source_id']
                    geneID = edge['target_id']
                elif edge['source_id'][0:9] == "NCBIGene:" and (edge['target_id'][0:6] == "MONDO:" or edge['target_id'][0:4] == "EFO:"):
                    diseaseID = edge['source_id']
                    geneID = edge['target_id']
                else:
                    continue
                cursor.execute("select ID,SCORE from SCORE_GENES where GENE='{}' and DISEASE='{}'".format(geneID,diseaseID))
                result = cursor.fetchall()
                if not result:
                    continue
                ksID   = result[0][0]
                pvalue = result[0][1]
                if 'results' not in body:
                    body['results'] = {}
                    body['results']['node_bindings'] = []
                    body['results']['edge_bindings'] = []
                    body['knowledge_graph'] = {}
                    body['knowledge_graph']['nodes'] = []
                    body['knowledge_graph']['edges'] = []
                body['knowledge_graph']['edges'].append({"id" : ksID, "source_id": diseaseID, "target_id" : geneID, "score_name" : "quantile", "score" : pvalue, "score_direction" : "higher_is_better", "type" : "associated"})
                body['results']['edge_bindings'].append({"qg_id" : edge['id'], "kg_id" : ksID})
                takenNodes[edge['source_id']] = 1;
                takenNodes[edge['target_id']] = 1;
    
            #Add pathway edges wth Magma score
            for edge in body['message']['query_graph']['edges']:
                if (edge['source_id'][0:6] == "MONDO:" or edge['source_id'][0:4] == "EFO:") and edge['target_id'][0:3] == "GO:":
                    diseaseID = edge['source_id']
                    pathwayID = edge['target_id']
                elif edge['source_id'][0:3] == "GO:" and (edge['target_id'][0:6] == "MONDO:" or edge['target_id'][0:4] == "EFO:"):
                    diseaseID = edge['source_id']
                    pathwayID = edge['target_id']
                else:
                    continue
                cursor.execute("select ID,PVALUE from MAGMA_PATHWAYS where PATHWAY='{}' and DISEASE='{}'".format(pathwayID,diseaseID))
                result = cursor.fetchall()
                if not result:
                    continue
                ksID   = result[0][0]
                pvalue = result[0][1]
                if 'results' not in body:
                    body['results'] = {}
                    body['results']['node_bindings'] = []
                    body['results']['edge_bindings'] = []
                    body['knowledge_graph'] = {}
                    body['knowledge_graph']['nodes'] = []
                    body['knowledge_graph']['edges'] = []
                body['knowledge_graph']['edges'].append({"id" : ksID, "source_id": diseaseID, "target_id" : geneID, "score_name" : "P-value", "score" : pvalue , "score_direction": "smaller_is_better", "type" : "associated"})
                body['results']['edge_bindings'].append({"qg_id" : edge['id'], "kg_id" : ksID})
                takenNodes[edge['source_id']] = 1;
                takenNodes[edge['target_id']] = 1;
    
            for node in body['message']['query_graph']['nodes']:
                nid = node['id']
                if nid in takenNodes:
                    if nid[0:6] == "MONDO:":
                        ntype = "disease"
                    elif nid[0:4] == "EFO:":
                        ntype = "phenotype"
                    elif nid[0:3] == "GO:":
                        ntype = "pathway"
                    elif nid[0:9] == "NCBIGene:":
                        ntype = "gene"
                    else:
                        ntype = ""
                    body['results']['node_bindings'].append({"qg_id" : node['id'], "kg_id" : node['id']})
                    body['knowledge_graph']['nodes'].append({"id" : node['id'], "type" : ntype})
        return body

    cnx.close() 
    return({"status": 400, "title": "body content not JSON", "detail": "Required body content is not JSON", "type": "about:blank"}, 400)
