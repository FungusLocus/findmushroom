CREATE TABLE observations (
    observationID SERIAL PRIMARY KEY,
    species TEXT,
    vernacularName TEXT,
    observationTime DATE,
    wgs84N DECIMAL(9,6),
    wgs84E DECIMAL(9,6)
);

CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    species TEXT NOT NULL,
    grid_x INTEGER NOT NULL,
    grid_y INTEGER NOT NULL,
    week INTEGER NOT NULL,
    probability DOUBLE PRECISION NOT NULL,
    UNIQUE (species, grid_x, grid_y, week)
);