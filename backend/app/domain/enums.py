"""
Módulo de enumeraciones para el dominio.

Contiene las enumeraciones que representan los roles de usuario,
planes de tenant y estados de tenant.
"""
from enum import Enum

class UserRole(str, Enum):
    """
    Enum para representar los roles de usuario.

    Roles disponibles:
    - SUPER_ADMIN: Super administrador de la plataforma
    - ADMIN_AGENCIA: Administrador de una agencia
    - AGENTE: Agente de una agencia
    """
    SUPER_ADMIN = "super_admin"
    ADMIN_AGENCIA = "admin_agencia"
    AGENTE = "agente"

class TenantPlan(str, Enum):
    """
    Enum para representar los planes de tenant.

    Planes disponibles:
    - TRIAL: Plan de prueba
    - STARTER: Plan inicial
    - PRO: Plan profesional
    - AGENCIA: Plan de agencia
    """
    TRIAL = "Trial"
    STARTER = "Starter"
    PRO = "Pro"
    AGENCIA = "Agencia"

class TenantStatus(str, Enum):
    """
    Enum para representar los estados de tenant.

    Estados disponibles:
    - ACTIVE: Tenant activo
    - TRIALING: Tenant en período de prueba
    - PAST_DUE: Tenant con pago vencido
    - CANCELLED: Tenant cancelado
    """
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"

class ClientStatus(str, Enum):
    """
    Enum para representar los estados de un cliente.

    Estados disponibles:
    - PROSPECTO: Lead
    - CONTACTADO: Follow-up realizado
    - COTIZANDO: Propuesta en proceso
    - CLIENTE_ACTIVO: Póliza vigente
    - INACTIVO: Sin póliza vigente o perdido
    """
    PROSPECTO = "Prospecto"
    CONTACTADO = "Contactado"
    COTIZANDO = "Cotizando"
    CLIENTE_ACTIVO = "Cliente Activo"
    INACTIVO = "Inactivo"

class PersonType(str, Enum):
    """
    Enum para representar el tipo de persona.

    Tipos disponibles:
    - FISICA: Persona física
    - MORAL: Persona moral
    """
    FISICA = "Física"
    MORAL = "Moral"
