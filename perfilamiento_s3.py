
import boto3
import pandas as pd
import json
import io
import os

from botocore.exceptions import ClientError, BotoCoreError

# ==========================================
# PRÁCTICA 1: PERFILAMIENTO MULTI-FUENTE S3
# ==========================================
BUCKET_NAME = "aws-academy-datacenter-bucket-23-02-003"
REGION = "us-east-1"

try:
    from conexion_s3_privada import (
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_SESSION_TOKEN
    )
except ImportError:
    # Alternativa para ejecutar desde GitHub
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

if not all([
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN
]):
    raise RuntimeError(
        "Configura las tres credenciales de AWS Academy."
    )


# Conexión explícita con AWS Academy
s3_client = boto3.client(
    "s3",
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)


def cargar_y_perfilar_s3(file_key, is_json=False):
    """
    Lee un archivo CSV o JSON directamente desde AWS S3
    en memoria y realiza su perfilamiento con Pandas.
    """

    print("\n" + "=" * 55)
    print(f"PROCESANDO ARCHIVO: {file_key}")
    print("=" * 55)

    try:
        # Descargar contenido a memoria
        response = s3_client.get_object(
            Bucket=BUCKET_NAME,
            Key=file_key
        )

        body = response["Body"].read()

        # Interpretar según el formato
        if is_json:
            datos_json = json.loads(body.decode("utf-8"))
            df = pd.json_normalize(datos_json)
        else:
            df = pd.read_csv(io.BytesIO(body))

        # Dimensiones
        print("\n1. DIMENSIONES DEL DATASET")
        print(f"Filas: {df.shape[0]}")
        print(f"Columnas: {df.shape[1]}")

        # Tipos de datos
        print("\n2. TIPOS DE DATOS")
        print(df.dtypes.to_string())

        # Valores faltantes
        print("\n3. VALORES NULOS POR COLUMNA")
        print(df.isnull().sum().to_string())

        # Estadísticas
        print("\n4. ESTADÍSTICAS DESCRIPTIVAS")
        numericas = df.select_dtypes(include="number")

        if not numericas.empty:
            print(numericas.describe().T.to_string())
        else:
            print("No hay columnas numéricas.")

        # Vista previa
        print("\n5. PRIMEROS REGISTROS")
        print(df.head().to_string(index=False))

        # Comprobar columna de fechas del CSV
        if "fecha" in df.columns:
            fechas = pd.to_datetime(
                df["fecha"],
                errors="coerce"
            )
            print("\n6. VALIDACIÓN DE FECHAS")
            print("Fechas inválidas:", fechas.isna().sum())

        print("\nPerfilamiento completado correctamente.")

        return df

    except ClientError as error:
        codigo = error.response["Error"]["Code"]
        print("Error de AWS S3:", codigo)

    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        print("Error al interpretar el JSON:", error)

    except pd.errors.ParserError as error:
        print("Error al interpretar el CSV:", error)

    except BotoCoreError as error:
        print("Error de comunicación con AWS:", error)

    return None


if __name__ == "__main__":

    print("PRÁCTICA 1 - INGESTA MULTI-FUENTE EN AWS S3")

    df_transacciones = cargar_y_perfilar_s3(
        "raw/transacciones.csv"
    )

    df_logs = cargar_y_perfilar_s3(
        "raw/logs_m2m.json",
        is_json=True
    )

    if df_transacciones is not None and df_logs is not None:
        print("\n¡AMBOS DATASETS PROCESADOS CORRECTAMENTE!")
