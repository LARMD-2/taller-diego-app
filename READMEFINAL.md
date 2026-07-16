# Sistema de Microservicios Hexagonal

Este documento resume el flujo de despliegue del sistema usando **Kubernetes**, **Minikube**, **Helm** y **Argo CD**. La idea es que el estado del clúster se mantenga sincronizado con la configuración declarativa del repositorio.

## Requisitos previos

Antes de desplegar, asegúrate de tener instalado lo siguiente:

- Minikube
- kubectl
- Helm
- Git

## Paso 1: Iniciar la infraestructura local

1. Inicia Minikube:

```bash
minikube start
```

2. Instala Argo CD en el clúster:

```bash
kubectl create namespace argocd
helm repo add argo https://argoproj.github.io/argo-helm
helm upgrade -i argo-cd argo/argo-cd -n argocd --create-namespace
```

3. Obtén la contraseña inicial del usuario `admin`:

```powershell
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}")))
```

4. Agrega el repositorio de Prometheus y actualiza los charts:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

5. Instala el stack de monitoreo:

```bash
helm install prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

6. Obtén la contraseña para acceder a Prometheus:

```powershell
$secret = kubectl get secret --namespace monitoring -l app.kubernetes.io/component=admin-secret -o jsonpath="{.items[0].data.admin-password}"
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($secret))
```

7. Agrega e instala Chaos Mesh:

```bash
# 1. Agregar el repositorio de Helm
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm repo update

# 2. Instalar Chaos Mesh
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-testing --create-namespace
```

## Paso 2: Conectar el repositorio con Argo CD

Una vez instalado Argo CD, aplica el manifiesto bootstrap que registra la aplicación y permite que Argo CD observe el repositorio.

```bash
kubectl apply -f application-mvp.yaml
```

Si tu archivo de bootstrap tiene otro nombre, sustituye `application-mvp.yaml` por el manifiesto correspondiente.

## Paso 3: Acceder al panel de Argo CD

Expón el servidor de Argo CD para acceder a su interfaz web:

```bash
kubectl port-forward svc/argo-cd-argocd-server -n argocd 8080:443
```

Abre `https://localhost:8080` en el navegador e inicia sesión con:

- Usuario: `admin`
- Contraseña: la obtenida con el comando anterior

## Paso 4: Verificar el frontend

Cuando el despliegue esté sincronizado, obtén la URL del frontend con:

```bash
minikube service frontend-deployment --url
```

Abre la URL resultante en el navegador para comprobar que la aplicación quedó disponible.

## Acceso a Grafana y Jaeger

Para revisar métricas y trazas, expón los servicios localmente con estos comandos:

```bash
kubectl port-forward svc/prometheus-stack-grafana -n monitoring 3000:80
```

Luego abre:

`http://localhost:3000`

```bash
kubectl port-forward svc/jaeger-ui -n monitoring 16686:16686
```

Luego abre:

`http://localhost:16686`

## Notas

- Este flujo asume que el repositorio contiene los manifiestos necesarios para Argo CD.
- Si el clúster ya está levantado, puedes saltar el paso de `minikube start`.
- Si cambias el nombre del servicio frontend, actualiza el comando `minikube service`.