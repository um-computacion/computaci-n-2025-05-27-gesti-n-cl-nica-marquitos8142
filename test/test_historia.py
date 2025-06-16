import unittest
from datetime import datetime
from src.modelos.paciente import Paciente
from src.modelos.medico import Medico
from src.modelos.especialidad import Especialidad
from src.modelos.turno import Turno
from src.modelos.receta import Receta
from src.modelos.historia_clinica import HistoriaClinica


class TestHistoriaClinica(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Luis Rodríguez", "11111111", "10/01/1980")
        self.medico = Medico("Dr. Patricia Silva", "MAT55555")
        self.pediatria = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.pediatria)

        self.fecha_hora = datetime(2025, 6, 16, 10, 0)
        self.turno = Turno(self.paciente, self.medico, self.fecha_hora, "Pediatría")
        self.receta = Receta(self.paciente, self.medico, ["Aspirina 100mg"])

        self.historia = HistoriaClinica(self.paciente)

    def test_crear_historia_clinica(self):
        self.assertEqual(len(self.historia.obtener_turnos()), 0)
        self.assertEqual(len(self.historia.obtener_recetas()), 0)
        self.assertIn("Luis Rodríguez", str(self.historia))

    def test_agregar_turno(self):
        self.historia.agregar_turno(self.turno)

        turnos = self.historia.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0], self.turno)

    def test_agregar_receta(self):
        self.historia.agregar_receta(self.receta)

        recetas = self.historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)
        self.assertEqual(recetas[0], self.receta)

    def test_obtener_copias_no_referencias(self):
        self.historia.agregar_turno(self.turno)

        turnos_obtenidos = self.historia.obtener_turnos()
        turnos_obtenidos.clear()  # Modificar la copia

        # La lista original no debe verse afectada
        self.assertEqual(len(self.historia.obtener_turnos()), 1)

    def test_agregar_turno_none(self):
        with self.assertRaises(ValueError):
            self.historia.agregar_turno(None)

    def test_agregar_receta_none(self):
        with self.assertRaises(ValueError):
            self.historia.agregar_receta(None)

    def test_str_representation_completa(self):
        self.historia.agregar_turno(self.turno)
        self.historia.agregar_receta(self.receta)
        resultado = str(self.historia)

        self.assertIn("Luis Rodríguez", resultado)
        self.assertIn("Turnos", resultado)
        self.assertIn("Recetas", resultado)
        self.assertIn("Dr. Patricia Silva", resultado)


if __name__ == "__main__":
    unittest.main()
