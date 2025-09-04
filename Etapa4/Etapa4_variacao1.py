import time
import random
from collections import deque
import heapq 

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

class GridWorldWithCosts:
    def __init__(self, n=8, obstacles=None):
        self.n = n
        self.obstacles = obstacles if obstacles else set()
        self.terrain = {}
        self.generate_terrain()

    def generate_terrain(self):
        """Gera um grid com custos de terreno aleatórios (1, 2 ou 3)."""
        for y in range(self.n):
            for x in range(self.n):
                pos = (x, y)
                if pos in self.obstacles:
                    continue
                rand_val = random.random()
                if rand_val < 0.6:
                    self.terrain[pos] = 1 
                elif rand_val < 0.9:
                    self.terrain[pos] = 2 
                else:
                    self.terrain[pos] = 3 
    
    def get_cost(self, position):
        """Retorna o custo de movimento para uma posição."""
        if position in self.obstacles:
            return float('inf')
        return self.terrain.get(position, 1)

    def is_free(self, position):
        x, y = position
        return 0 <= x < self.n and 0 <= y < self.n and position not in self.obstacles
        
    def print_grid(self, robot_position, visited, closed, goal_position, path_found=None):
        print("-" * (self.n * 2 + 1))
        for y in range(self.n - 1, -1, -1):
            row = "|"
            for x in range(self.n):
                pos = (x, y)
                if pos in self.obstacles:
                    row += " #"
                elif pos == robot_position:
                    row += " X"
                elif pos == goal_position:
                    row += " G"
                elif path_found and pos in path_found:
                    row += " *"
                else:
                    cost = self.terrain.get(pos, 1)
                    row += f" {cost}"
            row += " |"
            print(row)
        print("-" * (self.n * 2 + 1))
        print("Legenda: 1 = Normal (C:1), 2 = Arenoso (C:2), 3 = Rochoso (C:3), # = Obstáculo, X = Agente, G = Destino, * = Caminho")

class DijkstraAgent:
    def __init__(self, initial_position, goal_position, grid):
        self.initial_position = initial_position
        self.position = initial_position
        self.goal_position = goal_position
        self.grid = grid
        self.path = []
        self.total_cost = 0
        self.steps = 0
        self.visited = set()
        self.parents = {}
        self.found_goal = False

        self.find_path_dijkstra()

    def neighbors(self, pos):
        """Retorna os vizinhos válidos de uma posição."""
        x, y = pos
        candidates = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        return [p for p in candidates if self.grid.is_free(p)]

    def find_path_dijkstra(self):
        """
        Executa o algoritmo de Dijkstra para encontrar o caminho de menor custo.
        """
        pq = [(0, self.initial_position)]

        costs = {self.initial_position: 0}

        while pq:
            current_cost, current_pos = heapq.heappop(pq)
            self.visited.add(current_pos)

            if current_pos == self.goal_position:
                self.found_goal = True
                break

            if current_cost > costs.get(current_pos, float('inf')):
                continue

            for next_pos in self.neighbors(current_pos):
                new_cost = current_cost + self.grid.get_cost(next_pos)
                
                if new_cost < costs.get(next_pos, float('inf')):
                    costs[next_pos] = new_cost
                    self.parents[next_pos] = current_pos
                    heapq.heappush(pq, (new_cost, next_pos))

        if self.found_goal:
            self.reconstruct_path()
            self.total_cost = costs[self.goal_position]
        
    def reconstruct_path(self):
        """Reconstrói o caminho do objetivo até o início usando o dicionário parents."""
        path = []
        current = self.goal_position
        while current is not None:
            path.append(current)
            current = self.parents.get(current)
        path.reverse()
        self.path = path
        
    def act(self):
        """
        Avança o agente para o próximo passo no caminho pré-calculado.
        """
        if not self.found_goal:
            print("Nenhum caminho foi encontrado.")
            return False
            
        if self.position == self.goal_position:
            print("Objetivo alcançado!")
            return False

        current_index = self.path.index(self.position)
        if current_index + 1 < len(self.path):
            self.steps += 1
            next_pos = self.path[current_index + 1]
            self.position = next_pos
            print(f"Avançando para {self.position}")
            return True
        else:
            print("Fim do caminho pré-calculado.")
            return False

if __name__ == "__main__":
    grid_size = 8
    num_obstacles = 10

    obstacles = generate_obstacles(grid_size, num_obstacles)
    
    while True:
        initial_pos = generate_initial_position(grid_size, obstacles)
        goal_pos = generate_initial_position(grid_size, obstacles)
        if initial_pos != goal_pos:
            break
            
    world = GridWorldWithCosts(grid_size, obstacles)
    robot = DijkstraAgent(initial_pos, goal_pos, world)

    print(f"Iniciando planejamento do caminho de {initial_pos} para {goal_pos}.")
    
    if robot.found_goal:
        print("Caminho de menor custo calculado com sucesso!")
        print("Caminho planejado:", robot.path)
    else:
        print("Não foi possível encontrar um caminho.")
        
    world.print_grid(robot.position, set(), set(), goal_pos)

    while robot.act():
        world.print_grid(robot.position, robot.visited, set(), goal_pos, robot.path)
        time.sleep(0.5)

    success = "Não"
    path_length = 0

    if robot.found_goal:
        success = "Sim"
        path_length = len(robot.path)
    
    print("\n=== MÉTRICAS ===")
    print(f"Sucesso na Tarefa: {success}")
    print(f"Comprimento do Caminho: {path_length} passos")
    print(f"Custo Total do Caminho: {robot.total_cost}")
    print(f"Passos totais na busca: {robot.steps}")
    
    if robot.found_goal:
        print("\nVisualização do caminho final:")
        world.print_grid(robot.path[-1], set(), set(), goal_pos, robot.path)
