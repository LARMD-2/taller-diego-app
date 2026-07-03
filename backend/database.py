from db.base import engine, Base

# El bloque if asegura que esto SOLO se ejecute si llamas al archivo directamente
# desde la terminal (como lo hace tu GitHub Actions), y no cuando lo importas.
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas inicializadas correctamente (Aplica para Local, CI/CD o Nube)")