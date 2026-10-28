from typing import Optional
from sqlalchemy import create_engine, String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from pydantic import BaseModel, ConfigDict, field_validator

SQLALCHEMY_DATABASE_URL = "sqlite:///./talentcore.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Empleado(Base):
    __tablename__ = "empleados"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    rol: Mapped[str] = mapped_column(String, nullable=False)
    anios_antiguedad: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("empleados.id"), nullable=True)


class SolicitudVacaciones(Base):
    __tablename__ = "solicitudes_vacaciones"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empleado_id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), nullable=False)
    dias_solicitados: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    estado: Mapped[str] = mapped_column(String, nullable=False, default="PENDING")
    revisado_por_id: Mapped[Optional[int]] = mapped_column(ForeignKey("empleados.id"), nullable=True)


class EmpleadoCreate(BaseModel):
    nombre: str
    email: str
    rol: str
    anios_antiguedad: int = 1
    manager_id: Optional[int] = None

    @field_validator("manager_id", mode="before")
    @classmethod
    def empty_manager_id_is_none(cls, value):
        if isinstance(value, str) and not value.strip():
            return None
        return value


class EmpleadoResponse(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    anios_antiguedad: int
    manager_id: Optional[int]
    model_config = ConfigDict(from_attributes=True)


class SaldoResponse(BaseModel):
    empleado_id: int
    dias_totales: int
    dias_aprobados: int
    saldo_disponible: int


class SolicitudCreate(BaseModel):
    empleado_id: int
    dias_solicitados: int
    motivo: Optional[str] = None


class RevisionRequest(BaseModel):
    accion: str


class SolicitudResponse(BaseModel):
    id: int
    empleado_id: int
    dias_solicitados: int
    motivo: Optional[str]
    estado: str
    revisado_por_id: Optional[int]
    model_config = ConfigDict(from_attributes=True)
