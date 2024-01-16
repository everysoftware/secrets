import uvicorn

from domain.config import domain_settings
from interfaces.rest.config import rest_settings

if __name__ == "__main__":
    uvicorn.run(
        "backend.interfaces.rest.app:app",
        host=rest_settings.host,
        port=rest_settings.port,
        reload=domain_settings.environment.is_debug,
    )
