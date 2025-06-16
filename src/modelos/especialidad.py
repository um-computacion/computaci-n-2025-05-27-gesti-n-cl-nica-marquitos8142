class Especialidad:
    def __init__(self, tipo, dias):
        self.__dias_validos = {
            "lunes",
            "martes",
            "miercoles",
            "miércoles",
            "jueves",
            "viernes",
            "sabado",
            "sábado",
            "domingo",
        }

        if not tipo or not tipo.strip():
            raise ValueError("La especialidad no puede estar vacía")

        if dias is None or not isinstance(dias, list) or not dias:
            raise ValueError("Debes proporcionar una lista de días válida")

        self.__tipo = tipo.strip()
        self.__dias = []

        dias_normalizados = []
        for dia in dias:
            if not isinstance(dia, str):
                continue
            dia_normalizado = dia.strip().lower()
            if dia_normalizado in self.__dias_validos:
                if not self._dia_ya_agregado(dia_normalizado, dias_normalizados):
                    dias_normalizados.append(dia_normalizado)
        self.__dias = dias_normalizados

        if not self.__dias:
            raise ValueError("La especialidad debe tener al menos un día válido")

    def _dia_ya_agregado(self, dia_nuevo, dias_existentes):
        equivalencias = {
            "miercoles": "miércoles",
            "miércoles": "miercoles",
            "sabado": "sábado",
            "sábado": "sabado",
        }

        for dia_existente in dias_existentes:
            if (
                dia_nuevo == dia_existente
                or equivalencias.get(dia_nuevo) == dia_existente
                or equivalencias.get(dia_existente) == dia_nuevo
            ):
                return True
        return False

    def verificar_dia(self, dia):
        dia_normalizado = dia.strip().lower()
        if dia_normalizado in self.__dias:
            return True

        equivalencias = {
            "miercoles": "miércoles",
            "miércoles": "miercoles",
            "sabado": "sábado",
            "sábado": "sabado",
        }

        dia_equivalente = equivalencias.get(dia_normalizado)
        if dia_equivalente and dia_equivalente in self.__dias:
            return True
        return False

    def obtener_especialidad(self):
        return self.__tipo

    def __str__(self):
        dias_str = ", ".join(self.__dias)
        return f"{self.__tipo}. Días: {dias_str}"
