import json
import pandas as pd
from shapely.geometry import shape
from sqlalchemy.ext.asyncio import AsyncSession
from myapi.core.logger import log
from myapi.models.link import Link
from myapi.models.speed_record import SpeedRecord


async def load_links(session: AsyncSession, file_path: str):
    log.info(f"Loading links from {file_path}")
    df = pd.read_parquet(file_path)

    for _, row in df.iterrows():
        geometry_obj = shape(json.loads(row["geo_json"]))
        link = Link(
            id=row["link_id"],
            _length=float(row["_length"]) if row["_length"] else None,
            road_name=row["road_name"],
            usdk_speed_category=row["usdk_speed_category"],
            funclass_id=row["funclass_id"],
            speedcat=row["speedcat"],
            volume_value=row["volume_value"],
            volume_bin_id=row["volume_bin_id"],
            volume_year=row["volume_year"],
            volumes_bin_description=row["volumes_bin_description"],
            geometry=f"SRID=4326;{geometry_obj.wkt}",
        )
        session.add(link)

    await session.commit()
    log.info("✅ Links loaded.")


# GEOMETRY FORMAT AND PARQUET GEOJSON LOADING NOTES:
# 1.    geometry_obj = shape(json.loads(row["geo_json"]))
# 2.    geometry=f"SRID=4326;{geometry_obj.wkt}"
# 1. Parses a valid GeoJSON string into a shapely geometry object.    2. Converts it into WKT with SRID=4326 prefix.
# This stores it correctly into a PostGIS-compatible Geometry("MultiLineString", srid=4326) column using GeoAlchemy2.
# This matches our model and schema and determines our post-processing of retreived data and endpoint responses.


async def load_speed_records(session: AsyncSession, file_path: str):
    log.info(f"Loading speed_records from {file_path}")
    df = pd.read_parquet(file_path)

    # Preserve timezone awareness (best practice): Convert string/object values to true datetime type for col date_time.
    df["date_time"] = pd.to_datetime(df["date_time"])

    records = [
        SpeedRecord(
            link_id=row["link_id"],
            date_time=row["date_time"],
            freeflow=row["freeflow"],
            count=row["count"],
            std_dev=row["std_dev"],
            min=row["min"],
            max=row["max"],
            confidence=row["confidence"],
            average_speed=row["average_speed"],
            average_pct_85=row["average_pct_85"],
            average_pct_95=row["average_pct_95"],
            day_of_week=row["day_of_week"],
            period=row["period"],
        )
        for _, row in df.iterrows()
    ]

    # Record-by-record add is done to avoid ambiguous datetime data type issues with bulk methods like add_all().
    records = df.to_dict(orient="records")  # Becuase we use to_dict() our col names must match data file col names.
    for record in records:
        obj = SpeedRecord(**record)
        session.add(obj)

    await session.commit()
    log.info("✅ SpeedRecords loaded.")

