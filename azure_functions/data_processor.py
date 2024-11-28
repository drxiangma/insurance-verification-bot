import pandas as pd
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def read_excel(file_path: str) -> List[Dict[str, Any]]:
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            logger.warning(f"Empty Excel file: {file_path}")
            return []
        return df.to_dict("records")
    except Exception as e:
        logger.error(f"Error reading Excel file {file_path}: {str(e)}")
        raise

def write_excel(data: List[Dict[str, Any]], file_path: str) -> None:
    try:
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        logger.info(f"Successfully wrote data to {file_path}")
    except Exception as e:
        logger.error(f"Error writing Excel file {file_path}: {str(e)}")
        raise
