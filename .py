from datetime import date, timedelta

class Persona:
    def _init_(self, nombre):
        self.nombre = nombre

    def mostrar_nombre(self):
        print("Nombre:", self.nombre)

class Activo:
    def _init_(self, activo):
        self.activo = activo

    def verificar_activo(self):
        if not self.activo:
            raise ValueError(f"{self.nombre} no esta activo")

class Identificable:
    @staticmethod
    def es_codigo_valido(codigo):
        return codigo.isdigit() and len(codigo) == 10

class Bibliotecario(Persona, Activo):
    def _init_(self, nombre_empleado, num_empleado,
                 empleado_activo):
        Persona._init_(self, nombre_empleado)
        Activo._init_(self, empleado_activo)
        self.num_empl = num_empleado

    def prestar_libro(self, libro, usuario):
        self.verificar_activo()
        libro.prestar()
        usuario.recibir_prestamo(libro)
        print(f"{self.nombre} ha entregado {libro.titulo} "
              f"a {usuario.nombre} en prestamo.")

    def reintegro_libro(self, libro, usuario):
        libro.devolver()
        usuario.devolver_libro(libro)
        print(f"{self.nombre} ha recibido el libro "
              f"{libro.titulo} de {usuario.nombre}.")

class Usuario(Persona, Identificable, Activo):
    def _init_(self, nombre, pertenece_universidad,
                 es_activo, carnet,
                 tiene_devoluciones_pendientes=False,
                 tipo_usuario="estudiante"):

        Persona._init_(self, nombre)
        Activo._init_(self, es_activo)

        self.pertenece_universidad = pertenece_universidad
        self.carnet = carnet
        self.tiene_devoluciones_pendientes = (
            tiene_devoluciones_pendientes
        )
        self.tipo_usuario = tipo_usuario

    def recibir_prestamo(self, libro):
        print(f"{self.nombre} ha recibido el libro "
              f"{libro.titulo} en prestamo.")

    def devolver_libro(self, libro):
        print(f"{self.nombre} ha devuelto el libro "
              f"{libro.titulo}.")

    def pagar_multa(self, monto):
        print(f"{self.nombre} ha pagado una multa de {monto}.")

    def entregar_carnet(self):
        print("Carnet entregado.")

class Libro:
    def _init_(self, titulo, autor, isbn, ejemplares_totales,
                 estado="Bueno", **detalles):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.estado = estado
        self.ejemplares_totales = ejemplares_totales
        self._ejemplares_disponibles = ejemplares_totales
        self.detalles = detalles

    @property
    def disponibles(self):
        return self._ejemplares_disponibles

    @disponibles.setter
    def disponibles(self, valor):
        if valor < 0 or valor > self.ejemplares_totales:
            raise ValueError(
                f"Disponibles debe estar entre 0 y "
                f"{self.ejemplares_totales}"
            )
        self._ejemplares_disponibles = valor

    def esta_disponible(self):
        return self.disponibles > 0

    def prestar(self):
        if not self.esta_disponible():
            raise ValueError(
                f"No hay ejemplares disponibles de '{self.titulo}'"
            )
        self.disponibles -= 1
        return True

    def devolver(self):
        if self.disponibles >= self.ejemplares_totales:
            raise ValueError("Todos los ejemplares estan disponibles.")
        self.disponibles += 1

    def reservar(self):
        print("Libro reservado.")

    def buscar(self):
        print("Buscando libro...")

    def reportar_perdido(self):
        self.estado = "Perdido"
        self.disponibles = 0

    def renovar(self):
        print("Prestamo renovado.")


class Prestamo:
    def _init_(self, libro, estudiante, bibliotecario,
                 fecha_prestamo, fecha_devolucion):
        self.libro = libro
        self.estudiante = estudiante
        self.bibliotecario = bibliotecario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado = "Activo"

    @classmethod
    def registrar_hoy(cls, libro, estudiante, bibliotecario,
                      dias_prestamo=10):
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=dias_prestamo)

        return cls(
            libro, estudiante, bibliotecario, hoy, fecha_limite
        )

class Comprobanteprestamo:
    _slots_ = (
        "_libro_titulo",
        "_usuario_nombre",
        "_fecha_prestamo",
        "_fecha_devolucion"
    )

    def _init_(self, prestamo):
        self._libro_titulo = prestamo.libro.titulo
        self._usuario_nombre = prestamo.estudiante.nombre
        self._fecha_prestamo = prestamo.fecha_prestamo
        self._fecha_devolucion = prestamo.fecha_devolucion

    @property
    def libro_titulo(self):
        return self._libro_titulo

    @property
    def usuario_nombre(self):
        return self._usuario_nombre

    @property
    def fecha_prestamo(self):
        return self._fecha_prestamo

    @property
    def fecha_devolucion(self):
        return self._fecha_devolucion

if _name_ == "_main_":

    libro_1 = Libro(
        "Fluent Python", "Luciano Ramalho",
        "978-1492056355", 3
    )

    libro_2 = Libro(
        "Cien años de soledad", "Gabriel García Márquez",
        "978-0307474728", 5
    )

    libro_3 = Libro(
        "El Principito", "Antoine de Saint-Exupéry",
        "978-0156012195", 2
    )

    libro_4 = Libro(
        "Clean Code", "Robert C. Martin",
        "978-0132350884", 4,
        editorial="Prentice Hall", anio=2008
    )

    libro_5 = Libro(
        "Dune", "Frank Herbert",
        "978-0441172719", 1
    )

    for libro in (
        libro_1, libro_2, libro_3, libro_4, libro_5
    ):
        print(libro.titulo, "-> disponibles:", libro.disponibles)

    u1 = Usuario("Camila Ruiz", True, True, "1093812345")
    bib = Bibliotecario("Ana López", 42, True)

    bib.prestar_libro(libro_1, u1)
    print("Disponibles libro_1:", libro_1.disponibles)

    prestamo_1 = Prestamo.registrar_hoy(libro_1, u1, bib)
    comprobante = Comprobanteprestamo(prestamo_1)

    print(
        comprobante.libro_titulo, "|",
        comprobante.usuario_nombre, "|",
        comprobante.fecha_devolucion
    )

    print(Usuario.es_codigo_valido("1093812345"))  # True
    print(Usuario.es_codigo_valido("abc"))         # False

    u1.mostrar_nombre()
    bib.mostrar_nombre()

    bib.reintegro_libro(libro_1, u1)
    print("Disponibles libro_1:", libro_1.disponibles)