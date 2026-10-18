# Práctica 1: Perfilamiento e Ingesta Multi-Fuente en AWS S3 con Python

## Objetivo
Desarrollar un script en Python para obtener y perfilar archivos CSV y JSON almacenados en Amazon S3 utilizando Boto3 y Pandas.

## Tecnologías utilizadas
- Python 3.12
- Amazon S3
- Boto3
- Pandas
- Visual Studio Code

## Archivos procesados
- raw/transacciones.csv
- raw/logs_m2m.json

## Funcionamiento
El programa obtiene archivos desde AWS S3 mediante Boto3 y los procesa directamente en memoria.

Para CSV utiliza io.BytesIO y pandas.read_csv().

Para JSON utiliza json.loads() y pandas.json_normalize().

El perfilamiento incluye dimensiones, tipos de datos, valores nulos, estadísticas descriptivas y validación de fechas.

## Resultados
- CSV: 10 registros, 6 columnas y 0 valores nulos.
- JSON: 5 registros, 6 columnas y 2 valores nulos.
- Ambos archivos se procesaron correctamente.

## Instalación
Crear un entorno virtual e instalar las dependencias:

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

## Credenciales AWS Academy
Se requieren las credenciales obtenidas desde AWS Details > AWS CLI.

Las credenciales reales se mantienen fuera del repositorio.

## Ejecución
python perfilamiento_s3.py

## Seguridad
No se publican credenciales, claves privadas ni entornos virtuales.
