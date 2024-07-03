-- sql script to create the database and tables
-- if need to change table properties: do it here ONLY

-- Create the database
CREATE DATABASE IF NOT EXISTS aniani;

USE aniani;

-- CREATE INSTRUMENT CALIBRATION CHECK TABLES

CREATE TABLE CalibrationChecks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    certified BOOLEAN NOT NULL,
    measured_date DATE NULL,
    spectrum ENUM('400-540', '480-600', '590-720', '900-1100') NOT NULL,
    measurement_type ENUM('T', 'D', 'S') NOT NULL,
    reflectivity FLOAT NULL,
    notes MEDIUMTEXT NULL


);

-- CREATING MIRROR SAMPLE TABLE

CREATE TABLE MirrorSamples (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mirror ENUM('primary', 'secondary', 'tertiary'),
    segment_id INT NULL,
    mirror_type ENUM('1', '2', '3', '4', '5', '6', 'A', 'B', 'C') NOT NULL,
    measured_date DATE NULL,
    install_date DATE NULL,
    sample_status ENUM('clean', 'dirty'),
    telescope_num INT NULL,
    segment_position INT NULL (value >= 1 AND value <= 36),
    spectrum ENUM('400-540', '480-600', '590-720', '900-1100') NOT NULL,
    measurement_type ENUM('T', 'D', 'S') NOT NULL,
    reflectivity FLOAT NULL,
    notes MEDIUMTEXT NULL,
    is_deleted BOOLEAN NOT NULL
);
