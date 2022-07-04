import random
import math
import time

from numpy import column_stack

class Individuo_N_reinas():
    "Clase que permite modelar un individuo de N Reinas como objeto."

    def __init__(self, n , configuracion = None):
        # Constructor de la clase Individuo_N_reinas que permite instanciar un individuo, sea o no
        # solución del problema o no de N_reinas. 
        # Devuelve una lista cuyos valores representan la ubicación de cada reina en las columnas 
        # del tablero.
        # Recibe por parámetro a n como indicador de la dimensión del tablero en cuestión.
        # Si recibe por parámetro una lista de posiciones, instancia al individuo de acuerdo a ella. 
        # Si no la recibe, arma una lista con posiciones elegidas de forma aleatoria. 

        self.dimension = n

        #Si recibe la configuración en una lista de posiciones, instancia al individuo respecto de ella:
        if configuracion != None:
            self.individuo = configuracion
        #Si no recibe la configuración en una lista de posiciones, lo instancia de forma aleatoria:
        else:
            individuo = []
            # Genero la configuración del individuo, distribuyendo de manera aleatoria las reinas en el tablero.
            for i in range (self.dimension):
                individuo.append(random.randrange(1, self.dimension + 1, 1))
            self.individuo = individuo
        
        self.puntaje =self.evaluar_aptitud()

    def evaluar_aptitud(self):
        # Método de la clase Individuo_N_reinas que permite evaluar el puntaje de un determinado 
        # individuo (tablero) según sea apto como solución al problema de N_rerinas. 
        # Devuelve el puntaje total obtenido tras evaluarlo.
        puntaje = 0
        # Recorro cada valor del individuo (que representa cada columna)
        for columna_actual in range(self.dimension):
            # Recorro cada valor previo HASTA la posición anterior a la actual
            for columna_anterior in range(columna_actual):
                # Guardo el valor de posición en la que se encuentra la reina
                valor_columa_actual = self.individuo[columna_actual]

                # Guardo el valor de la posición en la que se encuentra la reina respecto 
                # de aquella con la que estoy comparando.
                valor_columna_anterior = self.individuo[columna_anterior]

                # Guardo la diferencia de posiciones entre la columna actual y la columna
                # de la reina contra la que estoy realizando la comparación.
                diferencia = columna_actual - columna_anterior

                # Valida que ambas reinas no estén en la misma fila
                if valor_columa_actual == valor_columna_anterior:
                    puntaje += 1
                
                # Valida que la reina actual no esté en diagonal a la anterior (arriba)
                elif valor_columa_actual == valor_columna_anterior + diferencia:
                    puntaje += 1

                # Valida que la reina actual no esté en diagonal a la anterior (abajo)
                elif valor_columa_actual == valor_columna_anterior - diferencia:
                    puntaje += 1

        return puntaje

    def cruce (self , individuo_2):
        # Método de la clase Individuo_N_reinas que permite, a partir de dos individuos, cruzarlos
        # para obtener uno nuevo. Devuelve una lista con la configuración del individuo nuevo.
        nuevo_individuo = []
        for i in range (self.dimension):
            indicador = random.randint(0, 1)
            if indicador == 0:
                nuevo_individuo.append(self.individuo[i])
            else:
                nuevo_individuo.append(individuo_2.individuo[i])
        return nuevo_individuo

    def mutar (self):
        # Método de la clase Individuo_N_reinas que permite, a partir de un determinado individuo, 
        # obtener una lista con la configuración de una mutación obtenida de manera aleatoria.
        # Devuelve una lista con la configuración del individuo nuevo.
        
        mutacion_individuo = []
        for i in range (self.dimension):
            indicador = random.randint(0, 1)
            if indicador == 0:
                mutacion_individuo.append(self.individuo[i])
            else:
                mutacion_individuo.append(random.randrange(1, self.dimension + 1, 1))
        return mutacion_individuo

    def imprimir_en_tablero(self):	
	    # Método de la clase Individuo_N_reinas que permite, imprimir por pantalla la configuración
        # de reinas en un tablero. 

        separacion_filas = "  +-----+" + "-----+"*(self.dimension-2) + "-----+"
        fila_tablero = []
        print (separacion_filas)
        # Nos desplazamos en el tablero:
        for fila in range (self.dimension):
            contenido_fila = "|"
            for columna in range (self.dimension):
                posicion_ocupada= self.individuo[columna] -1 
                if self.dimension - fila - 1  == posicion_ocupada:
                    # Hay una reina
                    contenido_fila+= "  " + "X" + "  |"
                else:
                     # No hay reina
                     contenido_fila+= "  " + " " + "  |"
            print (str(self.dimension - fila ) + " " + contenido_fila)
            print (separacion_filas)
        # Se imprime la referencia de las columnas como pie del tablero:
        pie = " "
        for i in range (1 , self.dimension+1):
            if i<10:
                pie+= "    " + str(i) + " "	
            else:
                pie+= "   " + str(i) + " "
        print (pie)
        print("")
        print("----------------------------------------")

class Poblacion_N_Reinas():
    "Clase que permite modelar una población de N Reinas como objeto."

    def __init__(self, n, cant_individuos,indice_seleccion):
        # Constructor de la clase Poblacion_N_Reinas que permite instanciar la población
        # para la resolución del problema de N_reinas.
        # Recibe n como indicador de la dimensión del tablero en cuestión y cant_individuos que
        # indica cúantos individuos deben considerarse para armar la población inicial (en nuestro 
        # caso los individuos son los tableros con la distribución las n reinas).
        self.dimension = n
        self.indice_seleccion = indice_seleccion

        #Calculo los parámetros:
        self.cant_seleccion = math.trunc(cant_individuos * indice_seleccion)
        self.cant_a_repoblar = cant_individuos - self.cant_seleccion
        
        poblacion = []
        for i in range (cant_individuos):
            #Instancio un individuo:
            individuo = Individuo_N_reinas(self.dimension)
            poblacion.append(individuo)
        self.poblacion = poblacion
            
    def ordenar_por_puntaje(self):
        # Método de la clase Poblacion_N_Reinas que permite ordenar_por_puntaje los individuos de una población 
        # según su puntaje.
        self.poblacion.sort(key=lambda x : x.evaluar_aptitud())

    def seleccion(self):
        # Método de la clase Poblacion_N_Reinas que permite seleccionar a partir de una población,
        # cuáles de los individuos que la conforman van a conservarse dentro de la base que se
        # contemplará como soluciones más adecuadas al problema del tablero de N reinas.
        
        poblacion_mas_apta = [] 
        self.ordenar_por_puntaje()
        poblacion_mas_apta = self.poblacion[0:self.cant_seleccion]
        self.poblacion = poblacion_mas_apta

    def repoblar(self):
        # Método de la clase Poblacion_N_Reinas que permite repoblar tras la selección de los 
        # individuos más aptos de una población, aplicando cruzamiento y mutación de forma aleatoria
        # sobre dichos individuos.

        repoblacion = []
        for i in range (self.cant_a_repoblar):
            # Elijo al azar un individuo de la poblacion:
            posicion = random.randrange(0, len(self.poblacion)-1 , 1) #Descarto el último porque no tiene sucesor
            individuo = self.poblacion[posicion]
            individuo_2 = self.poblacion[posicion+1]
            # Cruzo el individuo con su siguiente:
            configuracion_cruza = individuo.cruce(individuo_2)
            # Instancio el nuevo individuo con la configuración obtenida:
            individuo_cruza = Individuo_N_reinas (len(configuracion_cruza) , configuracion_cruza)

            # Aleatoriamente elegimos si nos quedamos con el individuo obtenido por cruzamiento 
            # (indicador = 1) o si tomamos el afectado por mutación (indicador = 0):
            indicador = random.randint(0, 1)
            if indicador == 0:
                repoblacion.append(individuo_cruza)
            else:
                configuracion_mutacion = individuo_cruza.mutar()
                individuo_muta = Individuo_N_reinas (len(configuracion_mutacion) , configuracion_mutacion)
                repoblacion.append(individuo_muta)
        for individuo in repoblacion:
            self.poblacion.append(individuo)
        self.ordenar_por_puntaje()

    def listar(self):
        # Método de la clase Poblacion_N_Reinas que permite listar su población.
        for i in range (len(self.poblacion)):
            print (self.poblacion[i].individuo, self.poblacion[i].puntaje)

def iterar_generaciones(min_cant_soluciones, max_iteraciones , poblacion):
    # Función que permite realizar una cierta cantidad desoluciones sobre una població 
    # para hallar solución el problema de N_reinas aplicando los métodos del algorítmo genético.

    cant_iteraciones = 0
    cant_soluciones = 0

    # Establecemos un ciclo de iteraciones con una condición de terminación.
    while cant_soluciones != min_cant_soluciones and cant_iteraciones < max_iteraciones:
        cant_soluciones = 0
        individuos_solucion=[]
        for individuo in poblacion.poblacion:
            if individuo.puntaje == 0:
                if individuo.individuo not in individuos_solucion:
                    individuos_solucion.append(individuo.individuo)
                    cant_soluciones+=1
        poblacion.seleccion()
        poblacion.repoblar()
        print ("Iteración número " + str(cant_iteraciones))
        cant_iteraciones+=1
    return individuos_solucion , cant_iteraciones , cant_soluciones

def mostrar_resultados(dimension_tablero, individuos_solucion, min_cant_soluciones, cant_soluciones, cant_iteraciones):
    # Función que permite mostrar el resultado obtenido tras aplicar el algoritmo genético sobre 
    # una determinada población. 
    # Imprime además el/los tablero/s hallado/s como solucón del problema de N_reinas según corresponda:
    
    # Instancio los individuos de acuerdo a la configración registrada en individuos_solucion para poder usar el métodos para imprimir tablero:
    poblacion_solucion = []
    for individuo in individuos_solucion:
        poblacion_solucion.append(Individuo_N_reinas(dimension_tablero,individuo))

    if len(individuos_solucion) < min_cant_soluciones:
        # Si no se encuentran la cantidad de soluciones indicada:
        print ("Bajo la cantidad de iteraciones máximas seteadas, no se han encontrado " + str(min_cant_soluciones) + " resultados posibles para el problema.")
        if len(individuos_solucion) == 1:
            # Si se encuentra sólo una solución (aunque no sea suficientes)
            print ("Sólo se encontró una solución: ") 
            poblacion_solucion[0].imprimir_en_tablero() 
        else:
            # Si se encuentran varias soluciones (aunque no las suficientes)
            print ("Se encontraron " + str(len(individuos_solucion)) + " soluciones en la iteración número " + str(cant_iteraciones))
            for i in range (cant_soluciones):
                poblacion_solucion[i].imprimir_en_tablero()   
    else:
        # Si se encuentran igual o más soluciones que la cantidad indicada:
        if len(individuos_solucion) == 1:
            print ("Se encontró la solución requerida en la iteración número " + str(cant_iteraciones))
            for i in range (cant_soluciones):
                poblacion_solucion[i].imprimir_en_tablero()
        else:
            print ("Se encontraron " + str(len(individuos_solucion)) + " soluciones en la iteración número " + str(cant_iteraciones))
            for i in range (cant_soluciones):
                poblacion_solucion[i].imprimir_en_tablero()

def decorador(function):
	def wrapper(*args, **kwargs):
		start_time = time.time()
		function(*args, *kwargs)
		print("---\nResolución alcanzada en {s} segundos".format(s = (time.time() - start_time)))
	return wrapper

@decorador
def Algoritmo_Genetico_N_Reinas(dimension_tablero = 5 , cant_individuos = 70 , indice_seleccion = 0.3 , max_iteraciones = 10000 , min_cant_soluciones = 1 ):
    # Función que permite hallar soluciones para el problema de N_reinas aplicando un algorítmo genético.
    # Recibe los siguientes parámetros, los cuales poseen asignados valores por defecto:
    # dimension_tablero= indica la dimensión del tablero a resolver. 
    # cant_individuos= indica la cantidad de individuos con la que deberá instanciarse la población inicial y con la cual deberá repoblarse.
    # indice de seleccion= indica la proporción que deberá conservarse de una población tras aplicar el método de selección.
    # max_iteraciones= inidca la cantidad de generaciones que deberán crearse.
    # min_cant_soluciones= indica la cantidad mínima de soluciones que deberán encontrarse. 

    if dimension_tablero < 4: 
        print ("No existen soluciones posibles del problema para " + str(dimension_tablero) + " dimensiones.")
    else: 
        # Instanciamos una población
        poblacion = Poblacion_N_Reinas(dimension_tablero, cant_individuos,indice_seleccion)
        
        # Mostrar por pantalla la configuración de la población creada en la última iteración del ciclo:
        print ("Población inicial: ")
        poblacion.listar()
        print()

        individuos_solucion , cant_iteraciones , cant_soluciones = iterar_generaciones(min_cant_soluciones, max_iteraciones , poblacion) 

        # Mostrar por pantalla la configuración de la población alcanzada en el último ciclo de la iteración:
        print ("Población de la Última Generación creada: ")
        poblacion.listar()
        print()

        mostrar_resultados(dimension_tablero, individuos_solucion, min_cant_soluciones, cant_soluciones, cant_iteraciones)
        

# Invocamos al mail seteando los parámetros para el proceso; si no se los pasamos toma
# valores por defecto para todos ellos:
Algoritmo_Genetico_N_Reinas ( 5 , 100 , 0.3 , 10000 , 1)