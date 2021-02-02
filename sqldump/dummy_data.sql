
INSERT INTO `info` VALUES (1,'<p>Haben Sie eine Lieferung von oder nach Norderney?<br>Oder etwa eine Führerschein- oder KFZ-Angelegenheit und wollen nicht selber nach Aurich fahren?</p><h4>Melden Sie sich!</h4><p>tel.: 04932 927939 (Mo - Fr 16:30 - 18:30 Uhr)<br>mail: <a href=\"mailto:info@boteweber.de\">info@boteweber.de</a></p>','<p>Am Hafen 14&nbsp;<br>26548 Norderney</p>','<p>Annahme &amp; Büro:&nbsp;<br>Mo - Do 16:30 - 18:30 Uhr&nbsp;<br>So 18:00 - 19:00 Uhr</p>','<p>Glückauf 15&nbsp;<br>26506 Norden</p>','<p>Annahme (bei C.E. Popken im Laden):&nbsp;<br>Mo - Fr 8:30 - 18:00 Uhr&nbsp;<br>Sa 8:00 - 13:00 Uhr&nbsp;<br><br>Annahme (persönlich vor Ort):&nbsp;<br>Mo - Fr 9:30 - 10:30 Uhr</p>');
INSERT INTO `news` VALUES (1,'<p>Verschlafen</p>','<p>Mahlzeit, heute war das Bett leider zu gemütlich. Mit Verspätungen muss gerechnet werden. Sorry!</p>','2012-05-29 19:30:03', 1),(14,'<p>Wieder pünktlich</p>','<p>Heute läuft wieder alles wie gewohnt.</p>','2012-05-10 19:30:03', 1);

INSERT INTO `subscribers` VALUES (8,'ad@cool.com','Adrian Richter'),(9,'dehns@example.com','Dehns'),(12,'ttest@uos.de','Tom Test'),(13,'joerg@voba.de','Jörg');
INSERT INTO `groups` VALUES (1,'privat'),(2,'alle');

INSERT INTO `subscribers_groups` VALUES (42,8,1),(43,12,2);
INSERT INTO `groups_subscribers` VALUES (32,1,8),(33,2,12);
