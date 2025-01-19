# Maze generation original code provided by https://inventwithpython.com/recursion/chapter11.html
import random

def generatemaze(width, height, seed, difficulty):
    # Width of the maze must be odd, Height of the maze must be odd.
    assert width % 2 == 1 and width >= 3
    assert height % 2 == 1 and height >= 3
    random.seed(seed)

    # Use these characters for displaying the maze:
    OBSTACLE = 4
    BREAKABLE = 3
    BREAKABLE_PROBABILITY = 0.05
    FIREWALL = 2
    FIREWALL_PROBABILITY = 0.03 * (difficulty / 3 + 2) 
    WALL = 1
    OBJECTIVE = 0
    EMPTY = -1
    GHOST_WALL = -2
    GHOST_WALL_PROBABILITY = 0.06 - (difficulty * 0.005)
    KEY = -3
    FLASHLIGHT = -4
    CROSSBOW = -5
    BOMB = -6
    SHOE = -7
    FLARE = -8
    ARMOR = -9
    MEGA_BOMB = -10
    KNIFE = -11
    GUN = -12
    MEDKIT = -13
    # RPG = -14
    SPIDER = -15
    GAURD = -16
    NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'
    powerups = int(width * height / random.randrange(100, 150) / ((difficulty + 1) / 3))
    armor = difficulty // 2
    gun = True
    bombs = 1
    spiders = 0
    gaurds = 0
    if difficulty > 2:  
        spiders = random.randint(difficulty, difficulty * 2)
        if difficulty == 5:
            gaurds = random.randint(3, 5)
    objective_locations = []
    key_locations = []
    obstacles = width * height // 50
    # Create the filled-in maze data structure to start:
    maze = {}
    for x in range(width):
        for y in range(height):
            maze[(x, y)] = WALL
    def printmaze(maze, width, height):
        print("  ", end="")
        for i in range(width):
            if i > 9:
                print(f" {i}", end="")
            else:
                print(f"  {i}", end="")
        print()
        for j in range(height):
            print(j, end="")
            for i in range(width):
               if maze[(i, j)] == 1:
                   print("  #", end="")
               elif maze[(i, j)] == 2:
                   print("  @", end="")
               elif maze[(i, j)] == -1:
                   print("   ", end="")
               elif maze[(i, j)] == 0:
                   print("  x", end="")
               elif maze[(i, j)] < 0:
                   print(f" {maze[(i, j)]}", end="")
               else:
                   print(f"  {maze[(i, j)]}", end="")
            print()
    
    def visit(x, y):
        """"Carve out" empty spaces in the maze at x, y and then
        recursively move to neighboring unvisited spaces. This
        function backtracks when the mark has reached a dead end."""
        nonlocal powerups
        nonlocal obstacles
        nonlocal difficulty
        nonlocal bombs
        maze[(x, y)] = EMPTY # "Carve out" the space at x, y.
        
        while True:
            # Check which neighboring spaces adjacent to
            # the mark have not been visited already:
            unvisitedNeighbors = []
            if y > 1 and (x, y - 2) not in hasVisited:
                unvisitedNeighbors.append(NORTH)

            if y < height - 2 and (x, y + 2) not in hasVisited:
                unvisitedNeighbors.append(SOUTH)

            if x > 1 and (x - 2, y) not in hasVisited:
                unvisitedNeighbors.append(WEST)

            if x < width - 2 and (x + 2, y) not in hasVisited:
                unvisitedNeighbors.append(EAST)

            if len(unvisitedNeighbors) == 0:
                # BASE CASE
                # All neighboring spaces have been visited, so this is a
                # dead end. Backtrack to an earlier space:
                return
            else:
                # RECURSIVE CASE
                # Randomly pick an unvisited neighbor to visit:
                # nextIntersection = random.choice(unvisitedNeighbors) # This broke on very high values of maze size
                nextIntersection = unvisitedNeighbors[int(random.random() * len(unvisitedNeighbors))]

                # Move the mark to an unvisited neighboring space:

                if nextIntersection == NORTH:
                    nextX = x
                    nextY = y - 2
                    maze[(x, y - 1)] = EMPTY # Connecting hallway.
                elif nextIntersection == SOUTH:
                    nextX = x
                    nextY = y + 2
                    maze[(x, y + 1)] = EMPTY # Connecting hallway.
                elif nextIntersection == WEST:
                    nextX = x - 2
                    nextY = y
                    maze[(x - 1, y)] = EMPTY # Connecting hallway.
                elif nextIntersection == EAST:
                    nextX = x + 2
                    nextY = y
                    maze[(x + 1, y)] = EMPTY # Connecting hallway.

                hasVisited.append((nextX, nextY)) # Mark as visited.
                visit(nextX, nextY) # Recursively visit this space.
    # Carve out the paths in the maze data structure:
    hasVisited = [(1, 1)] # Start by visiting the top-left corner.
    visit(1, 1)
    def filter_locations(locations): # This f unction was generated with the help of ChatGPT
        """Removes elements from locations if they have more than one orthogonal empty space (-1)."""
        filtered_locations = []
        for loc in locations:
            x, y = loc
            # Count orthogonal empty spaces (-1)
            if maze[(x, y)] != -1 or x in (0, width - 1) or y in (0, height - 1):
                continue

            empty_count = sum([
                maze.get((x - 1, y), None) == -1,  # Check above
                maze.get((x + 1, y), None) == -1,  # Check below
                maze.get((x, y - 1), None) == -1,  # Check left
                maze.get((x, y + 1), None) == -1   # Check right
            ])
            # Keep the location if it has at most 1 orthogonal empty space
            if empty_count <= 1:
                filtered_locations.append(loc)
        return filtered_locations
    # Filter both objective_locations and key_locations
    filtered_maze = filter_locations(maze)
    for location in filtered_maze:
        if location[0] >= width - 4:
            objective_locations.append(location)
        elif location[1] > height / 2:
            key_locations.append(location)
    if len(objective_locations) != 0:
        maze[random.choice(objective_locations)] = OBJECTIVE
    else:
        maze[width - 2, height - 2] = OBJECTIVE
        print("Objective defaulted")
    if difficulty > 1:
        try:
            maze[random.choice(key_locations)] = KEY
        except:
            maze[(width - 2, 1)] = KEY
            print("Key defaulted")
        if difficulty > 2:
            knife_locations = [(1, 2), (2, 1)]
            temp = random.randint(0, 1)
            if maze[knife_locations[temp]] == -1:
                maze[knife_locations[temp]] = KNIFE
            else:
                maze[knife_locations[(temp - 1) % 2]] = KNIFE
    # Add variated walls and powerups to maze
    for pos in sorted(maze.keys(),key=lambda x: random.random()):
        if pos[0] not in (0, width - 1) and pos[1] not in (0, height - 1) and pos != (1, 1):
            if bombs >= 1 and maze[(pos[0], pos[1])] == EMPTY:
                bombs -= 1
                if difficulty > 2:
                    if random.random() < 0.2:
                        maze[(pos[0], pos[1])] = MEGA_BOMB
                    else:
                        maze[(pos[0], pos[1])] = BOMB
                else:
                    maze[(pos[0], pos[1])] = BOMB
            elif armor and maze[(pos[0], pos[1])] == EMPTY and difficulty >= 4:
                maze[(pos[0], pos[1])] = ARMOR
                armor -=1
            elif gun and maze[(pos[0], pos[1])] == EMPTY and difficulty == 5:
                maze[(pos[0], pos[1])] = GUN
                gun = False
            elif powerups and maze[(pos[0], pos[1])] == EMPTY:
                if difficulty == 1:
                    maze[(pos[0], pos[1])] = random.choice([MEDKIT, SHOE])
                    if random.random() < 0.01 and powerups == 1:
                        maze[(pos[0], pos[1])] = GUN
                elif difficulty == 2:
                    maze[(pos[0], pos[1])] = random.choice([MEDKIT, FLARE, SHOE])
                elif difficulty == 3:
                    maze[(pos[0], pos[1])] = random.choice([MEDKIT, CROSSBOW, FLARE, SHOE])
                else:
                    maze[(pos[0], pos[1])] = random.choice([MEDKIT, CROSSBOW, FLARE, FLASHLIGHT, SHOE])
                powerups -= 1
            elif spiders and maze[(pos[0], pos[1])] == EMPTY and pos[0] > width / 4 and pos[1] > height / 4:
                maze[(pos[0], pos[1])] = SPIDER
                spiders -= 1
            elif gaurds and maze[(pos[0], pos[1])] == EMPTY and pos[0] > width / 2:
                maze[(pos[0], pos[1])] = GAURD
                gaurds -= 1
            elif obstacles and maze[(pos[0], pos[1])] == EMPTY and difficulty > 2:
                if random.random() < 0.1 and pos[0] > width / 2:
                    maze[(pos[0], pos[1])] = BREAKABLE
                else:
                    maze[(pos[0], pos[1])] = OBSTACLE
                obstacles -= 1
            elif maze[pos[0], pos[1]] == WALL:
                neighbors = [maze[(pos[0] + 1, pos[1])], maze[(pos[0], pos[1] + 1)], maze[(pos[0] - 1, pos[1])], maze[(pos[0], pos[1] - 1)], 0, 0]
                for i in range(4):
                    if neighbors[i] > 0:
                        neighbors[i % 2 + 4] += 1
                if neighbors[4] == 2 and not neighbors[5] or neighbors[5] == 2 and not neighbors[4]:
                    randwall = random.random()
                    if randwall < GHOST_WALL_PROBABILITY:
                        maze[(pos[0], pos[1])] = GHOST_WALL
                    elif randwall < GHOST_WALL_PROBABILITY + FIREWALL_PROBABILITY:
                        maze[(pos[0], pos[1])] = FIREWALL
                    elif randwall < GHOST_WALL_PROBABILITY + FIREWALL_PROBABILITY + BREAKABLE_PROBABILITY:
                        maze[(pos[0], pos[1])] = BREAKABLE
                        bombs += random.random() / 4 + 0.1
    return maze