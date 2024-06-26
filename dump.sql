/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.2-MariaDB, for osx10.19 (arm64)
--
-- Host: localhost    Database: aniani
-- ------------------------------------------------------
-- Server version	11.4.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `CommentLog`
--

DROP TABLE IF EXISTS `CommentLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CommentLog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(50) DEFAULT NULL,
  `comments` varchar(1000) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CommentLog`
--

LOCK TABLES `CommentLog` WRITE;
/*!40000 ALTER TABLE `CommentLog` DISABLE KEYS */;
INSERT INTO `CommentLog` VALUES
(1,'LG','Original file from Luke titled \"Reflectivity data _MASTER_2020-01-08\"','2024-06-26 19:07:25'),
(2,'KS','Populate 2019 with measurements taken after 2020 calibration of SOC Reflectometer, still checking to ensure all data is present -- could not find witness for one coating run','2024-06-26 19:07:25'),
(3,'KS','Add Tabs for Witness Data and Optical Surface data','2024-06-26 19:07:25'),
(4,'LG','Relabeled the witness sample and optical surface to Primary Witness Sample & Primary Surface Data. Modified the data for those tabs to match the 2020 and 2019 data format coming from the spectrometer.  Added Instrument Calibration Check and Secondary & Tertiary Witness Sample & Surface Data worksheets. Removed the Primary and Secondary worksheets, datahas been resaved in new format in the added worksheets.','2024-06-26 19:07:25'),
(5,'KS','Begin data dump in Primary Witness page.','2024-06-26 19:07:25');
/*!40000 ALTER TABLE `CommentLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `InstrumentCalibrationCertifiedReference`
--

DROP TABLE IF EXISTS `InstrumentCalibrationCertifiedReference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `InstrumentCalibrationCertifiedReference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `certification_date` date DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `InstrumentCalibrationCertifiedReference`
--

LOCK TABLES `InstrumentCalibrationCertifiedReference` WRITE;
/*!40000 ALTER TABLE `InstrumentCalibrationCertifiedReference` DISABLE KEYS */;
INSERT INTO `InstrumentCalibrationCertifiedReference` VALUES
(1,NULL,0.916,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
(2,NULL,NULL,NULL,NULL,0.912,NULL,NULL,0.9,NULL,NULL,0.894,NULL,NULL);
/*!40000 ALTER TABLE `InstrumentCalibrationCertifiedReference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `InstrumentCalibrationMeasurement`
--

DROP TABLE IF EXISTS `InstrumentCalibrationMeasurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `InstrumentCalibrationMeasurement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `calibration_sample_measured_date` date DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `InstrumentCalibrationMeasurement`
--

LOCK TABLES `InstrumentCalibrationMeasurement` WRITE;
/*!40000 ALTER TABLE `InstrumentCalibrationMeasurement` DISABLE KEYS */;
INSERT INTO `InstrumentCalibrationMeasurement` VALUES
(1,'2020-09-23',0.913,0.002,0.911,0.909,0.002,0.907,0.898,0.002,0.896,0.895,0.003,0.892),
(2,'2021-02-02',0.917,0.003,0.914,0.913,0.003,0.91,0.901,0.003,0.898,0.897,0.004,0.894);
/*!40000 ALTER TABLE `InstrumentCalibrationMeasurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MirrorBarnPrimary`
--

DROP TABLE IF EXISTS `MirrorBarnPrimary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MirrorBarnPrimary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `segment_id` int(11) DEFAULT NULL,
  `mirror_type` int(11) DEFAULT NULL,
  `measured_date` date DEFAULT NULL,
  `install_date` date DEFAULT NULL,
  `from_telescope` int(11) DEFAULT NULL,
  `from_segment_position` int(11) DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MirrorBarnPrimary`
--

LOCK TABLES `MirrorBarnPrimary` WRITE;
/*!40000 ALTER TABLE `MirrorBarnPrimary` DISABLE KEYS */;
/*!40000 ALTER TABLE `MirrorBarnPrimary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PrimaryOpticalSurface`
--

DROP TABLE IF EXISTS `PrimaryOpticalSurface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PrimaryOpticalSurface` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `segment_id` int(11) DEFAULT NULL,
  `mirror_type` int(11) DEFAULT NULL,
  `measured_date` date DEFAULT NULL,
  `install_date` date DEFAULT NULL,
  `from_telescope` int(11) DEFAULT NULL,
  `from_segment_position` int(11) DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PrimaryOpticalSurface`
--

LOCK TABLES `PrimaryOpticalSurface` WRITE;
/*!40000 ALTER TABLE `PrimaryOpticalSurface` DISABLE KEYS */;
/*!40000 ALTER TABLE `PrimaryOpticalSurface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PrimaryWitnessSample`
--

DROP TABLE IF EXISTS `PrimaryWitnessSample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PrimaryWitnessSample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `segment_id` int(11) DEFAULT NULL,
  `mirror_type` int(11) DEFAULT NULL,
  `witness_measured_date` date DEFAULT NULL,
  `install_date` date DEFAULT NULL,
  `to_telescope` int(11) DEFAULT NULL,
  `to_segment_position` int(11) DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PrimaryWitnessSample`
--

LOCK TABLES `PrimaryWitnessSample` WRITE;
/*!40000 ALTER TABLE `PrimaryWitnessSample` DISABLE KEYS */;
INSERT INTO `PrimaryWitnessSample` VALUES
(1,46,1,'2016-10-07','2016-10-11',2,4,0.91,NULL,0.91,0.91,NULL,0.91,0.9,NULL,0.9,0.92,NULL,0.92,''),
(2,71,4,'2016-10-05',NULL,NULL,NULL,0.91,NULL,0.91,0.91,NULL,0.91,0.9,NULL,0.9,0.92,NULL,0.92,''),
(3,45,5,'2016-09-29','2016-10-11',2,29,0.91,NULL,0.91,0.9,NULL,0.9,0.9,NULL,0.9,0.92,NULL,0.92,''),
(4,9,2,'2016-09-22','2016-10-11',2,14,0.91,NULL,0.91,0.91,NULL,0.9,0.9,NULL,0.9,0.92,NULL,0.92,'');
/*!40000 ALTER TABLE `PrimaryWitnessSample` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SecondaryOpticalSurface`
--

DROP TABLE IF EXISTS `SecondaryOpticalSurface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SecondaryOpticalSurface` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `secondary_number` int(11) DEFAULT NULL,
  `mirror_type` int(11) DEFAULT NULL,
  `measured_date` date DEFAULT NULL,
  `install_date` date DEFAULT NULL,
  `from_telescope` int(11) DEFAULT NULL,
  `from_segment_position` int(11) DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SecondaryOpticalSurface`
--

LOCK TABLES `SecondaryOpticalSurface` WRITE;
/*!40000 ALTER TABLE `SecondaryOpticalSurface` DISABLE KEYS */;
/*!40000 ALTER TABLE `SecondaryOpticalSurface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SecondaryWitnessSample`
--

DROP TABLE IF EXISTS `SecondaryWitnessSample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SecondaryWitnessSample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `secondary_number` varchar(1) DEFAULT NULL,
  `mirror_type` int(11) DEFAULT NULL,
  `witness_measured_date` date DEFAULT NULL,
  `install_date` date DEFAULT NULL,
  `to_telescope` int(11) DEFAULT NULL,
  `to_segment_position` int(11) DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SecondaryWitnessSample`
--

LOCK TABLES `SecondaryWitnessSample` WRITE;
/*!40000 ALTER TABLE `SecondaryWitnessSample` DISABLE KEYS */;
INSERT INTO `SecondaryWitnessSample` VALUES
(1,'B',NULL,'2019-06-29','2012-07-31',2,NULL,0.91,NULL,0.91,0.91,NULL,0.91,0.9,NULL,0.9,0.92,NULL,0.92,'Where did this come from, confirm dates.'),
(2,'A',NULL,'2019-03-11','2019-06-20',1,NULL,0.91,0.011,0.9,0.906,0.01,0.896,0.895,0.008,0.887,0.894,0.005,0.889,''),
(3,'B',NULL,'2021-06-23','2021-06-23',2,NULL,0.9155,0.0005,0.915,0.912,0.0005,0.9115,0.899,0,0.899,0.893,0.001,0.892,''),
(4,'A',NULL,'2021-11-03','2019-06-20',1,NULL,0.91,0.01,0.9,0.91,0.01,0.9,0.9,0.01,0.89,0.89,0.005,0.89,'');
/*!40000 ALTER TABLE `SecondaryWitnessSample` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TertiaryOpticalSurface`
--

DROP TABLE IF EXISTS `TertiaryOpticalSurface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TertiaryOpticalSurface` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tertiary_number` int(11) DEFAULT NULL,
  `mirror_type` int(11) DEFAULT NULL,
  `measured_date` date DEFAULT NULL,
  `install_date` date DEFAULT NULL,
  `from_telescope` int(11) DEFAULT NULL,
  `from_segment_position` int(11) DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TertiaryOpticalSurface`
--

LOCK TABLES `TertiaryOpticalSurface` WRITE;
/*!40000 ALTER TABLE `TertiaryOpticalSurface` DISABLE KEYS */;
/*!40000 ALTER TABLE `TertiaryOpticalSurface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TertiaryWitnessSample`
--

DROP TABLE IF EXISTS `TertiaryWitnessSample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TertiaryWitnessSample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tertiary_number` varchar(1) DEFAULT NULL,
  `mirror_type` int(11) DEFAULT NULL,
  `witness_measured_date` date DEFAULT NULL,
  `install_date` date DEFAULT NULL,
  `to_telescope` int(11) DEFAULT NULL,
  `to_segment_position` int(11) DEFAULT NULL,
  `T400_540` float DEFAULT NULL,
  `D400_540` float DEFAULT NULL,
  `S400_540` float DEFAULT NULL,
  `T480_600` float DEFAULT NULL,
  `D480_600` float DEFAULT NULL,
  `S480_600` float DEFAULT NULL,
  `T590_720` float DEFAULT NULL,
  `D590_720` float DEFAULT NULL,
  `S590_720` float DEFAULT NULL,
  `T900_1100` float DEFAULT NULL,
  `D900_1100` float DEFAULT NULL,
  `S900_1100` float DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TertiaryWitnessSample`
--

LOCK TABLES `TertiaryWitnessSample` WRITE;
/*!40000 ALTER TABLE `TertiaryWitnessSample` DISABLE KEYS */;
INSERT INTO `TertiaryWitnessSample` VALUES
(1,'A',NULL,'2021-10-10','2021-10-14',2,NULL,0.91,0,0.9,0.9,0,0.9,0.89,0,0.89,0.89,0.004,0.88,'');
/*!40000 ALTER TABLE `TertiaryWitnessSample` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-06-26 10:09:42
