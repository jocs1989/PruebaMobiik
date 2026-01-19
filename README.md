# 🧠 DevIA Technical Test

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-00A86B?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-1F2937?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-0DB7ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

---
# Impulsa tu Futuro con Soluciones de IA y Nube
## 📌 Descripción


Este proyecto corresponde a una **prueba técnica para el puesto DevIA**, enfocada en el desarrollo de una **API backend con capacidades de inferencia de IA**, diseñada bajo principios de **arquitectura limpia, escalabilidad y buenas prácticas**.

La solución demuestra:

* Diseño backend moderno
* Integración de modelos de lenguaje (LLM)
* Separación clara de responsabilidades
* Contenerización y despliegue reproducible
* Manejo de autenticación, inferencia y persistencia

---

## 🧩 Arquitectura General

* **FastAPI** como framework principal
* **Motor de inferencia de IA desacoplado**
* **PostgreSQL** para persistencia relacional
* **Base documental** para modelos de IA
* **Docker / Docker Compose** para orquestación
* **Poetry** para manejo de dependencias
* **Sistema de logging centralizado**

---

## 📁 Estructura del Proyecto

```bash
├── main.py                 # Punto de entrada de la aplicación
├── Dockerfile              # Imagen de la API
├── docker-compose.yml      # Orquestación de servicios
├── config.py               # Configuración global
├── logger.py               # Sistema de logging
├── app.log                 # Logs de la aplicación
├── run.bash                # Script de arranque
├── src/
│   ├── api/                # Ruteo de la API
│   │   └── v1/
│   │       ├── endpoints/  # Endpoints REST
│   │       └── docs/       # Documentación
│   ├── services/           # Lógica de negocio
│   ├── repositories/       # Acceso a datos
│   ├── models/             # Modelos de BD (relacional / documental)
│   ├── schemas/            # Esquemas Pydantic
│   ├── authentication/     # Seguridad y autenticación
│   ├── database/           # Inicialización y seeds
│   └── tools/              # Excepciones y utilidades
```

---

## 🚀 Ejecución del Proyecto

### 1️⃣ Clonar el repositorio

```bash
git clone <repo-url>
cd devia-technical-test
```

---

### 2️⃣ Construir y levantar los servicios

```bash
docker-compose up --build
```

La API estará disponible en:

```
http://localhost:8000
```

---

## 🤖 Inferencia con IA

La aplicación expone endpoints para **procesamiento de prompts y generación de respuestas**, utilizando un **motor de inferencia desacoplado**, lo que permite:

* Cambiar el modelo sin afectar la API
* Escalar el componente de IA de forma independiente
* Mantener una arquitectura limpia y extensible

La lógica de inferencia se encuentra encapsulada en la capa de **services**.

---

## 🔐 Autenticación y Seguridad

El proyecto incluye:

* Gestión de usuarios
* Manejo de roles
* Validación de tokens
* Servicios de seguridad desacoplados

Todo el flujo de autenticación se implementa siguiendo principios de **separación de responsabilidades**.

---

## 🧪 Documentación de la API

FastAPI expone automáticamente:

* **Swagger UI**

  ```
  http://localhost:8000/docs
  ```

* **ReDoc**

  ```
  http://localhost:8000/redoc
  ```

---

## 🧠 Decisiones Técnicas

* Arquitectura por capas (API, Services, Repositories)
* Uso de schemas como contratos de datos
* Persistencia desacoplada del dominio
* Preparado para escalar a entornos productivos
* Código orientado a mantenibilidad y claridad

---

## 🎯 Enfoque de la Prueba

Este proyecto está orientado a evaluar:

* Capacidad de diseño backend
* Integración práctica de IA
* Organización y calidad del código
* Preparación para entornos reales de trabajo

---

## 👨‍💻 Autor

Prueba técnica desarrollada para el puesto **DevIA**.
Enfocada en **backend, IA aplicada y arquitectura moderna**.

---

💚 *Solución pensada con mentalidad de producto y estándares profesionales.*
