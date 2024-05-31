
# imports



# constants



# methods
def get_basic_sqlite_query(log=False):
    '''
    will return the basic no param sql query
    '''
    # initialize
    sql_string = "select ed.id || ed.edge_id || so.ontology_id || ta.ontology_id, so.ontology_id, ta.ontology_id, ed.score, \
            so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator, ed.id, \
            ed.p_value, ed.beta, ed.standard_error, ed.probability, ed.probability_app_bayes_factor, ed.enrichment\
        from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta \
        where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id \
        and ed.source_node_id = so.id and ed.target_node_id = ta.id "

    # return
    return sql_string



