# PYTHON 3 🐍

## Guía básica del lenguaje

----

### [Conceptos generales](#generales)

- [Comentarios](#comentarios)
- [Importar código](#import)
- [Variables](#variables)
- [Tipos de Variables](#tipos_variables)
- [Interpolación y suma de cadenas](#interpolacion)
- [Fechas](#fechas)

### [Estructuras de control](#estructuras)

- [If elif y else](#if)
- [ciclos](#ciclos)

### [Funciones y clases](#funciones_clases)
- [funciones](#funciones)
- [Clases](#clases)
- [Encapsulamiento](#encapsulamiento)
- [Herencia de clases](#herencia)

### [Conceptos avanzados](#avanzados)
- [Shorthands](#shorthands)
- [Validar vacíos](#validar_vacios)

---
---

## Conceptos generales <a id="generales"></a>
---

    ### Comentarios <a id="comentarios"></a>
    #Comentario en simple linea
    """
        comentario multilinea
    """
### Importar código <a id="import"></a>

   

     # importar un módulo
    import math
    numero = 49
    # ya se puede usar el módulo
    print(f"la raíz cuadrada de {numero} es {math.sqrt(numero)}")
    
    # Importar sólo un miembro de un módulo
    from math import sqrt
    
    print(f"la raíz cuadrada de {numero} es {sqrt(numero)}")
    
    
    # Importar sólo un miembro de un módulo con un alias
    from math import sqrt as raiz
    
    print(f"la raíz cuadrada de {numero} es {raiz(numero)}")
### Variables <a id="variables"></a>

    #Declaración de variable
    cadena = "cadena"
    numero = 28
    decimal = 3.14159265359
    
    print(cadena, numero, decimal)

### Tipos de variables <a id="tipos_variables"></a>

    numerico = 1
    
    decimal = 1.5
    
    cadena = "texto"
    
    booleano = True
    
    lista = [1, 2, "3", 4.5, 5]
    
    conjunto = (1, 8, 9, 7)
    
    diccionario = {"a":9}

### Interpolación y suma de cadenas <a id="interpolacion"></a>

    # Concatenación
    
    a = "Primera parte"
    b = "de"
    c = "un mensaje de prueba"
    print("Concatenación: "+ a + " " + b + " " + c)
    
    # Interpolación de cadenas
    
    print(f"Interpolación: {a} {b} {c}")
### Fechas <a id="fechas"></a>

    from datetime import datetime
    
    # Obtener fecha actual
    print(f"hoy: {datetime.now()}")
    
    # crear una fecha dia, mes, año, hora, minutos, segudos, microsegundos
    print(f"nueva fecha: {datetime(2020, 12, 31, 23, 59, 59, 999999)}")
## Estructuras de control <a id="estructuras"></a>
---
### IF, ELIF y ELSE <a id="if"></a>

    a = 8
    b = 3
    c = 5
    
    # IF
    if a > b and a > c:
        print('a es mayor')
    
    #IF ELSE
    if a > b and c > a:
        print("no entrara")
    else:
        print("entro")
        
    # IF anidado
    if a > b:
        print("a es mayor")
    elif a < b:
        print("a es menor")
    else:
        print("a y b son iguales")
    
    # Asignacion con if else
    
    variable = "8 es mayor" if a > b and a > c else "no entrara" 
    print(variable)
        
### CICLOS <a id="ciclos"></a>

    contador = 0
    max = 5
    while contador < max: 
        contador= contador + 1
        print(contador)
    else:
        print("no se cumplió")
        
    for contador in range(0, max):
        print(contador)
    else:
        print("no se cumplió")

## Funciones y clases <a id="funciones_clases"></a>
---
### Funciones <a id="funciones"></a>

    #declaracion de un método o funcion
    
    def f_vacia():
        print("invocado")
        
    def f_parametro(a):
        return 8 + a
    
    def f_opcional(a, b=9):
        return a + b
    
    def f_variante(*var):
        print(var)
        
    def f_variante_nombre(**var):
        print(var)
    
    # Invocacion funcion sin parametros
    f_vacia()
    
    # Invocacion funcion con 1 parametro
    print(f_parametro(4))
    
    # Invocacion funcion con 1 parametro opcional
    print(f_opcional(4))
    # Invocacion funcion con 1 parametro opcional con nombre
    print(f_opcional(4, 6))
    
    print(f_opcional(4, b=6))
    
    # Invocación funcion con parametros variables
    print(f_variante(1,2,3,4,5))
    
    # Invocación función con parametros variables con nombre
    f_variante_nombre()
    f_variante_nombre(uno=1, dos=2)

### Clases

    class Clase:
        # Atributo público
        x = "hola"
        __saludo = False
        
        def __init__(self, nombre="amigo", despedida=True):
            # actualización variable pública
            if self.__saludo:
                self.x= "adios"
            
            # declaración de variable privada
            self.__y= nombre
        
        # Método público
        def saluda(self):
            self.__silencio()
            print(f"{self.x} {self.__y}\n")
            
        def __silencio(self):
            print("shhh!")
        
    instancia = Clase()
    instancia.saluda()# adios amigo
    
    pepe = Clase("josé")
    # Actualiza variable pública
    pepe.x = "Qué tal"
    
    # Invocación de función pública
    pepe.saluda()
    
    pepe.__y = "Variable privada" #error
    pepe.saluda()# Qué tal josé

### Encapsulamiento <a id="encapsulamiento"></a>

    # TBA
### Herencia

    # Declaración
    class Animal:
        nombre = 'Anonimo'
        
        def __init__(self):
            print(f"soy {self.nombre} y me acaban de crear")
        
        def come(self):
            print(f"soy {self.nombre} y estoy comiendo")
            
            
    class Vaca(Animal):     
        
        def __init__(self, nuevo_nombre):
            self.nombre = nuevo_nombre
        
        def muge(self):
            print(f"{self.nombre} mu!")
            
        def come(self):
            print(f"{self.nombre} voltee")
            super(Vaca, self).come()
            
    # Ejecución    
    mi_vaca = Vaca('lola')
    mi_vaca.come()
    mi_vaca.muge()
    print()
    otra = Vaca('josefina')
    otra.come()
    otra.muge()
    print()
    otro_animal = Animal()
    otro_animal.come()

## Conceptos avanzados <a id="avanzados"></a>
---
## Notación de slices

    coleccion = list(range(10))
    print(f'lista {coleccion}')
    
    print(f'primer elemento: {coleccion[0]}')
    
    print(f'último elemento: {coleccion[-1]}')
    
    print(f'Desde el 5to elemento: {coleccion[5:]}')
    
    print(f'Hasta el 5to elemento: {coleccion[:5]}')
    
    print(f'Del 2do al 5to elemento: {coleccion[2:5]}')
    
    print(f'Números pares: {coleccion[::2]}')
    
    print(f'Números pares de media lista: {coleccion[:5:2]}')
    
    print(f'Números impares: {coleccion[1::2]}')

### Shorthands y list, map comprehension

    # SHORTHANDS
    """
    Shorthand es la forma reducida de una instrucción
    """
    a = 4
    b = 6
    c = 8
    # IF ElSE
    print(f"{a} es mayor que {b}" if a > b else f"{a} no es mayor que {b}")
    
    # IF ElSE Compuesto
    print(f"{a} es mayor que {b}" if a > b else f"{a} es mayor que {c}" if a > c else f"{a} es menor que {b} y {c}")
    
    # List comprehension
    # FOR
    numeros = [i for i in range(1, 11)]
    print(f"numeros del 0 al 10 {numeros}")
    
    # list comprehension con FOR filtrado
    
    pares = [i for i in range(1, 11) if i % 2 == 0]
    print(f"pares del 0 al 10 {pares}")
    
    # list comprehension con FOR con if
    
    paresTexto = [f"{i} par" if i % 2 == 0 else f"{i} non" for i in range(1, 11) if i > 5]
    print(f"paresTexto: {paresTexto}")
    
    # Funciones
    
    esPar = lambda n: True if n % 2 == 0 else False
    
    print(f"¿5 es par?: {esPar(5)}")
    
    # dictionary comprehension
    numero_y_su_cuadrado = {n:n**2 for n in range(1,11)}
    print(f'cada cuadrado del 1 al 10:\n {numero_y_su_cuadrado}')

    diccionario = {"uno" : 1, "dos":2}
    if 'tres' in diccionario:
        print(diccionario['tres'])
    else:
        print('Tres no existe')

### Validar vacíos <a id="validar_vacios"></a>

    import datetime
    hoy = datetime.datetime.now()
    # validar vacíos
    v = "Vacío"
    tv = 'Tiene Valor'
    
    valores = [3, "cadena", True, ["lista", "con", "valores"], {"diccionario":"con valor"}, hoy]
    
    for v in valores:
        if v: # validar que sea valido solo con if
            print(f"{v} tiene un valor válido")
            
    print()
    
    valores = [0, "", False, [], {}, None]
    
    for v in valores:
        if not v: # validar que no sea valido solo negandolo
            print(f"{v} tiene un valor NO válido")

