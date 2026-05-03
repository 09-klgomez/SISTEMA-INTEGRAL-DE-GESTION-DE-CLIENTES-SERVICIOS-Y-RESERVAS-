"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Autor: Proyecto académico
Descripción: Implementación orientada a objetos sin base de datos,
con manejo avanzado de excepciones y registro en logs.
"""

from abc import ABC, abstractmethod
from datetime import datetime

# ===================== LOGS =====================

def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {mensaje}\n")

# ===================== EXCEPCIONES =====================

class SistemaError(Exception):
    pass

class ClienteError(SistemaError):
    pass

class ServicioError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass

# ===================== CLASE ABSTRACTA =====================

class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def mostrar_info(self):
        pass

# ===================== CLIENTE =====================

class Cliente(Entidad):
    def __init__(self, id, nombre, email):
        super().__init__(id)
        self.nombre = nombre
        self.email = email

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if not value:
            raise ClienteError("Nombre inválido")
        self._nombre = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ClienteError("Email inválido")
        self._email = value

    def mostrar_info(self):
        return f"Cliente: {self.nombre} - {self.email}"

# ===================== SERVICIOS =====================

class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self):
        pass

class ReservaSala(Servicio):
    def calcular_costo(self, horas=1):
        return self.precio_base * horas

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias=1):
        return self.precio_base * dias

class Asesoria(Servicio):
    def calcular_costo(self, sesiones=1):
        return self.precio_base * sesiones

# ===================== RESERVA =====================

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaError("Cliente inválido")
        if not isinstance(servicio, Servicio):
            raise ReservaError("Servicio inválido")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        try:S
            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "Confirmada"
            registrar_log(f"Reserva confirmada - {self.cliente.nombre} - ${costo}")
            return costo
        except Exception as e:
            registrar_log(f"Error al confirmar reserva: {e}")
            raise ReservaError("No se pudo confirmar")

    def cancelar(self):
        self.estado = "Cancelada"
        registrar_log(f"Reserva cancelada - {self.cliente.nombre}")

# ===================== SISTEMA =====================

class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        try:
            self.clientes.append(cliente)
        except Exception as e:
            registrar_log(f"Error cliente: {e}")

    def agregar_servicio(self, servicio):
        try:
            self.servicios.append(servicio)
        except Exception as e:
            registrar_log(f"Error servicio: {e}")

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(cliente, servicio, duracion)
            self.reservas.append(reserva)
            return reserva
        except Exception as e:
            registrar_log(f"Error reserva: {e}")

# ===================== SIMULACIÓN =====================

if __name__ == "__main__":
    sistema = SistemaGestion()

    try:
        c1 = Cliente(1, "Juan", "juan@mail.com")
        sistema.agregar_cliente(c1)

        s1 = ReservaSala("Sala VIP", 100)
        s2 = AlquilerEquipo("Proyector", 50)
        sistema.agregar_servicio(s1)
        sistema.agregar_servicio(s2)

        r1 = sistema.crear_reserva(c1, s1, 2)
        print("Costo:", r1.confirmar())

        r2 = sistema.crear_reserva(c1, s2, 3)
        print("Costo:", r2.confirmar())

        # Error intencional
        c2 = Cliente(2, "", "correo_invalido")
        sistema.agregar_cliente(c2)

    except ClienteError as e:
        registrar_log(f"Error cliente detectado: {e}")
    except Exception as e:
        registrar_log(f"Error general: {e}")

    print("Sistema ejecutado correctamente")

