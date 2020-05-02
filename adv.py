from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
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
traversal_path = []

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def room_path(graph, starting_room, ending_room):
    # create a queue to keep track of the path
    paths_queue = Queue()
    # add the starting room to the queue
    paths_queue.enqueue([starting_room])
    # create a set for visited rooms
    visited_rooms = set()
    # while the queue is not empty
    while paths_queue.size() > 0:
        # dequeue the first room path
        current_path = paths_queue.dequeue()
        # get grab the last room from current path
        current_room = current_path[-1]
        # if I haven't visited this room yet
        if current_room not in visited_rooms:
            # if the current room is not the ending room
            if current_room == ending_room:
                # return the path
                return current_path
            # mark the room visited
            visited_rooms.add(current_room)
            # for every direction in current room, make a new path to check
            for direction in graph[current_room]:
                # if the room has not been visited and is not unexplored
                if graph[current_room][direction] != '?' and graph[current_room][direction] not in visited_rooms:
                    # duplicate the path
                    new_path = current_path.copy()
                    # add the direction room to the new path
                    new_path.append(graph[current_room][direction])
                    # add the new path to the queue
                    paths_queue.enqueue(new_path)

def automove(curr_exits, paths, curr_room, graph, paths_to_visit):
    # if I can go north, go north
    if 'n' in curr_exits:
        if paths['n'] == '?':
            player.travel('n')
            return 'n' 
        # else:
            # raise IndexError("Error: no untravelled paths found from this room")
    # if can't go north, try east
    elif 'e' in curr_exits:
        if paths['e'] == '?':
            player.travel('e')
            return 'e' 
        # else:
            # raise IndexError("Error: no untravelled paths found from this room")
    # if can't go north or east, try south
    elif 's' in curr_exits:
        if paths['s'] == '?':
            player.travel('s')
            return 's' 
        # else:
        #     raise IndexError("Error: no untravelled paths found from this room")
    # if can't go north, east or south, try west`
    elif 'w' in curr_exits:
        if paths['w'] == '?':
            player.travel('w')
            return 'w' 
        # else:
        #     raise IndexError("Error: no untravelled paths found from this room")
    # if can't go north, east, south or west, raise error
    else:
        # grab the last next path needed from stack
        ending_room = paths_to_visit.pop()
        # go back to the most recent room with an unexplored path
        return room_path(graph, curr_room, ending_room)
        # raise IndexError("Error: can't go in any direction")
        
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
    prev_room = -1
    # set a variable for the current room
    curr_room = player.current_room.id
    # set variable for later
    moved = 'none'
    moved_opposite = 'none'
    # stack for paths needed to visit
    paths_to_visit = Stack()

    # temp loop limit
    i = 0
    while True:
        # set current room
        curr_room = player.current_room.id
        # get all the available exits for current room
        curr_exits = player.current_room.get_exits()

        print(f'Room # {curr_room}')

        if moved is None:
            # grab the last next path needed from stack
            ending_room = paths_to_visit.pop()
            # go back to the most recent room with an unexplored path
            print(f'This is the path: {room_path(rooms_graph, curr_room, ending_room[0])}')
            return full_path
    
        # only if moved has been set to a direction
        if moved != 'none':
            print(f'prev_room: {prev_room}, moved: {moved}')
            # set moved direction for previous room
            rooms_graph[prev_room][moved] = curr_room
            # get the opposite direction moved
            print(f'Moved before getting opposite: {moved}')
            moved_opposite = opposite_dir(moved)
            # add the moved direction to the full path
            full_path.append(moved)
        # create a dictionary in our room dictionary for current room
        rooms_graph[curr_room] = {}

        # if the previous room had paths I didn't go through
        if prev_room != -1:
            # for every direction in the room
            for direction in rooms_graph[prev_room]:
                # if the direction is not explored
                if rooms_graph[prev_room][direction] == '?':
                    # add it to the stack of paths need to visit
                    paths_to_visit.push((prev_room, direction))

        print(paths_to_visit.stack)

        # for every direction available from this room
        for direction in curr_exits:
            # if the direction is the one we came from
            if direction == moved_opposite:
                # set it to the previous room
                rooms_graph[curr_room][direction] = prev_room
            else:
                # add the key with a temp value of ? to the graph
                rooms_graph[curr_room][direction] = '?'

        # set the current room as the previous one
        prev_room = curr_room
        # go in the next best direction
        moved = automove(curr_exits, rooms_graph[curr_room], curr_room, rooms_graph, paths_to_visit)
        print(f'Trying to go: {moved}')

        # temp loop limiter
        i += 1
        if i > 10:
            break
        # check if any path direction still has an unknown room
        if paths_check(rooms_graph) is False:
            # if all paths are checked, end while loop
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