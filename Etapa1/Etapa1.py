import random
import time

class GridWorld:
    """
    Representa o ambiente de grid n x n.
    """
    def __init__(self, n=10):
        self.n = n
        self.bounds = {'norte': n - 1, 'sul': 0, 'leste': n - 1, 'oeste': 0}

    def is_wall(self, position):
        """
        Verifica se a posição está nos limites do grid (uma "parede").
        Retorna um dicionário com a direção e se é uma parede.
        """
        x, y = position
        walls = {
            'norte': y == self.bounds['norte'],
            'sul': y == self.bounds['sul'],
            'leste': x == self.bounds['leste'],
            'oeste': x == self.bounds['oeste']
        }
        return walls
    
    def print_grid(self, robot_position):
        """
        Imprime o estado atual do grid com o robô.
        'R' representa a posição do robô, '.' é uma célula vazia.
        """
        print("-" * (self.n * 2 + 1))
        for y in range(self.n - 1, -1, -1):
            row = "|"
            for x in range(self.n):
                if (x, y) == robot_position:
                    row += " R"
                else:
                    row += " ."
            row += " |"
            print(row)
        print("-" * (self.n * 2 + 1))

class SequentialReactiveAgent:
    """
    Representa o agente reativo que segue uma sequência de direções.
    """
    def __init__(self, initial_position, grid):
        self.position = initial_position
        self.grid = grid
        self.move_sequence = ['norte', 'leste', 'sul', 'oeste']
        self.current_step = 0
        self.walls_collided = set()
    
    def act(self):
        """
        Ações do agente: move-se na direção atual até colidir, depois avança para a próxima.
        Retorna True se todos os limites foram encontrados, False caso contrário.
        """
        if self.current_step >= len(self.move_sequence):
            print("Objetivo alcançado: todas as quatro paredes foram colididas!")
            return True

        current_direction = self.move_sequence[self.current_step]
        
        next_position = list(self.position)
        if current_direction == 'norte': next_position[1] += 1
        elif current_direction == 'leste': next_position[0] += 1
        elif current_direction == 'sul': next_position[1] -= 1
        elif current_direction == 'oeste': next_position[0] -= 1
        
        if self.grid.is_wall(tuple(next_position))[current_direction]:
            print(f"Colisão detectada na parede {current_direction}. Movendo para a próxima direção.")
            self.walls_collided.add(current_direction)
            self.current_step += 1
        else:
            self.position = tuple(next_position)
            print(f"Movendo para {current_direction}. Nova posição: {self.position}")
        
        return False

if __name__ == "__main__":
    grid_size = 10
    
    initial_x = random.randint(0, grid_size - 1)
    initial_y = random.randint(0, grid_size - 1)
    initial_pos = (initial_x, initial_y)
    
    print(f"Iniciando simulação em um grid {grid_size}x{grid_size}...")
    print(f"Posição inicial do robô: {initial_pos}\n")
    
    world = GridWorld(grid_size)
    robot = SequentialReactiveAgent(initial_pos, world)

    world.print_grid(robot.position)
    
    step = 0
    while not robot.act():
        step += 1
        print(f"Passo {step}. Direção atual: {robot.move_sequence[robot.current_step] if robot.current_step < len(robot.move_sequence) else 'N/A'}")
        print(f"Paredes colididas até agora: {robot.walls_collided}\n")
        world.print_grid(robot.position)
        time.sleep(0.5)

    print(f"\nSimulação concluída em {step} passos.")
