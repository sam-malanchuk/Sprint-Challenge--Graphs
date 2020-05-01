from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def automove(curr_exits):
    # if I can go north, go north
    if 'n' in curr_exits:
        player.travel('n')
        return 'n' 
    # if can't go north, try east
    elif 'e' in curr_exits:
        player.travel('e')
        return 'e' 
    # if can't go north or east, try south
    elif 's' in curr_exits:
        player.travel('s')
        return 's' 
    # if can't go north, east or south, try west
    elif 'w' in curr_exits:
        player.travel('w')
        return 'w' 
    # if can't go north, east, south or west, raise error
    else:
        raise IndexError("Error: can't go in any direction")
        
def paths_check(graph):
    # for every room in graph
    for room in graph:
        # every direction in every room
        for direction in graph[room]:
            # check to see if there are any paths unchecked
            if graph[room][direction] == '?':
                return True
    return False

def opposite_dir(direction):
    # if current is n, return s
    if direction == "n":
        return 's'
    # if current is e, return w
    elif direction == "e":
        return 'w'
    # if current is s, return n
    elif direction == "s":
        return 'n'
    # if current is w, return e
    elif direction == "w":
        return 'e'
    # else, raise error
    else:
        raise IndexError("Error: can't go in any direction")

def traversal_calc():
    # create a graph to track all the rooms and their directions
    rooms_graph = {}
    # create the full traversal path
    full_path = []
    # set a variable for the previous room
    prev_room = 0
    # set a variable for the current room
    curr_room = player.current_room.id
    # set variable for later
    moved = 'none'
    moved_opposite = 'none'

    # temp loop limit
    i = 0
    while True:
        # set current room
        curr_room = player.current_room.id
        # get all the available exits for current room
        curr_exits = player.current_room.get_exits()

        print(f'Room # {curr_room}')
    
        if moved != 'none':
            print(f'prev_room: {prev_room}, moved: {moved}')
            # set moved direction for previous room
            rooms_graph[prev_room][moved] = curr_room
            # get the opposite direction moved
            moved_opposite = opposite_dir(moved)
        # create a dictionary in our room dictionary for current room
        rooms_graph[curr_room] = {}
        # for every direction available from this room
        for direction in curr_exits:
            if direction == moved_opposite:
                rooms_graph[curr_room][direction] = prev_room
            else:
                # add the key with a temp value of ? to the graph
                rooms_graph[curr_room][direction] = '?'

        # set the current room as the previous one
        prev_room = curr_room
        # add the moved direction to the full path
        full_path.append(moved)
        # go in the next best direction
        moved = automove(curr_exits)

        i += 1
        if i > 10:
            break
        if paths_check(rooms_graph) is False:
            break

    print(rooms_graph)
    return full_path

"""

Understand: create a code that walks through all the rooms at least once and returns the path it took.
Create a adjacency list graph recording the room located in every direction available to a room.

Plan: Get the available directions from get_exits and add them to the new graph.
Each empty at the time, save the current room to prev_room and then pick the first
direction starting from north and so on depending on availablity and visited_rooms.  
Add the current room number to the followed direction on prev_room in my graph.
Fill the opposite direction of the followed on the current room in the graph
as the prev_room. And add the followed direction to a final path array. Repeat
the loop until all the rooms have been visited.


"""

traversal_path = traversal_calc()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")