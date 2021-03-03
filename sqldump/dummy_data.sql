
INSERT INTO info (text, greet_ny_top, greet_ny_bot, greet_no_top, greet_no_bot) VALUES
    ('<p>Haben Sie eine Lieferung von oder nach Norderney?<br>Oder etwa eine Führerschein- oder KFZ-Angelegenheit und wollen nicht selber nach Aurich fahren?</p><h4>Melden Sie sich!</h4><p>tel.: 04932 927939 (Mo - Fr 16:30 - 18:30 Uhr)<br>mail: <a href=\"mailto:info@boteweber.de\">info@boteweber.de</a></p>','<p>Am Hafen 14&nbsp;<br>26548 Norderney</p>','<p>Annahme &amp; Büro:&nbsp;<br>Mo - Do 16:30 - 18:30 Uhr&nbsp;<br>So 18:00 - 19:00 Uhr</p>','<p>Glückauf 15&nbsp;<br>26506 Norden</p>','<p>Annahme (bei C.E. Popken im Laden):&nbsp;<br>Mo - Fr 8:30 - 18:00 Uhr&nbsp;<br>Sa 8:00 - 13:00 Uhr&nbsp;<br><br>Annahme (persönlich vor Ort):&nbsp;<br>Mo - Fr 9:30 - 10:30 Uhr</p>');


INSERT INTO news (title, message, timestamp, priority) VALUES
    ('<p>Verschlafen</p>','<p>Mahlzeit, heute war das Bett leider zu gemütlich. Mit Verspätungen muss gerechnet werden. Sorry!</p>','2012-05-29 19:30:03', 1),
    ('<p>Titel nummer 1</p>','<p>Langer sinnvoler Text nummer 1</p>','2012-05-29 19:30:03', 1),
    ('<p>Titel nummer 2</p>','<p>Langer sinnvoler Text nummer 2</p>','2012-05-29 19:30:03', 1),
    ('<p>Titel nummer 3</p>','<p>Langer sinnvoler Text nummer 3</p>','2012-05-29 19:30:03', 1),
    ('<p>Titel nummer 4</p>','<p>Langer sinnvoler Text nummer 4</p>','2012-05-29 19:30:03', 1),
    ('<p>Titel nummer 5</p>','<p>Langer sinnvoler Text nummer 5</p>','2012-05-29 19:30:03', 1),
    ('<p>Titel nummer 6</p>','<p>Langer sinnvoler Text nummer 6</p>','2012-05-29 19:30:03', 1),
    ('<p>Titel nummer 7</p>','<p>Langer sinnvoler Text nummer 7</p>','2012-05-29 19:30:03', 1),
    ('<p>Wieder pünktlich</p>','<p>Heute läuft wieder alles wie gewohnt.</p>','2012-05-10 19:30:03', 1);


INSERT INTO subscribers (email, name) VALUES
    ('ad@cool.com','Adrian Richter'),
    ('dehns@example.com','Dehns'),
    ('ttest@uos.de','Tom Test'),
    ('joerg@voba.de','Jörg');

INSERT INTO groups (name) VALUES
    ('privat'),
    ('alle');


INSERT INTO subscribers_groups (subscribers_id, groups_id) VALUES
    (3,1),
    (4,2);

INSERT INTO groups_subscribers (groups_id, subscribers_id) VALUES
    (1,3),
    (2,4);


INSERT INTO admin (name, password) VALUES
    ('admin','pbkdf2:sha256:150000$bMfuk4Nt$d7c5db7e4fe0234aefbb370877a4aae31e7b41c51e04a454063f82a1bc678b99');
