import polars as pl
from datetime import datetime

from bshtmlwix import records_w
from bswoocomerce import results_w
from bswp import results_ch

def build_dataframe():
    all_records = []
    all_records.extend(records_w())
    all_records.extend(results_w())
    all_records.extend(results_ch())
    return pl.DataFrame(all_records)

if __name__ == "__main__":
    df = build_dataframe()

    # Asegurar que category_url exista (sin modificar valores)
    df = df.with_columns(
        pl.col("category_url").fill_null("").alias("category_url")
        if "category_url" in df.columns
        else pl.lit("").alias("category_url")
    )

    # Aplanar raw_text si es lista (única manipulación necesaria para CSV)
    if df.schema["raw_text"] == pl.List(pl.Utf8):
        df = df.with_columns(
            pl.col("raw_text").list.join(" ").alias("raw_text")
        )

    # Agregar timestamp sin tocar los datos
    df = df.with_columns(
        pl.lit(datetime.now().isoformat()).alias("updated_at")
    )

    print(df.head())

    df.write_csv("dataset.csv")

    print("\nCSV creado exitosamente.")
