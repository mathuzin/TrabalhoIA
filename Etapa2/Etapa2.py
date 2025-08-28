import time
import random

class GridWorld:
    def __init__(self, n=8, obstacles=None):
        """Inicializa o ambiente do grid."""
        self.n = n
        self.bounds = {'norte': n - 1, 'sul': 0, 'leste': n - 1, 'oeste': 0}
        self.obstacles = obstacles if obstacles else set()

    def is_free(self, position):
        """Verifica se uma posição está dentro dos limites e não é um obstáculo."""
        x, y = position
        return 0 <= x < self.n and 0 <= y < self.n and position not in self.obstacles
    
    def print_grid(self, robot_position, visited, closed):
        """Imprime o grid com a posição do robô e as células visitadas/fechadas."""
        print("-" * (self.n * 2 + 1))
        for y in range(self.n - 1, -1, -1):
            row = "|"
            for x in range(self.n):
                pos = (x, y)
                if pos == robot_position:
                    row += " X"
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

class ModelBasedAgentDFS:
    """
    Agente baseado no fluxo de exploração DFS (Busca em Profundidade).
    Mantém uma pilha de visitados e uma lista de células fechadas.
    """
    def __init__(self, initial_position, grid):
        self.position = initial_position
        self.grid = grid
        self.visited_stack = [initial_position]  
        self.closed_stack = []  
        self.visited_set = {initial_position} 
        self.steps = 0
        self.redundant_steps = 0

    def neighbors(self, pos):
        """Retorna os vizinhos válidos de uma posição."""
        x, y = pos
        candidates = {
            'norte': (x, y + 1),
            'sul': (x, y - 1),
            'leste': (x + 1, y),
            'oeste': (x - 1, y)
        }
        return {d: p for d, p in candidates.items() if self.grid.is_free(p)}

    def act(self):
        """
        Implementa a lógica de exploração:
        - Avança para um vizinho não visitado.
        - Se não houver, fecha a célula atual e faz backtracking.
        """
        current = self.position
        neighbors = self.neighbors(current)

        unvisited = [p for p in neighbors.values() if p not in self.visited_set]

        if unvisited:
            next_pos = unvisited[0]
            self.visited_stack.append(next_pos)
            self.visited_set.add(next_pos)
            self.position = next_pos
            print(f"Avançando para {next_pos}")
        else:
            if self.visited_stack:
                closed = self.visited_stack.pop()
                self.closed_stack.append(closed)
                if self.visited_stack:
                    self.position = self.visited_stack[-1]
                    self.redundant_steps += 1
                    print(f"Voltando para {self.position} (fechou {closed})")
                else:
                    return False
            else:
                return False

        self.steps += 1
        return True

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

if __name__ == "__main__":
    grid_size = 8
    num_obstacles = 5

    obstacles = generate_obstacles(grid_size, num_obstacles)
    initial_pos = generate_initial_position(grid_size, obstacles)

    world = GridWorld(grid_size, obstacles)
    robot = ModelBasedAgentDFS(initial_pos, world)

    print("Iniciando simulação baseada no fluxograma (DFS com pilha de fechados).")
    world.print_grid(robot.position, robot.visited_set, robot.closed_stack)

    while robot.act():
        world.print_grid(robot.position, robot.visited_set, robot.closed_stack)
        time.sleep(0.1)

    total_cells = grid_size * grid_size - len(obstacles)
    completeness_calc = len(robot.visited_set)
    completeness_percentage = completeness_calc / total_cells * 100 if total_cells > 0 else 0

    print("\n=== MÉTRICAS ===")
    print(f"Células acessíveis: {total_cells}")
    print(f"Células exploradas: {completeness_calc}")
    print(f"Completude da exploração: {completeness_percentage:.2f}%")
    print(f"Passos totais: {robot.steps}")
    print(f"Passos redundantes (backtracking): {robot.redundant_steps}")
    
    success = "Sim" if completeness_percentage >= 100 else "Não"
    print(f"Sucesso no desvio: {success}")
