# Inventario de Ítems de Configuración - TAREA 1
## Backend Core + Autenticación

**Responsable:** Adriana  
**Objetivo:** Identificar y documentar los ICs del núcleo del backend y autenticación  
**Total de ICs:** 13  

---

## Tabla de Ítems de Configuración

| ID-IC | Categoría | Nombre | Ubicación | Versión | Responsable | Criticidad | Tipo de Relación |
|-------|-----------|--------|-----------|---------|------------|-----------|------------------|
| CORE-001 | FastAPI Application | FastAPI App | backend/main.py | 1.0 | Adriana | Crítica | - |
| CORE-002 | Middleware | CORSMiddleware | backend/main.py | 1.0 | Adriana | Alta | Derivación |
| CORE-003 | Middleware | GZipMiddleware | backend/main.py | 1.0 | Adriana | Media | Derivación |
| CORE-004 | Middleware | Cache Headers Middleware | backend/main.py | 1.0 | Adriana | Media | Derivación |
| CORE-005 | Configuration | Settings | backend/core/config.py | 1.0 | Adriana | Crítica | Derivación |
| CORE-006 | ORM Base | SQLAlchemy Base | backend/db/base.py | 1.0 | Adriana | Crítica | Derivación |
| CORE-007 | Database Engine | Database Engine | backend/db/base.py | 1.0 | Adriana | Crítica | Derivación |
| CORE-008 | Session Manager | SessionLocal | backend/db/base.py | 1.0 | Adriana | Alta | Derivación |
| CORE-009 | Health Check | Health Check Route | backend/db/status_routes.py | 1.0 | Adriana | Alta | Derivación |
| AUTH-001 | Bounded Context | Auth Service | backend/src/auth/application/auth_service.py | 1.0 | Adriana | Crítica | - |
| AUTH-002 | ORM Model | Auth Model | backend/src/auth/infrastructure/auth.py | 1.0 | Adriana | Alta | Derivación |
| AUTH-003 | Schema/DTO | Auth Schema | backend/src/auth/infrastructure/auth_schema.py | 1.0 | Adriana | Media | Derivación |
| AUTH-004 | API Routes | Auth Routes | backend/src/auth/infrastructure/auth_routes.py | 1.0 | Adriana | Crítica | Derivación |

---

## Relaciones entre ICs (Trazabilidad)

### Sucesión (Versiones)
- No aplica en v1.0 (próximas versiones tendrán hotfixes)

### Derivación
- **CORE-002, CORE-003, CORE-004** → Derivados de **CORE-001** (FastAPI app necesita middlewares)
- **CORE-005** → Derivado del requisito de configuración centralizada (gestiona variables de entorno)
- **CORE-006, CORE-007, CORE-008** → Derivados de **CORE-005** (configuración determina conexión a BD)
- **CORE-009** → Derivado de **CORE-007** (health check valida la conexión a BD)
- **AUTH-002** → Derivado de **AUTH-001** (modelo ORM materializa la entidad Auth)
- **AUTH-003** → Derivado de **AUTH-001** (schema comunica datos de autenticación)
- **AUTH-004** → Derivado de **AUTH-001** (expone endpoints de autenticación)

### Dependencia
- **AUTH-001** depende de **CORE-005** (AuthService requiere configuración de Supabase)
- **AUTH-004** depende de **AUTH-001** y **CORE-008** (rutas necesitan servicio y sesión de BD)
- **CORE-009** depende de **CORE-008** (health check necesita sesión para verificar conectividad)
- Todos los ICs de **src/** (Bounded Contexts) dependen de **CORE-005, CORE-006, CORE-007** (configuración y ORM)

---

## Arquitectura de Dependencias

```
FastAPI App (CORE-001)
├── Middlewares (CORE-002, CORE-003, CORE-004)
└── Settings Config (CORE-005)
    ├── Database Engine (CORE-007)
    │   ├── SessionLocal (CORE-008)
    │   │   ├── Health Check (CORE-009)
    │   │   └── Auth Service (AUTH-001)
    │   │       ├── Auth Model (AUTH-002)
    │   │       ├── Auth Schema (AUTH-003)
    │   │       └── Auth Routes (AUTH-004)
    │   └── Base ORM (CORE-006)
    └── [Otros Bounded Contexts dependen de esta capa]
```

---

## Notas Importantes
- **Criticidad Crítica:** ICs cuya falla impide que el sistema funcione
- **CORE-005 (Settings)** es el epicentro de configuración centralizada
- **CORE-007 (Database Engine)** es fundamental para toda persistencia
- **AUTH-001** actúa como intermediario entre frontend y Supabase Auth
- Los Middlewares garantizan seguridad (CORS), rendimiento (GZIP) y observabilidad (caché)
- El Health Check (CORE-009) valida toda la pila: Frontend → Backend → BD → Backend → Frontend
