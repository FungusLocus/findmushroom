CREATE TABLE observations (
    observationID SERIAL PRIMARY KEY,
    species TEXT,
    vernacularName TEXT,
    observationTime DATE,
    wgs84N DECIMAL(9,6),
    wgs84E DECIMAL(9,6)
);