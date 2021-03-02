import connexion
import six
import pymysql
import copy
# import mysql.connector

from openapi_server.models.message import Message
from openapi_server.models.knowledge_graph import KnowledgeGraph
from openapi_server.models.edge import Edge
from openapi_server.models.node import Node
from openapi_server.models.result import Result
from openapi_server.models.edge_binding import EdgeBinding
from openapi_server.models.node_binding import NodeBinding
from openapi_server.models.response import Response
from openapi_server.models.attribute import Attribute

from openapi_server import util

from openapi_server.dcc.utils import translate_type
from openapi_server.dcc.genetics_model import GeneticsModel, NodeOuput, EdgeOuput
import openapi_server.dcc.query_builder as qbuilder


def queryGenerated(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: dict | bytes

    :rtype: Message
    """
    return 'do some magic!'

def queryOld(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: Response
    """
    # cnx = mysql.connector.connect(database='Translator', user='mvon')
    # cnx = pymysql.connect(host='localhost', port=3306, database='Translator', user='mvon')
    cnx = pymysql.connect(host='localhost', port=3306, database='tran_genepro', user='root', password='yoyoma')
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
            sourceType = translate_type(sourceNode['type'])
            targetType = translate_type(targetNode['type'])

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
                    print("result of type {} is {}".format(type(results), results))
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


def get_request_elements(body):
    """ translates the json into a neutral format """
    # initialize
    results = []
    edge_map = body['message']['query_graph']['edges']
    node_map = body['message']['query_graph']['nodes']

    # build the 
    for edge_key, edge in edge_map.items():

        # if 'predicate' not in edge or translate_type(edge['predicate']) != 'associated' or 'subject' not in edge or 'object' not in edge:
        if 'subject' not in edge or 'object' not in edge:
            print("========== invalid edge format: {}".format(edge))
            continue
        else:
            edge['edge_key'] = edge_key
        
        sourceNode = node_map.get(edge.get('subject'))
        # if sourceNode is None or 'category' not in sourceNode or 'id' not in sourceNode:
        if sourceNode is None:
            print("=========== invalid source node format: {}".format(sourceNode))
            continue
        else:
            sourceNode['node_key'] = edge.get('subject')

        targetNode = node_map.get(edge.get('object'))
        # if targetNode is None or 'category' not in targetNode:
        if targetNode is None:
            print("============= invalid target node format: {}".format(targetNode))
            continue
        else:
            targetNode['node_key'] = edge.get('object')

        # create the edge/node object
        new_edge = GeneticsModel(edge, sourceNode, targetNode)

        # add to the list
        results.append(new_edge)

    # return
    return results

def build_results(results_list, query_graph):
    """ build the trapi v1.0 response from the genetics model """
    # build the empty collections
    results = []
    knowledge_graph = KnowledgeGraph(nodes={}, edges={})
    nodes = {}
    edges = {}

    # loop through the results
    for edge_element in results_list:
        # get the nodes
        source = edge_element.source_node
        target = edge_element.target_node
        # print("edge element: {}".format(edge_element))

        # add the edge
        attributes = None
        if edge_element.score is not None:
            attributes = []
            if edge_element.score_type == 'biolink:probability':
                attributes.append(Attribute(name='probability', value=edge_element.score, type=edge_element.score_type))
            else:
                attributes.append(Attribute(name='pValue', value=edge_element.score, type=edge_element.score_type))
            # print("added attributes: {}".format(attributes))
        edge = Edge(predicate=translate_type(edge_element.predicate, False), subject=source.curie, object=target.curie, attributes=attributes, relation=None)
        knowledge_graph.edges[edge_element.id] = edge
        edges[(source.node_key, target.node_key)] = edge

        # add the subject node
        node = Node(name=source.name, category=translate_type(source.category, False), attributes=None)
        nodes[source.node_key] = node           
        knowledge_graph.nodes[source.curie] = node

        # add the target node
        node = Node(name=target.name, category=translate_type(target.category, False), attributes=None)
        nodes[target.node_key] = node           
        knowledge_graph.nodes[target.curie] = node

        # build the bindings
        source_binding = NodeBinding(id=source.curie)
        edge_binding = EdgeBinding(id=edge_element.id)
        target_binding = NodeBinding(id=target.curie)
        edge_map = {edge_element.edge_key: [edge_binding]}
        nodes_map = {source.node_key: [source_binding], target.node_key: [target_binding]}
        results.append(Result(nodes_map, edge_map))

    # build out the message
    message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph)
    results_response = Response(message = message)

    # return
    return results_response

def query2(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: Response
    """
    # node types
    node_gene ='biolink:Gene'
    node_disease = 'biolink:Disease'
    node_phenotype = 'biolink:PhenotypicFeature'
    node_pathway = 'biolink:Pathway'

    # edge types
    edge_gene_disease = 'biolink:gene_associated_with_condition'
    edge_disease_gene = 'biolink:condition_associated_with_gene'
    edge_pathway_disease = 'biolink:genetic_association'
    edge_disease_pathway = 'biolink:genetic_association'

    if connexion.request.is_json:
        # initialize
        # cnx = mysql.connector.connect(database='Translator', user='mvon')
        # cnx = pymysql.connect(host='localhost', port=3306, database='Translator', user='mvon')
        # cnx = pymysql.connect(host='localhost', port=3306, database='tran_genepro', user='root', password='this is no password')
        cnx = pymysql.connect(host='localhost', port=3306, database='tran_genepro', user='root', password='yoyoma')
        cursor = cnx.cursor()
        genetics_results = []
        query_response = {}

        # verify the json
        body = connexion.request.get_json()
        print("got {}".format(body))
        query_graph = copy.deepcopy(body['message']['query_graph'])
        takenNodes = {}
        takenEdges = {}

        body['results'] = []
        body['knowledge_graph'] = {}
        body['knowledge_graph']['nodes'] = []
        body['knowledge_graph']['edges'] = []

        # build the interim data structure
        request_input = get_request_elements(body)
        print("got request input {}".format(request_input))
 
        for temp_edge in request_input:
            # get the pertinent sql data
            qeID       = temp_edge.edge['edge_key']
            sourceID   = temp_edge.source['id']
            qn0ID      = temp_edge.source['node_key']
            qn1ID      = temp_edge.target['node_key']
            # sourceType = translate_type(temp_edge.source['category'])
            # targetType = translate_type(temp_edge.target['category'])
            sourceType = temp_edge.source['category']
            targetType = temp_edge.target['category']
            edge_type = temp_edge.edge['predicate']

            # N = 0
            info    = []
            queries = []

            # log
            print("running query for source type: {} and source_id: {} and target type: {} and edge type: {}".format(sourceType, sourceID, targetType, edge_type))

            # queries
            if (sourceType == node_disease or sourceType == node_phenotype) and targetType == node_gene and edge_type == edge_disease_gene:
                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["Richards-effector-genes", "higher_is_better"],\
                        ["ABC-genes", "not_displayed"],\
                        ["Genetics-quantile", "higher_is_better"]]
                queries = [
                            """select mg.ncbi_id, concat('magma_gene_', mg.id) as id, mg.p_value, mg.phenotype, mg.gene from magma_gene_phenotype mg
                                where mg.phenotype_ontology_id='{}' and mg.biolink_category='{}' and mg.p_value < 0.05 ORDER by mg.p_value ASC""".format(sourceID, sourceType),\

                            # """select mg.GENE, mg.ID, mg.PVALUE, pl.efo_name, gl.gene from MAGMA_GENES mg, gene_lookup gl, phenotype_lookup pl
                            #     where mg.GENE = gl.ncbi_id and mg.DISEASE = pl.tran_efo_id and 
                            #     mg.DISEASE='{}' and mg.CATEGORY='{}' and mg.PVALUE<2.5e-6 ORDER by mg.PVALUE  ASC""".format(sourceID, translate_type(sourceType)),\

                           """select rg.gene, rg.id, rg.probability, pl.efo_name, gl.gene from richards_gene rg, gene_lookup gl, phenotype_lookup pl  
                                where rg.gene = gl.ncbi_id and rg.phenotype = pl.tran_efo_id and 
                                rg.phenotype='{}' and rg.category='{}' ORDER by rg.probability desc""".format(sourceID, translate_type(sourceType)),\

                           """select abc.gene_ncbi_id, abc.edge_id, null, pl.efo_name, gl.gene from abc_gene_phenotype abc, gene_lookup gl, phenotype_lookup pl  
                                where abc.gene_ncbi_id = gl.ncbi_id and abc.phenotype_efo_id = pl.tran_efo_id and 
                                abc.phenotype_efo_id='{}' and abc.category='{}' and abc.gene_ncbi_id is not null order by abc.edge_id""".format(sourceID, translate_type(sourceType)),\

                           """select mg.GENE, mg.ID, mg.SCORE, pl.efo_name, gl.gene from SCORE_GENES  mg, gene_lookup gl, phenotype_lookup pl 
                                where mg.GENE = gl.ncbi_id and mg.DISEASE = pl.tran_efo_id and 
                                mg.DISEASE='{}' and mg.CATEGORY='{}' and mg.SCORE >0.95   ORDER by mg.SCORE  DESC""".format(sourceID, translate_type(sourceType))]

            elif (sourceType == node_disease or sourceType == node_phenotype) and targetType == node_pathway and edge_type == edge_disease_pathway:
                info = [["MAGMA-pvalue", "smaller_is_better"]]
                queries = ["""select mp.PATHWAY, mp.ID, mp.PVALUE, pl.efo_name, null from MAGMA_PATHWAYS mp, phenotype_lookup pl 
                        where mp.DISEASE = pl.tran_efo_id and 
                        mp.DISEASE='{}' and mp.CATEGORY='{}' and mp.PVALUE<2.0e-6 ORDER by mp.PVALUE ASC""".format(sourceID, translate_type(sourceType))]

            elif sourceType == node_gene and (targetType == node_disease or targetType == node_phenotype) and edge_type == edge_gene_disease:
                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["Richards-effector-genes", "higher_is_better"],\
                        ["ABC-genes", "not_displayed"],\
                        ["Genetics-quantile", "higher_is_better"]]
                queries = [
                            """select mg.phenotype_ontology_id, concat('magma_gene_', mg.id) as id, mg.p_value, mg.gene, mg.phenotype from magma_gene_phenotype mg
                                where mg.ncbi_id='{}' and mg.biolink_category='{}' and mg.p_value < 0.05 ORDER by mg.p_value ASC""".format(sourceID, targetType),\

                            # """select mg.DISEASE, mg.ID, mg.PVALUE, gl.gene, pl.efo_name from MAGMA_GENES mg, gene_lookup gl, phenotype_lookup pl 
                            #     where mg.GENE = gl.ncbi_id and mg.DISEASE = pl.tran_efo_id and 
                            #     mg.GENE='{}' and mg.CATEGORY='{}' and mg.PVALUE<0.05 ORDER by mg.PVALUE ASC""".format(sourceID, translate_type(targetType)),\

                           """select rg.phenotype, rg.id, rg.probability, gl.gene, pl.efo_name from richards_gene rg, gene_lookup gl, phenotype_lookup pl 
                                where rg.gene = gl.ncbi_id and rg.phenotype = pl.tran_efo_id and 
                                rg.gene='{}' and rg.category='{}' ORDER by rg.probability desc""".format(sourceID, translate_type(targetType)),\

                           """select abc.phenotype_efo_id, abc.edge_id, null, gl.gene, pl.efo_name from abc_gene_phenotype abc, gene_lookup gl, phenotype_lookup pl  
                                where abc.gene_ncbi_id = gl.ncbi_id and abc.phenotype_efo_id = pl.tran_efo_id and 
                                abc.gene_ncbi_id='{}' and abc.category='{}' and abc.phenotype_efo_id is not null order by abc.edge_id""".format(sourceID, translate_type(targetType)),\

                           """select mg.DISEASE, mg.ID, mg.SCORE, gl.gene, pl.efo_name from SCORE_GENES mg, gene_lookup gl, phenotype_lookup pl 
                                where mg.GENE = gl.ncbi_id and mg.DISEASE = pl.tran_efo_id and 
                                mg.GENE='{}' and mg.CATEGORY='{}' and mg.SCORE >0.80 ORDER by SCORE DESC""".format(sourceID, translate_type(targetType))]

            elif sourceType == node_pathway and (targetType == node_disease or targetType == node_phenotype) and edge_type == edge_pathway_disease:
                info = [["MAGMA-pvalue", "smaller_is_better"]]
                queries = ["""select mp.DISEASE, mp.ID, mp.PVALUE, null, pl.efo_name from MAGMA_PATHWAYS  mp, phenotype_lookup pl 
                        where mp.DISEASE = pl.tran_efo_id and 
                        mp.PATHWAY='{}' and mp.CATEGORY='{}' and mp.PVALUE<0.05 ORDER by mp.PVALUE ASC""".format(sourceID, translate_type(targetType))]

            if len(queries) > 0:
                for i in range(0, len(queries)):
                    print("running query: {}".format(queries[i]))
                    cursor.execute(queries[i])
                    results = cursor.fetchall()
                    print("result of type {} is {}".format(type(results), results))
                    if results:
                        for record in results:
                            targetID  = record[0]
                            edgeID    = record[1]
                            score     = record[2]
                            sourceName = record[3]
                            targetName = record[4]

                            # build the result objects
                            source_node = NodeOuput(curie=sourceID, name=sourceName, category=sourceType, node_key=qn0ID)
                            target_node = NodeOuput(curie=targetID, name=targetName, category=targetType, node_key=qn1ID)
                            output_edge = EdgeOuput(id=edgeID, source_node=source_node, target_node=target_node, predicate=edge_type, score=score, edge_key=qeID)

                            # add to the results list
                            genetics_results.append(output_edge)

        # close the connection
        cnx.close()

        # build the response
        query_response = build_results(results_list=genetics_results, query_graph=query_graph)
        return query_response

    else :
        # return error
        return({"status": 400, "title": "body content not JSON", "detail": "Required body content is not JSON", "type": "about:blank"}, 400)

def query(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: Response
    """
    if connexion.request.is_json:
        # initialize
        # cnx = mysql.connector.connect(database='Translator', user='mvon')
        # cnx = pymysql.connect(host='localhost', port=3306, database='Translator', user='mvon')
        # cnx = pymysql.connect(host='localhost', port=3306, database='tran_genepro', user='root', password='this is no password')
        cnx = pymysql.connect(host='localhost', port=3306, database='tran_genepro', user='root', password='yoyoma')
        cursor = cnx.cursor()
        genetics_results = []
        query_response = {}

        # verify the json
        body = connexion.request.get_json()
        print("got {}".format(body))
        query_graph = copy.deepcopy(body['message']['query_graph'])
        takenNodes = {}
        takenEdges = {}

        # build the interim data structure
        request_input = get_request_elements(body)
        print("got request input {}".format(request_input))
 
        for web_request_object in request_input:
            # log
            print("running query for web query object: {}".format(web_request_object))

            # queries
            queries = qbuilder.get_queries(web_request_object)
            if len(queries) > 0:
                for i in range(0, len(queries)):
                    sql_object = queries[i]
                    print("running query: {}".format(sql_object))
                    cursor.execute(sql_object.sql_string, tuple(sql_object.param_list))
                    results = cursor.fetchall()
                    print("result of type {} is {}".format(type(results), results))
                    if results:
                        for record in results:
                            edgeID    = record[0]
                            sourceID  = record[1]
                            targetID  = record[2]
                            score     = record[3]
                            scoreType = record[4]
                            sourceName = record[5]
                            targetName = record[6]
                            edgeType = record[7]
                            sourceType = record[8]
                            targetType = record[9]

                            # build the result objects
                            source_node = NodeOuput(curie=sourceID, name=sourceName, category=sourceType, node_key=web_request_object.get_source_key())
                            target_node = NodeOuput(curie=targetID, name=targetName, category=targetType, node_key=web_request_object.get_target_key())
                            output_edge = EdgeOuput(id=edgeID, source_node=source_node, target_node=target_node, predicate=edgeType, score=score, score_type=scoreType, edge_key=web_request_object.get_edge_key())

                            # add to the results list
                            genetics_results.append(output_edge)

        # close the connection
        cnx.close()

        # build the response
        query_response = build_results(results_list=genetics_results, query_graph=query_graph)
        return query_response

    else :
        # return error
        return({"status": 400, "title": "body content not JSON", "detail": "Required body content is not JSON", "type": "about:blank"}, 400)
