from django.core.management.base import BaseCommand
from exams.models import Question
from django.contrib.auth.models import User


# ---------------------------------------------------------------
# FRENCH QUESTIONS
# Format: (question, correct_answer, wrong1, wrong2, wrong3)
# The wrong answers are plausible but incorrect.
# ---------------------------------------------------------------
FRENCH = [
    ("Comment tu t'appelles ?", "Je m'appelle Paul.", "J'ai dix ans.", "Ça va bien.", "J'habite à Lagos."),
    ("Quel âge as-tu ?", "J'ai dix ans.", "Je m'appelle Paul.", "Ça va bien.", "Je suis Nigérian."),
    ("Comment ça va ?", "Ça va bien.", "Je m'appelle Paul.", "J'ai dix ans.", "J'habite à Lagos."),
    ("Où habites-tu ?", "J'habite à Lagos.", "Je m'appelle Paul.", "Ça va bien.", "Je suis étudiant."),
    ("Quelle est ta nationalité ?", "Je suis Nigérian.", "J'habite à Lagos.", "J'ai dix ans.", "Ça va bien."),
    ("Es-tu étudiant ?", "Oui, je suis étudiant.", "Non, je suis professeur.", "Oui, j'ai un frère.", "Non, je suis fatigué."),
    ("Quelle est ta couleur préférée ?", "Le bleu.", "La pomme.", "Le riz.", "Le chien."),
    ("Quel est ton fruit préféré ?", "La pomme.", "Le bleu.", "Le riz.", "Le chien."),
    ("As-tu un frère ?", "Oui, j'ai un frère.", "Oui, j'ai une sœur.", "Non, je n'ai pas de frère.", "Je suis étudiant."),
    ("As-tu une sœur ?", "Oui, j'ai une sœur.", "Oui, j'ai un frère.", "Non, je n'ai pas de sœur.", "Je suis étudiant."),
    ("Quel jour sommes-nous ?", "Nous sommes lundi.", "Nous sommes en janvier.", "Il est huit heures.", "Nous sommes en 2024."),
    ("Quel mois sommes-nous ?", "Nous sommes en janvier.", "Nous sommes lundi.", "Il est huit heures.", "Nous sommes en 2024."),
    ("Quelle heure est-il ?", "Il est huit heures.", "Nous sommes lundi.", "Nous sommes en janvier.", "Il est très chaud."),
    ("Où vas-tu ?", "Je vais à l'école.", "Je mange du riz.", "Je bois de l'eau.", "Je suis heureux."),
    ("Que manges-tu ?", "Je mange du riz.", "Je bois de l'eau.", "Je vais à l'école.", "Je suis heureux."),
    ("Que bois-tu ?", "Je bois de l'eau.", "Je mange du riz.", "Je vais à l'école.", "Je suis heureux."),
    ("Aimes-tu le football ?", "Oui, j'aime le football.", "Non, je n'aime pas le football.", "Oui, j'aime chanter.", "Non, je préfère danser."),
    ("Parles-tu français ?", "Oui, je parle français.", "Non, je parle anglais.", "Oui, je parle yoruba.", "Non, je ne parle pas."),
    ("Quelle est ta matière préférée ?", "Les mathématiques.", "Le riz.", "Le bleu.", "Le chien."),
    ("Qui est ton professeur ?", "Monsieur Jean.", "Paul.", "Marie.", "David."),
    ("Où est ton livre ?", "Il est sur la table.", "Il est dans le sac.", "Il est sous la chaise.", "Il est à l'école."),
    ("Combien de livres as-tu ?", "J'ai trois livres.", "J'ai deux livres.", "J'ai quatre livres.", "J'ai cinq livres."),
    ("Quel est ton animal préféré ?", "Le chien.", "Le chat.", "Le poisson.", "L'oiseau."),
    ("As-tu un chien ?", "Oui, j'ai un chien.", "Oui, j'ai un chat.", "Non, je n'ai pas de chien.", "Oui, j'ai un frère."),
    ("Quelle est la capitale du Nigeria ?", "Abuja.", "Lagos.", "Paris.", "Accra."),
    ("Quelle est la capitale de la France ?", "Paris.", "Abuja.", "Lagos.", "Accra."),
    ("Qui es-tu ?", "Je suis un élève.", "Je suis un professeur.", "Je suis un docteur.", "Je suis un père."),
    ("Es-tu heureux ?", "Oui, je suis heureux.", "Non, je suis triste.", "Oui, je suis fatigué.", "Non, je suis malade."),
    ("Es-tu fatigué ?", "Non, je ne suis pas fatigué.", "Oui, je suis fatigué.", "Oui, je suis heureux.", "Non, je suis triste."),
    ("Quel est ton plat préféré ?", "Le riz.", "La pomme.", "Le bleu.", "Le chien."),
    ("Quand te réveilles-tu ?", "Je me réveille à six heures.", "Je me réveille à huit heures.", "Je me réveille à midi.", "Je me réveille le soir."),
    ("Quand vas-tu à l'école ?", "Je vais à l'école le matin.", "Je vais à l'école le soir.", "Je vais à l'école la nuit.", "Je ne vais pas à l'école."),
    ("Aimes-tu chanter ?", "Oui, j'aime chanter.", "Non, je n'aime pas chanter.", "Oui, j'aime danser.", "Non, j'aime lire."),
    ("Aimes-tu danser ?", "Oui, j'aime danser.", "Non, je n'aime pas danser.", "Oui, j'aime chanter.", "Non, j'aime lire."),
    ("Quel est ton sport préféré ?", "Le football.", "La danse.", "Le chant.", "La lecture."),
    ("Combien de jours y a-t-il dans une semaine ?", "Sept jours.", "Cinq jours.", "Dix jours.", "Douze jours."),
    ("Combien de mois y a-t-il dans une année ?", "Douze mois.", "Sept mois.", "Dix mois.", "Six mois."),
    ("Quelle est la couleur du soleil ?", "Jaune.", "Verte.", "Bleue.", "Rouge."),
    ("Quelle est la couleur de l'herbe ?", "Verte.", "Jaune.", "Bleue.", "Rouge."),
    ("Où travailles-tu ?", "Je travaille à l'école.", "Je travaille à la maison.", "Je travaille à l'hôpital.", "Je travaille au marché."),
    ("Que fais-tu ?", "J'étudie.", "Je dors.", "Je mange.", "Je danse."),
    ("Sais-tu nager ?", "Oui, je sais nager.", "Non, je ne sais pas nager.", "Oui, je sais courir.", "Non, je sais danser."),
    ("Peux-tu courir ?", "Oui, je peux courir.", "Non, je ne peux pas courir.", "Oui, je peux nager.", "Non, je peux chanter."),
    ("Quel est ton prénom ?", "Mon prénom est Marie.", "Mon prénom est Paul.", "Mon prénom est David.", "Mon prénom est Jean."),
    ("Comment s'appelle ton père ?", "Il s'appelle David.", "Il s'appelle Paul.", "Il s'appelle Jean.", "Il s'appelle Pierre."),
    ("Comment s'appelle ta mère ?", "Elle s'appelle Grace.", "Elle s'appelle Marie.", "Elle s'appelle Anne.", "Elle s'appelle Julie."),
    ("Quel temps fait-il ?", "Il fait chaud.", "Il fait froid.", "Il pleut.", "Il neige."),
    ("Est-ce que tu aimes l'école ?", "Oui, j'aime l'école.", "Non, je n'aime pas l'école.", "Oui, j'aime la maison.", "Non, j'aime le marché."),
    ("Que veux-tu devenir ?", "Je veux devenir médecin.", "Je veux devenir professeur.", "Je veux devenir pilote.", "Je veux devenir avocat."),
    ("Comment dit-on merci en français ?", "Merci.", "Bonjour.", "Au revoir.", "S'il vous plaît."),
]

# ---------------------------------------------------------------
# ENGLISH QUESTIONS
# ---------------------------------------------------------------
ENGLISH = [
    ("What is your name?", "My name is John.", "I am ten years old.", "I am fine.", "I live in Lagos."),
    ("How old are you?", "I am ten years old.", "My name is John.", "I am fine.", "I live in Lagos."),
    ("How are you?", "I am fine.", "My name is John.", "I am ten years old.", "I live in Lagos."),
    ("Where do you live?", "I live in Lagos.", "My name is John.", "I am fine.", "I am ten years old."),
    ("What is your country?", "My country is Nigeria.", "My country is Ghana.", "My country is France.", "My country is England."),
    ("What is your favourite colour?", "My favourite colour is blue.", "My favourite colour is red.", "My favourite colour is green.", "My favourite colour is yellow."),
    ("What is your favourite food?", "My favourite food is rice.", "My favourite food is bread.", "My favourite food is beans.", "My favourite food is yam."),
    ("What is your favourite fruit?", "My favourite fruit is mango.", "My favourite fruit is orange.", "My favourite fruit is banana.", "My favourite fruit is apple."),
    ("Do you have a brother?", "Yes, I do.", "No, I don't.", "Yes, I am.", "No, I am not."),
    ("Do you have a sister?", "Yes, I do.", "No, I don't.", "Yes, I am.", "No, I am not."),
    ("What is your father's name?", "His name is David.", "Her name is Mary.", "My name is John.", "His name is Peter."),
    ("What is your mother's name?", "Her name is Mary.", "His name is David.", "My name is John.", "Her name is Grace."),
    ("What is the name of your school?", "My school is Bright Academy.", "My school is Green College.", "My school is Blue School.", "My school is High School."),
    ("Who is your teacher?", "My teacher is Mr James.", "My teacher is Mrs Grace.", "My teacher is Mr David.", "My teacher is Miss Anne."),
    ("What is your favourite subject?", "Mathematics.", "English.", "French.", "Yoruba."),
    ("What do you eat for breakfast?", "I eat bread and tea.", "I eat rice and beans.", "I eat yam and egg.", "I eat fruit and milk."),
    ("What do you drink?", "I drink water.", "I drink tea.", "I drink milk.", "I drink juice."),
    ("Do you like football?", "Yes, I do.", "No, I don't.", "Yes, I am.", "No, I am not."),
    ("Can you swim?", "Yes, I can.", "No, I can't.", "Yes, I do.", "No, I don't."),
    ("Can you read?", "Yes, I can.", "No, I can't.", "Yes, I do.", "No, I don't."),
    ("What day is today?", "Today is Monday.", "Today is Sunday.", "Today is Friday.", "Today is Saturday."),
    ("How many days are in a week?", "Seven days.", "Five days.", "Ten days.", "Twelve days."),
    ("How many months are in a year?", "Twelve months.", "Seven months.", "Ten months.", "Six months."),
    ("How many hours are in a day?", "Twenty-four hours.", "Twelve hours.", "Ten hours.", "Six hours."),
    ("What is the capital of Nigeria?", "Abuja.", "Lagos.", "Kano.", "Ibadan."),
    ("What is the capital of Ghana?", "Accra.", "Abuja.", "Lagos.", "Paris."),
    ("What is the capital of France?", "Paris.", "Abuja.", "Lagos.", "Accra."),
    ("What is the colour of the sky?", "Blue.", "Green.", "Red.", "Yellow."),
    ("What is the colour of grass?", "Green.", "Blue.", "Red.", "Yellow."),
    ("Which animal gives us milk?", "A cow.", "A dog.", "A cat.", "A goat."),
    ("Which animal barks?", "A dog.", "A cat.", "A cow.", "A goat."),
    ("Which animal meows?", "A cat.", "A dog.", "A cow.", "A goat."),
    ("Where does a fish live?", "In water.", "On land.", "In the sky.", "In a tree."),
    ("What do bees produce?", "Honey.", "Milk.", "Water.", "Bread."),
    ("What do we use to write?", "A pen.", "A book.", "A ruler.", "An eraser."),
    ("What do we use to read?", "A book.", "A pen.", "A ruler.", "An eraser."),
    ("What do we use to see?", "Our eyes.", "Our ears.", "Our nose.", "Our mouth."),
    ("What do we use to hear?", "Our ears.", "Our eyes.", "Our nose.", "Our mouth."),
    ("How many fingers do you have?", "Ten fingers.", "Five fingers.", "Eight fingers.", "Twelve fingers."),
    ("How many legs does a dog have?", "Four legs.", "Two legs.", "Six legs.", "Eight legs."),
    ("What do you want to become?", "I want to become a doctor.", "I want to become a teacher.", "I want to become a farmer.", "I want to become a driver."),
    ("What time do you wake up?", "I wake up at six o'clock.", "I wake up at eight o'clock.", "I wake up at noon.", "I wake up at night."),
    ("Do you like reading?", "Yes, I do.", "No, I don't.", "Yes, I am.", "No, I am not."),
    ("Do you like dancing?", "Yes, I do.", "No, I don't.", "Yes, I am.", "No, I am not."),
    ("What is your favourite sport?", "Football.", "Basketball.", "Tennis.", "Swimming."),
    ("Who is your best friend?", "My best friend is Peter.", "My best friend is John.", "My best friend is David.", "My best friend is James."),
    ("What is your religion?", "I am a Christian.", "I am a Muslim.", "I am a student.", "I am a teacher."),
    ("What do you use to brush your teeth?", "A toothbrush.", "A pen.", "A book.", "A towel."),
    ("What do plants need to grow?", "Water, air and sunlight.", "Water and sand.", "Air and stones.", "Sunlight and rocks."),
    ("What do you say when someone helps you?", "Thank you.", "Goodbye.", "Hello.", "Please."),
]

# ---------------------------------------------------------------
# YORUBA QUESTIONS
# ---------------------------------------------------------------
YORUBA = [
    ("Kí ni orúkọ rẹ?", "Orúkọ mi ni Adé.", "Orúkọ mi ni Bọ́lá.", "Orúkọ mi ni Ṣadé.", "Orúkọ mi ni Túndé."),
    ("Ọmọ ọdún mélòó ni ọ́?", "Ọmọ ọdún mẹ́wàá ni mí.", "Ọmọ ọdún méjì ni mí.", "Ọmọ ọdún mẹ́ta ni mí.", "Ọmọ ọdún márùn-ún ni mí."),
    ("Ṣé àlàáfíà ni?", "Àlàáfíà ni.", "Béẹ̀ kọ́.", "Mo dúpẹ́.", "Ó dàbọ̀."),
    ("Níbo ni o ń gbé?", "Mo ń gbé ní Èkó.", "Mo ń gbé ní Abuja.", "Mo ń gbé ní Ìbàdàn.", "Mo ń gbé ní Kànò."),
    ("Orílẹ̀-èdè wo ni o ti wá?", "Mo wá láti Nàìjíríà.", "Mo wá láti Gánà.", "Mo wá láti Faransé.", "Mo wá láti Íngílàndì."),
    ("Kí ni àwọ̀ tí o fẹ́ràn jù?", "Mo fẹ́ràn àwọ̀ búlúù.", "Mo fẹ́ràn àwọ̀ pupa.", "Mo fẹ́ràn àwọ̀ ewé.", "Mo fẹ́ràn àwọ̀ ofeefee."),
    ("Èso wo ni o fẹ́ràn?", "Mo fẹ́ràn máńgòrò.", "Mo fẹ́ràn ọ̀gẹ̀dẹ̀.", "Mo fẹ́ràn ọsàn.", "Mo fẹ́ràn èso ápù."),
    ("Ṣé o ní arákùnrin?", "Béẹ̀ ni, mo ní arákùnrin.", "Béẹ̀ kọ́, n kò ní arákùnrin.", "Béẹ̀ ni, mo ní arábìnrin.", "Béẹ̀ kọ́, n kò ní arábìnrin."),
    ("Ṣé o ní arábìnrin?", "Béẹ̀ ni, mo ní arábìnrin.", "Béẹ̀ kọ́, n kò ní arábìnrin.", "Béẹ̀ ni, mo ní arákùnrin.", "Béẹ̀ kọ́, n kò ní arákùnrin."),
    ("Kí ni orúkọ bàbá rẹ?", "Orúkọ bàbá mi ni Adé.", "Orúkọ bàbá mi ni Bọ́lá.", "Orúkọ bàbá mi ni Ṣadé.", "Orúkọ bàbá mi ni Túndé."),
    ("Kí ni orúkọ ìyá rẹ?", "Orúkọ ìyá mi ni Rónkẹ́.", "Orúkọ ìyá mi ni Bọ́lá.", "Orúkọ ìyá mi ni Ṣadé.", "Orúkọ ìyá mi ni Túndé."),
    ("Ọjọ́ wo ni òní?", "Ọjọ́ Ajé ni.", "Ọjọ́ Àìkú ni.", "Ọjọ́ Ẹtì ni.", "Ọjọ́ Àbámẹ́ta ni."),
    ("Oṣù mélòó ló wà nínú ọdún kan?", "Oṣù méjìlá.", "Oṣù méje.", "Oṣù mẹ́wàá.", "Oṣù mẹ́fà."),
    ("Ọjọ́ mélòó ló wà nínú ọ̀sẹ̀ kan?", "Ọjọ́ méje.", "Ọjọ́ márùn-ún.", "Ọjọ́ mẹ́wàá.", "Ọjọ́ méjìlá."),
    ("Kí ni o ń jẹ?", "Mo ń jẹ ìrẹsì.", "Mo ń jẹ iṣu.", "Mo ń jẹ ẹ̀wà.", "Mo ń jẹ ọ̀gẹ̀dẹ̀."),
    ("Kí ni o ń mu?", "Mo ń mu omi.", "Mo ń mu tíì.", "Mo ń mu wàrà.", "Mo ń mu oje."),
    ("Ṣé o fẹ́ràn bọ́ọ̀lù?", "Béẹ̀ ni, mo fẹ́ràn bọ́ọ̀lù.", "Béẹ̀ kọ́, n kò fẹ́ràn bọ́ọ̀lù.", "Béẹ̀ ni, mo fẹ́ràn orin.", "Béẹ̀ kọ́, mo fẹ́ràn ijó."),
    ("Ṣé o lè lúwẹ̀ẹ́?", "Béẹ̀ ni, mo lè lúwẹ̀ẹ́.", "Béẹ̀ kọ́, n kò lè lúwẹ̀ẹ́.", "Béẹ̀ ni, mo lè sáré.", "Béẹ̀ kọ́, mo lè jó."),
    ("Ibo ni o ti ń kẹ́kọ̀ọ́?", "Mo ń kẹ́kọ̀ọ́ ní ilé-ẹ̀kọ́.", "Mo ń kẹ́kọ̀ọ́ ní ilé.", "Mo ń kẹ́kọ̀ọ́ ní ọjà.", "Mo ń kẹ́kọ̀ọ́ ní ilé-ìwé."),
    ("Ta ni olùkọ́ rẹ?", "Olùkọ́ mi ni Ọ̀gbẹ́ni Adé.", "Olùkọ́ mi ni Ọ̀gbẹ́ni Bọ́lá.", "Olùkọ́ mi ni Ọ̀gbẹ́ni Ṣadé.", "Olùkọ́ mi ni Ọ̀gbẹ́ni Túndé."),
    ("Kí ni ẹ̀kọ́ tí o fẹ́ràn jù?", "Mátímátíkì.", "Èdè Gẹ̀ẹ́sì.", "Èdè Faransé.", "Èdè Yorùbá."),
    ("Ẹranko wo ni o fẹ́ràn?", "Mo fẹ́ràn ajá.", "Mo fẹ́ràn ológbò.", "Mo fẹ́ràn ẹja.", "Mo fẹ́ràn ẹyẹ."),
    ("Ibo ni ẹja ń gbé?", "Nínú omi.", "Lórí ilẹ̀.", "Nínú ojú ọ̀run.", "Nínú igi."),
    ("Ẹranko wo ni ń gbó?", "Ajá.", "Ológbò.", "Màlúù.", "Ewúrẹ́."),
    ("Kí ni màlúù ń fún wa?", "Wàrà.", "Oyin.", "Omi.", "Búrẹ́dì."),
    ("Kí ni oyin ń ṣe?", "Ó ń ṣe oyin.", "Ó ń ṣe wàrà.", "Ó ń ṣe omi.", "Ó ń ṣe búrẹ́dì."),
    ("Ẹsẹ̀ mélòó ni ajá ní?", "Ẹsẹ̀ mẹ́rin.", "Ẹsẹ̀ méjì.", "Ẹsẹ̀ mẹ́fà.", "Ẹsẹ̀ mẹ́jọ."),
    ("Ika mélòó ni ọwọ́ méjì ní?", "Ika mẹ́wàá.", "Ika márùn-ún.", "Ika mẹ́jọ.", "Ika méjìlá."),
    ("Kí ni a fi ń kọ̀wé?", "A fi pẹ́ńsùlù ń kọ̀wé.", "A fi ìwé ń kọ̀wé.", "A fi páńtì ń kọ̀wé.", "A fi ọwọ́ ń kọ̀wé."),
    ("Kí ni a fi ń kàwé?", "A fi ìwé ń kàwé.", "A fi pẹ́ńsùlù ń kàwé.", "A fi páńtì ń kàwé.", "A fi ọwọ́ ń kàwé."),
    ("Kí ni a fi ń ríran?", "A fi ojú ń ríran.", "A fi etí ń ríran.", "A fi imú ń ríran.", "A fi ẹnu ń ríran."),
    ("Kí ni a fi ń gbọ́ràn?", "A fi etí ń gbọ́ràn.", "A fi ojú ń gbọ́ràn.", "A fi imú ń gbọ́ràn.", "A fi ẹnu ń gbọ́ràn."),
    ("Kí ni orúkọ olú-ìlú Nàìjíríà?", "Abuja.", "Èkó.", "Ìbàdàn.", "Kànò."),
    ("Kí ni orúkọ olú-ìlú Èkó?", "Èkó ni.", "Abuja ni.", "Ìbàdàn ni.", "Kànò ni."),
    ("Kí ni o fẹ́ di lọ́jọ́ iwájú?", "Mo fẹ́ di dókítà.", "Mo fẹ́ di olùkọ́.", "Mo fẹ́ di àgbẹ̀.", "Mo fẹ́ di awakọ̀."),
    ("Ìgbà wo ni o máa ń jí?", "Mo máa ń jí ní agogo mẹ́fà.", "Mo máa ń jí ní agogo mẹ́jọ.", "Mo máa ń jí ní ọ̀sán.", "Mo máa ń jí ní alẹ́."),
    ("Ṣé o fẹ́ràn orin?", "Béẹ̀ ni, mo fẹ́ràn orin.", "Béẹ̀ kọ́, n kò fẹ́ràn orin.", "Béẹ̀ ni, mo fẹ́ràn ijó.", "Béẹ̀ kọ́, mo fẹ́ràn ìwé."),
    ("Ṣé o fẹ́ràn ijó?", "Béẹ̀ ni, mo fẹ́ràn ijó.", "Béẹ̀ kọ́, n kò fẹ́ràn ijó.", "Béẹ̀ ni, mo fẹ́ràn orin.", "Béẹ̀ kọ́, mo fẹ́ràn ìwé."),
    ("Kí ni o máa ń ṣe ní ilé?", "Mo máa ń kàwé.", "Mo máa ń sùn.", "Mo máa ń jẹun.", "Mo máa ń jó."),
    ("Ṣé o ní ọ̀rẹ́?", "Béẹ̀ ni, mo ní ọ̀rẹ́.", "Béẹ̀ kọ́, n kò ní ọ̀rẹ́.", "Béẹ̀ ni, mo ní ẹbí.", "Béẹ̀ kọ́, mo ní ilé."),
    ("Kí ni orúkọ ọ̀rẹ́ rẹ?", "Orúkọ rẹ̀ ni Bọ́lá.", "Orúkọ rẹ̀ ni Adé.", "Orúkọ rẹ̀ ni Ṣadé.", "Orúkọ rẹ̀ ni Túndé."),
    ("Kí ni o máa ń ṣe ní òwúrọ̀?", "Mo máa ń wẹ̀.", "Mo máa ń sùn.", "Mo máa ń jẹun.", "Mo máa ń kọrin."),
    ("Kí ni o máa ń ṣe ní alẹ́?", "Mo máa ń sùn.", "Mo máa ń wẹ̀.", "Mo máa ń jẹun.", "Mo máa ń kọrin."),
    ("Ṣé o fẹ́ràn ilé-ẹ̀kọ́?", "Béẹ̀ ni, mo fẹ́ràn ilé-ẹ̀kọ́.", "Béẹ̀ kọ́, n kò fẹ́ràn ilé-ẹ̀kọ́.", "Béẹ̀ ni, mo fẹ́ràn ilé.", "Béẹ̀ kọ́, mo fẹ́ràn ọjà."),
    ("Kí ni o fi ń fọ eyín?", "Mo fi páńtì eyín ń fọ eyín.", "Mo fi ọwọ́ ń fọ eyín.", "Mo fi omi ń fọ eyín.", "Mo fi ìwé ń fọ eyín."),
    ("Kí ni a fi ń rìn?", "A fi ẹsẹ̀ ń rìn.", "A fi ọwọ́ ń rìn.", "A fi ojú ń rìn.", "A fi etí ń rìn."),
    ("Kí ni àwọ̀ koríko?", "Àwọ̀ ewé.", "Àwọ̀ búlúù.", "Àwọ̀ pupa.", "Àwọ̀ ofeefee."),
    ("Kí ni àwọ̀ ọ̀run?", "Àwọ̀ búlúù.", "Àwọ̀ ewé.", "Àwọ̀ pupa.", "Àwọ̀ ofeefee."),
    ("Kí ni o máa ń sọ nígbà tí ẹnìkan bá ràn ọ́ lọ́wọ́?", "Ẹ ṣé.", "Ó dàbọ̀.", "Ẹ káàárọ̀.", "Jọ̀wọ́."),
    ("Báwo ni a ṣe ń kí ènìyàn ní òwúrọ̀?", "Ẹ káàárọ̀.", "Ẹ káàsán.", "Ẹ kúùrọ̀lẹ́.", "Ó dàbọ̀."),
]


class Command(BaseCommand):
    help = "Import French, English and Yoruba questions into the database"

    def handle(self, *args, **kwargs):
        admin_user = User.objects.filter(is_superuser=True).first()
        created_count = 0
        skipped_count = 0

        for language, data in [("French", FRENCH), ("English", ENGLISH), ("Yoruba", YORUBA)]:
            for item in data:
                question_text, correct, wrong1, wrong2, wrong3 = item

                # Skip if this question already exists
                if Question.objects.filter(language=language, text=question_text).exists():
                    skipped_count += 1
                    continue

                # Build the 4 options; correct answer is always option A
                options = [correct, wrong1, wrong2, wrong3]

                Question.objects.create(
                    language=language,
                    text=question_text,
                    option_a=options[0],
                    option_b=options[1],
                    option_c=options[2],
                    option_d=options[3],
                    correct_answer='A',
                    created_by=admin_user,
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created_count} questions, skipped {skipped_count} duplicates."
        ))
        