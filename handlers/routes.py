#Import handlers

#Add routes and handlers to the dict {"route_key": handler_function}
route_dic = {

}

def routes(route_key, table, event, connection_id, apig_management_client):
    action = route_dic[route_key]
    action(table, event, connection_id, apig_management_client)
