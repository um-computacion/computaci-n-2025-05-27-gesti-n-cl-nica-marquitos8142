import unittest
from datetime import datetime, timedelta
from src.modelos.paciente import Paciente
from src.modelos.medico import Medico
from src.modelos.especialidad import Especialidad
from src.modelos.clinica import Clinica
from src.modelos.excepciones import (
    ElPacienteNoExisteException,
    ElMedicoNoExisteException,
    MedicoNoDisponibleException,
    TurnoTomadoException,
    RecetaNoValidaException,
)


class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()

        # Crear pacientes y médicos de prueba
        self.paciente1 = Paciente("Joseph Joestar", "87654321", "20/05/1985")
        self.paciente2 = Paciente("Jonathan Joestar", "12345678", "15/03/1990")

        self.medico1 = Medico("Dr. Alan Brito", "MAT99999")
        self.pediatria = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.medico1.agregar_especialidad(self.pediatria)

        # Usamos próxima fecha válida (lunes) para test de turnos
        self.fecha_lunes = self._proximo_dia_a_las_1430("lunes")

    def _proximo_dia_a_las_1430(self, dia_semana: str):
        dias = {
            "lunes": 0,
            "martes": 1,
            "miércoles": 2,
            "jueves": 3,
            "viernes": 4,
            "sábado": 5,
            "domingo": 6,
        }
        hoy = datetime.now()
        hoy_index = hoy.weekday()
        target_index = dias[dia_semana]

        dias_a_sumar = (target_index - hoy_index) % 7
        # Si hoy es el mismo día pero pasó la hora, avanza una semana
        if dias_a_sumar == 0 and (
            hoy.hour > 14 or (hoy.hour == 14 and hoy.minute >= 30)
        ):
            dias_a_sumar = 7

        proxima_fecha = hoy + timedelta(days=dias_a_sumar)
        return proxima_fecha.replace(hour=14, minute=30, second=0, microsecond=0)

    # Tests pacientes

    def test_agregar_paciente(self):
        self.clinica.agregar_paciente(self.paciente1)

        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0].obtener_dni(), "87654321")

    def test_paciente_duplicado(self):
        self.clinica.agregar_paciente(self.paciente1)

        paciente_duplicado = Paciente("Joseph Copia", "87654321", "01/01/2000")
        with self.assertRaises(ValueError):
            self.clinica.agregar_paciente(paciente_duplicado)

    # Tests médicos

    def test_agregar_medico(self):
        self.clinica.agregar_medico(self.medico1)

        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0].obtener_matricula(), "MAT99999")

    def test_medico_duplicado(self):
        self.clinica.agregar_medico(self.medico1)

        medico_duplicado = Medico("Dr. Alan Copia", "MAT99999")
        with self.assertRaises(ValueError):
            self.clinica.agregar_medico(medico_duplicado)

    # Tests especialidades

    def test_agregar_especialidad(self):
        self.clinica.agregar_medico(self.medico1)
        cardiologia = Especialidad("Cardiología", ["martes", "jueves"])

        medico = self.clinica.obtener_medico_por_matricula("MAT99999")
        medico.agregar_especialidad(cardiologia)

        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Cardiología")

    def test_error_agregar_especialidad(self):
        with self.assertRaises(ElMedicoNoExisteException):
            self.clinica.obtener_medico_por_matricula("MAT00000")

    # Tests turnos

    def test_agendar_turno_exitoso(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        self.clinica.agendar_turno(
            "87654321", "MAT99999", "Pediatría", self.fecha_lunes
        )

        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].obtener_medico().obtener_matricula(), "MAT99999")

    def test_turno_duplicado(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)

        self.clinica.agendar_turno(
            "87654321", "MAT99999", "Pediatría", self.fecha_lunes
        )

        with self.assertRaises(TurnoTomadoException):
            self.clinica.agendar_turno(
                "12345678", "MAT99999", "Pediatría", self.fecha_lunes
            )

    def test_error_turno_fecha_pasada(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        fecha_pasada = datetime.now() - timedelta(days=1)
        fecha_pasada = fecha_pasada.replace(hour=10, minute=0, second=0, microsecond=0)

        with self.assertRaises(ValueError) as context:
            self.clinica.agendar_turno(
                "87654321", "MAT99999", "Pediatría", fecha_pasada
            )

        self.assertIn("pasado", str(context.exception).lower())

    def test_error_turno_paciente_inexistente(self):
        self.clinica.agregar_medico(self.medico1)

        with self.assertRaises(ElPacienteNoExisteException):
            self.clinica.agendar_turno(
                "00000000", "MAT99999", "Pediatría", self.fecha_lunes
            )

    def test_error_turno_medico_inexistente(self):
        self.clinica.agregar_paciente(self.paciente1)

        with self.assertRaises(ElMedicoNoExisteException):
            self.clinica.agendar_turno(
                "87654321", "MAT00000", "Pediatría", self.fecha_lunes
            )

    def test_error_medico_no_trabaja_ese_dia(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        fecha_martes = self._proximo_dia_a_las_1430("martes")
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno(
                "87654321", "MAT99999", "Pediatría", fecha_martes
            )

    # Tests recetas

    def test_emitir_receta(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        self.clinica.emitir_receta(
            "87654321", "MAT99999", ["Ibuprofeno 200mg", "Rubifem 20mg"]
        )

        historia = self.clinica.obtener_historia_clinica("87654321")
        recetas = historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)

    def test_error_receta_sin_medicamentos(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        with self.assertRaises(RecetaNoValidaException):
            self.clinica.emitir_receta("87654321", "MAT99999", [])

    # Tests historia clínica

    def test_historia_clinica_guarda_correctamente(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        self.clinica.agendar_turno(
            "87654321", "MAT99999", "Pediatría", self.fecha_lunes
        )
        self.clinica.emitir_receta("87654321", "MAT99999", ["Ibuprofeno 200mg"])

        historia = self.clinica.obtener_historia_clinica("87654321")
        self.assertEqual(len(historia.obtener_turnos()), 1)
        self.assertEqual(len(historia.obtener_recetas()), 1)


if __name__ == "__main__":
    unittest.main()
