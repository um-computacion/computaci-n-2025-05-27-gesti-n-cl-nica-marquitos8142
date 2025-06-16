from datetime import datetime
from .paciente import Paciente
from .medico import Medico


class Receta:
    def __init__(self, paciente, medico, medicamentos):
        self.__fecha = datetime.now()

        if not isinstance(paciente, Paciente):
            raise ValueError("El paciente debe ser una instancia válida de Paciente.")
        if not isinstance(medico, Medico):
            raise ValueError("El médico debe ser una instancia válida de Medico.")
        if (
            not isinstance(medicamentos, list)
            or not medicamentos
            or not all(isinstance(m, str) and m.strip() for m in medicamentos)
        ):
            raise ValueError(
                "Debe proporcionar una lista válida de medicamentos no vacíos."
            )

        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = [m.strip() for m in medicamentos]

    def obtener_paciente(self):
        return self.__paciente

    def obtener_medico(self):
        return self.__medico

    def obtener_medicamentos(self):
        return self.__medicamentos.copy()

    def obtener_fecha(self):
        return self.__fecha

    def __str__(self):
        nombre_paciente = (
            str(self.__paciente).split(":")[1].split(",")[0].strip()
            if self.__paciente
            else "Desconocido"
        )
        nombre_medico = (
            str(self.__medico).split(",")[0] if self.__medico else "Desconocido"
        )
        medicamentos_str = ", ".join(self.__medicamentos)
        fecha_str = self.__fecha.strftime("%d/%m/%Y %H:%M")

        return (
            f"Receta para {nombre_paciente} - Médico: {nombre_medico} "
            f"- Fecha: {fecha_str} - Medicamentos: {medicamentos_str}"
        )
