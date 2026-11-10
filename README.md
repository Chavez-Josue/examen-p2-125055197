# Examen Segundo Parcial - Pipeline de Datos con Hadoop, PostgreSQL y Flask

**Matrícula:** 125055197
**Pregunta Asignada:** Top 10 productos por ingreso total en todo el año (Dígitos 6 o 7).

---

## 1. Arquitectura del Proyecto

El sistema está orquestado mediante Docker Compose y se compone de 3 servicios principales:
* **Hadoop (Standalone/Pseudo-distribuido):** Contenedor basado en Debian que ejecuta el procesamiento MapReduce mediante Hadoop Streaming y soporte SSH sin contraseña.
* **Database (PostgreSQL):** Base de datos relacional `ventas_db` con volumen persistente nombrado para conservar los datos de la analítica.
* **API (Flask):** Servicio web RESTful en Python que expone los resultados guardados en PostgreSQL a través de endpoints GET y POST.

---

## 2. Instrucciones para Reproducir el Ambiente

1. **Generar el dataset:**
   ```bash
   python generar_dataset.py 125055197