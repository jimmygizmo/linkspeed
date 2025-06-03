import pandas as pd
import dotenv
import os
import time

# The panda install does not bring in pyarrow and we do not import it here either. The pyarrow module is imported
# internally by pandas via the following pd.read_parquet() call which specifies the pyarrow engine.

pd.set_option('display.max_columns', None)  # Show all columns


# Locate any .env file in the hierarchy here or above here and load it
dotenv.load_dotenv(dotenv.find_dotenv())


# IMPORTANT! - The following path likely assumes you are running this script from within the /scripts/ directory
#   inside the project.
SEED_DATA_FILE_DIR = '../datavolume/'


# For the Magma code that cares about the format of these two seed data files, see:
# /bedrock-gis/bedrock/magma/models/link.py             [maga.models.link]
# /bedrock-gis/bedrock/magma/schemas/link.py            [maga.schemas.link]
# /bedrock-gis/bedrock/magma/models/speed_record.py     [maga.models.speed_record]
# /bedrock-gis/bedrock/magma/schemas/speed_record.py    [maga.schemas.speed_record]


# Link Info Dataset
# PARQUET_FILE__LINKS: str = os.getenv('PARQUET_FILE__LINKS', default='DEFAULT--link_info.parquet.gz')
PARQUET_FILE__LINKS: str = os.getenv('PARQUET_FILE__LINKS')
if PARQUET_FILE__LINKS:
    print(f"✅ PARQUET_FILE__LINKS: {PARQUET_FILE__LINKS}", flush=True)
else:
    print('🟥 ERROR: MISSING ENV VAR:  PARQUET_FILE__LINKS', flush=True)
    exit(1)

# Speed Data
# PARQUET_FILE__SPEED_RECORDS: str = os.getenv('PARQUET_FILE__SPEED_RECORDS', default='DEFAULT--duval_jan1_2024.parquet.gz')
PARQUET_FILE__SPEED_RECORDS: str = os.getenv('PARQUET_FILE__SPEED_RECORDS')
if PARQUET_FILE__SPEED_RECORDS:
    print(f"✅ PARQUET_FILE__SPEED_RECORDS: {PARQUET_FILE__SPEED_RECORDS}", flush=True)
else:
    print('🟥 ERROR: MISSING ENV VAR:  PARQUET_FILE__SPEED_RECORDS', flush=True)
    exit(1)

parquet_file_path__links = os.path.join(SEED_DATA_FILE_DIR, PARQUET_FILE__LINKS)
df_link = pd.read_parquet(parquet_file_path__links, engine='pyarrow')

parquet_file_path__speed_records = os.path.join(SEED_DATA_FILE_DIR, PARQUET_FILE__SPEED_RECORDS)
df_speed_record = pd.read_parquet(parquet_file_path__speed_records, engine='pyarrow')

# Why all the flush=True? Pandas has many simultaneous async processes here. flush=True helps keep output in order.

def summarize(df):
    print(flush=True)
    print('- - - - SHAPE ---- df.shape - - - - - - - - - - - - - - - - - - - - - - -', flush=True)
    print(f'SHAPE: {df.shape}', flush=True)
    print(flush=True)
    print('- - - - DTYPES ---- df.dtypes - - - - - - - - - - - - - - - - - - - - - - -', flush=True)
    print(f'SHAPE: {df.dtypes}', flush=True)
    print(flush=True)
    print('- - - - HEAD(20) ---- df.head(20) - - - - - - - - - - - - - - - - - - - - - - -', flush=True)
    print(f'SHAPE: {df.head(20)}', flush=True)
    print(flush=True)
    print('- - - - INFO() ---- df.info() - - - - - - - - - - - - - - - - - - - - - - -', flush=True)
    print(f'SHAPE: {df.info()}', flush=True)
    print(flush=True)
    print('- - - - DESCRIBE() ---- df.describe() - - - - - - - - - - - - - - - - - - - - - - -', flush=True)
    print(f'SHAPE: {df.describe()}', flush=True)


def summarize_geo_json_column(df):
    print("- - - - HEAD 20 GEO_JSON COL ---- df.['geo_json'] - - - - - - - - - - - - - - - - - - -", flush=True)
    for _ in range(20):
        print('- - - - - - - -', flush=True)
        print(df['geo_json'], flush=True)


def main():
    # Pandas does this work asynchronously so the output can get jumbled without moving the slower one last
    # and adding the sleep. This is not critical code so such crude measures are fine to address this async case.
    # To help keep output in order in such an asynchronous case, we add the flush=True to all print() calls.

    print(flush=True)
    print('========  ANALYSIS OF PARQUET FILE:  SPEED_RECORDS  ================================', flush=True)
    summarize(df_speed_record)
    print(flush=True)

    time.sleep(2)

    print(flush=True)
    print('========  ANALYSIS OF PARQUET FILE:  LINKS  ================================', flush=True)
    summarize(df_link)
    summarize_geo_json_column(df_link)
    print(flush=True)


if __name__ == '__main__':
    main()

