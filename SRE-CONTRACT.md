# Contrato de SRE — Taller Diego

## 1. Mapa de Riesgos — EventStorming (Hot Spots 🟣)

| # | Punto Caliente (Hot Spot) | Bounded Context | Riesgo Identificado |
|---|---|---|---|
| 1 | `Adaptador REST → Adaptador de Persistencia` | Ventas | La llamada a Supabase/PostgreSQL puede introducir latencia variable o timeouts |
| 2 | `Adaptador de Persistencia → BD externa` | Ventas / Inventario | Conexión de red externa (Supabase Cloud). Un corte de internet o throttling del proveedor afecta todas las operaciones de escritura |
| 3 | `JWT Middleware → Adaptador REST` | Auth | Un secret incorrecto o expirado bloquea el acceso total al sistema en el mostrador |
| 4 | `Pool de Conexiones SQLAlchemy` | Transversal | Con múltiples workers de Uvicorn y un pool pequeño, las conexiones se agotan bajo carga concurrente mínima |

---

## 2. Contrato de SRE — Estado Estable (Steady State)

El **estado estable** del sistema es la condición operativa normal bajo la que el taller puede atender clientes sin interrupciones.

### SLI de Latencia (Endpoint Crítico: `POST /api/v1/ventas`)
- **Definición:** Proporción de peticiones de venta válidas (excluyendo 400 de dominio) que se resuelven en ≤ 200 ms.
- **Medición:** `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{handler="/api/v1/ventas"}[5m]))`
- **SLO:** El **99%** de las transacciones de venta deben completarse en < 200 ms en un periodo de 30 días.

### SLI de Disponibilidad (Endpoint Crítico: `POST /api/v1/ventas`)
- **Definición:** Proporción de peticiones de venta que devuelven 2xx o 4xx (controlados) frente a errores 5xx (fallas internas).
- **Medición:** `sum(rate(http_requests_total{handler="/api/v1/ventas", status!~"5.."}[30d])) / sum(rate(http_requests_total{handler="/api/v1/ventas"}[30d]))`
- **SLO:** El **99.5%** de los intentos de registro de venta no deben generar errores 5xx en 30 días.

### Presupuesto de Error (Error Budget)
Basado en un volumen real de **500 transacciones de venta al mes**:
- **Latencia:** Máximo **5 ventas lentas** (> 200 ms) al mes. Si se llega a 6, el presupuesto se agota.
- **Disponibilidad:** Máximo **2 transacciones fallidas** (5xx) al mes. Una tercera falla obliga a estabilizar infraestructura antes de cualquier nueva funcionalidad.

---

## 3. Hipótesis de Caos

### Hipótesis Formal

> **"Si inyectamos una latencia de red de 200 ms en el pod de la API (simulando degradación del enlace hacia la base de datos Supabase), entonces el sistema comenzará a reportar peticiones POST /api/v1/ventas con un P99 superior a 200 ms, agotando el presupuesto de error de latencia dentro del periodo de observación de 5 minutos, SIN que el pod colapse o reinicie, demostrando que el fallo es de tipo 'degradación controlada' y no una caída en cascada."**

### Variables del Experimento

| Variable | Valor |
|---|---|
| **Fallo Inyectado** | Latencia de red: `+200ms` |
| **Radio de Impacto (Blast Radius)** | 1 pod aleatorio del deployment `api-deployment` |
| **Duración del Experimento** | 5 minutos |
| **Señal de Éxito (Steady State Mantenido)** | Pod no reinicia, Health Probe `/health/live` sigue en 200 OK |
| **Señal de Fallo (Hipótesis Confirmada)** | P99 de latencia supera 200ms en Grafana durante el caos |
| **Recuperación Esperada** | Al terminar el experimento, P99 vuelve por debajo de 200ms automáticamente |
