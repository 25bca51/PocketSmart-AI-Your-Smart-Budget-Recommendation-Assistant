from importlib import import_module


_sqlalchemy = import_module("sqlalchemy")
_sqlalchemy_orm = import_module("sqlalchemy.orm")
create_engine = _sqlalchemy.create_engine
declarative_base = _sqlalchemy_orm.declarative_base
sessionmaker = _sqlalchemy_orm.sessionmaker

from app.config import settings


connect_args = {}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def init_db():
    # Import models before create_all so SQLAlchemy knows about them.
    # Import using importlib to avoid static-analysis warnings when the package
    # is not yet resolved in the editor environment.
    try:
        import_module("app.models.db_models")
    except ModuleNotFoundError:
        pass

    Base.metadata.create_all(bind=engine)