from datetime import datetime
from src.modelos.clinica import Clinica
from src.modelos.paciente import Paciente
from src.modelos.medico import Medico
from src.modelos.especialidad import Especialidad
from src.modelos.excepciones import (
    ElPacienteNoExisteException,
    ElMedicoNoExisteException,
    MedicoNoDisponibleException,
    TurnoTomadoException,
    RecetaNoValidaException,
)


class interfaz:
    def __init__(self):
        self.clinica = Clinica()

    def menu(self):
        print("\nSistema de gestion de clinica")
        print("1 - Agregar paciente")
        print("2 - Agregar medico")
        print("3 - Agendar turno")
        print("4 - Agregar especialidad a medico")
        print("5 - Emitir receta")
        print("6 - Ver historia clinica")
        print("7 - Ver todos los turnos")
        print("8 - Ver todos los pacientes")
        print("9 - Ver todos los medicos")
        print("0 - Salir")

    def ejecutar(self):
        while True:
            self.menu()

            try:
                opcion = input("Selecciona una opcion: ").strip()

                if opcion == "0":
                    print("\nSesion Cerrada con exito")
                    break
                elif opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad_a_medico()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_todos_los_turnos()
                elif opcion == "8":
                    self.ver_todos_los_pacientes()
                elif opcion == "9":
                    self.ver_todos_los_medicos()
                else:
                    print("Opcion invalida.")
            except KeyboardInterrupt:
                print("Sesion cerrada con exito")
                break
            except Exception as e:
                print(f"Error: {e}")
                input("\nAprete Enter para continuar")

    def agregar_paciente(self):
        print("\nAgregar paciente")

        while True:
            try:
                nombre = input("Nombre completo: ").strip()
                if not nombre:
                    raise ValueError("El nombre no debe estar vacío")

                dni = input("DNI: ").strip()
                if not dni:
                    raise ValueError("El DNI no debe estar vacío")
                if not dni.isdigit():
                    raise ValueError("El DNI debe contener solo números")

                fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ").strip()
                if not fecha_nacimiento:
                    raise ValueError("La fecha de nacimiento no debe estar vacía")
                try:
                    datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
                except ValueError:
                    raise ValueError(
                        "La fecha debe estar en formato dd/mm/aaaa y ser válida"
                    )

                paciente = Paciente(nombre, dni, fecha_nacimiento)
                self.clinica.agregar_paciente(paciente)

                print("Paciente agregado")
                print(f"{paciente}")
                break  # Sale del bucle si se agregó correctamente

            except ValueError as e:
                print(f"Error: {e}")
                print("Por favor, intente nuevamente.\n")

        input("\nEnter para continuar")

    def agregar_medico(self):
        print("\nAgregar medico")

        try:
            while True:
                nombre = input("Nombre completo del medico: ").strip()
                if not nombre:
                    print("El nombre del medico no debe estar vacio.")
                    continue
                break

            while True:
                matricula = input("Matricula: ").strip()
                if not matricula:
                    print("La matricula no debe estar vacia.")
                    continue
                break

            medico = Medico(nombre, matricula)

            print("\nAgregue especialidades (Enter para dejar en blanco):")

            while True:
                especialidad_nombre = input("Especialidad: ").strip()
                if not especialidad_nombre:
                    break

                dias = self.solicitar_dias_atencion()
                if dias:
                    especialidad = Especialidad(especialidad_nombre, dias)
                    medico.agregar_especialidad(especialidad)
                    print(f"Especialidad '{especialidad_nombre}' agregada")
                else:
                    print("No se proporcionaron dias validos")
                    continue

            self.clinica.agregar_medico(medico)

            print("Medico agregado")
            print(f"{medico}")

        except Exception as e:
            print(f"Error: {e}")

        input("\nEnter para continuar")

    def solicitar_dias_atencion(self):
        print(
            "Dias disponibles: lunes, martes, miercoles, jueves, viernes, sabado, domingo"
        )
        dias_input = input("Dias de atencion: (!!separelos por comas!!) : ").strip()

        if not dias_input:
            return []

        dias = [dia.strip() for dia in dias_input.split(",") if dia.strip()]
        return dias

    def agendar_turno(self):
        print("\nAgendar turno")

        try:
            while True:
                dni = input("DNI: ").strip()
                if not dni:
                    print("El DNI no debe estar vacío.")
                    continue
                if not dni.isdigit():
                    print("El DNI debe contener solo números.")
                    continue
                break

            while True:
                matricula = input("Matrícula del médico: ").strip()
                if not matricula:
                    print("La matrícula no debe estar vacía.")
                    continue
                break

            while True:
                especialidad = input("Especialidad solicitada: ").strip().lower()
                if not especialidad:
                    print("La especialidad no debe estar vacía.")
                    continue
                break

            while True:
                fecha_str = input("Fecha del turno (dd/mm/aaaa): ").strip()
                hora_str = input("Hora del turno (HH:MM): ").strip()
                try:
                    fecha_hora = self.parse_fecha_hora(fecha_str, hora_str)
                    break
                except ValueError:
                    print("Fecha u hora inválida. Intente de nuevo.")
                    continue

            # Si todas las validaciones pasaron, se agenda el turno
            self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)

            print("Turno agendado")
            print(f"Paciente DNI: {dni}")
            print(f"Médico: {matricula}")
            print(f"Fecha: {fecha_hora.strftime('%d/%m/%Y %H:%M')}")

        except (
            ElPacienteNoExisteException,
            ElMedicoNoExisteException,
            MedicoNoDisponibleException,
            TurnoTomadoException,
        ) as e:
            print(f"{e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")

    def agregar_especialidad_a_medico(self):
        print("\nAgregar especialidad a médico")

        try:
            while True:
                matricula = input("Matrícula del médico: ").strip()
                if not matricula:
                    print("La matrícula no debe estar vacía.")
                    continue
                break

            medico = self.clinica.obtener_medico_por_matricula(matricula)

            while True:
                especialidad_nombre = input("Nombre especialidad: ").strip()
                if not especialidad_nombre:
                    print("La especialidad no debe estar vacía.")
                    continue
                break

            dias = self.solicitar_dias_atencion()
            if not dias:
                print("Debe ingresar al menos un día válido.")
                input("\nEnter para continuar")
                return

            # Filtrar solo días válidos
            dias_validos = {
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

            dias_filtrados = [
                d.strip().lower() for d in dias if d.strip().lower() in dias_validos
            ]

            if not dias_filtrados:
                print("No se ingresaron días válidos.")
                input("\nEnter para continuar")
                return

            especialidad = Especialidad(especialidad_nombre, dias_filtrados)
            medico.agregar_especialidad(especialidad)

            print("Especialidad agregada")
            print(f"{especialidad}")

        except ElMedicoNoExisteException as e:
            print(f"{e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")

    def emitir_receta(self):
        print("\nEmitir receta")

        try:
            while True:
                dni = input("DNI del paciente: ").strip()
                if not dni:
                    print("El DNI no debe estar vacío.")
                    continue
                if not dni.isdigit():
                    print("El DNI debe contener solo números.")
                    continue
                break

            while True:
                matricula = input("Matrícula del médico: ").strip()
                if not matricula:
                    print("La matrícula no debe estar vacía.")
                    continue
                break

            print("\nMedicamentos (Enter para dejar en blanco):")
            medicamentos = []

            while True:
                medicamento = input("Medicamento: ").strip()
                if not medicamento:
                    break
                medicamentos.append(medicamento)

            if not medicamentos:
                print("Debe ingresar por lo menos un medicamento.")
                return

            self.clinica.emitir_receta(dni, matricula, medicamentos)

            print("Receta emitida")
            print(f"Paciente DNI: {dni}")
            print(f"Médico: {matricula}")
            print(f"Medicamentos: {', '.join(medicamentos)}")

        except (
            ElPacienteNoExisteException,
            ElMedicoNoExisteException,
            RecetaNoValidaException,
        ) as e:
            print(f"{e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")

    def ver_historia_clinica(self):
        print("\n Ver historia clinica")

        try:
            dni = input("DNI paciente: ").strip()

            historia = self.clinica.obtener_historia_clinica(dni)

            print(historia)

        except ElPacienteNoExisteException as e:
            print(f"{e}")
        except Exception as e:
            print(f"Error: {e}")

        input("\nEnter para continuar")

    def ver_todos_los_turnos(self):
        print("\nTodos los turnos")

        try:
            turnos = self.clinica.obtener_turnos()

            if not turnos:
                print("No hay turnos agendados")

            else:
                print(f"Total de turnos: {len(turnos)}")

            for i, turno in enumerate(turnos, 1):
                print(f"{i}. {turno}")

        except Exception as e:
            print(f"Error: {e}")

        input("\nEnter para continuar")

    def ver_todos_los_pacientes(self):
        print("\nTodos los pacientes")

        try:
            pacientes = self.clinica.obtener_pacientes()

            if not pacientes:
                print("No hay pacientes registrados")
            else:
                print(f"Total de pacientes: {len(pacientes)}")

                for i, paciente in enumerate(pacientes, 1):
                    print(f"{i}. {paciente}")

        except Exception as e:
            print(f"Error: {e}")

        input("\nEnter para continuar")

    def ver_todos_los_medicos(self):
        print("\nTodos los medicos")

        try:
            medicos = self.clinica.obtener_medicos()

            if not medicos:
                print("No hay medicos registrados")
            else:
                print(f"Total de medicos: {len(medicos)}")

                for i, medico in enumerate(medicos, 1):
                    print(f"{i}. {medico}")

        except Exception as e:
            print(f"Error: {e}")

        input("\nEnter para continuar")

    def parse_fecha_hora(self, fecha_str, hora_str):
        try:
            fecha_hora_str = f"{fecha_str} {hora_str}"
            return datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
        except ValueError:
            raise ValueError("Formato de fecha u hora invalido. (dd/mm/aaaa)")
