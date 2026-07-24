from app.core.database import Base, engine

# Importa los modelos para que SQLAlchemy los registre
from app.models import User

Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")
