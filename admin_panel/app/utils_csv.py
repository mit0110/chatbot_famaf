import csv
from io import TextIOWrapper
from typing import Tuple, List, Dict


def parse_csv_file(file_content: TextIOWrapper) -> Tuple[bool, List[Dict], str]:
    """
    Parse CSV file and validate structure.
    
    Returns:
        Tuple with (success: bool, data: List[Dict], message: str)
    """
    try:
        # Reset file pointer to beginning
        file_content.seek(0)
        
        # Read CSV
        reader = csv.DictReader(file_content)
        
        # Check if required columns exist
        if reader.fieldnames is None:
            return False, [], "El archivo CSV está vacío"
        
        required_columns = {'Preguntas', 'Respuesta', 'Categoría'}
        file_columns = set(reader.fieldnames)
        
        if not required_columns.issubset(file_columns):
            missing = required_columns - file_columns
            return False, [], f"Columnas faltantes: {', '.join(missing)}"
        
        # Read data
        data = []
        for row_num, row in enumerate(reader, start=2):  # start at 2 because row 1 is header
            # Validate required fields
            if not row.get('Preguntas', '').strip():
                return False, [], f"Fila {row_num}: La columna 'Preguntas' está vacía"
            
            if not row.get('Respuesta', '').strip():
                return False, [], f"Fila {row_num}: La columna 'Respuesta' está vacía"
            
            if not row.get('Categoría', '').strip():
                return False, [], f"Fila {row_num}: La columna 'Categoría' está vacía"
            
            data.append({
                'question': row['Preguntas'].strip(),
                'answer': row['Respuesta'].strip(),
                'category': row['Categoría'].strip()
            })
        
        if not data:
            return False, [], "El archivo CSV no contiene datos"
        
        return True, data, f"Se leyeron {len(data)} filas correctamente"
    
    except Exception as e:
        return False, [], f"Error al procesar el CSV: {str(e)}"
