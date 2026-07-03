# Inventario de Ítems de Configuración - TAREA 2
## Bounded Contexts: Órdenes + Servicios

**Responsable:** Russell  
**Objetivo:** Identificar y documentar los ICs del contexto de Operaciones del Taller (Órdenes y Servicios)  
**Total de ICs:** 16  

---

## Tabla de Ítems de Configuración

| ID-IC | Categoría | Nombre | Ubicación | Versión | Responsable | Criticidad | Tipo de Relación |
|-------|-----------|--------|-----------|---------|------------|-----------|------------------|
| ORD-001 | Domain Model | OrdenDomain | backend/src/ordenes/domain/orden_domain.py | 1.0 | Russell | Alta | - |
| ORD-002 | Value Object | GarantiaVO | backend/src/shared/domain/value_objects.py | 1.0 | Russell | Alta | Derivación |
| ORD-003 | Value Object | EstadoPagoVO | backend/src/shared/domain/value_objects.py | 1.0 | Russell | Media | Derivación |
| ORD-004 | Value Object | PrecioOrdenVO | backend/src/shared/domain/value_objects.py | 1.0 | Russell | Alta | Derivación |
| ORD-005 | Entity | OrdenEmpleado | backend/src/ordenes/infrastructure/orden_empleado.py | 1.0 | Russell | Media | Dependencia |
| ORD-006 | Entity | OrdenServicio | backend/src/ordenes/infrastructure/orden_servicio.py | 1.0 | Russell | Media | Dependencia |
| ORD-007 | ORM Model | Orden | backend/src/ordenes/infrastructure/orden.py | 1.0 | Russell | Alta | Derivación |
| ORD-008 | Application Service | OrdenService | backend/src/ordenes/application/orden_service.py | 1.0 | Russell | Alta | Derivación |
| ORD-009 | Repository | OrdenRepository | backend/src/ordenes/infrastructure/orden_repo.py | 1.0 | Russell | Alta | Derivación |
| ORD-010 | Schema/DTO | OrdenSchema | backend/src/ordenes/infrastructure/orden_schema.py | 1.0 | Russell | Media | Derivación |
| ORD-011 | API Routes | OrdenRoutes | backend/src/ordenes/infrastructure/orden_routes.py | 1.0 | Russell | Alta | Derivación |
| SER-001 | Domain Model | ServicioDomain | backend/src/servicios/domain/servicio_domain.py | 1.0 | Russell | Media | - |
| SER-002 | Value Object | InformacionServicioVO | backend/src/shared/domain/value_objects.py | 1.0 | Russell | Media | Derivación |
| SER-003 | ORM Model | Servicio | backend/src/servicios/infrastructure/servicio.py | 1.0 | Russell | Media | Derivación |
| SER-004 | Application Service | ServicioService | backend/src/servicios/application/servicio_service.py | 1.0 | Russell | Media | Derivación |
| SER-005 | Repository | ServicioRepository | backend/src/servicios/infrastructure/servicio_repo.py | 1.0 | Russell | Media | Derivación |
| SER-006 | Schema/DTO | ServicioSchema | backend/src/servicios/infrastructure/servicio_schema.py | 1.0 | Russell | Media | Derivación |
| SER-007 | API Routes | ServicioRoutes | backend/src/servicios/infrastructure/servicio_routes.py | 1.0 | Russell | Media | Derivación |

---

## Relaciones entre ICs (Trazabilidad)

### Sucesión (Versiones)
- No aplica en v1.0 (próximas versiones tendrán evoluciones)

### Derivación
- **ORD-002, ORD-003, ORD-004** → Derivados de requisitos de **ORD-001** (necesarios para validar datos)
- **ORD-007** → Derivado de **ORD-001** (modelo ORM materializa el domain model)
- **ORD-008** → Derivado de **ORD-001** (orquesta la lógica de negocio)
- **ORD-009** → Derivado de **ORD-007** (persiste datos del modelo ORM)
- **ORD-010** → Derivado de **ORD-001** (comunica datos hacia el cliente)
- **ORD-011** → Derivado de **ORD-008** (expone los servicios de aplicación)
- **SER-002** → Derivado de **SER-001** (valida información)
- **SER-003** → Derivado de **SER-001** (materializa el domain model)
- **SER-004** → Derivado de **SER-001** (orquesta la lógica)
- **SER-005** → Derivado de **SER-003** (persiste datos)
- **SER-006** → Derivado de **SER-001** (comunica hacia cliente)
- **SER-007** → Derivado de **SER-004** (expone servicios)

### Dependencia
- **ORD-005** (OrdenEmpleado) depende de **ORD-001** (necesita referencia a orden)
- **ORD-006** (OrdenServicio) depende de **ORD-001** y **SER-001** (relaciona órdenes con servicios)
- **ORD-008** (OrdenService) depende de **ORD-002, ORD-003, ORD-004** (usa Value Objects)
- **SER-004** (ServicioService) depende de **SER-002** (usa Value Objects)

---

## Notas Importantes
- **Criticidad Alta:** ICs que de tener errores impactan directamente en operaciones
- **Criticidad Media:** ICs importantes pero con menor impacto inmediato
- Los Value Objects están en el módulo **shared** para ser reutilizados por otros contextos
- Las relaciones de **Derivación** muestran cómo evoluciona el código desde el model de dominio hasta la API
- Las relaciones de **Dependencia** muestran acoplamiento entre componentes
