"""
Extracción de datos farmacológicos mediante la API de openFDA.

Este script realiza peticiones GET al endpoint Drug Labeling de openFDA,
transforma los registros obtenidos y los almacena en formato JSON.

La API Key se obtiene desde una variable de entorno definida en el archivo .env.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.fda.gov/drug/label.json"

OUTPUT_FILE = "data/data_extracted.json"

TARGET_RECORDS = 15000
LIMIT = 1000

# Funcion de manejo de campos
def get_first_value(dictionary, field):
    """Obtiene el primer valor de un campo."""
    
    value = dictionary.get(field)
    
    if isinstance(value, list):
        return value[0] if value else None
    
    return value

#Funcion de transformacion 
def transform_record(record):
    """Transforma un registro de openFDA en una estructura plana."""
    
    openfda = record.get("openfda", {})
    
    transformed = {
        # Identificación del producto
        "brand_name": get_first_value(openfda, "brand_name"),
        "generic_name": get_first_value(openfda, "generic_name"),
        "manufacturer_name": get_first_value(openfda, "manufacturer_name"),
        "product_type": get_first_value(openfda, "product_type"),
        "route": get_first_value(openfda, "route"),
        "dosage_form": get_first_value(openfda, "dosage_form"),
        "substance_name": get_first_value(openfda, "substance_name"),
        "product_ndc": get_first_value(openfda, "product_ndc"),

        # Información farmacológica
        "clinical_pharmacology": get_first_value(
            record, "clinical_pharmacology"
        ),
        "pharmacokinetics": get_first_value(
            record, "pharmacokinetics"
        ),
        "pharmacodynamics": get_first_value(
            record, "pharmacodynamics"
        ),
        "pharmacogenomics": get_first_value(
            record, "pharmacogenomics"
        ),
        "mechanism_of_action": get_first_value(
            record, "mechanism_of_action"
        ),

        # Información clínica y de seguridad
        "indications_and_usage": get_first_value(
            record, "indications_and_usage"
        ),
        "contraindications": get_first_value(
            record, "contraindications"
        ),
        "warnings": get_first_value(record, "warnings"),
        "precautions": get_first_value(record, "precautions"),
        "adverse_reactions": get_first_value(
            record, "adverse_reactions"
        ),
        "drug_interactions": get_first_value(
            record, "drug_interactions"
        ),
        "dosage_and_administration": get_first_value(
            record, "dosage_and_administration"
        ),
        "clinical_studies": get_first_value(
            record, "clinical_studies"
        ),

        # Identificadores y metadatos
        "set_id": record.get("set_id"),
        "id": record.get("id"),
        "effective_time": record.get("effective_time")
    }
    
    return transformed

# Funcion de extraccion y paginacion
def extract_data():
    """Extrae registros de openFDA mediante paginación."""
    
    if not API_KEY:
        raise ValueError(
            "No se encontró API_KEY. Verificá el archivo .env."
        )

    records = []
    skip = 0

    search_query = (
        "pharmacokinetics:[* TO *] "
        "AND pharmacodynamics:[* TO *]"
    )

    while len(records) < TARGET_RECORDS:
        params = {
            "api_key": API_KEY,
            "search": search_query,
            "limit": LIMIT,
            "skip": skip
        }

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=30
            )

            if response.status_code != 200:
                print(
                    f"Error HTTP {response.status_code}: "
                    f"{response.text[:300]}"
                )
                break

            data = response.json()
            batch = data.get("results", [])

            if not batch:
                print("No se encontraron más registros.")
                break

            transformed_batch = [
                transform_record(record)
                for record in batch
            ]

            records.extend(transformed_batch)

            print(
                f"Registros recuperados: "
                f"{len(records)}/{TARGET_RECORDS}"
            )

            skip += LIMIT

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con la API: {e}")
            break

        except ValueError as e:
            print(f"Error al procesar la respuesta JSON: {e}")
            break

    return records[:TARGET_RECORDS]

# Ejecucion y guardado del archivo JSON
if __name__ == "__main__":
    
    print("Iniciando extracción desde openFDA...")
    
    records = extract_data()

    if records:
        os.makedirs("data", exist_ok=True)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(
                records,
                file,
                ensure_ascii=False,
                indent=2
            )

        print("\nExtracción finalizada.")
        print(f"Registros guardados: {len(records)}")
        print(f"Variables por registro: {len(records[0])}")
        print(f"Archivo generado: {OUTPUT_FILE}")

    else:
        print("No se obtuvieron registros.")
