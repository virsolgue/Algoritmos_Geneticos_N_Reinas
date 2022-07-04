# Algoritmo_Genetico_N_Reinas
Implementación de un algoritmo genético para resolver el problema de N reinas.

### FUENTES UTILIZADAS:
- ALGORITMOS GENÉTICOS: 

    https://www.frba.utn.edu.ar/wp-content/uploads/2021/02/AlgoritmosGeneticos-compressed.pdf
- IMPLEMENTACIÓN DE ALGORITMOS GENÉTICOS SOBRE PROBLEMA N REINAS: 

    https://www.cs.buap.mx/~zacarias/FZF/nreinas3.pdf


# Introducción
Los algoritmos genéticos se fundamentan metafóricamente a la evolución natural, en la que cada especia se modifica en la búsqueda de adaptaciones benéficas a un ambiente complicado y cambiante.
Por esto, los algoritmos genéticos incorporan la terminología genética natural y se usan principalmente en problemas de optimización y búsqueda de máximos (o mínimos) pero no está limitados exclusivamente a esta clase de problemas.
Para un problema particular se deben tener los siguientes 5 componentes:

1. Una representación genética de las soluciones potenciales.
2. Una forma de crear la población inicial.
3. Una función de evaluación que juegue el rol del ambiente clasificando los individuos en función de su adaptación.
4. Operadores genéticos que alteren la composición de los hijos (selección, cruza, mutación). 
5. Valores de los parámetros para las distintas variables que usa el algoritmo (tamaño de la población, probabilidad de aplicación de operadores genéticos, etc).

# Definición del problema

El problema de las n-Reinas consiste en encontrar una distribución de n reinas en un tablero de ajedrez de n x n de modo tal que éstas no se ataquen. Así, no pueden encontrarse en la misma fila, columna o diagonal.

Teniendo en cuenta lo antes mencionado respecto a algoritmos genéticos, se propone a continuación un programa implementado con clases en Python que permite dar con al menos una solución del problema de n-Reinas.

# Modelo propuesto

## 1. Representación genética
Partiendo del hecho de que un tablero no puede tener más de una reina por fila, optaremos por representar un tablero como una lista en cuyas posiciones se almacene el valor que ocupa la reina en cada una de las filas.
De esta forma, por ejemplo, el tablero siguiente quedaría representado por la lista [4, 7, 3, 6, 2, 5, 1], constituyendo así nuestro código genético:

```
     1     2     3     4     5     6     7
  +-----+-----+-----+-----+-----+-----+-----+
7 |     |  X  |     |     |     |     |     |
  +-----+-----+-----+-----+-----+-----+-----+
6 |     |     |     |  X  |     |     |     |
  +-----+-----+-----+-----+-----+-----+-----+
5 |     |     |     |     |     |  X  |     |
  +-----+-----+-----+-----+-----+-----+-----+
4 |  X  |     |     |     |     |     |     |
  +-----+-----+-----+-----+-----+-----+-----+
3 |     |     |  X  |     |     |     |     |
  +-----+-----+-----+-----+-----+-----+-----+
2 |     |     |     |     |  X  |     |     |
  +-----+-----+-----+-----+-----+-----+-----+
1 |     |     |     |     |     |     |  X  |
  +-----+-----+-----+-----+-----+-----+-----+
```
*Considerar que las X representan la ubicación de cada una de las reinas*

## 2. Creación de una población inicial

Para poder crear una población, utilizaremos las clases **Poblacion_N_Reinas** e **Individuo_N_reinas**. 
La primer clase arma la población a partir de la dimensión del tablero en cuestión y la definición de la cantidad de individuos que debe presentar; para hacerlo, mediante un ciclo for determinado por la dimensión del tablero, instancia individuos aleatoriamente mediante la clase Individuo_N_reinas.

Al ser aleatoria la constitución de la población, los individuos en ella no son más que posibles configuraciones de tableros, sean o no solución del problema.

## 3. Evalución de la aptitud de la población a la supervivencia

Evaluar la aptitud de la población para resolver el problema, implicará evaluar la aptitud de cada uno de los individuos que la componen.
Para esto, se creó el método *evaluar_aptitud* para la clase **Individuo_N_reinas**, el cual devuelve el puntaje asignado al individuo según sea la cantidad de posiciones incorrectas de reinas que tenga su tablero; este puntaje indica el grado de aptitud: si es cero significa que resuelve el problema, cuánto más grande, más alejado de ser solución.

## 4. Operadores genéticos

Se trata de métodos que permiten crear una nueva población a partir de una inicial. 

### 4.1 - Selección
Se implementó como método *seleccion* de la clase **Poblacion_N_Reinas**. Lo que hace es invocar al método *ordenar_por_puntaje* para ubicar a los individuos más aptos al inicio de la población según su puntaje, y luego actualiza la instancia de la población dejando sólo la cantidad de individuos que deban conformarla. 
Para poder definir cuántos individuos de la población inicial deben conservarse, se utiliza el parámetro indice_selección. 
Si le pasamos el valor 0.3, significa que sólo se seleccionará un 30% de la población inicial.

### 4.2 - Repoblación
Se implementó como método *repoblar* de la clase **Poblacion_N_Reinas** y permite repoblar tras la selección de los individuos más aptos de una población, aplicando cruzamiento y mutación de forma aleatoria sobre dichos individuos.

La repoblación se realiza considerando la cantidad de individuos que le faltan a la población para volver a tener la cantidad fijada al inicio (antes de la selección). El método va alternando aleatoriamemte entre la repoblación mediante cruza o mutación, mediante el uso de la función random, tomando el valor 0 o 1 (cruza o mutación respectivamente), lo que le confiere al nuevo individuo generado para repoblar una probabilidad de 0.5 para tomar una u otra configuración.
A continucación detallamos cómo se utilizan en el modelo para la repoblación tanto la cruza como la mutación.

### 4.2.A - Cruza
Se implementó como método *cruce* de la clase **Individuo_N_reinas** y lo que hace es, para un determinado individuo, dado un segundo que recibe por parámetro y para crear un nuevo individuo, recorre la configuración del individuo primario y va decidiendo aleatoriamente si conserva la configuración del mismo o si la cambia por el del segundo individuo. 
Esta aleatoriedad está implementada mediante la función random, tomando el valor 0 o 1 (individuo primario o secundario respectivamente), lo que le confiere al nuevo individuo generado por cruza una probabilidad de 0.5 para tomar uno u otro valor en cada una de sus filas.

### 4.2.B - Mutación
Se implementó como método *mutar* de la clase **Individuo_N_reinas** y lo que hace es, para un determinado individuo, recorrer su configuración fila por fila y va decidiendo aleatoriamente si conserva la configuración que tenía o si la modifica por cualquiera de los valores posibles según la dimensión del tablero). Esta aleatoriedad está implementada mediante la función random, de manera similar a lo detallado para el método cruza.

## 5. Parametrizaciones

Los parámetros son útiles para ir realizando variaciones en la amplitud del alcance del algoritmo, teniendo en cuenta que la cantidad total de soluciones posibles se acomplejiza bastante con el creciemiento de las dimensiones del tablero.
Entre ellos se encuentran los que se detallan a continuación; los mismos poseen además configurado un valor por defecto.

|Parámetro|Detalle|Valor por defecto|
|---|---|:---:|
|`dimension_tablero`| Indica la dimensión del tablero a resolver. |5|
|`cant_individuos`| Indica la cantidad de individuos con la que deberá instanciarse la población inicial y con la cual deberá repoblarse.|70|
|`indice de seleccion`| Indica la proporción que deberá conservarse de una población tras aplicar el método de selección.|0.3|
|`max_iteraciones`| inidca la cantidad de generaciones que deberán crearse.|10000|
|`min_cant_soluciones`| Indica la cantidad mínima de soluciones que deberán encontrarse. |1|

En principio, no existen soluciones posibles para un tablero de dimensión menor a 4; a continuación mostramos estas cantidades para 4 dimensiones en adelante:

|dimension_tablero|Soluciones|
|:-:|:--:|
|4|2|
|5|10|
|6|4|
|7|40|
|8|92|
|9|352|
|10|724|
|11|2.680|
|12|14.200|
|13|73.712|
|14|365.596|
|15|2.279.184|
|16|14.772.512|
|17|95.815.104|
|18|666.090.624|
|19|4.968.057.848|
|20|39.029.188.884|






