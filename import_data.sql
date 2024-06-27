load data infile '/Users/adelagarza/Desktop/KECK/aniani/csv/commentlog.csv' 
into table commentlog 
fields terminated by ',' lines terminated by '\n' 
(author, created_at, comments);

LOAD DATA INFILE '/Users/adelagarza/Desktop/KECK/aniani/csv/CalibrationMeasurement.csv'
INTO TABLE CalibrationMeasurement
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
(@calibration_sample_measured_date, T400_540, D400_540, S400_540, T480_600, D480_600, S480_600, T590_720, D590_720, S590_720, T900_1100, D900_1100, S900_1100)
SET calibration_sample_measured_date = DATE(@calibration_sample_measured_date);


load data infile '/Users/adelagarza/Desktop/KECK/aniani/csv/CalibrationCertifiedMeasurement.csv' 
into table CalibrationCertifiedReference fields
terminated by ',' lines terminated by '\n' 
(calibration_sample_measured_date, T400_540, D400_540, S400_540, T480_600, D480_600, S480_600, T590_720, D590_720, S590_720, T900_1100, D900_1100, S900_1100);
