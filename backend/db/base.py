from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings
import logging

# Configuración de logs para ver qué pasa al iniciar
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 10,
    "keepalives_count": 5
}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    from src.metrics import taller_diego_database_connections_active
    taller_diego_database_connections_active.set_function(lambda: engine.pool.checkedout())
except ImportError:
    pass


def init_db():
    """
    Función para inicializar la DB solo cuando el contenedor esté listo.
    Llamaremos a esta función desde main.py, no aquí.
    """
    #if engine.url.get_backend_name() == "postgresql":
     #   try:
      #      with engine.connect() as conn:
       #         conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        ##       logger.info("Extensión pg_trgm verificada/creada con éxito.")
        #except Exception as e:
         #   logger.error(f"Error inicializando la base de datos: {e}")

# ELIMINAMOS el bloque 'if engine.url...' que estaba aquí afuera.