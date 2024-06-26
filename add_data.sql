-- INSERT INTO COMMENT LOG

INSERT INTO COMMENTLOG (author, comments)
VALUES 
('LG','Original file from Luke titled "Reflectivity data _MASTER_2020-01-08"' ),
('KS','Populate 2019 with measurements taken after 2020 calibration of SOC Reflectometer, still checking to ensure all data is present -- could not find witness for one coating run'),
('KS','Add Tabs for Witness Data and Optical Surface data'),
('LG','Relabeled the witness sample and optical surface to Primary Witness Sample & Primary Surface Data. Modified the data for those tabs to match the 2020 and 2019 data format coming from the spectrometer.  Added Instrument Calibration Check and Secondary & Tertiary Witness Sample & Surface Data worksheets. Removed the Primary and Secondary worksheets, datahas been resaved in new format in the added worksheets.'),
('KS','Begin data dump in Primary Witness page.');

-- INSERT INTO INSTRUMENTCALIBRATIONMEASUREMENT

INSERT INTO InstrumentCalibrationMeasurement(calibration_sample_measured_date, T400_540, D400_540, S400_540, T480_600, D480_600, S480_600, T590_720, D590_720, S590_720, T900_1100, D900_1100,S900_1100)
VALUES
('2020-09-23', 0.913, 0.002, 0.911, 0.909, 0.002, 0.907, 0.898, 0.002, 0.896, 0.895, 0.003, 0.892),
('2021-02-02', 0.917, 0.003, 0.914, 0.913, 0.003, 0.91, 0.901, 0.003, 0.898, 0.897, 0.004, 0.894);

-- INSERT INTO INSRUMENT 

INSERT INTO InstrumentCalibrationCertifiedReference (certification_date, T400_540, D400_540, S400_540, T480_600, D480_600, S480_600, T590_720, D590_720, S590_720, T900_1100, D900_1100,S900_1100)
VALUES
(NULL, 0.916, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(NULL, NULL, NULL, NULL, 0.912, NULL, NULL, 0.9, NULL, NULL, 0.894, NULL, NULL);

--INSERT INTO PRIMARYWITNESSSAMPLE

INSERT INTO PRIMARYWITNESSSAMPLE (segment_id, mirror_type, witness_measured_date, install_date, to_telescope, to_segment_position, T400_540, D400_540, S400_540, T480_600, D480_600, S480_600, T590_720, D590_720, S590_720, T900_1100, D900_1100,S900_1100, notes)
VALUES
(46, 1, '2016-10-07', '2016-10-11', 2, 4, 0.91, NULL, 0.91, 0.91, NULL, 0.91, 0.90, NULL, 0.90, 0.92, NULL, 0.92, ""),
(71, 4, '2016-10-05', NULL, NULL, NULL, 0.91, NULL, 0.91, 0.91, NULL, 0.91, 0.90, NULL, 0.90, 0.92, NULL, 0.92, ""),
(45, 5, '2016-09-29', '2016-10-11', 2, 29, 0.91, NULL, 0.91, 0.90, NULL, 0.90, 0.90, NULL, 0.90, 0.92, NULL, 0.92, ""),
(9, 2, '2016-09-22', '2016-10-11', 2, 14, 0.91, NULL, 0.91, 0.91, NULL, 0.90, 0.90, NULL, 0.90, 0.92, NULL, 0.92, "");

--INSERT INTO SECONDARYWITNESSSAMPLE

INSERT INTO SECONDARYWITNESSSAMPLE (secondary_number, mirror_type, witness_measured_date, install_date, to_telescope, to_segment_position, T400_540, D400_540, S400_540, T480_600, D480_600, S480_600, T590_720, D590_720, S590_720, T900_1100, D900_1100,S900_1100, notes)
VALUES
('B', NULL, '2019-06-29', '2012-07-31', 2, NULL, 0.91, NULL, 0.91, 0.91, NULL, 0.91, 0.90, NULL, 0.90, 0.92, NULL, 0.92, "Where did this come from, confirm dates."),
('A', NULL, '2019-03-11', '2019-06-20', 1, NULL, 0.91, 0.011, 0.90, 0.906, 0.01, 0.896, 0.895, 0.008, 0.887, 0.894, 0.005, 0.889, ""),
('B', NULL, '2021-06-23', '2021-06-23', 2, NULL, 0.9155, 0.0005, 0.915, 0.912, 0.0005, 0.9115, 0.899, 0, 0.899, 0.893, 0.001, 0.892, ""),
('A', NULL, '2021-11-03', '2019-06-20', 1, NULL, 0.91, 0.01, 0.90, 0.91, 0.01, 0.90, 0.90, 0.01, 0.89, 0.89, 0.005, 0.89, "");

-- INSERT INTO TERTIARY WITNESS SAMPLE

INSERT INTO TertiaryWitnessSample (tertiary_number, mirror_type, witness_measured_date, install_date, to_telescope, to_segment_position,T400_540, D400_540, S400_540, T480_600, D480_600, S480_600, T590_720, D590_720, S590_720, T900_1100, D900_1100,S900_1100, notes)
VALUES
('A', NULL, '2021-10-10', '2021-10-14', 2, NULL, 0.91, 0.00, 0.90, 0.90, 0.00, 0.90, 0.89, 0.00, 0.89, 0.89, 0.004, 0.88, "");

-- INSERT INTO

INSERT INTO PrimaryOpticalSurface (segment_id, mirror_type, measured_date, install_date, from_telescope, from_segment_position, T400_540, D400_540, S400_540, T480_600, D480_600, S480_600, T590_720, D590_720, S590_720, T900_1100, D900_1100,S900_1100, is_deleted)
VALUES 
(46, 1, '2016-09-16', '2014-09-10', 2, 4, 0.91, NULL, 0.88, 0.90, NULL, 0.88, 0.89, NULL, 0.87, 0.92, NULL, 0.90, "", FALSE),
(71, 4, '2016-09-16', '2014-09-10', 2, NULL, 0.91, NULL, 0.89, 0.90, NULL, 0.89, 0.90, NULL, 0.88, 0.92, NULL, 0.90, "", FALSE),
(45, 5, '2016-09-16', '2014-09-09', 2, 29, 0.91, NULL, 0.89, 0.90, NULL, 0.89, 0.90, NULL, 0.88, 0.92, NULL, 0.90, "", FALSE),
(9, 2, '2016-09-16', '2014-06-10', 2, 14, 0.91, NULL, 0.90, 0.91, NULL, 0.90, 0.90, NULL, 0.89, 0.92, NULL, 0.91, "", FALSE);