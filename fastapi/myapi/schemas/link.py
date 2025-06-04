from pydantic import BaseModel
from typing import Dict, Any, Literal


# ########    PYDANTIC SCHEMA:  link  (link aggregates only)    ########


class LinkAggregateResponse(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: Dict[str, Any]  # Must include 'type' and 'coordinates' keys as per GeoJSON spec
    properties: Dict[str, Any]  # Contains metadata and scalar fields for this feature

    class Config:
        schema_extra = {
            "example": {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [[-121.123, 38.123], [-121.124, 38.124]]
                    ]
                },
                "properties": {
                    "link_id": 123,
                    "road_name": "Main St",
                    "average_speed": 45.0,
                    "usdk_speed_category": 2,
                    "funclass_id": 3,
                    "volume_year": 2023,
                    "day": 2,
                    "period": 3
                }
            }
        }

