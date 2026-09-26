import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# ------------------------------------------------
# EXTRACT
# ------------------------------------------------

def extract_data(folder_path):
    """
    Read all CSV files from the specified folder
    and combine them into one DataFrame.
    """

    folder = Path(folder_path)

    files = list(folder.glob("*.csv"))

    if not files:
        raise ValueError("No CSV files found!")

    data = []

    for file in files:

        df = pd.read_csv(file)

        data.append(df)

    return pd.concat(
        data,
        ignore_index=True
    )


# ------------------------------------------------
# TRANSFORM
# ------------------------------------------------

def transform_data(df):

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # -------------------------
    # CUSTOMER ID
    # -------------------------

    if "customer_id" in df.columns:

        df["customer_id"] = pd.to_numeric(
            df["customer_id"],
            errors="coerce"
        )

        # Remove records with invalid customer_id
        df = df.dropna(subset=["customer_id"])

        df["customer_id"] = df["customer_id"].astype(int)

    # -------------------------
    # NAME
    # -------------------------

    if "name" in df.columns:

        df["name"] = (
            df["name"]
            .astype("string")
            .str.strip()
            .str.title()
        )

    # -------------------------
    # EMAIL
    # -------------------------

    if "email" in df.columns:

        df["email"] = (
            df["email"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    # -------------------------
    # PHONE
    # -------------------------

    if "phone" in df.columns:

        df["phone"] = (
            df["phone"]
            .astype("string")
            .str.strip()
        )

    # -------------------------
    # CITY
    # -------------------------

    if "city" in df.columns:

        df["city"] = (
            df["city"]
            .astype("string")
            .str.strip()
            .str.title()
        )

    # -------------------------
    # STATE
    # -------------------------

    if "state" in df.columns:

        df["state"] = (
            df["state"]
            .astype("string")
            .str.strip()
            .str.title()
        )

    # -------------------------
    # AGE
    # -------------------------

    if "age" in df.columns:

        df["age"] = pd.to_numeric(
            df["age"],
            errors="coerce"
        )

        # Invalid ages become NULL
        df.loc[
            ~df["age"].between(1, 120),
            "age"
        ] = None

    # -------------------------
    # SIGNUP DATE
    # -------------------------

    if "signup_date" in df.columns:

        df["signup_date"] = pd.to_datetime(
            df["signup_date"],
            errors="coerce"
        )

    # -------------------------
    # STATUS
    # -------------------------

    if "status" in df.columns:

        df["status"] = (
            df["status"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    # -------------------------
    # NOTES
    # -------------------------

    if "notes" in df.columns:

        df["notes"] = (
            df["notes"]
            .astype("string")
            .str.strip()
        )

    return df.reset_index(drop=True)


# ------------------------------------------------
# LOAD
# ------------------------------------------------

def get_database_engine():

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(connection_url)

def load_data(df):
    """
    Load transformed DataFrame
    into MySQL customers table.
    """

    engine = get_database_engine()

    df.to_sql(

        "customers",

        con=engine,

        if_exists="append",

        index=False
    )

    engine.dispose()

    return True