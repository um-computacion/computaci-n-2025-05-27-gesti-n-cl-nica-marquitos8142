from datetime import datetime
from .paciente import Paciente
from .medico import Medico


class Turno:
    def __init__(self, paciente, medico, fecha_hora, especialidad):
        if not isinstance(paciente, Paciente):
            raise ValueError("El paciente no es válido")
        if not isinstance(medico, Medico):
            raise ValueError("El médico no es válido")
        if not isinstance(fecha_hora, datetime):
            raise ValueError("La fecha y hora no es válida")
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValueError("La especialidad no puede estar vacía")

        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad.strip()

    def obtener_medico(self):
        return self.__medico

    def obtener_fecha_hora(self):
        return self.__fecha_hora

    def __str__(self):
        fecha_str = self.__fecha_hora.strftime("%d/%m/%Y %H:%M")
        nombre_paciente = self.__paciente.obtener_nombre()

        # Si Medico no tiene este método, agregarlo. Sino, usar str(self.__medico)
        try:
            nombre_medico = self.__medico.obtener_nombre_completo()
        except AttributeError:
            # Fallback: intentamos sacar nombre del __str__ del médico
            nombre_medico = str(self.__medico).split(",")[0].replace("Dr. ", "").strip()

        return (
            f"Turno: {self.__paciente.obtener_dni()} ({nombre_paciente}) "
            f"con Dr. {nombre_medico} "
            f"- Especialidad: {self.__especialidad} "
            f"- Fecha: {fecha_str}"
        )
