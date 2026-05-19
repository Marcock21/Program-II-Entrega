class SistemaError(Exception):
    pass

class EstudianteNoEncontrado(SistemaError):
    pass

class CursoNoEncontrado(SistemaError):
    pass

class CursoSinCupo(SistemaError):
    pass

class InscripcionNoEncontrada(SistemaError):
    pass

class DatoInvalido(SistemaError):
    pass


class Estudiante:
    def __init__(self, nombre, apellido, matricula, carrera):
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula
        self.carrera = carrera
        self.cursos = []


class Curso:
    def __init__(self, nombre, codigo, profesor, capacidad):
        self.nombre = nombre
        self.codigo = codigo
        self.profesor = profesor
        self.capacidad = capacidad
        self.estudiantes = []

    def hay_cupo(self):
        return len(self.estudiantes) < self.capacidad


class Sistema:
    def __init__(self):
        self.estudiantes = []
        self.cursos = []

    def agregar_estudiante(self, nombre, apellido, matricula, carrera):
        if not nombre or not apellido or not matricula or not carrera:
            raise DatoInvalido("Datos incompletos")

        if not nombre.replace(" ", "").isalpha():
            raise DatoInvalido("Nombre inválido")

        self.estudiantes.append(Estudiante(nombre, apellido, matricula, carrera))

    def agregar_curso(self, nombre, codigo, profesor, capacidad):
        if not nombre or not codigo or not profesor:
            raise DatoInvalido("Datos del curso incompletos")

        if capacidad <= 0:
            raise DatoInvalido("Capacidad inválida")

        self.cursos.append(Curso(nombre, codigo, profesor, capacidad))

    def inscribir(self, matricula, codigo):
        estudiante = None
        curso = None

        for e in self.estudiantes:
            if e.matricula == matricula:
                estudiante = e

        if not estudiante:
            raise EstudianteNoEncontrado("Estudiante no encontrado")

        for c in self.cursos:
            if c.codigo == codigo:
                curso = c

        if not curso:
            raise CursoNoEncontrado("Curso no encontrado")

        if not curso.hay_cupo():
            raise CursoSinCupo("No hay cupo disponible")

        curso.estudiantes.append(estudiante)
        estudiante.cursos.append(curso)

    def baja(self, matricula, codigo):
        for e in self.estudiantes:
            if e.matricula == matricula:
                for c in e.cursos:
                    if c.codigo == codigo:
                        e.cursos.remove(c)
                        c.estudiantes.remove(e)
                        return

                raise InscripcionNoEncontrada("El estudiante no está en ese curso")

        raise EstudianteNoEncontrado("Estudiante no encontrado")

    def mostrar_cursos(self):
        for c in self.cursos:
            print(f"{c.nombre} ({c.codigo})")
            print(f"Inscritos: {len(c.estudiantes)}/{c.capacidad}")

    def mostrar_estudiantes(self):
        for e in self.estudiantes:
            print(f"{e.nombre} {e.apellido} ({e.matricula})")
            for c in e.cursos:
                print(f"  - {c.nombre}")


def main():
    sistema = Sistema()

    while True:
        print("\n0- Salir")
        print("1- Agregar Estudiante")
        print("2- Agregar Curso")
        print("3- Inscribir a Curso")
        print("4- Dar de baja")
        print("5- Ver Cursos")
        print("6- Ver Estudiantes")

        op = input("Opción: ")

        try:
            if op == "0":
                break

            elif op == "1":
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                matricula = input("Matrícula: ")
                carrera = input("Carrera: ")
                sistema.agregar_estudiante(nombre, apellido, matricula, carrera)
                print("Estudiante agregado")

            elif op == "2":
                nombre = input("Curso: ")
                codigo = input("Código: ")
                profesor = input("Profesor: ")
                
                try:
                    capacidad = int(input("Capacidad: "))
                except ValueError:
                    raise DatoInvalido("La capacidad debe ser un número")

                sistema.agregar_curso(nombre, codigo, profesor, capacidad)
                print("Curso agregado")

            elif op == "3":
                matricula = input("Matrícula: ")
                codigo = input("Código curso: ")
                sistema.inscribir(matricula, codigo)
                print("Inscripción exitosa")

            elif op == "4":
                matricula = input("Matrícula: ")
                codigo = input("Código curso: ")
                sistema.baja(matricula, codigo)
                print("Baja realizada")

            elif op == "5":
                sistema.mostrar_cursos()

            elif op == "6":
                sistema.mostrar_estudiantes()

            else:
                print("Opción inválida")

        except SistemaError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()