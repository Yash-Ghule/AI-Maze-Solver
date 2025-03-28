import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 0(path) : walkable space
# 1(wall) : impassable wall

# Recursive backtracking algorithm to generate a classic maze
def generate_classic_maze(width, height):
    maze = [[1] * (2 * width + 1) for _ in range(2 * height + 1)] 

    def carve(x, y): 
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)] 
        random.shuffle(directions) 
        for direction in directions:
            nx, ny = x + direction[0], y + direction[1]
            if 0 <= nx < 2 * height + 1 and 0 <= ny < 2 * width + 1 and maze[nx][ny] == 1:
                maze[nx][ny] = 0
                maze[x + direction[0] // 2][y + direction[1] // 2] = 0
                carve(nx, ny) 

    maze[1][1] = 0 
    carve(1, 1) 
    return maze


# Here it recursively explores all paths n keep tack of visited nodes/cells n current path
def dfs(maze, current, end, visited, path):
    if current == end: 
        return path
    visited.add(current) 

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # possible moves (0,1) move right | (1,0) move down | (0,-1) move left | (-1,0) move up
    for direction in directions:
        next_pos = (current[0] + direction[0], current[1] + direction[1])
        if (0 <= next_pos[0] < len(maze)) and (0 <= next_pos[1] < len(maze[0])) and maze[next_pos[0]][next_pos[1]] == 0 and next_pos not in visited: 
            result = dfs(maze, next_pos, end, visited, path + [next_pos])
            if result: 
                return result
    return None

# Create the animation for the DFS path solution
def animate_solution(maze, path, start, end):
    fig, ax = plt.subplots(figsize=(8, 8)) 
    maze_array = np.array(maze)  

    # Display the maze
    ax.imshow(maze_array, cmap="binary") 

    # Mark start and end points
    ax.scatter(start[1], start[0], color="blue", s=100, label="Start")  
    ax.scatter(end[1], end[0], color="red", s=100, label="End") 

    # Initialize line for the path
    line, = ax.plot([], [], color="green", linewidth=2)

    # Path coordinates for the animation
    xdata, ydata = [], []

    def init():
        line.set_data([], []) 
        return line,

    # Update function to animate the line segment by segment
    def update(frame):
        x, y = path[frame]  
        xdata.append(y)    
        ydata.append(x)   
        line.set_data(xdata, ydata)  
        return line,

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(path), init_func=init, blit=True, repeat=False)

    # Display the animation
    plt.legend()   
    plt.axis('off')  
    plt.show()   

# Main function to generate and solve the maze with animation
def maze_game(width, height):
    # Generate a classic maze
    maze = generate_classic_maze(width, height)

    # Set the start and end points
    start = (1, 1)
    end = (2 * height - 1, 2 * width - 1)

    # Solve the maze using DFS
    path = dfs(maze, start, end, set(), [start])

    if path:
        print("Path found:", path)
    else:
        print("No path found.")

    # Animate the solution path
    animate_solution(maze, path, start, end)

# Run the maze game with size parameters (e.g., 10x10 maze)
maze_game(10, 10)
