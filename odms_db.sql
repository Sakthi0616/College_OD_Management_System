-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: daa
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `approved_od`
--

DROP TABLE IF EXISTS `approved_od`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approved_od` (
  `id` int NOT NULL AUTO_INCREMENT,
  `od_number` varchar(10) NOT NULL,
  `roll_number` varchar(20) NOT NULL,
  `from_time` time NOT NULL,
  `to_time` time NOT NULL,
  `date` date NOT NULL,
  `reason` text NOT NULL,
  `proof` varchar(255) DEFAULT NULL,
  `teacher_approved` tinyint(1) DEFAULT '0',
  `hod_approved` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approved_od`
--

LOCK TABLES `approved_od` WRITE;
/*!40000 ALTER TABLE `approved_od` DISABLE KEYS */;
INSERT INTO `approved_od` VALUES (1,'OD1996','CH.SC.U4CSE23124','09:00:00','14:00:00','2025-04-15','test 3','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABS1AtsKWed840KQVenSGKNg?e=uDr2t4',1,1,'2025-04-03 15:49:52'),(2,'OD3647','CH.SC.U4CSE23124','10:00:00','15:00:00','2025-04-23','test 4','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABS1AtsKWed840KQVenSGKNg?e=uDr2t4',1,1,'2025-04-03 16:16:40'),(3,'OD7839','CH.SC.U4CSE23124','09:00:00','15:30:00','2025-04-06','Summa thaan','static/uploads\\OD7839_logo.png',1,1,'2025-04-03 13:42:27'),(4,'OD2021','CH.SC.U4CSE23124','09:30:00','12:30:00','2025-04-10','Dance Practice','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABS1AtsKWed840KQVenSGKNg?e=uDr2t4',1,1,'2025-04-03 16:47:16'),(5,'OD3064','CH.SC.U4CSE23124','08:00:00','18:00:00','2025-04-19','final test 1','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABf35iV4WOqF63KJ18m45oVg?e=KvdjNK',1,1,'2025-04-03 21:29:40'),(6,'OD8906','CH.SC.U4CSE23125','12:00:00','18:00:00','2025-04-10','test 10','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23209_ch_students_amrita_edu/EeitaTrxOuBOnoFaMnUfIzsBoqVPJV8zC-fui-kApMVl3A?e=KNMzJC',1,1,'2025-04-04 05:28:28'),(7,'OD1064','CH.SC.U4CSE23124','12:00:00','18:00:00','2025-04-16','NPtel exam','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABS1AtsKWed840KQVenSGKNg?e=uDr2t4',1,1,'2025-04-04 08:09:06');
/*!40000 ALTER TABLE `approved_od` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `od_requests`
--

DROP TABLE IF EXISTS `od_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `od_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `od_number` varchar(10) NOT NULL,
  `roll_number` varchar(20) NOT NULL,
  `from_time` time NOT NULL,
  `to_time` time NOT NULL,
  `date` date NOT NULL,
  `reason` text NOT NULL,
  `proof` varchar(255) DEFAULT NULL,
  `teacher_approved` tinyint(1) DEFAULT '0',
  `hod_approved` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `od_number` (`od_number`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `od_requests`
--

LOCK TABLES `od_requests` WRITE;
/*!40000 ALTER TABLE `od_requests` DISABLE KEYS */;
INSERT INTO `od_requests` VALUES (14,'OD9992','CH.SC.U4CSE23124','09:30:00','10:30:00','2025-04-07','Test 6','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABS1AtsKWed840KQVenSGKNg?e=uDr2t4',1,0,'2025-04-04 09:38:10');
/*!40000 ALTER TABLE `od_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reject_od`
--

DROP TABLE IF EXISTS `reject_od`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reject_od` (
  `id_number` int NOT NULL AUTO_INCREMENT,
  `od_number` varchar(20) DEFAULT NULL,
  `roll_number` varchar(20) NOT NULL,
  `from_time` time DEFAULT NULL,
  `to_time` time DEFAULT NULL,
  `date` date DEFAULT NULL,
  `reason` text,
  `proof` varchar(255) DEFAULT NULL,
  `teacher_approved` tinyint(1) DEFAULT '0',
  `hod_approved` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `status` varchar(20) DEFAULT 'rejected',
  PRIMARY KEY (`id_number`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reject_od`
--

LOCK TABLES `reject_od` WRITE;
/*!40000 ALTER TABLE `reject_od` DISABLE KEYS */;
INSERT INTO `reject_od` VALUES (1,'OD9271','CH.SC.U4CSE23124','11:00:00','13:00:00','2025-04-12','summa thaan 2','static/uploads\\OD9271_logo.png',0,0,'2025-04-03 14:15:02','rejected'),(2,'OD6459','CH.SC.U4CSE23124','08:00:00','18:00:00','2025-04-25','test 7','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABf35iV4WOqF63KJ18m45oVg?e=gShbrt',0,0,'2025-04-03 21:00:12','rejected'),(3,'OD3752','CH.SC.U4CSE23124','07:00:00','17:00:00','2025-04-16','final test 3','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABf35iV4WOqF63KJ18m45oVg?e=KvdjNK',0,0,'2025-04-03 21:30:27','rejected'),(4,'OD4393','CH.SC.U4CSE23124','09:00:00','16:00:00','2025-04-13','final test 2','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABS1AtsKWed840KQVenSGKNg?e=uDr2t4',1,0,'2025-04-03 21:30:07','rejected'),(5,'OD9637','CH.SC.U4CSE23125','10:00:00','17:00:00','2025-04-30','test 5','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABS1AtsKWed840KQVenSGKNg?e=uDr2t4',1,0,'2025-04-03 16:54:12','rejected'),(6,'OD5788','CH.SC.U4CSE23120','09:00:00','18:00:00','2025-04-21','test 6','https://amritacampuschennai-my.sharepoint.com/:w:/g/personal/ch_sc_u4cse23239_ch_students_amrita_edu/ESkARHwmfpxMkKUJLWocXPABS1AtsKWed840KQVenSGKNg?e=uDr2t4',0,0,'2025-04-03 16:56:10','rejected');
/*!40000 ALTER TABLE `reject_od` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staffinfo`
--

DROP TABLE IF EXISTS `staffinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffinfo` (
  `staff_id` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `department` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `campus` varchar(50) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `class` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffinfo`
--

LOCK TABLES `staffinfo` WRITE;
/*!40000 ALTER TABLE `staffinfo` DISABLE KEYS */;
INSERT INTO `staffinfo` VALUES ('HOD1001','Natrajan','Computer Science','hod1@amrita.edu','8752345690','Chennai','HOD',NULL),('TCH001','Dr. Priya Sharma','Computer Science','teacher1@amrita.edu','8765432109','Chennai','Class Advisor','CSEB'),('TCH002','Dr.Manoj Mehra','Computer Science','teacher2@amrita.edu','9988776655','Chennai','Class Advisor','CSEA'),('TCH003','Dr.Ajay','Computer Science','teacher3@amrita.edu','9876543210','Chennai','Class Advisor','CSEC');
/*!40000 ALTER TABLE `staffinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studinfo`
--

DROP TABLE IF EXISTS `studinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studinfo` (
  `student_id` varchar(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `batch` varchar(20) DEFAULT NULL,
  `campus` varchar(50) DEFAULT NULL,
  `school` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studinfo`
--

LOCK TABLES `studinfo` WRITE;
/*!40000 ALTER TABLE `studinfo` DISABLE KEYS */;
INSERT INTO `studinfo` VALUES ('AM.SC.U4CSE24150','KRISHNA KUMAR','krishnastudent@gmail.com','Computer Science',1,'2006-08-24','6876523456','Computer Science and Engineering','CH23UCSEA','Chennai','School of Computing'),('CB.SC.U4CSE24130','VIJAY SHANKAR','vijaystudent@gmail.com','Computer Science',1,'2006-08-22','6876543211','Computer Science and Engineering','CH23UCSEA','Chennai','School of Computing'),('CH.SC.U4CSE23120','SRADDHA JAISWAL','sraddhastudent@gmail.com','Computer Science',1,'2006-08-24','9976523456','Computer Science and Engineering','CH23UCSEB','Chennai','School of Computing'),('CH.SC.U4CSE23124','MARADANI BALAJI','example@amrita.edu','Computer Science',2,'2005-10-30','7358328512','Computer Science and Engineering','CH23UCSEB','Chennai','School of Computing - Chennai'),('CH.SC.U4CSE23125','ARUN KUMAR','arunstudent@gmail.com','Computer Science',2,'2005-09-22','9876543211','Computer Science and Engineering','CH23UCSEC','Chennai','School of Computing');
/*!40000 ALTER TABLE `studinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(150) DEFAULT NULL,
  `password` varchar(75) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'bhoomish@gmail.com','bhoomish123','student'),(2,'example@amrita.edu','12345','student'),(3,'arunstudent@gmail.com','12345','student'),(4,'vijaystudent@gmail.com','12345','student'),(5,'krishnastudent@gmail.com','12345','student'),(6,'sraddhastudent@gmail.com','12345','student'),(7,'teacher1@amrita.edu','23456','class advisor'),(8,'hod1@amrita.edu','12345','hod'),(9,'teacher2@amrita.edu','12345','class advisor'),(10,'teacher3@amrita.edu','12345','class advisor');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-04 10:12:35
