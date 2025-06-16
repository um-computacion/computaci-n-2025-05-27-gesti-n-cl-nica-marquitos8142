import unittest
from src.modelos.medico import Medico
from src.modelos.especialidad import Especialidad

class TestMedico(unittest.TestCase):

    def setUp(self):#                         Codigo Normal
        self.pediatria = Especialidad("Dermatologia", ["lunes", "miercoles", "viernes"])
        self.cardiologia = Especialidad("Odontologia", ["martes", "jueves"])

    def test_crear_medico(self):  
        medico = Medico("Dr. Alan Brito", "MAT122333")

        self.assertEqual(medico.obtener_matricula(), "MAT122333")
        self.assertIn("Dr. Alan Brito", str(medico))
        self.assertIn("MAT122333", str(medico))

    def test_agregar_especialidad(self):
        medico = Medico("Dr. Alan Brito", "MAT122333")

        medico.agregar_especialidad(self.pediatria)
        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Dermatologia")
        self.assertIn("Dermatologia", str(medico))
    
    def test_duplicados_especialidad(self):
        medico = Medico("Dr. Carlitos", "MAT67890")

        medico.agregar_especialidad(self.pediatria)
        with self.assertRaises(ValueError):
            medico.agregar_especialidad(self.pediatria)

    def test_especialidad_para_dia_disponible(self):
        medico = Medico("Dr. Juanito", "MAT11111")
        medico.agregar_especialidad(self.pediatria)
        medico.agregar_especialidad(self.cardiologia)

        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Dermatologia")
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Odontologia")
        self.assertIsNone(medico.obtener_especialidad_para_dia("sabado"))

    def test_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Medico("", "MAT33333")#   Campo vacio

    def test_matricula_vacia(self):
        with self.assertRaises(ValueError):
            Medico("Dr. Jorge Nitales", "")#   Campo vacio

    def test_str_(self):
        medico = Medico("Dr. Joseph Joestar", "MAT55555")
        medico.agregar_especialidad(self.pediatria)
        resultado = str(medico)

        self.assertIn("Dr. Joseph Joestar", resultado)
        self.assertIn("MAT55555", resultado)
        self.assertIn("Dermatologia", resultado)

if __name__ == "__main__":
    unittest.main()