import random
import time

class GridWorld:
    def __init__(self, n=10, obstacles=None):
        self.n = n
        self.obstacles = obstacles if obstacles else set()
        self.bounds = {'norte': n - 1, 'sul': 0, 'leste': n - 1, 'oeste': 0}

    def is_wall_or_obstacle(self, position):
        x, y = position
        if (x, y) in self.obstacles:
            return True
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            return True
        return False

    def print_grid(self, robot_position, visited):
        print("-" * (self.n * 2 + 1))
        for y in range(self.n - 1, -1, -1):
            row = "|"
            for x in range(self.n):
                if (x, y) == robot_position:
                    row += " X"
                elif (x, y) in self.obstacles:
                    row += " #"
                elif (x, y) in visited:
                    row += " o"
                else:
                    row += " ."
            row += " |"
            print(row)
        print("-" * (self.n * 2 + 1))


class ModelBasedReactiveAgent:
    def __init__(self, initial_position, grid):
        self.position = initial_position
        self.grid = grid
        self.visited = set()
        self.closed = set()
        self.stack = [initial_position]  # memória (backtracking)

        # movimentos possíveis
        self.directions = {
            'norte': (0, 1),
            'leste': (1, 0),
            'sul': (0, -1),
            'oeste': (-1, 0)
        }

    def act(self):
        self.visited.add(self.position)

        # tenta mover para vizinho não visitado
        for direction, (dx, dy) in self.directions.items():
            next_pos = (self.position[0] + dx, self.position[1] + dy)

            if not self.grid.is_wall_or_obstacle(next_pos) and next_pos not in self.visited:
                self.stack.append(next_pos)
                self.position = next_pos
                return False  # continua explorando

        # se não há vizinhos disponíveis → fecha e volta
        self.closed.add(self.position)
        self.stack.pop()

        if not self.stack:  # explorou tudo
            return True

        self.position = self.stack[-1]
        return False


if __name__ == "__main__":
    grid_size = 10
    obstacles = {(3, 3), (4, 3), (5, 5), (2, 7)}  # exemplo

    initial_x = random.randint(0, grid_size - 1)
    initial_y = random.randint(0, grid_size - 1)
    initial_pos = (initial_x, initial_y)

    print(f"Iniciando simulação em um grid {grid_size}x{grid_size}...")
    print(f"Posição inicial do robô: {initial_pos}\n")

    world = GridWorld(grid_size, obstacles)
    robot = ModelBasedReactiveAgent(initial_pos, world)

    step = 0
    done = False
    while not done:
        step += 1
        done = robot.act()
        print(f"Passo {step}. Posição: {robot.position}")
        world.print_grid(robot.position, robot.visited)
        time.sleep(0.2)

    print(f"\nExploração concluída em {step} passos!")
    print(f"Células visitadas: {len(robot.visited)}")
    print(f"Células fechadas: {len(robot.closed)}")

