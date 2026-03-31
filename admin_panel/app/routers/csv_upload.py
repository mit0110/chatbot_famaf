from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.question import Question
from app.utils import (
    ensure_category_exists,
    get_or_create_answer,
)
from app.utils_csv import parse_csv_file
from app.routers.admin import _cleanup_orphan_answer, _cleanup_orphan_category
from io import StringIO
from typing import List
import csv

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ============== PARSERS ESPECÍFICOS ==============
def parse_csv_fechas_examen(csv_content: str, cantidad_fechas: int, cargar_especialidades: bool) -> tuple[bool, list, str]:
    """
    Parser para Opción 1: Fechas Examen
    
    Si cargar_especialidades=True:
      Espera: titulo, especialidad, fecha1 (o "fecha 1"), fecha2 (o "fecha 2"), fecha3 (o "fecha 3"), y fecha4 (o "fecha 4") si cantidad_fechas=4
    Si cargar_especialidades=False:
      Espera: titulo, fecha1 (o "fecha 1"), fecha2 (o "fecha 2"), fecha3 (o "fecha 3"), y fecha4 (o "fecha 4") si cantidad_fechas=4
    
    Retorna: (success: bool, data: list[dict], message: str)
    """
    try:
        lines = csv_content.strip().split('\n')
        if not lines:
            return False, [], "Archivo CSV vacío"
        
        # Parsear headers
        reader = csv.DictReader(lines)
        if reader.fieldnames is None:
            return False, [], "No se pudieron parsear los headers"
        
        # Normalizar nombres de columnas (minúsculas, sin espacios)
        # Esto permite aceptar "fecha 1", "fecha1", "Fecha 1", etc.
        normalized_field_mapping = {field.strip().lower().replace(' ', ''): field for field in reader.fieldnames}
        fieldnames_normalized = list(normalized_field_mapping.keys())
        
        # Columnas requeridas en orden
        required_fields = ['titulo']
        if cargar_especialidades:
            required_fields.append('especialidad')
        
        required_fields.extend(['fecha1', 'fecha2', 'fecha3'])
        if cantidad_fechas == 4:
            required_fields.append('fecha4')
        
        missing_fields = [field for field in required_fields if field not in fieldnames_normalized]
        
        if missing_fields:
            return False, [], f"Columnas requeridas: {', '.join(required_fields)}"
        
        # Extraer datos con normalización de claves (removiendo espacios)
        data = []
        for row in reader:
            normalized_row = {k.strip().lower().replace(' ', ''): v for k, v in row.items()}
            row_data = {
                'titulo': normalized_row.get('titulo', '').strip(),
                'fecha1': normalized_row.get('fecha1', '').strip(),
                'fecha2': normalized_row.get('fecha2', '').strip(),
                'fecha3': normalized_row.get('fecha3', '').strip(),
            }
            
            if cantidad_fechas == 4:
                row_data['fecha4'] = normalized_row.get('fecha4', '').strip()
            
            # Si se cargan especialidades, es requerida
            if cargar_especialidades:
                row_data['especialidad'] = normalized_row.get('especialidad', '').strip()
            
            data.append(row_data)
        
        return True, data, "CSV parseado correctamente"
    
    except Exception as e:
        return False, [], f"Error parseando CSV: {str(e)}"


# ============== HELPER FUNCTION ==============
async def _insert_questions_batch(questions_data: List[dict]):
    """
    Función reutilizable para insertar un lote de preguntas.
    Espera datos en formato: [{"question": str, "answer": str, "category": str}, ...]
    
    Comportamiento:
    - Si la pregunta no existe: la crea
    - Si la pregunta existe:
      - Si el contenido de la respuesta es IGUAL: no hace nada, deja tal cual
      - Si el contenido de la respuesta es DIFERENTE: actualiza y limpia respuestas huérfanas
    
    Retorna: {"created": int, "errors": list}
    """
    created_count = 0
    updated_counter = 0
    error_details = []

    for item in questions_data:
        try:
            new_category = await ensure_category_exists(item["category"])
            new_answer = await get_or_create_answer(item["answer"])

            existing_q = await Question.find_one(
                Question.content == item["question"]
            )
            
            if existing_q:
                # Pregunta existe: verificar si la respuesta es igual en contenido
                # Fetch el Link para obtener el documento Answer real
                old_answer = await existing_q.answer.fetch()
                
                # Comparar contenido de respuestas
                old_answer_content = old_answer.content 
                old_category = existing_q.category  
                new_answer_content = new_answer.content 

                if old_answer_content != new_answer_content or old_category != new_category:
                    # Actualizar pregunta con nueva respuesta y categoría
                    
                    answer_change = old_answer_content != new_answer_content
                    category_change = old_category != new_category

                    if answer_change:
                        # Si la respuesta cambió, asignar la nueva respuesta
                        existing_q.answer = new_answer

                    if category_change:
                        existing_q.category = new_category
                    
                    await existing_q.save()
                    
                    # AHORA limpiar los documentos huérfanos
                    if answer_change:
                        await _cleanup_orphan_answer(old_answer)
                    
                    if category_change:
                        await _cleanup_orphan_category(old_category)
                    
                    updated_counter += 1
            else:
                # Pregunta no existe: crearla
                await Question(
                    content=item["question"],
                    category=new_category,
                    answer=new_answer,
                ).insert()
                created_count += 1

        except Exception as e:
            error_details.append(f"Error procesando pregunta: {str(e)}")

    return {"created": created_count, "updated": updated_counter, "errors": error_details}


# ============== SELECTOR DE TIPOS ==============
@router.get("/upload-csv", response_class=HTMLResponse)
async def csv_upload_selector(request: Request):
    return templates.TemplateResponse("csv_type_selector.html", {"request": request})


# ============== OPCIÓN 1: FECHAS EXAMEN ==============
@router.get("/upload-csv-fechas-examen", response_class=HTMLResponse)
async def csv_upload_form_fechas_examen(request: Request):
    return templates.TemplateResponse(
        "csv_upload_exams.html", 
        {"request": request, "csv_endpoint": "/admin/csv/upload-csv-fechas-examen"}
    )


@router.post("/upload-csv-fechas-examen")
async def upload_csv_fechas_examen(
    file: UploadFile = File(...), 
    month: str = Form(...), 
    year: str = Form(...),
    cantidadFechas: str = Form(...),
    cargarEspecialidades: str = Form(...)
):
    if not file.filename.endswith(".csv"):
        return {"status": "error", "message": "El archivo debe ser un CSV"}

    # Validar año (debe ser 4 dígitos)
    try:
        year_int = int(year)
        if year_int < 1000 or year_int > 9999:
            return {"status": "error", "message": "El año debe ser un número de 4 dígitos"}
    except ValueError:
        return {"status": "error", "message": "El año debe ser un número válido"}
    
    # Validar etapa
    if month not in ["Julio", "Diciembre-Febrero"]:
        return {"status": "error", "message": "Etapa inválida"}
    
    # Validar cantidad de fechas
    try:
        cantidad_fechas_int = int(cantidadFechas)
        if cantidad_fechas_int not in [3, 4]:
            return {"status": "error", "message": "La cantidad de fechas debe ser 3 o 4"}
    except ValueError:
        return {"status": "error", "message": "La cantidad de fechas debe ser un número"}
    
    # Convertir cargarEspecialidades a boolean
    cargar_esp = cargarEspecialidades.lower() == 'true'

    try:
        contents = await file.read()
        csv_content = contents.decode("utf-8")
        
        # Parsear con parser específico para opción 1, pasando la cantidad de fechas y si cargar especialidades
        success, data, message = parse_csv_fechas_examen(csv_content, cantidad_fechas_int, cargar_esp)
        
        if not success:
            return {"status": "error", "message": message}
        
        # Crear la categoría una sola vez antes de procesar los datos
        category_name = await ensure_category_exists(f"Fechas Examen {month} - {year}")
        
        # Procesar cada fila y preparar datos para insertar
        questions_to_insert = []
        error_details = []
        
        for row in data:
            titulo = row['titulo']
            fecha1 = row['fecha1']
            fecha2 = row['fecha2']
            fecha3 = row['fecha3']
            
            # Construir las fechas dinámicamente según cantidad
            fechas = [fecha1, fecha2, fecha3]
            if cantidad_fechas_int == 4:
                fecha4 = row.get('fecha4', '')
                if not fecha4:
                    return {"status": "error", "message": f"Fila incompleta: falta fecha4 en '{titulo}'"}
                fechas.append(fecha4)

            # Validar que no estén vacíos
            campos_validar = [titulo] + fechas
            if cargar_esp:
                especialidad = row.get('especialidad', '')
                campos_validar.append(especialidad)
            
            if not all(campos_validar):
                error_details.append(f"Fila incompleta: {titulo}")
                return {"status": "error", "message": f"Fila incompleta: {titulo}"}
            
            # Construir el texto de fechas como lista MD
            fechas_texto = "\n".join([f"- Fecha {i+1}: {f}" for i, f in enumerate(fechas)])

            # Especialidad (con salto previo)
            especialidad_texto = ""
            if cargar_esp and 'especialidad' in row:
                especialidad_texto = f"\n\n *{row['especialidad']}*"

            # Texto final bien formateado
            answer_text = (
                f"Las fechas de examen para la materia *{titulo}* {especialidad_texto} en {month} - {year} son:\n\n"
                f"{fechas_texto}"
            )
            
            # Preparar datos en formato para insertar
            questions_to_insert.append({
                "question": f"¿Cuáles son las fechas de examen para {titulo}?",
                "answer": answer_text,
                "category": category_name
            })
        
        if error_details:
            return {
                "status": "error",
                "message": f"Errores de validación: {'; '.join(error_details[:5])}",
                "errors": error_details
            }
        
        # Insertar todas las preguntas
        result = await _insert_questions_batch(questions_to_insert)
        
        # Construir mensaje con creadas y actualizadas
        msg = f"Se importaron {result['created']} nuevas fechas de examen exitosamente \n"
        if result.get("updated", 0) > 0:
            msg += f" y se actualizaron {result['updated']} \n"
        msg += f" ({cantidad_fechas_int} fechas por materia, Etapa: {month}, Año: {year})"
        if result["errors"]:
            msg += f". Errores: {'; '.join(result['errors'][:5])}"
        
        return {
            "status": "success",
            "message": msg,
            "created": result["created"],
            "updated": result.get("updated", 0),
            "errors": result["errors"],
        }

    except Exception as e:
        return {"status": "error", "message": f"Error al procesar archivo: {str(e)}"}


# ============== OPCIÓN 2 ==============
@router.get("/upload-csv-qa", response_class=HTMLResponse)
async def csv_upload_form_qa(request: Request):
    return templates.TemplateResponse(
        "csv_upload_qa.html", 
        {"request": request, "csv_endpoint": "/admin/csv/upload-csv-qa"}
    )


@router.post("/upload-csv-qa")
async def upload_csv_qa(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"status": "error", "message": "El archivo debe ser un CSV"}

    try:
        contents = await file.read()
        text_file = StringIO(contents.decode("utf-8"))
        success, data, message = parse_csv_file(text_file)

        if not success:
            return {"status": "error", "message": message}

        result = await _insert_questions_batch(data)
        
        # Construir mensaje con creadas y actualizadas
        msg = f"Se importaron {result['created']} preguntas exitosamente"
        if result.get("updated", 0) > 0:
            msg += f" y se actualizaron {result['updated']}"
        if result["errors"]:
            msg += f". Errores: {'; '.join(result['errors'][:5])}"

        return {
            "status": "success",
            "message": msg,
            "created": result["created"],
            "updated": result.get("updated", 0),
            "errors": result["errors"],
        }

    except Exception as e:
        return {"status": "error", "message": f"Error al procesar archivo: {str(e)}"}

