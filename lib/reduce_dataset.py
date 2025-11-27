import os
import pandas as pd

input_file = "data/accidents.csv"
output_dir = "data/"
os.makedirs(output_dir, exist_ok=True)

target_size_bytes = 1.5 * 1024**3  # 1.5 GB
current_size = 0
rows = []

# Leemos en chunks para no cargar todo en memoria
chunk_iter = pd.read_csv(input_file, chunksize=100_000)

for chunk in chunk_iter:
    for _, row in chunk.iterrows():
        rows.append(row)
        current_size += row.memory_usage(index=True, deep=True)

        if current_size >= target_size_bytes:
            # Guardamos el subset
            out_file = os.path.join(output_dir, "accidents_subset.csv")
            pd.DataFrame(rows).to_csv(out_file, index=False)
            print(f"Guardado {out_file} con tamaño aproximado {current_size/1024**3:.2f} GB")
            break
    else:
        continue
    break
