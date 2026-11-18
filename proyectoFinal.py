import modulosProyectoFinal as mpf #modulos

programa = "1" #arranca el programar desde menu

while programa != "0": #programa
    if programa == "1": #menu
        mpf.menu()
        programa = input().strip()
        continue #Esto es para que programa = "0" termine el proceso de una   

    if programa == "2": #agregar
        cantidad = mpf.validacionNumerosEnteros(input("\nCuantos productos va a agregar: "))
        if type(cantidad) == int:
            mpf.agregar(cantidad)
        else:
            print(cantidad)
            
        print("\nVolviendo al MENU\n")
        programa = "1"
        continue

    if programa == "3": #ver todo
        if mpf.baseVacia() == 0:
            productos = mpf.ver()
            for producto in productos:
                    print(f"\nProducto {producto[0]}\n\nNombre : {producto[1]}\nCategoria : {producto[2]}\nPrecio : ${producto[3]}\n")
        
            if productos == []:
                print("No hay productos guardados")
        else:
            print("No hay productos cargados")

            print("\nVolviendo al MENU\n")
        programa = "1"
        continue

    if programa == "4": #buscar por nombre, categoria o precio
        buscando = "" #reseteo para cada busqueda
        tipo = ""
        if mpf.baseVacia() == "Vacia": #validacion de base de datos
            print("\nNo hay productos cargados\n\nVolviendo al menu\n")
            programa = "1"
            continue
        tipo = mpf.validacionVacio(input("\nBuscar por\n\nNOMBRE/ID - 1\nCATEGORIA - 2\nPRECIO - 3\n"))

        if tipo == "1":
            buscando = mpf.validacionVacio(input("\nQue producto va a buscar: ").upper())
            if buscando != "vacio": #busqueda por nombre
                item = mpf.buscar(buscando)
                if type(item) == tuple:
                    print(f"\nProducto encontrado, esta en la posicion {item[0]}\n"
                        f"{item[1]}\n{item[2]}\n${item[3]}")
                else:
                    print("El producto no se encuentra en la lista")
            else:
                if buscando == "vacio": 
                    print("\nNo se puede buscar el vacio\n")

        if tipo == "2":
            buscando = mpf.validacionVacio(input("\nQue categoria va a buscar: ").upper())
            if buscando != "vacio": #busqueda por categoria
                resultado = mpf.buscarCategorias(buscando)
                if resultado == []:
                    print("\nNo hay productos con esa categoria\n")
                else:
                    print(f"\nSe encontraron {len(resultado)} resultados \n{resultado}\n")
            else:
                if buscando == "vacio": 
                    print("\nNo se puede buscar el vacio\n")

        if tipo == "3": #busqueda por dinero
            buscando = mpf.validacionNumeroPositivos(input("\nCantidad de dinero: "))
            diferenciador = input("\nMayor a la cantidad = 1\nMenor a la cantidad = 2\nIgual a la cantidad = 3\n").strip()
            if (diferenciador == "1" or diferenciador == "2" or diferenciador == "3") and type(buscando) == float:
                resultado = mpf.buscarPrecio(buscando, diferenciador)
                if resultado == []:
                    print("\nNo hay productos que cumplan la condicion pedida\n")
                else:
                    print(f"\nSe encontraron {len(resultado)} resultado/s \n{resultado}\n")
            else:
                if diferenciador != "1" and diferenciador != "2" and diferenciador != "3":
                    print("\nNo ingreso un diferenciador valido\n")
                if type(buscando) != float:
                    print("\nLa cantidad debe estar en numeros\n")
                    
        if tipo != "1" and tipo != "2" and tipo != "3": #validacion del tipo
            print("No ingreso uno de los numeros pedidos")

        print("\nVolviendo al MENU\n")

        programa = "1"
        continue

    if programa == "5": #actualizar datos
        if mpf.baseVacia() == "Vacia": #validacion de base de datos
            print("\nNo hay productos cargados\n\nVolviendo al menu\n")
            programa = "1"
            continue

        actualizando = mpf.buscar(input("\nQue producto quiere actualizar\n").upper())
        tipo = input("\nCAMBIAR PRECIO == 1\nCAMBIAR CATEGORIA == 2\n") 
    
        if tipo == "1" and actualizando != None: #precio
            viejo, nuevo = mpf.actualizar(actualizando, tipo)
            if viejo != "no" and nuevo != 0:
                print(f"\nAntiguo precio ${viejo[3]}\nNuevo precio ${nuevo[3]}\n")
            if viejo == "no":
                print("\nEl producto a actualizar no pertenecia a la base de datos\n")
            if nuevo == 0:
                print(f"\n{viejo}\nEl precio debe ser un real positivo\n")

        if tipo == "2" and actualizando != None: #categoria
            viejo, nuevo = mpf.actualizar(actualizando, tipo)
            if viejo != "no" and nuevo != 0:
                print(f"\nAntigua categoria {viejo[2]}\nNueva categoria {nuevo[2]}\n")
            if viejo == "no":
                print("\nEl producto a actualizar no pertenecia a la base de datos\n")
            if nuevo == 0:
                print("\nLa nueva categoria no puede estar vacia\n")

        if tipo != "1" and tipo != "2": #validacion del tipo
            print("\nNo ingreso uno de los numeros pedidos\n")

        if actualizando == None:
            print("\nSu producto no pertenece a la tabla\n")

        print("\nVolviendo al MENU\n")

        programa = "1"
        continue

    if programa == "6": #eliminar
        buscando = ""
        elemento = ""

        if mpf.baseVacia() == "Vacia": #validacion de base de datos
            print("\nNo hay productos cargados\n\nVolviendo al menu\n")
            programa = "1"
            continue

        buscando = mpf.validacionVacio(input("\nQue producto va a eliminar: ").upper())
        if buscando != "vacio": 
            elemento = mpf.eliminar(buscando)
            if elemento != []:
                print(f"Se a eliminado\n{elemento}")
            else:
                print("Su elemento no se encuentra en la lista")

        else:
            print("No se puede eleminar el vacio")

        print("\nVolviendo al MENU\n")
        programa = "1"
        continue
    
    if programa == "7": #exportar lista
        if mpf.baseVacia() == "Vacia": #validacion de base de datos
            print("\nNo hay productos cargados\n\nVolviendo al menu\n")
            programa = "1"
            continue

        mpf.exportar()
        print("\nVolviendo al MENU\n")
        programa = "1"
        continue

    else: #validacion programa
        print("\nNo ingreso una de las opciones pedidas\n\nVolviendo al MENU\n")
        programa = "1"


print("FIN")