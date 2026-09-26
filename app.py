import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def extract_data(folder_path):

    folder = Path(folder_path)

    files = folder.glob("*.csv")

    data = []

    for file in files:

        df = pd.read_csv(file)

        data.append(df)

    if not data:
        raise ValueError("No CSV files found!")

    return pd.concat(data, ignore_index=True)



def transform_data(df):

  
    df = df.dropna(how="all")

    
    df = df.drop_duplicates()

   
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

   
    if "name" in df.columns:
        df["name"] = (
            df["name"]
            .astype(str)
            .str.strip()
            .str.title()
        )

   
    if "email" in df.columns:
        df["email"] = (
            df["email"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

  
    if "city" in df.columns:
        df["city"] = (
            df["city"]
            .astype(str)
            .str.strip()
            .str.title()
        )

  
    if "age" in df.columns:
        df["age"] = pd.to_numeric(
            df["age"],
            errors="coerce"
        )

    return df.reset_index(drop=True)




def load_data(df):

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username="admin",
        password="Admin@12345",
        host="localhost",
        port=3306,
        database="etlpipeline"
    )

    engine = create_engine(connection_url)

    df.to_sql(
        "customers",
        con=engine,
        if_exists="append",
        index=False
    )

    print("Data loaded successfully!")


def main():
    df = extract_data("uploads")

    print("Extracted:")
    print(df)

    df = transform_data(df)

    print("\nTransformed:")
    print(df)

    load_data(df)



if __name__ == "__main__":
    main()

