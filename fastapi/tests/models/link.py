from geoalchemy2.shape import from_shape
from shapely.geometry import LineString
from magma.models.link import Link
from magma.core.dependencies import AsyncSessionDep

def create_sample_link(session: AsyncSessionDep):
    line = LineString([(0, 0), (1, 1), (2, 2)])
    geom = from_shape(line, srid=4326)  # SRID 4326 for GPS lat/lon
    link = Link(geom=geom)
    session.add(link)
    session.commit()
    session.refresh(link)
    return link
