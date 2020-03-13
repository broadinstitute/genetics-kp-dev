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

        if len(body['message']['query_graph']['edges'])==0:

            queryNodes={}
            for node in body['message']['query_graph']['nodes']:
                queryNodes[node['id']] = 1

            takenNodes={}
            takenSourceTarget={}
            for node in body['message']['query_graph']['nodes']:
                nodeID = node['id']
                if nodeID[0:6] == "MONDO:":
                    diseaseID = nodeID
                    cursor.execute("select GENE,ID,PVALUE from MAGMA_GENES where DISEASE='{}' ORDER by PVALUE ASC".format(diseaseID))
                    results = cursor.fetchall()
                    if not results:
                        continue

                    for record in results:
                        geneID = record[0]
                        edgeID = record[1]
                        pvalue = record[2]
                        if diseaseID + "-" + geneID in takenSourceTarget:
                            continue

                        if 'results' not in body:
                             body['results'] = {}
                             body['results']['nodes'] = []
                             body['results']['edges'] = []
                             body['results']['node_bindings'] = []
        
                        body['results']['edges'].append({"id" : edgeID, "source_id": diseaseID, "target_id" : geneID, "score_name" : "MAGMA-pvalue", "score" : pvalue, "score_direction" : "smaller_is_better" })
                        takenSourceTarget[diseaseID + "-" + geneID] = 1

                        if not diseaseID in takenNodes:
                             body['results']['nodes'].append({"id" : diseaseID, "type" : "gene"})
                             takenNodes[diseaseID] = 1

                             if diseaseID in queryNodes:
                                 body['results']['node_bindings'].append({"qg_id" : diseaseID, "kg_id" : diseaseID})                
                             
                             if geneID in queryNodes:
                                 body['results']['node_bindings'].append({"qg_id" : geneID, "kg_id" : geneID})                
                                  
               # elif node['id'][0:4] == "EFO:":
               # elif node['id'][0:9] == "NCBIGene:":
               # elif node['id'][0:3] == "GO:":
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
                  #  body['results']['nodes'] = []
                  #  body['results']['edges'] = []
                    body['results']['node_bindings'] = []
                    body['results']['edge_bindings'] = []
                body['results']['edge_bindings'].append({"qg_id" : edge['id'], "kg_id" : ksID, "score_name" : "P-value", "score" : pvalue })
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
                    body['results']['edge_bindings'] = []
                    body['results']['node_bindings'] = []
                body['results']['edge_bindings'].append({"qg_id" : edge['id'], "kg_id" : ksID, "score_name" : "Genomics-score", "score" : pvalue, "score_direction" : "higher_is_better" })
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
                    body['results']['edge_bindings'] = []
                    body['results']['node_bindings'] = []
                body['results']['edge_bindings'].append({"qg_id" : edge['id'], "kg_id" : ksID, "score_name" : "P-value", "score" : pvalue })
                takenNodes[edge['source_id']] = 1;
                takenNodes[edge['target_id']] = 1;
    
            for node in body['message']['query_graph']['nodes']:
                if node['id'] in takenNodes:
                    body['results']['node_bindings'].append({"qg_id" : node['id'], "kg_id" : node['id']})                
        return body

    cnx.close() 
    return({"status": 400, "title": "body content not JSON", "detail": "Required body content is not JSON", "type": "about:blank"}, 400)
