from fastapi import FastAPI,UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from etl import extract_data,transform_data,load_data



# ------------------------------------------------
# FASTAPI APP
# ------------------------------------------------

app = FastAPI(

    title="ETL Pipeline API",

    description=(
        "CSV ETL Pipeline using "
        "FastAPI, Pandas and MySQL"
    ),

    version="1.0.0"
)


# ------------------------------------------------
# CORS
# ------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ------------------------------------------------
# UPLOAD DIRECTORY
# ------------------------------------------------

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# ------------------------------------------------
# TEMPORARY PIPELINE DATA
# ------------------------------------------------

pipeline_data = {

    "raw": None,

    "transformed": None
}


# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------

@app.get("/")
def root():

    return {

        "success": True,

        "message": (
            "ETL Pipeline API is running"
        )
    }


# ------------------------------------------------
# UPLOAD / EXTRACT
# ------------------------------------------------

@app.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...)
):

    try:

        uploaded_files = []

        for file in files:

            if not file.filename:
                continue

            if not file.filename.lower().endswith(
                ".csv"
            ):
                continue

            file_path = os.path.join(
                UPLOAD_DIR,
                file.filename
            )

            with open(
                file_path,
                "wb"
            ) as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            uploaded_files.append(
                file.filename
            )

        if not uploaded_files:

            raise HTTPException(

                status_code=400,

                detail=(
                    "No CSV files uploaded"
                )
            )

        # Extract
        df = extract_data(
            UPLOAD_DIR
        )

        pipeline_data[
            "raw"
        ] = df

        return {

            "success": True,

            "message": (
                "Files uploaded and "
                "extracted successfully"
            ),

            "files": uploaded_files,

            "rows": len(df),

            "columns": list(
                df.columns
            ),

            "preview": (
                df.head(20)
                .fillna("")
                .to_dict(
                    orient="records"
                )
            )
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


# ------------------------------------------------
# TRANSFORM
# ------------------------------------------------

@app.post("/transform")
def transform():

    try:

        if pipeline_data["raw"] is None:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Please upload CSV "
                    "files first"
                )
            )

        raw_df = pipeline_data[
            "raw"
        ]

        before_rows = len(
            raw_df
        )

        transformed_df = transform_data(
            raw_df.copy()
        )

        after_rows = len(
            transformed_df
        )

        pipeline_data[
            "transformed"
        ] = transformed_df

        return {

            "success": True,

            "message": (
                "Data transformed "
                "successfully"
            ),

            "before_rows": before_rows,

            "after_rows": after_rows,

            "removed_rows": (
                before_rows -
                after_rows
            ),

            "columns": list(
                transformed_df.columns
            ),

            "preview": (
                transformed_df
                .head(20)
                .fillna("")
                .to_dict(
                    orient="records"
                )
            )
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


# ------------------------------------------------
# LOAD
# ------------------------------------------------

@app.post("/load")
def load():

    try:

        if (
            pipeline_data[
                "transformed"
            ] is None
        ):

            raise HTTPException(

                status_code=400,

                detail=(
                    "Please transform "
                    "data first"
                )
            )

        df = pipeline_data[
            "transformed"
        ]

        load_data(df)

        return {

            "success": True,

            "message": (
                "Data loaded successfully "
                "into MySQL"
            ),

            "rows_loaded": len(df),

            "table": "customers"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


# ------------------------------------------------
# COMPLETE ETL PIPELINE
# ------------------------------------------------

@app.post("/run")
def run_pipeline():

    try:

        if pipeline_data["raw"] is None:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Please upload CSV "
                    "files first"
                )
            )

        # Transform
        transformed_df = transform_data(

            pipeline_data[
                "raw"
            ].copy()
        )

        pipeline_data[
            "transformed"
        ] = transformed_df

        # Load
        load_data(
            transformed_df
        )

        return {

            "success": True,

            "message": (
                "ETL pipeline completed "
                "successfully"
            ),

            "extracted_rows": len(
                pipeline_data["raw"]
            ),

            "transformed_rows": len(
                transformed_df
            ),

            "loaded_rows": len(
                transformed_df
            ),

            "columns": list(
                transformed_df.columns
            ),

            "preview": (
                transformed_df
                .head(20)
                .fillna("")
                .to_dict(
                    orient="records"
                )
            )
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )