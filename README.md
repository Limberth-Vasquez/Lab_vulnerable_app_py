# Laboratorio: Aplicación Vulnerable a SQL Injection con Docker Compose

## 📌 Descripción

Este proyecto implementa una aplicación web vulnerable a **SQL Injection** desarrollada en Flask y conectada a una base de datos Microsoft SQL Server.

La aplicación y la base de datos se ejecutan en contenedores separados utilizando **Docker Compose**, cumpliendo con el requisito de contenerización y orquestación.

El objetivo del laboratorio es demostrar:

- Separación de servicios en contenedores
- Comunicación interna entre contenedores
- Automatización de despliegue
- Ejecución reproducible
- Explotación de vulnerabilidad SQL Injection

---

## 🏗 Arquitectura

El entorno se compone de:

- 🐍 Contenedor 1: Aplicación Flask (Puerto 5001)
- 🗄 Contenedor 2: SQL Server 2022 (Puerto 1433)
- 🛠 Contenedor auxiliar: Inicialización automática de base de datos

┌─────────────────────┐
│ Flask App │
│ Puerto 5001 │
└─────────┬───────────┘
│
│ Red interna Docker
│
┌─────────▼───────────┐
│ SQL Server │
│ Puerto 1433 │
└─────────────────────┘


---

## 📂 Estructura del Proyecto

vulnerable-docker-lab/
│
├── app.py
├── Dockerfile
├── docker-compose.yml
├── init.sql
└── README.md


---

## ⚙️ Requisitos

- Docker
- Docker Compose (v2 o superior)

Verificar instalación:

docker --version
docker compose version


---

## 🚀 Ejecución del Proyecto

1. Clonar el repositorio:

git clone <URL_DEL_REPOSITORIO>
cd vulnerable-docker-lab


2. Construir y levantar los contenedores:

docker compose up --build


El sistema realizará automáticamente:

- Descarga de SQL Server
- Construcción de imagen Flask
- Creación de red interna
- Inicialización automática de la base de datos
- Inserción de datos de prueba

---

## 🌐 Acceso a la Aplicación

Abrir en el navegador:

http://localhost:5001


---

## 🔎 Pruebas Normales

Consultar usuario válido:

http://localhost:5001/login?username=admin


Resultado esperado:

[(1, 'admin', 'admin123')]



---

## 🔥 Prueba de SQL Injection

Ejecutar:

http://localhost:5001/login?username=
' OR 1=1--


Resultado esperado:

Se devuelven todos los registros de la tabla `users`.

Esto demuestra la vulnerabilidad por concatenación directa de parámetros en la consulta SQL.

---

## 🗄 Base de Datos

La base de datos se crea automáticamente mediante el archivo `init.sql`, el cual ejecuta:

- Creación de base `vulnerable_db`
- Creación de tabla `users`
- Inserción de registros de prueba

---

## 🛑 Detener el Entorno

Para detener los contenedores:

docker compose down


Para eliminar volúmenes y reiniciar completamente:

docker compose down -v


---

## 🎓 Objetivos Académicos Cumplidos

- Contenerización de aplicación web
- Contenerización de base de datos
- Orquestación con Docker Compose
- Automatización de despliegue
- Comunicación entre servicios por red Docker
- Demostración práctica de SQL Injection

---

## ⚠️ Advertencia

Este proyecto tiene fines exclusivamente educativos.
La vulnerabilidad implementada es intencional para fines de demostración académica.

No debe utilizarse en entornos productivos.
