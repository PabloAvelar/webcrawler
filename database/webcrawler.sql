-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: webcrawler
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Table structure for table `search`
--

DROP TABLE IF EXISTS `search`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  `link` text NOT NULL,
  `html_origin` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `search_unique` (`link`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabla para usarse como caché y aumentar la velocidad de búsqueda del webcrawler';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search`
--

LOCK TABLES `search` WRITE;
/*!40000 ALTER TABLE `search` DISABLE KEYS */;
INSERT INTO `search` VALUES (31,'Acuerdo por el que se da a conocer el cierre de la Oficina de Pasaportes de la Secretaría de Relaciones Exteriores en la demarcación territorial Iztacalco, en la Ciudad de México.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726235&fecha=10/05/2024','enlaces'),(32,'Acuerdo por el cual se dan a conocer los montos de los estímulos fiscales aplicables a la enajenación de gasolinas en la región fronteriza con Guatemala, correspondientes al periodo que se especifica.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726246&fecha=10/05/2024','enlaces'),(33,'Acuerdo mediante el cual se aprueba la modificación de los Lineamientos en Materia de Recursos Humanos, Servicio Profesional y Personal de Libre Designación del Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726270&fecha=10/05/2024','enlaces'),(34,'Acuerdo número 06/05/24 por el que se modifican las Reglas de Operación del Programa Nacional de Inglés para el ejercicio fiscal 2024, emitidas mediante diverso número 16/12/23, publicado el 26 de diciembre de 2023.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726251&fecha=10/05/2024','enlaces'),(35,'Acuerdo por el que se expide el Manual de Integración y Funcionamiento del Comité de Bienes Muebles de la Secretaría de Desarrollo Agrario, Territorial y Urbano.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726256&fecha=10/05/2024','enlaces'),(36,'Acuerdo mediante el cual se aprueba la modificación al Reglamento de Recursos Financieros y Presupuestales del Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726271&fecha=10/05/2024','enlaces'),(37,'Acuerdo por el que se dan a conocer los porcentajes, los montos del estí­mulo fiscal y las cuotas disminuidas del impuesto especial sobre producción y servicios, así­ como las cantidades por litro aplicables a los combustibles que se indican, correspondientes al periodo que se especifica.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726244&fecha=10/05/1924','enlaces_leido'),(38,'Acuerdo G/JGA/17/2024 por el que se da a conocer la adscripción de Magistrados del Tribunal Federal de Justicia Administrativa.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726273&fecha=10/05/2024','enlaces'),(39,'Acuerdo de Coordinación para el ejercicio de facultades en materia de control y fomento sanitarios, que celebran la Secretaría de Salud, con la participación de la Comisión Federal para la Protección contra Riesgos Sanitarios, y el Estado de Michoacán de Ocampo.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726254&fecha=10/05/2024','enlaces'),(40,'Acuerdo por el que se dan a conocer los porcentajes, los montos del estímulo fiscal y las cuotas disminuidas del impuesto especial sobre producción y servicios, así como las cantidades por litro aplicables a los combustibles que se indican, correspondientes al periodo que se especifica.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726244&fecha=10/05/2024','enlaces'),(41,'Acuerdo número 07/05/24 por el que se modifican las Reglas de Operación del Programa Jóvenes Escribiendo el Futuro para el ejercicio fiscal 2024, emitidas mediante diverso número 25/12/23, publicado el 29 de diciembre de 2023.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726252&fecha=10/05/2024','enlaces'),(42,'Acuerdo mediante el cual se aprueba la modificación del artículo 190 Bis del Reglamento en Materia de Recursos Materiales del Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726269&fecha=10/05/2024','enlaces'),(43,'Acuerdo por el cual se dan a conocer los montos de los estímulos fiscales aplicables a la enajenación de gasolinas en la región fronteriza con los Estados Unidos de América, correspondientes al periodo que se especifica.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726245&fecha=10/05/2024','enlaces'),(44,'Acuerdo por el que se habilitan días y horas para las unidades administrativas que se indican, a efecto de que lleven a cabo procedimientos de contratación en materia de adquisiciones, arrendamientos y servicios, así como para la ejecución y formalización de los actos e instrumentos jurídicos correspondientes.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726258&fecha=10/05/2024','enlaces'),(45,'Acuerdo G/JGA/18/2024 por el que se deja sin efectos el Acuerdo G/ JGA/15/2024.','https://www.dof.gob.mx/nota_detalle.php?codigo=5726274&fecha=10/05/2024','enlaces');
/*!40000 ALTER TABLE `search` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'webcrawler'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-12 21:03:18
