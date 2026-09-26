# OpenFDA Pharmacology Data Pipeline

Pipeline de extracción, transformación y almacenamiento de datos farmacológicos utilizando la API pública **openFDA Drug Labeling**.

El proyecto fue desarrollado como parte de una práctica de **Data Science II**, aplicando conceptos de consumo de APIs, manejo seguro de credenciales, transformación básica de datos y almacenamiento estructurado.

---

## 🎯 Objetivo

Construir un pipeline reproducible capaz de:

* Conectarse a una API pública mediante peticiones HTTP GET.
* Gestionar de forma segura una API Key mediante variables de entorno.
* Extraer información farmacológica y clínica de etiquetas de medicamentos.
* Transformar la respuesta JSON en una estructura más simple y consistente.
* Almacenar los datos en formato JSON.
* Implementar manejo básico de errores y paginación.

Los datos seleccionados incluyen información relacionada con **farmacocinética, farmacodinamia, farmacogenómica, mecanismo de acción, indicaciones, interacciones y seguridad**.

---

## 🔬 Fuente de datos

La fuente utilizada es **openFDA Drug Labeling**, una API de la U.S. Food and Drug Administration (FDA).

Endpoint utilizado:

`https://api.fda.gov/drug/label.json`

La extracción se restringió a registros que contienen información tanto de:

* `pharmacokinetics`
* `pharmacodynamics`

Esto permitió trabajar con un conjunto de datos orientado a información farmacológica, manteniendo además variables clínicas y de seguridad relevantes para posibles análisis posteriores.

---

## 📊 Datos extraídos

La extracción final contiene:

* **15.000 registros**
* **24 variables por registro**

Entre las principales variables se encuentran:

| Categoría           | Variables                                                                                                  |
| ------------------- | ---------------------------------------------------------------------------------------------------------- |
| Identificación      | `brand_name`, `generic_name`, `manufacturer_name`, `product_ndc`                                           |
| Características     | `route`, `dosage_form`, `substance_name`                                                                   |
| Farmacología        | `clinical_pharmacology`, `pharmacokinetics`, `pharmacodynamics`, `pharmacogenomics`, `mechanism_of_action` |
| Clínica y seguridad | `indications_and_usage`, `contraindications`, `warnings`, `adverse_reactions`, `drug_interactions`         |
| Metadatos           | `set_id`, `id`, `effective_time`                                                                           |

> Los registros de Drug Labeling corresponden a etiquetas regulatorias y no necesariamente representan medicamentos únicos. Por lo tanto, la cantidad de registros no equivale directamente a la cantidad de principios activos diferentes.

---

## 💾 ¿Por qué JSON?

Se eligió **JSON como formato principal de almacenamiento** porque es el formato nativo de respuesta de la API y permite conservar fácilmente la estructura semiestructurada de los registros.

Además, varios campos de openFDA pueden contener listas o estructuras variables. JSON permite conservar esta información sin imponer desde el comienzo un esquema tabular rígido.

El dataset completo ocupa aproximadamente **739 MB**, por lo que se mantiene localmente y no se incluye en el repositorio.

Para facilitar la exploración, el repositorio contiene una muestra reducida:

```text
data/sample_data.json
```

---

## 🔄 Pipeline

```text
openFDA API
     │
     ▼
HTTP GET requests
     │
     ▼
Paginación
     │
     ▼
Transformación de registros
     │
     ▼
JSON estructurado
     │
     ├── data_extracted.json (local)
     │
     └── sample_data.json (GitHub)
```

El script `src/extract_data.py` automatiza el proceso de extracción y transformación.

---

## 🔐 Seguridad

La A
