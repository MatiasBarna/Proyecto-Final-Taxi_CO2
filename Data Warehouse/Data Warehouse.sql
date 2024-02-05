DROP DATABASE IF EXISTS taxi2_co2;
CREATE DATABASE IF NOT EXISTS taxi2_co2;
USE taxi2_co2;

DROP TABLE IF EXISTS tipocontaminante;
CREATE TABLE IF NOT EXISTS tipocontaminante(
Contaminante_Id INT AUTO_INCREMENT PRIMARY KEY,
Tipo VARCHAR (50) NOT NULL
);

DROP TABLE IF EXISTS aire;
CREATE TABLE IF NOT EXISTS aire (
    Aire_Id INT AUTO_INCREMENT PRIMARY KEY,
    Pollutant VARCHAR(50) NOT NULL,
    MeasureInfo VARCHAR(50) NOT NULL,
    GeoPlaceName VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    DataValue DECIMAL(10, 2) NOT NULL, 
    Contaminante_Id INT,
    FOREIGN KEY (Contaminante_Id) REFERENCES tipocontaminante(Contaminante_Id)
);

DROP TABLE IF EXISTS emisiones;
CREATE TABLE IF NOT EXISTS emisiones (
    Emision_Id INT AUTO_INCREMENT PRIMARY KEY,
    ModelYear INT NOT NULL,
    Make VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    VehicleClass VARCHAR(50) NOT NULL,
    CO2Emissions DECIMAL(10, 2) NOT NULL,
    CO2Rating INT NOT NULL,
    SmogRating INT NOT NULL,
    CityKWhPer100Mi DECIMAL(10, 2) NOT NULL,
    HighwayKWhPer100Mi DECIMAL(10, 2) NOT NULL,
    RangeMi INT NOT NULL,
    RechargeTimeH INT NOT NULL,
    TypeCar VARCHAR(50) NOT NULL,
    CityGalPerMi DECIMAL(10, 2) NOT NULL,
    HighwayGalPerMi DECIMAL(10, 2) NOT NULL
    Modelo_Id INT,
    FOREIGN KEY (Modelo_Id) REFERENCES tipomodeloauto(Modelo_Id)
);

DROP TABLE IF EXISTS estaciones;
CREATE TABLE IF NOT EXISTS estaciones (
    Estacion_Id INT AUTO_INCREMENT PRIMARY KEY,
    StationName VARCHAR(50) NOT NULL,
    StreetAddress VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    ZIP VARCHAR(10) NOT NULL,
    StationPhone VARCHAR(15) NOT NULL,
    Latitude DECIMAL(10, 6) NOT NULL,
    Longitude DECIMAL(10, 6) NOT NULL,
    ID INT NOT NULL,
    EVPricingDetail VARCHAR(50) NOT NULL,
    EVPrice DECIMAL(10, 2) NOT NULL
);

DROP TABLE IF EXISTS borough;
CREATE TABLE IF NOT EXISTS borough (
	Borough_Id INT AUTO_INCREMENT PRIMARY KEY,
    Borough VARCHAR (50)
    );	

DROP TABLE IF EXISTS zona;
CREATE TABLE IF NOT EXISTS zona (
    PULocationID INT PRIMARY KEY,
    Borough_Id INT,
	Zone VARCHAR(50),
    Service_Zone VARCHAR(50),
	FOREIGN KEY (Borough_Id) REFERENCES borough(Borough_Id)
);

DROP TABLE IF EXISTS viajes_taxi;
CREATE TABLE IF NOT EXISTS viajes_taxi (
    Viaje_Id INT AUTO_INCREMENT PRIMARY KEY,
    PULocationID INT NOT NULL,
    Borough VARCHAR(50) NOT NULL,
    Zone VARCHAR(50) NOT NULL,
    ServiceZone VARCHAR(50) NOT NULL,
    PassengerCount INT NOT NULL,
    TripDistance DECIMAL(10, 2) NOT NULL,
    DOLocationID INT NOT NULL,
    RatecodeID INT NOT NULL,
    StoreAndFwdFlag VARCHAR(1) NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    DatePickup DATE NOT NULL,
    TimePickup TIME NOT NULL,
    DateDropoff DATE NOT NULL,
    TimeDropoff TIME NOT NULL
);

DROP TABLE IF EXISTS tipocombustible;
CREATE TABLE IF NOT EXISTS tipocombustible (
	Combustible_Id INT AUTO_INCREMENT PRIMARY KEY,
    Combustible VARCHAR (50)
    );
DROP TABLE IF EXISTS tipomodeloauto;
CREATE TABLE IF NOT EXISTS tipomodeloauto (
	Modelo_Id INT AUTO_INCREMENT PRIMARY KEY,
    Modelo VARCHAR (120)
    );

DROP TABLE IF EXISTS consumo_combustible;
CREATE TABLE IF NOT EXISTS consumo_combustible (
    Consumo_Id INT AUTO_INCREMENT PRIMARY KEY,
    Manufacturer VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    CO2PerMile DECIMAL(10, 2) NOT NULL,
    MilesPerGallon DECIMAL(10, 2) NOT NULL,
    EfficiencyTimesCombustible DECIMAL(10, 2) NOT NULL,
    CombustibleTimesYear DECIMAL(10, 2) NOT NULL,
    Fuel VARCHAR(50) NOT NULL,
    ScoreGHG DECIMAL(10, 2) NOT NULL,
    EfficiencyTimesCombustibleCity DECIMAL(10, 2) NOT NULL,
    YouSaveSpend DECIMAL(10, 2) NOT NULL,
    AlternativeFuel VARCHAR(50) NOT NULL,
    Modelo_Id INT,
    Combustible_Id INT,
    FOREIGN KEY (Combustible_Id) REFERENCES tipocombustible(Combustible_Id)
    FOREIGN KEY (Modelo_Id) REFERENCES tipomodeloauto(Modelo_Id)
);

DROP TABLE IF EXISTS sonido;
CREATE TABLE IF NOT EXISTS sonido (
    Sonido_Id INT AUTO_INCREMENT PRIMARY KEY,
    Borough_Id INT,
    Latitude DECIMAL(10, 6) NOT NULL,
    Longitude DECIMAL(10, 6) NOT NULL,
    Year INT NOT NULL,
    Day INT NOT NULL,
    Hour INT NOT NULL,
    EngineSound VARCHAR(50) NOT NULL, 
    FOREIGN KEY (Borough_Id) REFERENCES borough(Borough_Id)
);
