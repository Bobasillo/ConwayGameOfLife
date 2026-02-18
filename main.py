# import pygame
# import sys

# pygame.init()

# ANCHO_VENTANA = 800
# ALTO_VENTANA = 600

# CELDA = 30
# MARGEN = 0

# ANCHO_CELDAS = ANCHO_VENTANA // CELDA
# ALTO_CELDAS = ALTO_VENTANA // CELDA

# screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
# pygame.display.set_caption("Grid en Pygame")
# reloj = pygame.time.Clock()

# grid = [[0 for _ in range(ANCHO_CELDAS)] for _ in range(ALTO_CELDAS)]

# def dibujar_grid():
#     for i in range(len(grid)):
#         for j in range(len(grid[0])):
#             color = (0, 255, 0) if grid[i][j] else (50, 50, 50)
#             rect = pygame.Rect(i * (CELDA + MARGEN), j * (CELDA + MARGEN), CELDA, CELDA)
#             pygame.draw.rect(screen, color, rect)
#             pygame.draw.rect(screen, (255, 255, 255), rect, 1)

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
            
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mx, my = pygame.mouse.get_pos()
#             i = mx // (CELDA + MARGEN)
#             j = my // (CELDA + MARGEN)
#             if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
#                 grid[i][j] = 1 - grid[i][j]

#     screen.fill((20, 20, 20))
#     dibujar_grid()
#     pygame.display.flip()
#     reloj.tick(60)

import pygame
import sys

pygame.init()

# ----------------- Ventana fija -----------------
ANCHO_VENTANA = 1800
ALTO_VENTANA = 900
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Grid adaptado a ventana fija")
reloj = pygame.time.Clock()

# ----------------- Grid lógico ------------------
ANCHO_CELDAS = 100
ALTO_CELDAS = 50

CELDA = min(ANCHO_VENTANA / ANCHO_CELDAS, ALTO_VENTANA / ALTO_CELDAS)

GRID_ANCHO_PX = CELDA * ANCHO_CELDAS
GRID_ALTO_PX = CELDA * ALTO_CELDAS

OFFSET_X = (ANCHO_VENTANA - GRID_ANCHO_PX) / 2
OFFSET_Y = (ALTO_VENTANA - GRID_ALTO_PX) / 2

grid = [[0 for _ in range(ANCHO_CELDAS)] for _ in range(ALTO_CELDAS)]

# ----------------- Estado simulación -----------
running = False
STEP_TIME = 200
ultimo_step = 0

# ----------------- Botón Start -----------------
FONT = pygame.font.SysFont(None, 32)
BOTON_ANCHO = 120
BOTON_ALTO = 40
BOTON_X = 20
BOTON_Y = 20
boton_rect = pygame.Rect(BOTON_X, BOTON_Y, BOTON_ANCHO, BOTON_ALTO)

def dibujar_boton():
    color = (0, 180, 0) if running else (180, 0, 0)
    texto = "Stop" if running else "Start"
    pygame.draw.rect(screen, color, boton_rect, border_radius=5)
    label = FONT.render(texto, True, (255, 255, 255))
    label_rect = label.get_rect(center=boton_rect.center)
    screen.blit(label, label_rect)

# ----------------- Utilidades grid -------------
def dibujar_grid():
    for fila in range(ALTO_CELDAS):
        for col in range(ANCHO_CELDAS):
            color = (0, 255, 0) if grid[fila][col] else (50, 50, 50)
            x = int(OFFSET_X + col * CELDA)
            y = int(OFFSET_Y + fila * CELDA)
            rect = pygame.Rect(x, y, int(CELDA), int(CELDA))
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

def coord_a_celda(mx, my):
    gx = mx - OFFSET_X
    gy = my - OFFSET_Y
    if gx < 0 or gy < 0:
        return None
    col = int(gx // CELDA)
    fila = int(gy // CELDA)
    if 0 <= fila < ALTO_CELDAS and 0 <= col < ANCHO_CELDAS:
        return fila, col
    return None

def contar_vecinos(grid_ref, fila, col):
    vecinos = 0
    for df in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if df == 0 and dc == 0:
                continue
            nf = fila + df
            nc = col + dc
            if 0 <= nf < ALTO_CELDAS and 0 <= nc < ANCHO_CELDAS:
                vecinos += grid_ref[nf][nc]
    return vecinos

# ----------------- Reglas del juego ------------
def step():
    actual = grid
    nuevo = [[0 for _ in range(ANCHO_CELDAS)] for _ in range(ALTO_CELDAS)]
    for f in range(ALTO_CELDAS):
        for c in range(ANCHO_CELDAS):
            vivos = contar_vecinos(actual, f, c)
            if actual[f][c] == 1:
                if vivos < 2 or vivos > 3:
                    nuevo[f][c] = 0
                else:
                    nuevo[f][c] = 1
            else:
                if vivos == 3:
                    nuevo[f][c] = 1
                else:
                    nuevo[f][c] = 0
    return nuevo

while True:
    tiempo_actual = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            if boton_rect.collidepoint(mx, my):
                running = not running
            else:
                
                if not running:
                    celda = coord_a_celda(mx, my)
                    if celda is not None:
                        fila, col = celda
                        grid[fila][col] = 1 - grid[fila][col]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not running
            if event.key == pygame.K_c:
                grid = [[0 for _ in range(ANCHO_CELDAS)] for _ in range(ALTO_CELDAS)]

    if running and tiempo_actual - ultimo_step >= STEP_TIME:
        grid = step()
        ultimo_step = tiempo_actual

    screen.fill((0, 0, 0))
    dibujar_grid()
    dibujar_boton()
    pygame.display.flip()
    reloj.tick(60)