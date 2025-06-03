from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  speed_record    ########


class SpeedRecord(Base):
    __tablename__ = "speed_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link_id = Column(Integer, ForeignKey("links.id"), index=True, nullable=False)

    date_time = Column(DateTime(timezone=True), nullable=False)
    freeflow = Column(Float)
    count = Column(Integer)
    std_dev = Column(Float)
    min = Column(Float)
    max = Column(Float)
    confidence = Column(Integer)
    average_speed = Column(Float)  # ****
    average_pct_85 = Column(Float)
    average_pct_95 = Column(Float)

    day_of_week = Column(Integer)
    period = Column(Integer)

    link = relationship("Link", back_populates="speed_records")


#####################################
# - - - - SHAPE ---- df.shape - - - - - - - - - - - - - - - - - - - - - - -
# SHAPE: (1239946, 13)
# - - - - DTYPES ---- df.dtypes - - - - - - - - - - - - - - - - - - - - - - -
# SHAPE: link_id             int64
# date_time          object
# freeflow          float64
# count               int64
# std_dev           float64
# min               float64
# max               float64
# confidence          int64
# ####  average_speed     float64
# average_pct_85    float64
# average_pct_95    float64
# #??  day_of_week         int64   * In head 20 its all same day of week. Entire sample might be 1 day of week.  Need??
# ####  period              int64   * I'm seeing ints 1-7 in the head 20
# dtype: object

