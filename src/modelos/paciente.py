from datetime import datetime


class Paciente:
    def __init__(self, nombre, dni, fecha_nacimiento):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if not dni or not dni.isdigit():
            raise ValueError("El DNI debe ser numérico y no estar vacío.")
        if not fecha_nacimiento or not fecha_nacimiento.strip():
            raise ValueError("La fecha de nacimiento no puede estar vacía.")
        try:
            self.__fecha_nacimiento = datetime.strptime(
                fecha_nacimiento, "%d/%m/%Y"
            ).date()
        except ValueError:
            raise ValueError(
                "La fecha de nacimiento tiene un formato inválido o no existe."
            )

        self.__nombre = nombre.strip()
        self.__dni = dni.strip()

    def obtener_dni(self):
        return self.__dni

    def obtener_nombre(self):
        return self.__nombre

    def __str__(self):
        fecha = self.__fecha_nacimiento.strftime("%d/%m/%Y")
        return f"Paciente: {self.__nombre}, DNI: {self.__dni}, Fecha de Nacimiento: {fecha}"
