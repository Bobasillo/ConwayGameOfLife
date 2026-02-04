import numpy as np

tamano_grid_x = 20
tamano_grid_y = 30

generacion = 0

grid = np.random.choice([False, True], (tamano_grid_x, tamano_grid_y), p=[0.8, 0.2])
grid_en_buffer = np.zeros((tamano_grid_x, tamano_grid_y), dtype=bool)

def reset_grid():
    grid[:, :] = grid_en_buffer[:, :]
    grid_en_buffer[:, :] = False

def step(grid):
    for x in range(tamano_grid_x):
        for y in range(tamano_grid_y):
            celulas_vivas = 0
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if (i, j) != (x, y):
                        if grid[i % tamano_grid_x, j % tamano_grid_y]:
                            celulas_vivas += 1
            if grid[x, y]:
                if celulas_vivas == 2 or celulas_vivas == 3:
                    grid_en_buffer[x, y] = True
            else:
                if celulas_vivas == 3:
                    grid_en_buffer[x, y] = True
    reset_grid()
    print(f"Gen {generacion}: {np.sum(grid)} vivas")
    generacion += 1

for i in range(100):
    step(grid)