-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: wunderlistapp
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user_tasks`
--

DROP TABLE IF EXISTS `user_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tasks` (
  `task_id` int(11) NOT NULL,
  `user` varchar(100) DEFAULT NULL,
  `task_name` varchar(100) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `position` int(11) DEFAULT NULL,
  `started` datetime DEFAULT NULL,
  `completed` datetime DEFAULT NULL,
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tasks`
--

LOCK TABLES `user_tasks` WRITE;
/*!40000 ALTER TABLE `user_tasks` DISABLE KEYS */;
INSERT INTO `user_tasks` VALUES (847563608,'matthew.reider','Story Cleanup','closed',7,NULL,NULL),(847565407,'matthew.reider','BLOCKED: Set correct AMI in OPS MAN AWS How To Doc','closed',7,NULL,NULL),(881201846,'matthew.reider','Proof Read the Troubleshooting doc from docs team','closed',7,NULL,NULL),(881202062,'matthew.reider','Email OM team to recommend ways for Jemish to diagnose potential memory leaks in his own VM','closed',7,NULL,NULL),(881204654,'matthew.reider','Check if 1.3.4 with SHA 9af7391 has serial not parallel','closed',7,NULL,NULL),(881205072,'matthew.reider','Kano','closed',7,NULL,NULL),(881205582,'matthew.reider','Analyze how IPs are allocated with dynamic IPs and compilation VMs','closed',7,NULL,NULL),(881252563,'matthew.reider','Coordinate to point new stories','closed',7,NULL,NULL),(881268812,'matthew.reider','Ask VMware (again) for more IPs on vCA - or see if they are already in the account','closed',7,NULL,NULL),(882279367,'matthew.reider','Make AWS Doc Work','closed',7,NULL,NULL),(882282142,'matthew.reider','Read ticket and write story for DNS','closed',7,NULL,NULL),(882348925,'matthew.reider','Respond to ticket with 1.2 upgrade issue','closed',7,NULL,NULL),(882362845,'matthew.reider','Test DNS code change.','closed',7,NULL,NULL),(882363211,'matthew.reider','Check status on 1.4 in releng pipe','closed',7,NULL,NULL),(882378551,'matthew.reider','Release 1.3.4','closed',7,NULL,NULL),(882381063,'matthew.reider','Test 1.3.4 for vCD','closed',7,NULL,NULL),(882682461,'matthew.reider','Get git SHA for all releases','closed',7,NULL,NULL),(882871433,'matthew.reider','Test the lowering of IP addresses and HA proxy instances in 1.3.5','closed',7,NULL,NULL),(891938899,'matthew.reider','DNS TAG AND COMMENT','closed',7,NULL,NULL),(891939130,'matthew.reider','LOOK AT TICKET WITH IP PROBLEMS','closed',7,NULL,NULL),(892395659,'matthew.reider','TEST DIRECTOR WITH RUNTIME','closed',7,NULL,NULL),(901537889,'matthew.reider','Test clustering','closed',7,NULL,NULL),(901885418,'matthew.reider','Write stories for product stemcell dropdown','closed',7,NULL,NULL),(901899132,'matthew.reider','Acceptance Environment import installation(1)','closed',7,NULL,NULL),(913174620,'matthew.reider','Can releng take on vchs?','closed',7,NULL,NULL),(920121944,'matthew.reider','Write and group stories for take away IaaS interations','closed',7,NULL,NULL),(921416340,'matthew.reider','Talk about whether IPs should be able to change in Ops Man for MySQL and other products','closed',7,NULL,NULL),(930928535,'matthew.reider','Show the series of stories for uploading stemcells','closed',7,NULL,NULL),(930928978,'matthew.reider','Ask customers what IP constraints they can live with','closed',7,NULL,NULL),(930929126,'matthew.reider','Look at Kano results','closed',7,NULL,NULL),(931229117,'matthew.reider','Change to releases for PivNet','closed',7,NULL,NULL),(931265470,'matthew.reider','Ask what the YAML should look like for groups','closed',7,NULL,NULL),(932740012,'matthew.reider','Create prezo for Phillips','closed',7,NULL,NULL),(946911804,'matthew.reider','Test AZ double parens on VCHS','closed',7,NULL,NULL),(946912119,'matthew.reider','Test Collection Export / Import','closed',7,NULL,NULL),(946912716,'matthew.reider','Test IP Problem that ATOS is experiencing','closed',7,NULL,NULL),(946912955,'matthew.reider','Test deletion of Elastic Runtime','closed',7,NULL,NULL),(1078801562,'matthew.reider','Story: Textarea / checkbox for product authors to include a license.','closed',7,NULL,NULL),(1078807115,'matthew.reider','Work with James to prioritize the backlog','closed',7,NULL,NULL),(1078807516,'matthew.reider','Work with Kim on PivNet integration','closed',7,NULL,NULL),(1078920379,'matthew.reider','Talk to team about why install and actual install don\'t work together','closed',7,NULL,NULL),(1078932889,'matthew.reider','Look at the instance sizes from Stevenson and attach to story','closed',7,NULL,NULL),(1078954619,'matthew.reider','Ask Dmitriy what the best way would be to expose persistent datastroes','closed',7,NULL,NULL),(1078976206,'matthew.reider','Talk with Aram and Stevenson over Discuss Storie Labels','closed',7,NULL,NULL),(1078981758,'matthew.reider','Schedule a meeting to discuss API','closed',7,NULL,NULL),(1086773240,'matthew.reider','Change the PDF','closed',7,NULL,NULL),(1086773752,'matthew.reider','Publish all the thingz','closed',7,NULL,NULL),(1086773947,'matthew.reider','Release Notes','closed',7,NULL,NULL),(1086774263,'matthew.reider','What AWS Account?','closed',7,NULL,NULL),(1095090401,'matthew.reider','Create OpenStack Doc with Ryan and Stevenson','closed',7,NULL,NULL),(1095122174,'matthew.reider','Story Acceptance','closed',7,NULL,NULL),(1095122454,'matthew.reider','Test CloudFormating and put in docs / publish','closed',7,NULL,NULL),(1095123480,'matthew.reider','Video','closed',7,NULL,NULL),(1100690109,'matthew.reider','Tell Socialcast that exports of installations require thin timeout','closed',7,NULL,NULL),(1100692028,'matthew.reider','Publish to socialcast OpenStack specifically about IceHouse','closed',7,NULL,NULL),(1100757400,'matthew.reider','Check Mirantis Environment','closed',7,NULL,NULL),(1107814593,'matthew.reider','Make a movie of adding a key for dreamhost','closed',7,NULL,NULL),(1111617149,'matthew.reider','Write stories from https://gopivotal-com.socialcast.com/messages/24178927','closed',7,NULL,NULL),(1112485926,'matthew.reider','Write bug for dongfei\'s post','closed',7,NULL,NULL),(1122595026,'matthew.reider','Put bits back up on PivNet after checking with Evan','closed',7,NULL,NULL),(1122595683,'matthew.reider','Focus on documenting the entire process of bulding a tile','closed',7,NULL,NULL),(1122595872,'matthew.reider','Shoot video II','closed',7,NULL,NULL),(1122596588,'matthew.reider','Story acceptance','closed',7,NULL,NULL),(1122596843,'matthew.reider','Prioritize the datastore stories','closed',7,NULL,NULL),(1122597424,'matthew.reider','PERSONAL: MORTGAGE','closed',7,NULL,NULL),(1122598156,'matthew.reider','Get DreamCompute back up and running or cancel','closed',7,NULL,NULL),(1122598535,'matthew.reider','Get vCD back up and running','closed',7,NULL,NULL),(1132444796,'matthew.reider','Write an email about moving forward yes or no','closed',7,NULL,NULL),(1132446040,'matthew.reider','Check on why bosh-init fails?','closed',7,NULL,NULL),(1132446740,'matthew.reider','Check if stemcell on disk will get picked up on import','closed',7,NULL,NULL),(1134514618,'matthew.reider','PERSONAL: Fix 529','closed',7,NULL,NULL),(1134514984,'matthew.reider','PERSONAL: Mother\'s day!','closed',7,NULL,NULL),(1136067596,'matthew.reider','Build combo mysql redis','closed',7,NULL,NULL),(1136281315,'matthew.reider','Expense Report','closed',7,NULL,NULL),(1136314635,'matthew.reider','Accept Stories','closed',7,NULL,NULL),(1136316149,'matthew.reider','Put Priorites in Graphical Format','closed',7,NULL,NULL),(1147945266,'matthew.reider','Release Notes','closed',7,NULL,NULL),(1147945611,'matthew.reider','Story Acceptance','closed',7,NULL,NULL),(1148302309,'matthew.reider','Release CloudFormation Script?','closed',7,NULL,NULL),(1148378969,'matthew.reider','Change the docs to provide an elastic IP','closed',7,NULL,NULL),(1155456720,'matthew.reider','New Items','closed',7,NULL,NULL),(1156682974,'matthew.reider','say hi to aakash','closed',7,NULL,NULL),(1156988383,'matthew.reider','Finish How to build a tile.','closed',7,NULL,NULL),(1157159907,'matthew.reider','test','closed',7,NULL,NULL),(1157160548,'matthew.reider','Finish Build a Tile Doc','closed',7,NULL,NULL),(1158161769,'matthew.reider','Build a Tile Document','started',0,'2015-05-20 17:02:43',NULL),(1158162009,'matthew.reider','Deploy to OpenStack Document','open',1,NULL,NULL),(1158162196,'matthew.reider','Experiment with DreamHost','open',2,NULL,NULL),(1158162360,'matthew.reider','Remind Mirantis of Ticket','open',3,NULL,NULL),(1158162548,'matthew.reider','Remind vCA of IP Ticket','open',4,NULL,NULL),(1158162729,'matthew.reider','Accept Stories','open',5,NULL,NULL);
/*!40000 ALTER TABLE `user_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tokens`
--

DROP TABLE IF EXISTS `user_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tokens` (
  `user` varchar(100) NOT NULL,
  `access_token` varchar(250) DEFAULT NULL,
  `refreshedat` datetime DEFAULT NULL,
  PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tokens`
--

LOCK TABLES `user_tokens` WRITE;
/*!40000 ALTER TABLE `user_tokens` DISABLE KEYS */;
INSERT INTO `user_tokens` VALUES ('matthew.reider','815a873f58f6895187cb98837e20d12bab7ed1bc73641cb162e38348dfe9','2015-05-20 21:56:26');
/*!40000 ALTER TABLE `user_tokens` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-05-20 21:56:31
