#Import handlers
from handlers.handle_endturn import handle_endturn
from handlers.handle_game_start import handle_game_start

#Add routes and handlers to the dict {"route_key": handler_function}
route_dic = {
    "endturn": handle_endturn,
    "startgame": handle_game_start
}

def routes(route_key, table, event, connection_id, apig_management_client):
    action = route_dic[route_key]
    action(table, event, connection_id, apig_management_client)
