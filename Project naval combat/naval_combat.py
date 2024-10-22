import random # Importa la biblioteca random
class Ship:
    def __init__(self, name, size):
        self.name = name # Nombre del barco
        self.size = size # Tamaño del barco
        self.position = [] #Almacena la posiciones donde colocamos los barcos
        self.hits = 0 #Contador de impactos en el barco
    
    def place_ship(self, board, start_row, start_col, direction):
        positions = []  # Para almacenar las posiciones que ocupará el barco
        if direction == 'H':
            if start_col + self.size > len(board[0]):  # Verifica si el barco cabe horizontalmente
                return False
            for i in range(self.size):
                if board[start_row][start_col + i] != ' ': # Verifica si la posición está libre
                    return False
                positions.append((start_row, start_col + i)) # Almacena las posiciones
        elif direction == 'V':  
            if start_row + self.size > len(board):  # Verifica si el barco cabe verticalmente
                return False
            for i in range(self.size):
                if board[start_row + i][start_col] != ' ': # Verifica si la posición está libre
                    return False
                positions.append((start_row + i, start_col))  # Almacena las posiciones
        
        # Coloca el barco en el tablero
        for row, col in positions:
            board[row][col] = self.name[0] # Usa la primera letra del nombre del barco
        self.positions = positions  # Almacena las posiciones en el objeto del barco
        return True 

    def register_hits(self):
        self.hits += 1 # Incrementa el contador de impactos
        if self.hits == self.size: # Verifica si el barco ha sido hundido
            print(f"¡El {self.name} ha sido hundido!")
            return True
        else:
            print(f"¡El {self.name} ha sido impactado!! Número total de impactos: {self.hits}")
            return False 
        
class Player:
    def __init__(self, name, is_computer = False):
        self.name = name  # Nombre del jugador
        self.is_computer = is_computer  # Indica si el jugador es una computadora
        self.board = [[' ' for _ in range(10)] for _ in range(10)]  # Tablero del jugador
        self.ships = [] # Lista para almacenar los barcos del jugador
        self.hits = [[' ' for _ in range(10)] for _ in range(10)]  # Tablero para rastrear impactos

    def place_ships(self):
        ships_to_place = [Destroyer(), Submarine(), Battleship()] # Barcos a colocar

        for ship in ships_to_place:
            while True:
                print(f"Posicionando el {ship.name} de tamaño {ship.size}")
                if self.is_computer:  # Si es una computadora
                    start_row = random.randint(0, 9)
                    start_col = random.randint(0, 9)
                    direction = random.choice(['H', 'V'])
                    print(f"Computadora coloca su {ship.name} en ({start_row}, {start_col}) dirección {direction}")
                else:
                    try:
                        start_row = int(input(f"{self.name}, introduzca la fila inicial (0-9) para su {ship.name}: "))
                        start_col = int(input(f"{self.name}, introduzca la columna iniciar (0-9) para su {ship.name}: "))
                        direction = input("Introduzca la dirección (H para Horizontal y V para Vertical): ").upper()
                    except ValueError:
                        print("Datos de entrada no validos. Por favor, introduzca coordenadas válidas.")
                        continue

                if direction not in ['H', 'V']:
                    print("Dirección no válida. Debe ser 'H' para Horizontal o 'V' para Vertical.")
                    continue

                if self.place_ship(ship, start_row, start_col, direction):
                    print(f"¡{ship.name} colocado exitosamente!")
                    self.print_board(reveal_ships=True)  # Mostrar tablero con el barco colocado
                    break  
                else:
                    print(f"No se pudo posicionar el {ship.name}. Intente de nuevo.")
                    
    def place_ship(self, ship, start_row, start_col, direction):
        positions = [] # Para almacenar las posiciones que ocupará el barco
        if direction == 'H':
            if start_col + ship.size > 10: # Verifica si el barco cabe horizontalmente
                return False  
            for i in range(ship.size):
                if self.board[start_row][start_col + i] != ' ': # Verifica si la posición está libre
                    return False  
                positions.append((start_row, start_col + i))

        elif direction == 'V':
            if start_row + ship.size > 10: # Verifica si el barco cabe verticalmente 
                return False  
            for i in range(ship.size):
                if self.board[start_row + i][start_col] != ' ':  # Verifica si la posición está libre
                    return False  
                positions.append((start_row + i, start_col))

        for row, col in positions:
            self.board[row][col] = ship.name[0] # Usa la primera letra del nombre del barco
        ship.positions = positions
        self.ships.append(ship)  # Agrega el barco a la lista de barcos del jugador
        return True
    
    def print_board(self, reveal_ships=False):
        print(f" Tablero de: {self.name}")
        for row in self.board:
            if reveal_ships:
                 # Revela los barcos y muestra el mar como '~'
                print(' '.join([cell if cell != ' ' else '~' for cell in row]))
            else:
                 # Oculta los barcos al revelar el tablero al oponente y muestra el mar como '~'
                print(' '.join(['~' if cell == ' ' else cell for cell in row]))
    
    def attack(self, opponent):
        if self.is_computer:  # Si es una computadora
            while True:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                print(f"La computadora ataca en ({row}, {col})")
                if opponent.board[row][col] == 'X' or opponent.board[row][col] == 'O':
                    print("¡Ataque repetido! La computadora elige otra vez.")
                    continue
                break
        else:  # Si es un jugador humano
            while True:
                try:
                    row = int(input(f"{self.name}, introduzca la fila (0-9) para su ataque: "))
                    col = int(input(f"{self.name}, introduzca la columna (0-9) para su ataque: "))
                    if 0 <= row < 10 and 0 <= col < 10:  # Posición de ataque válida
                        if opponent.board[row][col] == 'X' or opponent.board[row][col] == 'O':
                            print("¡Ataque repetido! Intente otra vez.")
                            continue
                        break
                    else:
                        print("Coordenadas inválidas. Por favor, introduzca coordenadas entre 0 y 9.")
                except ValueError:
                    print("Datos de entrada no validos. Por favor, introduzca números.")

        # Realiza el ataque
        if opponent.board[row][col] != ' ':
            print("¡El ataque impacto!")
            self.hits[row][col] = 'X'  # Marca el impacto en el tablero de impactos del jugador
            opponent.board[row][col] = 'X'  # Marca el impacto en el tablero del oponente

            # Verifica si el barco ha sido hundido
            for ship in opponent.ships:
                if (row, col) in ship.positions:
                    ship.positions.remove((row, col))
                    if len(ship.positions) == 0:
                        print(f"{self.name} ha hundido el {ship.name} de {opponent.name}!")
        else:
            print("¡El ataque ha fallado!")
            self.hits[row][col] = 'O'  # Marca el fallo
            opponent.board[row][col] = 'O'  # Marca el fallo en el tablero del oponente

    def summary_board(self):
        # Crea una tabla nueva que refleje los impactos y fallos
        summary = [['~' for _ in range(10)] for _ in range(10)]  # Mostramos el agua 
        for row in range(10):
            for col in range(10):
                if self.hits[row][col] == 'X':
                    summary[row][col] = 'X'  # X para impactos 
                elif self.hits[row][col] == 'O':
                    summary[row][col] = 'O'  # 0 para fallos
        return summary

    def print_summary_board(self):
        # Imprimimos la tabla sumatoria de nuestros ataques
        print(f"Resumen de ataques de: {self.name}")
        for row in self.summary_board():
            print(' '.join(row))

    def all_ships_sunk(self):
        # Verifica si todos los barcos han sido hundidos
        return all(len(ship.positions) == 0 for ship in self.ships)


# Inicializando el Destructor
class Destroyer(Ship):
    def __init__(self):
        super().__init__('Destructor', 2)

# Inicializando el Submarino
class Submarine(Ship):
    def __init__(self):
        super().__init__('Submarino', 3)

# Inicializando el Submarino
class Battleship(Ship):
    def __init__(self):
        super().__init__('Acorazado', 4)



class BattleshipGame:
    def __init__(self, player1_name):
         # Mensaje de bienvenida
        print("¡Bienvenido al juego de Batalla Naval!")
        
        # Dandole inico a ambos jugadores
        player1_name = input("Introduzca su nombre: ")
        self.player1 = Player(player1_name)
        self.player2 = Player("Computadora", is_computer=True)

        print(f"Los jugadores son {self.player1.name} contra {self.player2.name}. ¡Buena suerte!")

        self.current_turn = self.player1  # comenzamos con el jugador 1
        self.opponent = self.player2  # Luego el jugador 2 será el que inicie como oponente

    def play(self):
        # Coloca los barcos para ambos jugadores
        print(f"{self.player1.name}, Coloca tus barcos!")
        self.player1.place_ships()

        print(f"{self.player2.name}, Coloca tus barcos!")
        self.player2.place_ships()

        # Bucle del juego: alterna turnos entre jugadores hasta que todos los barcos de un jugador sean hundidos
        while True:
            # Muestra los tableros
            print("\n" + "-" * 20)
            print(f"¡Es el turno de atacar de {self.current_turn.name}!")
            print("\n")

            self.current_turn.attack(self.opponent)

            # Mostrar el resumen de ataques de Player 1 después de su ataque
            if self.current_turn == self.player1:
                self.current_turn.print_summary_board()

            # Verifica si el oponente ha perdido todos los barcos
            if self.opponent.all_ships_sunk():
                print(f"\n¡Felicidades, {self.current_turn.name}! Has hundido todos los barcos de {self.opponent.name} y has ganado el juego!")
                break

            # Cambia de turno
            self.switch_turns()

    def switch_turns(self):
        # Alterna entre el jugador 1 y el jugador 2
        if self.current_turn == self.player1:
            self.current_turn = self.player2
            self.opponent = self.player1
        else:
            self.current_turn = self.player1
            self.opponent = self.player2

# Ejecuta el juego
game = BattleshipGame("Jugador 1")
game.play()


