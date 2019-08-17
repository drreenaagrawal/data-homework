CREATE TABLE emission (
id INT PRIMARY KEY,
make TEXT,
model TEXT,
year INTEGER,
co2_tailpipe_gpm TEXT,	
fuel_type TEXT,
fuel_type1 TEXT	
);

CREATE TABLE used_car (
id INT PRIMARY KEY,
make TEXT,
model TEXT,
year INTEGER,
vin TEXT,
price INT,	
mileage INT,
city TEXT,
state TEXT	
);

SELECT * FROM emission

SELECT * FROM used_car

DROP TABLE used_car;
DROP TABLE emission;


-- Joins tables
SELECT used_car.id, used_car.model, used_car.year, used_car.mileage, emission.co2_tailpipe_gpm
FROM used_car
JOIN emission
ON used_car.make = emission.make
AND used_car.model = emission.model;