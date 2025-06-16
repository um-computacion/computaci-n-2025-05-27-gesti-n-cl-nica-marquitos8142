import unittest
from datetime import datetime
from src.modelos.paciente import Paciente
from src.modelos.medico import Medico
from src.modelos.receta import Receta

class TestReceta(unittest.TestCase):
    
    def setUp(self):
        self.paciente = Paciente("Joseph Joestar", "87654321", "20/05/1985")
        self.medico = Medico("Dr. Alan Brito", "MAT99999")
        self.medicamentos = ["Ibuprofeno 200mg", "Rubifem 20mg"]
    
    def test_crear_receta(self):
        receta = Receta(self.paciente, self.medico, self.medicamentos)
        resultado = str(receta)
        
        self.assertIn("Joseph Joestar", resultado)
        self.assertIn("Dr. Alan Brito", resultado)
        self.assertIn("Ibuprofeno 200mg", resultado)
        self.assertIn("Rubifem 20mg", resultado)
        
        self.assertIsInstance(receta._Receta__fecha, datetime)
    
    def test_error_sin_medicamentos(self):
        with self.assertRaises(ValueError):
            Receta(self.paciente, self.medico, [])
    
    def test_error_medicamentos_none(self):
        with self.assertRaises(ValueError):
            Receta(self.paciente, self.medico, None)
    
    def test_error_paciente_none(self):
        with self.assertRaises(ValueError):
            Receta(None, self.medico, self.medicamentos)
    
    def test_error_medico_none(self):
        with self.assertRaises(ValueError):
            Receta(self.paciente, None, self.medicamentos)
    
    def test_str_(self):
        receta = Receta(self.paciente, self.medico, self.medicamentos)
        resultado = str(receta)
        
        self.assertIn("Receta", resultado)
        self.assertIn("Joseph Joestar", resultado)
        self.assertIn("Dr. Alan Brito", resultado)
        self.assertIn("Ibuprofeno 200mg", resultado)


if __name__ == "__main__":
    unittest.main()