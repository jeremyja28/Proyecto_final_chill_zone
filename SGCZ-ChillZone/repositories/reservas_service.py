# Shim module to provide patchable symbols for tests
# Exposes repo_cancelar used by services.reservas_service.cancelar_reserva
from .reserva_repository import cancelar as repo_cancelar
