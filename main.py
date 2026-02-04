import numpy as np

x = 20
y = 30

nx = len(range(x))
ny = len(range(y))

grid = np.zeros((nx, ny), dtype=bool)
grid_en_buffer = np.zeros((nx, ny), dtype=bool)

# def update_grid(grid):
#     for i in grid:
#         for j in i:
            
    
def reset_grid():
    grid[:, :] = grid_en_buffer[:, :]
    grid_en_buffer[:, :] = np.zeros((nx, ny), dtype=bool)
    
update_grid(grid)
reset_grid()