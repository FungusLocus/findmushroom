CREATE TABLE observations (
    observationID SERIAL PRIMARY KEY,
    species TEXT,
    vernacularName TEXT,
    observationNum INTEGER,
    observationTime TIMESTAMP,
    municipality TEXT,
    biogeographicalProvince TEXT,
    country TEXT,
    wgs84N DECIMAL(9,6),
    wgs84E DECIMAL(9,6),
    observationCertainty TEXT,
    observationReliability TEXT
);