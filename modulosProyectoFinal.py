import sqlite3

def menu():
    print("\nMENU\n\nFIN = 0\nMENU = 1\nAGREGAR = 2\nVER = 3\nBUSCAR = 4\nACTUALIZAR = 5\nELIMINAR = 6\nEXPORTAR = 7\n")

def validacionVacio(algo : str):
    """
    toma cualquier objeto y chequea que sea distinto a vacio
    si no esta vacio devuelve el objeto
    caso contrario devuelve vacio
    """
    if algo.strip() == "":
        return("vacio")
    else:
        return(algo.strip())

def validacionNumerosEnteros(algo : any):
    """
    chequea si un numero es positivo, mayor a 0 y sin coma
    si cumple devuelve el numero como int
    caso contrario dice que condicion no cumple
    """
    algo = validacionVacio(algo) 
    if algo == "vacio": #añadimos este paso para evitar el try si no es necesario
        return("vacio")
    try:
        numero = int(algo)
        if numero > 0:
            if numero % 1 == 0:
                return(numero)
            else:
                return("Su numero no era natural (numero positivio sin coma)")
        else:
            return("Su numero no era posivo")    
    except ValueError:
        return("El valor ingresado no era un numero")
    
    except:
        return("Error desconocido, volver a intentar")

def validacionNumeroPositivos(algo : any):
    """
    toma un dato, chequea que sea un numero mayor o igual a 0
    si cumple devuelve el numero como float
    caso contrario dice que condicion no cumple
    """ 
    algo = validacionVacio(algo) 
    if algo == "vacio": #añadimos este paso para evitar el try si no es necesario
        return("vacio")
    try:
        numero = float(algo)
        if numero >= 0:
            return(numero)
        
        else:
            return("El numero ingresado era negativo")
        
    except ValueError:
        return("El valor ingresado no era un numero")
    
    except:
        return("Error desconocido")

def baseVacia():
    """
    entra a la base de datos
    vacia -> "Vacia" (str)
    algo -> 0 (int)
    """
    conexion = sqlite3.connect("productos.db")
    cursor =  conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "nombre TEXT NOT NULL, categoria TEXT NOT NULL, precio REAL NOT NULL)")
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.commit()
    conexion.close()    

    if productos == []: 
        return("Vacia")
    else:
        return(0) 

def agregar(numero : int):
    """
    Dada una cantidad 
    el usuario agrega tantos objetos a la base de datos como la cantidad
    valida que el dato no este vacio 
    que el precio se un racional positivo
    y que el nombre del producto no se haya usado ya
    si no se cumple una condicion repite el bucle hasta que se cumpla
    """
    conexion = sqlite3.connect("productos.db")
    cursor =  conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "nombre TEXT NOT NULL, categoria TEXT NOT NULL, precio REAL NOT NULL)")
    conexion.commit()
    conexion.close()
    e = 0
    while e < numero:
        problema = False #reseteamos en cada iteracion
        #pedimos datos
        nombre = input(f"\nNombre del producto {e+1}: ").upper()
        categoria = input(f"\nCategoria del producto {e+1}: ").upper()
        precio = input(f"\nPrecio del producto {e+1}: ").upper() 
        #validacion de los datos
        if validacionVacio(nombre) == "vacio":
            print("\nEl nombre no puede estar vacio")
            problema = True
        if validacionVacio(categoria) == "vacio":
            print("\nLa categoria no puede estar vacia")
            problema = True
        if validacionVacio(precio) == "vacio":
            print("\nEl precio no puede estar vacio")
            problema = True
        if type(validacionNumeroPositivos(precio)) != float:
            print("\nEl precio debe estar en numeros positivos")
            problema = True
        #chequeamos que el elemento no pertenezca ya a la lista (se que no se pedia pero lo preferi asi)
        conexion = sqlite3.connect("productos.db") 
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM productos")
        nombres = cursor.fetchall() 

        for elementos in nombres:
            if elementos[0] == nombre:
                print("\nEl nombre del producto ya se encuentra en la lista")
                problema = True

        conexion.commit()
        conexion.close()
        #si no hay problemas sumamos como tupla a la base de datos
        if problema == False:
            #ista.append({"nombre":nombre, "categoria":categoria,"precio":precio})
            conexion = sqlite3.connect("productos.db")
            cursor =  conexion.cursor()

            cursor.execute("INSERT INTO productos (nombre, categoria, precio) VALUES (?,?,?)", (nombre, categoria, precio))

            conexion.commit()
            conexion.close()
            e += 1

def ver():
    """
    devuelve lista con todos los elementos
    """
    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return(productos)

def buscar(dato):
    """
    toma un dato
    revisa en la base de datos si encuentra devuelve todos los datos del producto
    caso contrario printea que no encontro el producto
    """     
    encontrado = False
    conexion = sqlite3.connect("productos.db")
    cursor =  conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conexion.commit()
    conexion.close()
    
    for producto in productos:
        nombre = producto[1]
        if nombre == dato: #busqueda por nombre
            encontrado = True

        if encontrado == True:
            return(producto)
        
    if encontrado == False:
        for producto in productos: #busqueda por id
            ids = str(producto[0])
            if ids == dato:
                encontrado = True
            if encontrado == True:
                return(producto)
    else:
        return("no")
    
def buscarCategorias(dato):
    """
    dado un dato devuelve todas las coincidencias en categoria como lista
    caso contrario devuelve lista vacia
    """
    encontrado = False
    ids = [] 
    coincidentes = []

    conexion = sqlite3.connect("productos.db")
    cursor =  conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    for producto in productos:
        categoria = producto[2]
        if dato == categoria:
            encontrado = True
            ids.append(producto[0])

    if encontrado == True:
    
        for identificador in ids:
            cursor.execute("SELECT * FROM productos WHERE id == ?",(identificador,))
            coincidencia = cursor.fetchone()
            coincidentes.append(coincidencia)

    conexion.commit()
    conexion.close()     
    return(coincidentes)

def buscarPrecio(dato : float, tipo):
    """
    dado un numero y un tipo de busqueda
    busca coincidencias del tipo mayor menor o igual en la categoria precio
    si no encuentra devuelve una lista vacia
    si encuentra una lista con lo encontrado
    """
    print(dato, "=", type(dato))
    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()
    if tipo == "1":
        cursor.execute("SELECT * FROM productos WHERE precio > ?", (dato,))
        resultados = cursor.fetchall()
    if tipo == "2":
        cursor.execute("SELECT * FROM productos WHERE precio < ?", (dato,))
        resultados = cursor.fetchall()
    if tipo == "3":
        cursor.execute("SELECT * FROM productos WHERE precio = ?", (dato,))
        resultados = cursor.fetchall()   
     
    conexion.commit()
    conexion.close()
    return(resultados)

def eliminar(dato):
    """
    dado un item chequea en la lista-diccionario si esta
    si lo encuentra lo elimina y devuelve
    caso contrario devuelve lista vacia
    """
    producto = buscar(dato)
    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()
    if producto != []:
        posicion = producto[0]
        cursor.execute("DELETE FROM productos WHERE id = ?", (posicion,))

    conexion.commit()
    conexion.close()
    return(producto)

def exportar():
    archivo = open("productos.txt", "w+", encoding = "utf-8")
    productos = ver()
    for producto in productos:
        identificador = producto[0]
        nombre = producto[1]
        categoria = producto[2]
        precio = producto[3]
        archivo.write(f"\nproducto n°{identificador}\n{nombre}\n{categoria}\n{precio}\n")

    leido = archivo.read()
    print(leido)
    archivo.close()

    archivo = open("productos.txt", "r", encoding = "utf-8")
    print("\nContenido exportado\n")
    leido = archivo.read()
    print(leido)
    archivo.close()

def actualizar (dato, tipo):
    """
    toma un dato busca que pertenezca a la table
    si lo hace pide dependiendo el tipo nuevo precio o categoria
    caso contrario devuelve dos lista vacia o el error y 0
    """

    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()

    if tipo == "1": # precio
        new = validacionNumeroPositivos(input("\nIngrese nuevo precio\n"))
        if type(new) == float:
            cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (new, dato[0]))
        else:
            conexion.close()
            return(new, 0)
    if tipo == "2": # categoria
        new = validacionVacio(input("\nIngrese nueva categoria:\n").upper())
        if new != "vacio":
            cursor.execute("UPDATE productos SET categoria = ? WHERE id = ?", (new, dato[0]))
        else:
            conexion.close()
            return(new, 0)            

    conexion.commit()
    nuevo = buscar(dato[1]) 
    conexion.commit()
    conexion.close()
    return(dato, nuevo)

print("Todo Ok") #si no exploto nada corre en la terminal