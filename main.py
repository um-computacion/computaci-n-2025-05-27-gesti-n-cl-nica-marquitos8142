from src.interfaz.interfaz import interfaz


def main():
    try:
        Interfaz = interfaz()
        Interfaz.ejecutar()

    except KeyboardInterrupt:
        print("\n Sistema terminado por usuario")
    except Exception as e:
        print(f"\nError en el sistema: {e}")


if __name__ == "__main__":
    main()
