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
    segment_id INT NULL,
    mirror VARCHAR(50) NULL,
    mirror_type CHAR NULL,
    measured_date DATE NULL,
    install_date DATE NULL,
    to_telescope INT NULL, 
    to_segment_position INT NULL,
    from_telescope INT NULL,
    from_segment_position INT NULL,
    spectrum ENUM('400-540', '480-600', '590-720', '900-1100') NOT NULL,
    measurement_type ENUM('T', 'D', 'S') NOT NULL,
    reflectivity FLOAT NULL,
    is_deleted BOOLEAN NOT NULL,
    notes MEDIUMTEXT NULL
);
