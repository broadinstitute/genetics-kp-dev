

def add_in_equals(sql, term, is_first=True):
    ''' add in and clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # add in the condition
    temp = temp + str(term) + " = %s "

    # return
    return temp

def add_in_in(sql, term, list_input, is_first=True):
    ''' add in and clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # build the in sql
    in_sql = ", ".join(list(map(lambda item: '%s', list_input)))

    # add in the condition
    temp = temp + str(term) + " in ({}) ".format(in_sql)

    # return
    return temp

def add_in_less_than(sql, term, is_first=True):
    ''' add in less than clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # add in the condition
    temp = temp + str(term) + " < %s "

    # return
    return temp

def add_in_more_than(sql, term, is_first=True):
    ''' add in less than clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # add in the condition
    temp = temp + str(term) + " > %s "

    # return
    return temp

def add_in_more_than_equals(sql, term, is_first=True):
    ''' add in less than clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # add in the condition
    temp = temp + str(term) + " >= %s "

    # return
    return temp
