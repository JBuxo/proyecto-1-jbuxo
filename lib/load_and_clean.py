import polars as pl
import pandas as pd

def load_and_clean(path: str) -> pd.DataFrame:
    """
    Load and clean a CSV using Polars and convert to Pandas.
    """
    # Load CSV in Polars
    df_polars = pl.read_csv(path)

    # Normalize column names
    df_polars = df_polars.rename({col: col.strip().replace(" ", "_").lower() for col in df_polars.columns})

    # Convert datetime columns
    for col in ["start_time", "end_time"]:
        if col in df_polars.columns:
            df_polars = df_polars.with_columns(pl.col(col).str.strptime(pl.Datetime, strict=False))

    # Convert distance(mi) -> km
    if "distance(mi)" in df_polars.columns:
        df_polars = df_polars.with_columns(
            (pl.col("distance(mi)") * 1.60934).alias("distancia_afectada_km")
        )

    # Clean zipcodes
    if "zipcode" in df_polars.columns:
        df_polars = df_polars.with_columns(
            pl.col("zipcode").cast(pl.Utf8).str.split("-").list.get(0).alias("zipcode")
        )

    # Drop unused columns
    drop_cols = [
        'source','distance(mi)','timezone','airport_code',
        'weather_timestamp','civil_twilight','nautical_twilight',
        'astronomical_twilight','country'
    ]
    df_polars = df_polars.drop([c for c in drop_cols if c in df_polars.columns])

    # Convert Polars DataFrame to Pandas manually (PyArrow-free)
    data = {col: df_polars[col].to_list() for col in df_polars.columns}
    df_pandas = pd.DataFrame(data)

    # Optimize memory usage
    for col in df_pandas.select_dtypes(include="object").columns:
        df_pandas[col] = df_pandas[col].astype("category")
    for col in df_pandas.select_dtypes(include="float64").columns:
        df_pandas[col] = df_pandas[col].astype("float32")
    for col in df_pandas.select_dtypes(include="int64").columns:
        df_pandas[col] = df_pandas[col].astype("int32")

    return df_pandas
