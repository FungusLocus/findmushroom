CREATE TABLE observations (
    observationID SERIAL PRIMARY KEY,
    species TEXT,
    vernacularName TEXT,
    observationTime DATE,
    wgs84N DECIMAL(9,6),
    wgs84E DECIMAL(9,6)
);

CREATE TABLE predictions (
    predictionID SERIAL PRIMARY KEY,
    geometry GEOMETRY(Polygon, 3067),
    grid_x INTEGER,
    grid_y INTEGER,
    station TEXT,
    week INTEGER,
    prec DOUBLE PRECISION,
    temp DOUBLE PRECISION,
    prec_7d DOUBLE PRECISION, 
    prec_14d DOUBLE PRECISION, 
    temp_7d DOUBLE PRECISION, 
    temp_14d DOUBLE PRECISION, 
    prob_herkkutatti DOUBLE PRECISION,
    prob_karvarousku DOUBLE PRECISION, 
    prob_keltavahvero DOUBLE PRECISION, 
    prob_korvasieni DOUBLE PRECISION,
    prob_lampaankääpä DOUBLE PRECISION, 
    prob_mustatorvisieni DOUBLE PRECISION, 
    prob_mustavahakas DOUBLE PRECISION,
    prob_sikurirousku DOUBLE PRECISION, 
    prob_suppilovahvero DOUBLE PRECISION, 
    prob_vaaleaorakas DOUBLE PRECISION,
);