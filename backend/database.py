from db.base import engine, Base

Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente en Supabase")
