from sqlalchemy import create_engine
from .config import DB_URI


# For Debug
# engine = create_engine(DB_URI, echo=True)
engine = create_engine(DB_URI)