
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import time

app = FastAPI(
    title="Sistema de Autenticación Institucional",
    version="1.0.0"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

logger = logging.getLogger("AuthService")

users_db = {
    "jgarcia": {
        "password": "Clave123",
        "active": True
    },
    "mlopez": {
        "password": "Admin456",
        "active": True
    }
}

class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {"message": "Sistema de autenticación activo"}


@app.post("/login")
def login(data: LoginRequest):

    start_time = time.time()

    try:
        # Simulación de consulta lenta
        time.sleep(7)

        user = users_db.get(data.username)

        if user is None:
            logger.warning("Intento de acceso con usuario inexistente")
            raise HTTPException(
                status_code=401,
                detail="Credenciales no válidas"
            )

        # ERROR SIMULADO: comparación incorrecta
        if user["password"] != data.password + "_incorrecto":
            logger.error("Error validating user token")
            logger.error("Timeout while querying table users")

            raise HTTPException(
                status_code=500,
                detail="Error interno de autenticación"
            )

        if not user["active"]:
            raise HTTPException(
                status_code=403,
                detail="Usuario inactivo"
            )

        elapsed = round(time.time() - start_time, 2)

        return {
            "message": "Inicio de sesión exitoso",
            "username": data.username,
            "response_time": elapsed
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Error inesperado en AuthService")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )
