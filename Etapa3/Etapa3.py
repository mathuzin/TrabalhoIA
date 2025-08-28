import time
import random
from collections import deque 

def generate_obstacles(grid_size, num_obstacles):
    """Gera um conjunto de posições aleatórias para os obstáculos."""
    all_positions = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    return set(random.sample(all_positions, num_obstacles))

def generate_initial_position(grid_size, obstacles):
    """Gera uma posição inicial aleatória para o robô, que não seja um obstáculo."""
    while True:
        pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if pos not in obstacles:
            return pos

class GridWorld:
    def __init__(self, n=8, obstacles=None):
        self.n = n
        self.obstacles = obstacles if obstacles else set()

    def is_free(self, position):
        x, y = position
        return 0 <= x < self.n and 0 <= y < self.n and position not in self.obstacles
    
    def print_grid(self, robot_position, visited, closed, goal_position, path_found=None):
        print("-" * (self.n * 2 + 1))
        for y in range(self.n - 1, -1, -1):
            row = "|"
            for x in range(self.n):
                pos = (x, y)
                if pos == robot_position:
                    row += " X"
                elif pos == goal_position:
                    row += " G"
                elif path_found and pos in path_found:
                    row += " *"
                elif pos in self.obstacles:
                    row += " #"
                elif pos in closed:
                    row += " -"
                elif pos in visited:
                    row += " o"
                else:
                    row += " ."
            row += " |"
            print(row)
        print("-" * (self.n * 2 + 1))

class ModelBasedAgent_BFS_Goal:
    """
    Agente que usa Busca em Largura (BFS) para encontrar o caminho mais curto.
    """
    def __init__(self, initial_position, goal_position, grid):
        self.position = initial_position
        self.goal_position = goal_position
        self.grid = grid
        self.queue = deque([initial_position]) 
        self.visited_set = {initial_position} 
        self.parents = {initial_position: None}
        self.steps = 0
        self.path_found = []

    def neighbors(self, pos):
        """Retorna os vizinhos válidos de uma posição."""
        x, y = pos
        candidates = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        return [p for p in candidates if self.grid.is_free(p)]

    def act(self):
        """
        Lógica da BFS: processa a fila até encontrar o objetivo.
        """
        if not self.queue:
            print("Não há caminho possível para o objetivo.")
            return False

        current = self.queue.popleft() 
        self.position = current
        self.steps += 1
        
        print(f"Avançando para {current}")
        
        if current == self.goal_position:
            self.reconstruct_path(current)
            print("Objetivo alcançado!")
            return False

        neighbors = self.neighbors(current)
        for next_pos in neighbors:
            if next_pos not in self.visited_set:
                self.visited_set.add(next_pos)
                self.queue.append(next_pos)
                self.parents[next_pos] = current

        return True

    def reconstruct_path(self, current):
        """Reconstrói o caminho do objetivo até o início usando o dicionário parents."""
        self.path_found = []
        while current is not None:
            self.path_found.append(current)
            current = self.parents[current]
        self.path_found.reverse()


if __name__ == "__main__":
    grid_size = 8
    num_obstacles = 10

    obstacles = generate_obstacles(grid_size, num_obstacles)
    
    while True:
        initial_pos = generate_initial_position(grid_size, obstacles)
        goal_pos = generate_initial_position(grid_size, obstacles)
        if initial_pos != goal_pos:
            break
            
    world = GridWorld(grid_size, obstacles)
    robot = ModelBasedAgent_BFS_Goal(initial_pos, goal_pos, world)

    print(f"Iniciando busca do caminho de {initial_pos} para {goal_pos}.")
    
    world.print_grid(robot.position, robot.visited_set, set(), goal_pos)

    while robot.act():
        world.print_grid(robot.position, robot.visited_set, set(), goal_pos)
        time.sleep(0.3)

    success = "Não"
    path_length = 0

    if robot.path_found:
        success = "Sim"
        path_length = len(robot.path_found)
        print("\n=== CAMINHO ENCONTRADO! ===")
        print("Caminho percorrido:", robot.path_found)
        
    print("\n=== MÉTRICAS ===")
    print(f"Sucesso na Tarefa: {success}")
    print(f"Comprimento do Caminho: {path_length} passos")
    print(f"Passos totais na busca: {robot.steps}")
    
    if robot.path_found:
        print("\nVisualização do caminho final:")
        world.print_grid(robot.path_found[-1], set(), set(), goal_pos, robot.path_found)
