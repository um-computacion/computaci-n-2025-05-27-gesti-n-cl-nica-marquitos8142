import unittest
from src.modelos.paciente import Paciente

class TestPaciente(unittest.TestCase):

    def setUp(self):
        self.nombre = "Misco Jones"
        self.dni = "45960230"
        self.fecha_nacimiento = "17/07/2000"

    def test_creacion_correcta_de_paciente(self):
        paciente = Paciente(self.nombre, self.dni, self.fecha_nacimiento)
        self.assertEqual(paciente.obtener_dni(), self.dni)
        self.assertIn(self.nombre, str(paciente))
        self.assertIn(self.dni, str(paciente))
        self.assertIn(self.fecha_nacimiento, str(paciente))

    def test_error_nombre_vacio(self):
        with self.assertRaises(ValueError) as ctx:
            Paciente("", self.dni, self.fecha_nacimiento)
        self.assertIn("nombre", str(ctx.exception).lower()) # Campo Vacio

    def test_error_dni_vacio(self):
        with self.assertRaises(ValueError) as ctx:
            Paciente(self.nombre, "", self.fecha_nacimiento)
        self.assertIn("dni", str(ctx.exception).lower()) # Campo Vacio

    def test_error_fecha_vacia(self):
        with self.assertRaises(ValueError) as ctx:
            Paciente(self.nombre, self.dni, "")
        self.assertIn("fecha", str(ctx.exception).lower()) # Campo Vacio
        
    def test_error_fecha_incompleta(self):
        with self.assertRaises(ValueError):
            Paciente(self.nombre, self.dni, "2000-07-17") # falta de los /

    def test_error_dni_no_numerico(self):
        with self.assertRaises(ValueError):
            Paciente(self.nombre, "ABC123", self.fecha_nacimiento) # Letras en DNI

    def test_error_formato_fecha_incorrecto(self):
        with self.assertRaises(ValueError):
            Paciente(self.nombre, self.dni, "2000/07/17")  # formato invalido

    def test_error_fecha_inexistente(self):
        with self.assertRaises(ValueError):
            Paciente(self.nombre, self.dni, "39/07/2000")  # dia inexistente

    def test_str_muestra_datos_correctos(self):
        paciente = Paciente(self.nombre, self.dni, self.fecha_nacimiento)
        salida = str(paciente)
        self.assertIn(self.nombre, salida)
        self.assertIn(self.dni, salida)
        self.assertIn(self.fecha_nacimiento, salida)

if __name__ == "__main__":
    unittest.main()

