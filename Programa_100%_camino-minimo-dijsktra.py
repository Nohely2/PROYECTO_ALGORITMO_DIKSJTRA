#-módulos a usar
import turtle                       #-para poder dibujar.
import numpy as np                  #-para matriz.
from queue import PriorityQueue     #-para cola de prioridad

#-entidades

#-entidad FIGURA
class Figure():

    #-constructor de clase
    def __init__(self, x=0, y=0,):

        #-inicializando atributos
        self.pen = turtle.Turtle()
        #-coordenadas de entidad
        self.__x = x  
        self.__y = y  
        #-iniciando entidad con lápiz levantado
        self.p_up()
        #-estableciendo posición de lápiz
        self.set_cursor(x, y)

        #-estableciendo velocidad de pintado
        self.pen.speed(10)

    #-métodos de clase
    def set_cursor(self, x, y):     #-establece posición de lapiz
        self.pen.goto(x, y)

    def set_color(self, color):     #-establece color de lápiz
        if color == '':
            return
        self.pen.pencolor(color)

    def set_width(self, width=1):     #-establece ancho del lápiz
        self.pen.width(width)

    def p_up(self):                 #-establece lápiz levantado
        self.pen.penup()

    def p_down(self):               #-establece lápiz en lienzo
        self.pen.pendown()

    def draw_fig(self):             #-dibuja entidad
        pass

    #getters
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    #setters
    @x.setter
    def x(self, v):
        self.__x = v
    @y.setter
    def y(self, v):
        self.__y = v


#-entidad CIRCULO
class Circle(Figure):
    
    #-constructor de clase
    def __init__(self, x, y, radio):
        super().__init__(x, y)

        #-inicializando atributos

        #-tamanio de circulo
        self.__radio = radio
        #-etiqueta de circulo
        self.__label = ''

    #-método de clase re-escrito
    def draw_fig(self):
        self.p_down()
        self.pen.circle(self.__radio)
        self.pen.write(self.__label, align='center', font=("Arial", 12, "normal"))
        self.p_up()

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, v):
        self.__label = v

#-entidad LINEA
class Line(Figure):

    #-constructor de clase
    def __init__(self, x=0, y=0, x2=0, y2=0, color='black'):
        super().__init__(x, y)

        #-incializando atributos

        #-coordenadas final
        self.__x2 = x2
        self.__y2 = y2
        #-color de línea
        self.__color = color

    #-método de clase re-escrito
    def draw_fig(self):
        self.p_down()
        self.set_cursor(self.__x2, self.__y2)
        self.p_up()

#-muestra la matriz
def show_matrix(matrix, n):
    
    for i in range(n):
        print('\t')
        for j in range(n):
            print(int(matrix[i, j]), end='\t')
        print('')

    print()

#-genera matriz en cero
def gen_zero_matrix(n):

    matrix = np.zeros((n, n))

    return matrix

#-genera matriz de forma aleatoria
def gen_random_matrix(matrix, n):

    for i in range(n):
        for j in range(n):
            if i != j: 
                v = np.random.randint(0, 13)
                matrix[i, j] = v
                matrix[j, i] = v

#-genera matriz de forma manual
def gen_manual_matrix(matrix, n):

    for i in range(n):
        for j in range(n):
            if i != j and matrix[i, j] == 0: 
                v = int(input(f'valor en [{i + 1}][{j + 1}]: '))
                matrix[i, j] = v
                matrix[j, i] = v

#-algoritmo dijsktra
def dijkstra(matrix, start_vertex, end_vertex):
    n = len(matrix)
    visited = [False] * n
    distance = [float('inf')] * n
    parent = [-1] * n

    distance[start_vertex] = 0

    for _ in range(n):
        min_distance = float('inf')
        u = -1

        for i in range(n):
            if not visited[i] and distance[i] < min_distance:
                min_distance = distance[i]
                u = i

        if u == -1:
            break

        visited[u] = True 

        for v in range(n):
            if not visited[v] and matrix[u, v] != 0 and distance[u] + matrix[u, v] < distance[v]:
                distance[v] = distance[u] + matrix[u, v]
                parent[v] = u

    path = []
    v = end_vertex
    #-acumulador para suma de distancia mín. acumulada
    total_distance = 0

    while v != -1:

        path.insert(0, v)
        
        if parent[v] != -1:
            #-acumulando suma de distancia total
            total_distance += matrix[v][parent[v]]
        
        v = parent[v]

    return path, total_distance

#-generar grafo
def draw_graph(matrix, path=None):
    n = len(matrix)
    circles = []

    #-conjunto de conexiones YA dibujadas
    drawn_connections = set()

    #-generamos los nodos en circulos
    for i in range(n):
        #-distribuir los nodos en un círculo
        x = 200 * np.cos(2 * np.pi * i / n) 
        y = 200 * np.sin(2 * np.pi * i / n)
        
        cir = Circle(x, y, 20)
        circles.append(cir)

    #-colocar etiquetas a los nodos
    for i in range(n):
        circles[i].label = i

    #-dibujar nodos
    for cir in circles:
        cir.draw_fig()

    #-dibujar conexiones entre nodos basadas en la matriz
    for i in range(n):
        for j in range(i + 1, n):
            if i != j and matrix[i, j] != 0:
                #-almacenando conexión que se realizará
                connection_key = (i, j)
                #-verificando si la conexión YA existe
                if connection_key not in drawn_connections:
                    weight = matrix[i, j]
                    line = Line(circles[i].x, circles[i].y, circles[j].x, circles[j].y)
                    line.draw_fig()
                    #-agregando etiqueta de peso
                    text_x = (circles[i].x + circles[j].x) / 2
                    text_y = (circles[i].y + circles[j].y) / 2
                    weight_label = f'{weight}'
                    text = Circle(text_x, text_y, 0)
                    text.label = weight_label
                    text.draw_fig()
                    #--
                    drawn_connections.add(connection_key)

    if path:
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            line = Line(circles[u].x, circles[u].y, circles[v].x, circles[v].y)
            line.set_color('red')
            line.set_width(5)
            line.draw_fig()


def request_matrix_size():

    while True:
        try:
            n = int(input('\nIngresar valor de N: '))
            if 5 <= n <= 15:
                break
        except Exception as e:
            print('¡Error de ingreso!')

    return n

def request_user_option():

    while True:
        resp = input('Valores manual[M] - auto[A]: ')
        resp = resp.upper()
        if resp == 'M' or resp == 'A':
            break

    return resp

def run_user_option(resp, matrix, n):

    if resp == 'A':
        print()
        gen_random_matrix(matrix, n)
        show_matrix(matrix, n)
    elif resp == 'M':
        print()
        gen_manual_matrix(matrix, n)
        show_matrix(matrix, n)

    start_vertex = int(input('Ingresar vértice de inicio (1 to N): ')) - 1
    end_vertex = int(input('Ingresar vértice de fin (1 to N): ')) - 1
    
    path, total_distance = dijkstra(matrix, start_vertex, end_vertex)
    
    print(f'\nCamino mínimo desde el vértice {start_vertex + 1} al vértice {end_vertex + 1}: {path}')
    print(f'Distancia mínima acumulada: {total_distance}')

    try:
        draw_graph(matrix, path)
    except Exception as e:
        print('¡PROCESO INTERRUMPIDO!')

def main():

    #-obteniendo tamanio de matriz
    n = request_matrix_size()
    #-generando matriz n * n
    matrix = gen_zero_matrix(n)

    #-mostrando matriz inicial generada
    show_matrix(matrix, n)

    #-solicitando opción de usuario
    resp = request_user_option()
    #-ejecutando según opción de usuario
    run_user_option(resp, matrix, n)


if __name__ == '__main__':
    main()
    wn = turtle.mainloop()
    wn= turtle.Screen()
    wn.title('GRAFO')
