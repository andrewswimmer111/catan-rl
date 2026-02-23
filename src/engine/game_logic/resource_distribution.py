from engine.board.board import Board

def distribute_resources(board: Board, roll: int):

    if roll == 7:
        # handle robber here
        pass

    tiles = board.get_tiles_with_number(roll)

    for tile in tiles:

        # if robber on tile: Ignore

        for vertex in tile.vertices():
            building = vertex.building
            if building:
                player = building.player
                amount = building.collection_amount
                player.add_resource(tile.resource, amount)