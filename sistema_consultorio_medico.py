"""Taller 8 - Persistencia de datos con SQLite.

Proyecto: Consultorio medico
Clase seleccionada: Paciente

El programa crea la base de datos consultorio_medico.db en la misma carpeta
del archivo Python y prueba las cuatro operaciones CRUD.
"""

import sqlite3
from pathlib import Path


RUTA_BD = Path(__file__).resolve().parent / "consultorio_medico.db"


class Paciente:
    def __init__(self, nombre, identificacion, fecha_nacimiento, telefono, correo):
        self.nombre = nombre
        self.identificacion = identificacion
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.correo = correo

    @staticmethod
    def crear_tabla():
        """Crea la tabla si todavia no existe."""
        conexion = sqlite3.connect(RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pacientes (
                identificacion TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                fecha_nacimiento TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correo TEXT NOT NULL
            )
            """
        )
        conexion.commit()
        conexion.close()

    def guardar(self):
        """Guarda un paciente nuevo en la base de datos."""
        conexion = sqlite3.connect(RUTA_BD)
        cursor = conexion.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO pacientes
                    (identificacion, nombre, fecha_nacimiento, telefono, correo)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.identificacion,
                    self.nombre,
                    self.fecha_nacimiento,
                    self.telefono,
                    self.correo,
                ),
            )
            conexion.commit()
            print(f"Paciente {self.nombre} guardado correctamente.")
            return True
        except sqlite3.IntegrityError:
            print(
                f"No se guardo a {self.nombre}: "
                "la identificacion ya esta registrada."
            )
            return False
        finally:
            conexion.close()

    @staticmethod
    def listar_todos():
        """Consulta y devuelve todos los pacientes registrados."""
        conexion = sqlite3.connect(RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT nombre, identificacion, fecha_nacimiento, telefono, correo
            FROM pacientes
            ORDER BY nombre
            """
        )
        registros = cursor.fetchall()
        conexion.close()
        return registros

    def actualizar(self, nuevo_telefono, nuevo_correo):
        """Actualiza el telefono y el correo usando la identificacion."""
        conexion = sqlite3.connect(RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE pacientes
            SET telefono = ?, correo = ?
            WHERE identificacion = ?
            """,
            (nuevo_telefono, nuevo_correo, self.identificacion),
        )
        filas_modificadas = cursor.rowcount
        conexion.commit()
        conexion.close()

        if filas_modificadas > 0:
            self.telefono = nuevo_telefono
            self.correo = nuevo_correo
            print(f"Paciente {self.nombre} actualizado correctamente.")
            return True

        print(f"No se encontro al paciente {self.nombre} para actualizar.")
        return False

    def eliminar(self):
        """Elimina el registro usando la identificacion como condicion."""
        conexion = sqlite3.connect(RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM pacientes WHERE identificacion = ?",
            (self.identificacion,),
        )
        filas_eliminadas = cursor.rowcount
        conexion.commit()
        conexion.close()

        if filas_eliminadas > 0:
            print(f"Paciente {self.nombre} eliminado correctamente.")
            return True

        print(f"No se encontro al paciente {self.nombre} para eliminar.")
        return False

    def __str__(self):
        return (
            f"Nombre: {self.nombre} | "
            f"Identificacion: {self.identificacion} | "
            f"Fecha de nacimiento: {self.fecha_nacimiento} | "
            f"Telefono: {self.telefono} | "
            f"Correo: {self.correo}"
        )


def mostrar_registros(titulo):
    print(f"\n{titulo}")
    print("-" * 100)
    registros = Paciente.listar_todos()

    if not registros:
        print("No hay pacientes registrados.")
        return

    for nombre, identificacion, fecha, telefono, correo in registros:
        print(
            f"Nombre: {nombre} | Identificacion: {identificacion} | "
            f"Fecha de nacimiento: {fecha} | Telefono: {telefono} | "
            f"Correo: {correo}"
        )


if __name__ == "__main__":
    Paciente.crear_tabla()

    paciente1 = Paciente(
        "Ana Gomez",
        "1023456789",
        "15/06/1990",
        "3004567890",
        "ana.gomez@correo.com",
    )

    paciente2 = Paciente(
        "Carlos Martinez",
        "1034567890",
        "22/09/1985",
        "3001234567",
        "carlos.martinez@correo.com",
    )

    print("TALLER 8 - PERSISTENCIA CON SQLITE")
    print("Base de datos:", RUTA_BD)

    # CREATE
    paciente1.guardar()
    paciente2.guardar()

    # READ
    mostrar_registros("PACIENTES DESPUES DE GUARDAR")

    # UPDATE
    paciente2.actualizar(
        "3112223344",
        "carlos.actualizado@correo.com",
    )
    mostrar_registros("PACIENTES DESPUES DE ACTUALIZAR")

    # DELETE
    paciente1.eliminar()
    mostrar_registros("PACIENTES DESPUES DE ELIMINAR")

    print("\nLa informacion permanece guardada en consultorio_medico.db.")