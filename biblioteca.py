class BibliotecaError(Exception):
    pass

class MiembroNoEncontrado(BibliotecaError):
    pass

class LibroNoEncontrado(BibliotecaError):
    pass

class LibroNoDisponible(BibliotecaError):
    pass

class PrestamoNoEncontrado(BibliotecaError):
    pass

class DatoInvalido(BibliotecaError):
    pass


class Biblioteca:
    def __init__(self):
        self.miembros = []
        self.libros = []

    def agregarMiembro(self, nombre, dni):
        if not nombre or not dni:
            raise DatoInvalido("Nombre o DNI vacío")

        if not nombre.replace(" ", "").isalpha():
            raise DatoInvalido("El nombre no puede tener números")

        for m in self.miembros:
            if m.dni == dni:
                raise DatoInvalido("Ya existe un miembro con ese DNI")

        miembro = Miembro(nombre, dni)
        self.miembros.append(miembro)

    def agregarLibro(self, titulo, autor, isbn):
        if not titulo or not autor or not isbn:
            raise DatoInvalido("Datos del libro incompletos")

        for l in self.libros:
            if l.isbn == isbn:
                raise DatoInvalido("Ya existe un libro con ese ISBN")

        libro = Libro(titulo, autor, isbn)
        self.libros.append(libro)

    def prestarLibro(self, dni, isbn):
        miembro = None
        libro = None

        for m in self.miembros:
            if m.dni == dni:
                miembro = m

        if not miembro:
            raise MiembroNoEncontrado("Miembro no encontrado")

        for l in self.libros:
            if l.isbn == isbn:
                libro = l

        if not libro:
            raise LibroNoEncontrado("Libro no encontrado")

        if not libro.disponible:
            raise LibroNoDisponible("El libro no está disponible")

        libro.disponible = False
        libro.prestado_a = miembro
        miembro.libros_prestados.append(libro)

    def devolverLibro(self, dni, isbn):
        for m in self.miembros:
            if m.dni == dni:
                for l in m.libros_prestados:
                    if l.isbn == isbn:
                        l.disponible = True
                        l.prestado_a = None
                        m.libros_prestados.remove(l)
                        return

                raise PrestamoNoEncontrado("El miembro no tiene ese libro")

        raise MiembroNoEncontrado("Miembro no encontrado")

    def mostrarLibros(self):
        for l in self.libros:
            if l.disponible:
                print(f"{l.titulo} - Disponible")
            else:
                print(f"{l.titulo} - Prestado a {l.prestado_a.nombre}")

    def mostrarMiembros(self):
        for m in self.miembros:
            print(f"{m.nombre} ({m.dni})")
            for l in m.libros_prestados:
                print(f"  - {l.titulo}")


class Libro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True
        self.prestado_a = None


class Miembro:
    def __init__(self, nombre, dni):
        self.nombre = nombre
        self.dni = dni
        self.libros_prestados = []


def main():
    biblioteca = Biblioteca()

    while True:
        print("\n0- Salir")
        print("1- Agregar Miembro")
        print("2- Agregar Libro")
        print("3- Prestar Libro")
        print("4- Devolver Libro")
        print("5- Ver Libros")
        print("6- Ver Miembros")

        opcion = input("Ingrese una opcion: ")

        try:
            if opcion == "0":
                break

            elif opcion == "1":
                nombre = input("Nombre: ")
                dni = input("DNI: ")
                biblioteca.agregarMiembro(nombre, dni)
                print("Miembro agregado correctamente")

            elif opcion == "2":
                titulo = input("Título: ")
                autor = input("Autor: ")
                isbn = input("ISBN: ")
                biblioteca.agregarLibro(titulo, autor, isbn)
                print("Libro agregado correctamente")

            elif opcion == "3":
                dni = input("DNI: ")
                isbn = input("ISBN: ")
                biblioteca.prestarLibro(dni, isbn)
                print("Libro prestado correctamente")

            elif opcion == "4":
                dni = input("DNI: ")
                isbn = input("ISBN: ")
                biblioteca.devolverLibro(dni, isbn)
                print("Libro devuelto correctamente")

            elif opcion == "5":
                biblioteca.mostrarLibros()

            elif opcion == "6":
                biblioteca.mostrarMiembros()

            else:
                print("Opción inválida")

        except BibliotecaError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()