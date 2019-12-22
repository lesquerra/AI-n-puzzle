import queue as q

import time

import sys

import math

class PuzzleState(object):

    """PuzzleState Class"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break

    def display(self):
        
        """Display the puzzle state visually"""

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):
        
        """Move puzzle to the left"""

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        """Move puzzle to the right"""
        
        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        """Move puzzle up"""
        
        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        """Move puzzle down"""
        
        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """Expand the node"""

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children
    
    def __lt__(self, other):
        return False


def writeOutput(puzzle_state, explored, start_time, sm):
    
    """Write output to txt file"""
   
    parent = puzzle_state
    
    path_to_goal = [puzzle_state.action]
    
    while parent.parent.action != 'Initial':
    
        parent = parent.parent
        
        path_to_goal = [parent.action] + path_to_goal

    cost_of_path = puzzle_state.cost
    
    nodes_expanded = len(explored) - 1    
    
    search_depth = len(path_to_goal)   
    
    max_search_depth = max([e.cost for e in explored])
    
    if sm == 'bfs':
    
        max_search_depth += 1   
        
    running_time = time.time() - start_time
    
    max_ram_usage = None
        
    
    f = open("output.txt", "w")
    
    print("path_to_goal:", path_to_goal, file=f)
    print("cost_of_path:", cost_of_path, file=f)
    print("nodes_expanded:", nodes_expanded, file=f)
    print("search_depth:", search_depth, file=f)
    print("max_search_depth:", max_search_depth, file=f)        
    print("running_time:", running_time, file=f)
    print("max_ram_usage:", max_ram_usage, file=f)
    
    f.close()

def bfs_search(initial_state):

    """BFS search"""

    start_time = time.time()
    
    frontier = q.Queue()
    
    frontier.put(initial_state)
    
    explored = set()
    
    frontier_explored_configs = [initial_state.config]
    
    count = 0
    
    while not frontier.empty():
    
        print(count)
        
        puzzle_state = frontier.get()
        
        explored.add(puzzle_state)
        
        if test_goal(puzzle_state):
        
            writeOutput(puzzle_state, explored, start_time, sm = 'bfs')
            
            return True
        
        for neighbor in puzzle_state.expand():
        
            if neighbor.config not in frontier_explored_configs:
            
                frontier.put(neighbor)
                
                frontier_explored_configs += [neighbor.config]
        
        count += 1
        
    return False
        
def dfs_search(initial_state):

    """DFS search"""

    start_time = time.time()
    
    frontier = q.LifoQueue()
    
    frontier.put(initial_state)
    
    explored = set()

    frontier_explored_configs = [initial_state.config]
    
    count = 0
    
    while not frontier.empty():
    
        print(count)
        
        puzzle_state = frontier.get()
        
        explored.add(puzzle_state)
        
        if test_goal(puzzle_state):
        
            writeOutput(puzzle_state, explored, start_time, sm = 'dfs')
            
            return True
        
        for neighbor in reversed(puzzle_state.expand()):
        
            if neighbor.config not in frontier_explored_configs:
            
                frontier.put(neighbor)
                
                frontier_explored_configs += [neighbor.config]
        
        count += 1
        
    return False

def A_star_search(initial_state):

    """A * search"""

    start_time = time.time()
    
    frontier = q.PriorityQueue()
    
    explored = set()
    
    total_cost = calculate_total_cost(initial_state)
    
    frontier.put((total_cost, initial_state))
    
    frontier_explored_configs = [initial_state.config]
    
    count = 0
    
    while not frontier.empty():
    
        print(count)
        
        puzzle_state = frontier.get()[1]
        
        explored.add(puzzle_state)
        
        if test_goal(puzzle_state):
        
            writeOutput(puzzle_state, explored, start_time, sm = 'ast')
            
            return True
        
        for neighbor in puzzle_state.expand():
        
            if neighbor.config not in frontier_explored_configs:
            
                total_cost = calculate_total_cost(neighbor)
                
                frontier.put((total_cost, neighbor))
                
                frontier_explored_configs += [neighbor.config]
        
        count += 1
        
    return False

def calculate_total_cost(state):

    """Calculate the total estimated cost of a state"""

    idx = tuple(range(0, state.n**2))
    
    h2_n = calculate_manhattan_dist(idx, state.config, state.n)
    
    g_n = state.cost
    
    return (h2_n + g_n)

def calculate_manhattan_dist(idx, value, n):

    """Calculate the manhattan distance of a tile"""

    manh_dist = 0
    
    for i,v in zip(idx, value):
    
        prev_row,prev_col = int(i/ n) , i % n
        
        goal_row,goal_col = int(v /n),v % n
        
        manh_dist += abs(prev_row-goal_row) + abs(prev_col - goal_col)
        
    return manh_dist

def test_goal(puzzle_state):

    """Test the state is the goal state or not"""
    
    goal = tuple(range(0, puzzle_state.n**2))
    
    return(puzzle_state.config == goal)

def main():
    
    """Main Function that reads in Input and Runs corresponding Algorithm"""
    
    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")
    
    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":

        bfs_search(hard_state)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")

if __name__ == '__main__':

    main()