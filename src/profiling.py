from __future__ import  annotations
import pandas as pd
from datetime import datetime
from typing import Any
from decorators.logger import logger
import json 
from pathlib import Path

class data_profilier:
    def __init__(self):
        self. logger = logger

    def profile(
        self,
        data_entity: str,
        records: list[dict[str, Any]],
        id_field: str
    ):
        self.logger.info(f"start profiling data [{data_entity}]")

        if not records:
            self.logger.warning(f"No data foud in {data_entity}")

            return {
                "data_entity": data_entity,
            "total_records": 0
            }
        
        df = pd.DataFrame(records)

        report = {
            "entity": data_entity,
            "generated_at": datetime.utcnow().isoformat(),

            # Basic Information
            "total_records": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),

            # Missing Values
            "missing_values": df.isnull().sum().to_dict(),

            # Duplicate Rows
            "duplicate_records": int(
                df.duplicated().sum()
            ),

            # Duplicate Primary Key
            "duplicate_ids": (
                int(df[id_field].duplicated().sum())
                if id_field in df.columns
                else None
            ),

            # Unique Values
            "unique_values": {
                column: int(df[column].nunique())
                for column in df.columns
            }
        }

        numeric_columns = df.select_dtypes(
            include=["int64", "float64"]
        )
        if not numeric_columns.empty:
            report["statistics"]= (
                    numeric_columns.describe().to_dict()
            ) 
        
        self.logger.info("Profiling prosses is Finshed")

        return report   

    def save_profiling(
        self,
        data_entity: str,
        report: dict
    ):
        report_dir = Path("report")
        report_dir.mkdir(exist_ok= True)

        report_file = report_dir / f"{data_entity}_profiling_data.json"

        with open(report_file, "w", encoding="utf_8") as file:
            json.dump(report, file, indent=4, ensure_ascii=False, default=str)
        self.logger.info(f"data profiling saved ----> {report_file}")

