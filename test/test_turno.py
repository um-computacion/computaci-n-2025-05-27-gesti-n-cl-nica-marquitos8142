import unittest
from datetime import datetime
from src.modelos.paciente import Paciente
from src.modelos.medico import Medico
from src.modelos.especialidad import Especialidad
from src.modelos.turno import Turno

class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Misco Jones", "12345678", "17/07/1977")
        self.medico = Medico("Dr. Alan Brito", "MAT11111")
        self.pediatria = Especialidad("Dermatologo", ["lunes", "miercoles", "viernes"])
        self.medico.agregar_especialidad(self.pediatria)
        self.fecha_hora = datetime(2025, 6, 16, 14, 30)

    def test_crear_turno(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "Dermatologo")

        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha_hora)
        self.assertIn("Misco Jones", str(turno))
        self.assertIn("Dr. Alan Brito", str(turno))
        self.assertIn("Dermatologo", str(turno))

    def test_paciente_none(self):
        with self.assertRaises(ValueError):
            Turno(None, self.medico, self.fecha_hora, "Dermatologo")

    def test_medico_none(self):
        with self.assertRaises(ValueError):
            Turno(self.paciente, None, self.fecha_hora, "Dermatologo")

    def test_fecha_none(self):
        with self.assertRaises(ValueError):
            Turno(self.paciente, self.medico, None, "Dermatologo")

    def test_especialidad_vacia(self):
        with self.assertRaises(ValueError):
            Turno(self.paciente, self.medico, self.fecha_hora, "")

    def test_str_(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "Dermatologo")
        resultado = str(turno)

        self.assertIn("Misco Jones", resultado)
        self.assertIn("Dr. Alan Brito", resultado)
        self.assertIn("Dermatologo", resultado)
        self.assertIn("2025", resultado)

if __name__ == "__main__":
    unittest.main()