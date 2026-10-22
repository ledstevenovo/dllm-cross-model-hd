# 签核复核表（draft，human_reviewed=false）

规则：`src/signoff_rule.py`（已对 pilot200 400/400 复现）；题单：`data/raw_qa/subsets/pool2000_v1.jsonl`

## llada（1800 条；correct 487）

| # | split | question | gold | prediction | 判定 | 说明 |
|---|---|---|---|---|---|---|
| 1 | validation | What is the name of Bruce Willis's character in Unbreakable? | David Dunn | 'Jack Cross.' | incorrect | gold 未命中 |
| 2 | test | Which "Blackzilians" fighter is currently competing in the M | Vitor Belfort | ' Conor McGregor.' | incorrect | gold 未命中 |
| 3 | test | Drisheen is what type of product made in Ireland and other p | Black pudding | 'Drisheen is a type of sweet bread made in Ireland ' | incorrect | gold 未命中 |
| 4 | test | What heritage site, known for a British explorer, is listed  | Captain Cook's Landing P | 'Captain Cook Monument' | incorrect | gold 未命中 |
| 5 | train | Kevin Wayne Durant was named what ?(An Award initiated follo | The National Basketball  | 'Kevin Wayne Durant was named NBA Rookie of the Yea' | incorrect | gold 未命中 |
| 6 | test | Seal Harris was born in what county? | Polk County | 'Seal Harris was born in Orange County, California.' | incorrect | gold 未命中 |
| 7 | train | When was the king that started coin production in Copenhagen | 2 February 1455 | '1573' | incorrect | 单 token 短答 '1573'（疑似错答，人工留意） |
| 8 | train | How many people live in the County serviced by The Collier A | 321,520 | 'Over 400,000' | incorrect | gold 未命中 |
| 9 | test | The creator of "Wallace and Gromit" also created what animat | Creature Comforts | 'My Zoo' | incorrect | gold 未命中 |
| 10 | train | Who was the architect of a Dutch museum dedicated to the art | Petrus Josephus Hubertus | 'Pieter Dudok' | incorrect | gold 未命中 |
| 11 | train | What Finnish Christmas figure, which eventually become more  | The Yule goat | 'Jukki' | incorrect | 单 token 短答 'Jukki'（疑似错答，人工留意） |
| 12 | test | Who is the son of the author of the short story "The Enormou | Benjamin Hale Cheever | 'Ray Bradbury' | incorrect | gold 未命中 |
| 13 | train | What airline holding company located in Solna Municipality,  | SAS Group | 'SAS Group' | correct | gold 命中（含等价/别名） |
| 14 | train | Which of Kylian Hazard's older brothers plays for the German | Thorgan Ganael Francis H | 'Eden Hazard' | incorrect | gold 未命中 |
| 15 | train | What is the character's name for which Anna Leonidovna Koval | Chief Detective Maria Sh | 'Masha.' | incorrect | 单 token 短答 'Masha.'（疑似错答，人工留意） |
| 16 | test | Who was born first, Samantha Cristoforetti or Jean-Loup Chré | Jean-Loup Jacques Marie  | 'Jean-Loup Chrétien was born first.' | incorrect | gold 未命中 |
| 17 | validation | Indie studio Jumpship developed what puzzle-platform video g | Limbo | 'Braid' | incorrect | 单 token 短答 'Braid'（疑似错答，人工留意） |
| 18 | test | Which star of Zork was also the voice of Pac-Man? | Martin Ingerman | 'Tim Allen.' | incorrect | gold 未命中 |
| 19 | train | Which football club appeared in the 2015 FA Community Shield | Chelsea | 'Manchester City' | incorrect | gold 未命中 |
| 20 | test | Who was convicted of murdering the director of Schoolboy Cru | Harlow Cuadra and Joseph | 'George Wallace.' | incorrect | gold 未命中 |
| 21 | train | What is the birth name of the woman that "A Woman Called Mos | Araminta Ross | 'Mary Brown.' | incorrect | gold 未命中 |
| 22 | train | Which player signed to Bayern Munich before the 2012-2013 se | Dante | 'Thomas Manuel Neuer' | incorrect | gold 未命中 |
| 23 | validation | The large subunit and small subunit that use two types of RN | Ribosomes | 'The large subunit and small subunit that use two t' | incorrect | gold 未命中 |
| 24 | test | Piers Bizony has written articles for which magazine based i | BBC Focus | 'The Guardian' | incorrect | gold 未命中 |
| 25 | train | Gaia is a space observatory of the European Space Agency, wh | India's first dedicated  | 'Astrosat is a Russian weather satellite.' | incorrect | gold 未命中 |
| 26 | train | What type of bank organization is Pondicherry Gramin Bank th | Regional Rural Bank | 'Pondicherry Gramin Bank is a public sector bank.' | incorrect | gold 未命中 |
| 27 | train | When the two Coldplay songs U.F.O and Princess of China were | was written by all four  | 'China.' | incorrect | 单 token 短答 'China.'（疑似错答，人工留意） |
| 28 | test | Thomas Henry Moray Followed work down on nuclear batteries i | Henry Moseley | 'Ern Rutherford' | incorrect | gold 未命中 |
| 29 | test | Lady Elizabeth Delmé and Her Children (1779) is a portrait g | Washington, D.C. | 'Washington' | incorrect | 单 token 短答 'Washington'（疑似错答，人 |
| 30 | test | Fantasy Records is know for recordings of comedian Lenny Bru | Vincent Anthony Guaraldi | 'Charlie Parker.' | incorrect | gold 未命中 |
| 31 | train | In which city are Anadoluhisarı and Church of St. Mary of Bl | Istanbul | 'Anadoluhisarı and Church of St. Mary of Blachernae' | correct | gold 命中（含等价/别名） |
| 32 | train | Was Atom Egoyans biggest commercial success on stage or on f | erotic thriller film | "Atom Egoyans' biggest commercial success was on fi" | incorrect | gold 未命中 |
| 33 | validation | What country is home to both Guadarrama National Park and Do | Spain | 'Spain' | correct | gold 命中（含等价/别名） |
| 34 | train | Mount Austin Barracks is located near the Peak Tram terminus | Victoria Peak | 'Mount Austin Barracks is located near the Peak Tra' | incorrect | gold 未命中 |
| 35 | train | Alex Haley wrote what novel about a man that was born in 175 | Roots: The Saga of an Am | 'Alex Haley wrote Roots.' | incorrect | gold 未命中 |
| 36 | train | What actress starred in "The Golden Girls" and was an animal | Bea Arthur | 'Whoopi Goldberg' | incorrect | gold 未命中 |
| 37 | test | What company claims to manufacture one out of every three ob | Crown Holdings Incorpora | 'The company that claims to manufacture one out of ' | incorrect | gold 未命中 |
| 38 | train | After coaching the red raiders to several winning seasons, w | Washington State | 'Mike Leach currently coaches at the Oakland Raider' | incorrect | gold 未命中 |
| 39 | test | What song was created by the group consisting of Jeffrey Jey | Blue | 'The song is "The Mission."' | incorrect | gold 未命中 |
| 40 | validation | Who was the husband of the prominent Walton family member wh | Sam Walton | 'The husband of the prominent Walton family member ' | incorrect | gold 未命中 |
| 41 | train | BOTH Skyang Kangri and Pumari Chhish are both what? | subrange of the Karakora | 'Mountains.' | incorrect | 单 token 短答 'Mountains.'（疑似错答，人 |
| 42 | validation | W. Tresper Clarke High School is in what county? | Nassau County | 'W. Tresper Clarke High School is in Clarke County,' | incorrect | gold 未命中 |
| 43 | validation | How many members does the Tennessee Volunteers football team | fourteen members | "The Tennessee Volunteers football team's conferenc" | incorrect | gold 未命中 |
| 44 | test | What retailer in ABQ Uptown is headquarted in Poole, Dorset, | Lush Ltd. | 'ABQ' | incorrect | 单 token 短答 'ABQ'（疑似错答，人工留意） |
| 45 | validation | When was the father of Princess Mafalda of Savoy born ? | 11 November 1869 | 'The father of Princess Mafalda of Savoy, Prince Al' | incorrect | gold 未命中 |
| 46 | train | What Russian ballet choreographer restaged a play based on a | Alexander Gorsky | 'Julius Petipa.' | incorrect | gold 未命中 |
| 47 | train | Which 1962 film starring Tom Courtenay is based on a short s | The Loneliness of the Lo | 'The Window.' | incorrect | gold 未命中 |
| 48 | test | What is the title of the person who is Head of the Departmen | Doctor | 'Professor' | incorrect | 单 token 短答 'Professor'（疑似错答，人工 |
| 49 | train | What Hindi thriller directed by Deepak SHivdasani features c | Julie 2 | 'Dhoom' | incorrect | 单 token 短答 'Dhoom'（疑似错答，人工留意） |
| 50 | test | Július Satinský was born in a city that has a current popula | about 450,000 | 'Július Satinský was born in Prague, Czech.' | incorrect | gold 未命中 |
| 51 | train | The Northern Chamber Orchestra gives concerts at what estate | Tatton Park | 'Walton Hall' | incorrect | gold 未命中 |
| 52 | train | What league, which is also known as the Barclays Premier Lea | The 2013–14 Premier Leag | 'The English Premier League.' | incorrect | gold 未命中 |
| 53 | test | Which team's 2013-2014 season had players including a Sloven | the Phoenix Suns | 'The Boston Celtics.' | incorrect | gold 未命中 |
| 54 | test | Robert Jan van Pelt testified for the defense in this "Churc | David Irving | 'David Irving.' | correct | gold 命中（含等价/别名） |
| 55 | train | What indigenous American ethnic group that inhabits land in  | Odawa | 'The Cree.' | incorrect | gold 未命中 |
| 56 | test | Which actress played a character that dated Mark Brendanawic | Rashida Jones | 'Jennifer Aniston' | incorrect | gold 未命中 |
| 57 | train | Alfred Balk served as the secretary of the Committee on the  | Nelson Rockefeller | 'Walter Mondale' | incorrect | gold 未命中 |
| 58 | train | Was the famous opera comique that was based on a Prosper Mer | "Carmen", perhaps the mo | 'The famous opera comique based on a Prosper Merime' | incorrect | gold 未命中 |
| 59 | train | Which American spy thriller TV series, which was developed b | Homeland | 'Homeland' | correct | gold 命中（含等价/别名） |
| 60 | train | The Stone Book series is set in what country? | North West England | 'England' | incorrect | 单 token 短答 'England'（疑似错答，人工留意 |
| 61 | train | What else was Baghdad known as during the Abbasid Caliphate? | the City of Peace | 'Baghdad was also known as Constantinople during th' | incorrect | gold 未命中 |
| 62 | train | Who was born in Ireland and has coached the captain of MLS c | Des McAleenan | 'Kevin Keegan' | incorrect | gold 未命中 |
| 63 | test | Kate Ashfield plays what role in the 2004 British horror com | Liz | 'Kate Ashfield plays the role of Kelly.' | incorrect | gold 未命中 |
| 64 | train | What actor from Northern Ireland born in 1983 starred in Who | Martin "Marty" McCann | 'Tom Hardy.' | incorrect | gold 未命中 |
| 65 | validation | What is the name of a Sri Lankan political party associated  | The Sri Lanka Freedom Pa | 'The National Party.' | incorrect | gold 未命中 |
| 66 | train | What is the name of the English poet who wrote a poem titled | Lord Byron | 'Lord Byron' | correct | gold 命中（含等价/别名） |
| 67 | validation | What is the mascot of the oldest private university in Georg | The Bears | 'The mascot of the oldest private university in Geo' | incorrect | gold 未命中 |
| 68 | train | What race track in the midwest hosts a 500 mile race eavery  | Indianapolis Motor Speed | 'Indianapolis Motor Speedway' | correct | gold 命中（含等价/别名） |
| 69 | train | What former two-weight world champion is represented by boxi | Tomasz Adamek | 'Mike Tyson.' | incorrect | gold 未命中 |
| 70 | train | What 1991 Disney film is also a 1946 French romantic fantasy | Beauty and the Beast | 'Fantasia' | incorrect | 单 token 短答 'Fantasia'（疑似错答，人工留 |
| 71 | train | St Anne's Academy is an 11–18 mixed comprehensive academy is | 42,972 | '15,000' | incorrect | gold 未命中 |
| 72 | train | Which jazz singer has a 2003 album entitled The Boy Next Doo | Stacey Kent | 'Bill Evans.' | incorrect | gold 未命中 |
| 73 | train | What is the species of animal which the town of Antelope, Ka | Antilocapra americana | 'The town of Antelope, Kansas was named after the A' | incorrect | gold 未命中 |
| 74 | train | Which band formed in England, Of Montreal or Vib Gyor? | Vib Gyor was a band that | 'Vib Gyor' | correct | gold 命中（含等价/别名） |
| 75 | train | What is the birthplace of the musician responsible for creat | Tennessee | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 76 | train | What scientist as well as a practising Roman Cathloic descri | Konstantīns Raudive | 'John Gray.' | incorrect | gold 未命中 |
| 77 | test | Which group did Masta Kill released Selling My Soul under? | Wu-Tang Clan | 'Cash Money Records' | incorrect | gold 未命中 |
| 78 | test | Jacques Coghen is a direct ancestor to the spouse of which B | Queen Mathilde | 'Jacques Coghen is a direct ancestor to the spouse ' | incorrect | gold 未命中 |
| 79 | test | The channel that has interviewed players such as the forward | YouTube | 'YouTube' | correct | gold 命中（含等价/别名） |
| 80 | train | Between two scientists Ernst Messerschmid and Philippe Perri | Ernst Willi Messerschmid | 'Ernst Messerschmid was born in 1891, while Philipp' | incorrect | gold 未命中 |
| 81 | train | Orange is the New Black, starring Annie Golden as Norma Roma | FCI Danbury | 'Felix.' | incorrect | 单 token 短答 'Felix.'（疑似错答，人工留意） |
| 82 | test | What is the birthday of the oldest among Vicente García and  | March 30, 1983 | 'Vicente García' | incorrect | gold 未命中 |
| 83 | train | What military formation were participated in by both Oscar W | Third Army | 'World War II' | incorrect | gold 未命中 |
| 84 | train | What is the country of origin of the film Dui Purush and the | Bengali | 'India' | incorrect | 单 token 短答 'India'（疑似错答，人工留意） |
| 85 | test | What age was Georgia Middleman when she started singing in t | ten | '16' | format_failure | 单 token 函数词/碎片 '16'，无答案内容 |
| 86 | validation | Former race car driver Jeff Wood made his CART debut at whic | Caesars Palace Grand Pri | 'San Diego.' | incorrect | gold 未命中 |
| 87 | test | The Church at Hoxne was dedicated to Edmund the Martyr who w | king of East Anglia | 'England' | incorrect | 单 token 短答 'England'（疑似错答，人工留意 |
| 88 | train | Which two occupations does Ronnie Dunn and Annie Lennox have | singer, songwriter | 'Singer and songwriter.' | incorrect | gold 未命中 |
| 89 | validation | This man who was born on April 25th, 1947, was a member of t | Robert "Bobby" Bunda | 'House of Representatives' | incorrect | gold 未命中 |
| 90 | train | Who was the final champion of the Thailand Masters that was  | Marco Fu | 'Stephen Lee.' | incorrect | gold 未命中 |
| 91 | train | In what California city was the first Torrid location opened | Brea, California | 'The first Torrid location was opened in San Diego,' | incorrect | gold 未命中 |
| 92 | train | In what part of Scotland is Bass Rock located? | the Firth of Forth in th | 'Bass Rock is located in the northern part of Scotl' | incorrect | gold 未命中 |
| 93 | validation | Bobby Bowden coached which former Toronto Blue Jays minor le | Chris Weinke | 'Mike Hampton.' | incorrect | gold 未命中 |
| 94 | train | New Jersey politicians Linda Stender and Leonard Lance were  | 1952 | '1949' | incorrect | 单 token 短答 '1949'（疑似错答，人工留意） |
| 95 | train | What Danish eurodance group had a single called "Barbie Girl | Aqua | 'The Danish eurodance group that had a single calle' | incorrect | gold 未命中 |
| 96 | train | How many times has the driver who placed third in the 2003 I | 11 | '2' | format_failure | 单 token 函数词/碎片 '2'，无答案内容 |
| 97 | train | Which of the starting pitchers for Team USA in the Baseball  | Ben Sheets | 'John Franco.' | incorrect | gold 未命中 |
| 98 | validation | When did Henrietta Ponsonby's father die? | 31 October 1783 | "Henrietta Ponsonby's father died in 1761." | incorrect | gold 未命中 |
| 99 | train | The Swallow Bluff Island Mounds is a Mississippian culture a | the Cherokee River | 'The Swallow Bluff Island Mounds is a Mississippian' | incorrect | gold 未命中 |
| 100 | train | What is the birthday of the author of "She Walks These Hills | February 26, 1948 | 'The author of "She Walks These Hills" is Maya Ange' | incorrect | gold 未命中 |
| 101 | train | What is the river that Sangin is found in the valley of the  | Sistan Basin | 'Sang River' | incorrect | gold 未命中 |
| 102 | train | Which Arab World's car was used in a American action film di | Lykan Hypersport | 'The Ford Mustang.' | incorrect | gold 未命中 |
| 103 | train | What type of media do Peter Filkins and The New Criterion ha | journal | 'Peter Filkins and The New Criterion are both film-' | incorrect | gold 未命中 |
| 104 | train | WHAT WAS THE NAME OF THE BOOK MADE INTO THE 2015 SOUTH KOREA | "Murder Request" | 'The name of the book made into the 2015 South Kore' | incorrect | gold 未命中 |
| 105 | train | What is the altitude of the town in England that has Leadgat | about 1,000 ft above sea | 'The town in England that has Leadgate between it a' | incorrect | gold 未命中 |
| 106 | train | The "civic rally cross" was sold alongside what other model  | Honda Ballade | 'The Honda Civic.' | incorrect | gold 未命中 |
| 107 | test | Beena Sarwar is the editor of a peace initiative sponsored b | Karachi, Pakistan | 'Beena Sarwar is the editor of a peace initiative s' | incorrect | gold 未命中 |
| 108 | validation | What current state is the location of unrecognized and auton | Tennessee | 'Tennessee' | correct | gold 命中（含等价/别名） |
| 109 | train | What is the fourth most populous urban area in the Republic  | Galway | 'Dublin' | incorrect | 单 token 短答 'Dublin'（疑似错答，人工留意） |
| 110 | test | Johnny Edwards and Ian Anderson are singers, who had joined  | John Douglas "Johnny" Ed | 'Ian Anderson' | incorrect | gold 未命中 |
| 111 | validation | What award won by only twelve people has a man who Ted Koosh | EGOT | 'Grammy' | incorrect | 单 token 短答 'Grammy'（疑似错答，人工留意） |
| 112 | test | What man is linked to both Johnny Tremain and Magic Kingdom? | Walt Disney | 'Jack Black.' | incorrect | gold 未命中 |
| 113 | train | Who did the player nicknamed "The Human Highlight Film" play | Boston Celtics | 'Los Angeles Lakers' | incorrect | gold 未命中 |
| 114 | train | How many assists did the Bosnian football player account for | 20 assists | '4' | format_failure | 单 token 函数词/碎片 '4'，无答案内容 |
| 115 | validation | What type of industry does Tony Bill and Flyboys have in com | film | 'Tony Bill and Flyboys are both music artists.' | incorrect | gold 未命中 |
| 116 | train | Blank Check and Air Bud are both examples of what type of mo | American comedy | 'Comedy.' | incorrect | 单 token 短答 'Comedy.'（疑似错答，人工留意 |
| 117 | test | What is the year of the event which orrurred first, Beecher' | 1907 | "Beecher's Handmade Cheese was founded in 1905, whi" | correct | gold 命中（含等价/别名） |
| 118 | train | The William Ulmer Brewery is located in a neighborhood that  | NYPD's 83rd Precinct | 'The William Ulmer Brewery is located in a neighbor' | incorrect | gold 未命中 |
| 119 | test | Milo Parker starred in which 2014 movie alongside Gillian An | Robot Overlords | 'Milo Parker starred in the 2014 movie "The Family"' | incorrect | gold 未命中 |
| 120 | train | In what town does the one-time star of "And There's More" no | Rochdale | 'London.' | incorrect | 单 token 短答 'London.'（疑似错答，人工留意 |
| 121 | test | Mr. Wilson's Cabinet of Wonder: Pronged Ants, Horned Humans, | Los Angeles | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 122 | validation | Luther: The Calling is based on the BBC crime drama comprisi | 2010 | '2003' | incorrect | 单 token 短答 '2003'（疑似错答，人工留意） |
| 123 | train | Howard Bilerman produced an album for which songwriter from  | Vic Chesnutt | 'Bob Dylan.' | incorrect | gold 未命中 |
| 124 | test | Which dog is considered a giant dog breed, the Leonberger or | The Leonberger is a gian | 'The Leonberger.' | correct | gold 命中（含等价/别名） |
| 125 | train | Which actress does this Netflix's project by Nick Bernardone | Ellie Kemper | ' Tina Fey' | incorrect | gold 未命中 |
| 126 | train | The American short horror The sub stars which American actre | Heather Langenkamp | 'Nancy Travis.' | incorrect | gold 未命中 |
| 127 | test | What ABC television series was inspired by a 2011 film and c | Agent Carter | 'Avengers' | incorrect | 单 token 短答 'Avengers'（疑似错答，人工留 |
| 128 | validation | What was the address of the penitentiary where Jimmy Elliot  | 2027 Fairmount Avenue | 'Unknown' | format_failure | 规则检出拒答 |
| 129 | train | What is the year of the event that occured first, Skeeter st | 1979 | '1961' | incorrect | 单 token 短答 '1961'（疑似错答，人工留意） |
| 130 | train | Who played the crime boss considered the father of modern or | Andy García | 'Al Pacino' | incorrect | gold 未命中 |
| 131 | train | The was the album with the song Unbelievable by American rap | September 13, 1994 | 'The album with the song "Unbelievable" by American' | incorrect | gold 未命中 |
| 132 | test | Who was born first Burton Cummings or Sharleen Spiteri? | Burton Lorne Cummings | 'Sharleen Spiteri was born first.' | incorrect | gold 未命中 |
| 133 | train | The Shrewsbury & Newport Canals Trust promotes the restorati | Shropshire Union Canal | 'The Shrewsbury & Newport Canals Trust promotes the' | incorrect | gold 未命中 |
| 134 | train | What year was the midfielder who shot the winning goal in th | 1988 | 'The midfielder who shot the winning goal in the 20' | incorrect | gold 未命中 |
| 135 | train | In what country does the director of Shirin in Love, live? | Iranian | 'Iran' | incorrect | 单 token 短答 'Iran'（疑似错答，人工留意） |
| 136 | train | What concert hall is located on the northern edge or South K | Royal Albert Hall | 'Royal Albert Hall' | correct | gold 命中（含等价/别名） |
| 137 | validation | Which ocean would the ingredients likely come from for the S | Atlantic Ocean | 'The ingredients for She-crab soup would likely com' | correct | gold 命中（含等价/别名） |
| 138 | test | Which Russian professional ice hockey player, known as the M | Pavel Valerievich Datsyu | 'Alexander Kovalchuk' | incorrect | gold 未命中 |
| 139 | test | Both Bishop Carroll Catholic High School and Kapaun Mt. Carm | Wichita | 'Both Bishop Carroll Catholic High School and Kapau' | correct | gold 命中（含等价/别名） |
| 140 | train | Metro West Ambulance serves event support for the building i | Rose Garden | 'The Rose Garden' | correct | gold 命中（含等价/别名） |
| 141 | test | What current NHL team owner played for the team that won the | Mario Lemieux | 'David Lee.' | incorrect | gold 未命中 |
| 142 | train | Myron F. Diduryk's exploits were described in a book by an a | lieutenant general | 'Colonel' | incorrect | 单 token 短答 'Colonel'（疑似错答，人工留意 |
| 143 | train | The first book in the Sprawl Trilogy won what three awards? | Nebula Award, the Philip | 'The first book in the Sprawl Trilogy, "Sprawl," wo' | incorrect | gold 未命中 |
| 144 | train | Who is younger, Billy Idol or Ray Wilson? | Raymond Wilson | 'Ray Wilson' | incorrect | gold 未命中 |
| 145 | train | Daddy was an American Pit Bull who was integral to the work  | Cesar Millan | 'Cesar Milan.' | incorrect | gold 未命中 |
| 146 | train | What was the other name of the textile mill on which The Mil | Styal Mill | 'The Cotton Mill' | incorrect | gold 未命中 |
| 147 | train | In what year did Farda Amiga win a race at the Saratoga Race | (foaled February 1, 1999 | 'Farda Amiga won a race at the Saratoga Race Course' | incorrect | gold 未命中 |
| 148 | test | The St. Louis Bay Bridge runs between Bay St. Louis and a ci | Harrison County, Mississ | 'The St. Louis Bay Bridge runs between Bay St. Loui' | incorrect | gold 未命中 |
| 149 | train | In the 2012-13 FC Sion they brought in Gennaro Gattuso and a | Scottish Premiership clu | 'Celtic' | incorrect | 单 token 短答 'Celtic'（疑似错答，人工留意） |
| 150 | train | The Hindmarsh Stadium is sponsored by a brewery that sold ho | 69.7 million litres | 'The Hindmarsh Stadium is sponsored by a brewery th' | incorrect | gold 未命中 |
| 151 | train | Which Hells Angel member stabbed and beat an attendant of th | Alan Passaro | 'Tom Wilson.' | incorrect | gold 未命中 |
| 152 | test | WHICH GROUP OF PEOPLE NICKNAMED THE US ARMYS REGIMENT "BUFFA | Native American tribes | "The group of people who nicknamed the US Army's re" | correct | gold 命中（含等价/别名） |
| 153 | train | Are Bangkok Girl and Home both horror movies? | no | 'No, Bangkok Girl and Home are not both horror movi' | correct | gold 命中（含等价/别名） |
| 154 | train | Which professional baseball player and National 1993 Basebal | Reginald Martinez "Reggi | 'Ted Williams.' | incorrect | gold 未命中 |
| 155 | train | St. John's College, Belize offers an education in a traditio | Grammar, logic, and rhet | 'Latin, Greek, and Mathematics' | incorrect | gold 未命中 |
| 156 | test | What was the author of Freeway Warrior's original occupation | Originally a musician | 'Writer.' | incorrect | 单 token 短答 'Writer.'（疑似错答，人工留意 |
| 157 | train | Who co-wrote The Hidden History of the Human Race with a man | Richard L. Thompson | 'Graham Hancock.' | incorrect | gold 未命中 |
| 158 | test | The actress who played Clementine Churchill in "The Crown" j | Paula D'Alessandris | 'David Hare.' | incorrect | gold 未命中 |
| 159 | train | The terminology of algebraic geometry changed drastically wi | German | 'German' | correct | gold 命中（含等价/别名） |
| 160 | train | The term snake eyes is used in a particular casino game that | a pair of dice | 'Dice' | incorrect | 单 token 短答 'Dice'（疑似错答，人工留意） |
| 161 | train | Whom was the cofounder of Orange County Choppers and appeare | Paul Teutul Jr. | 'Bob Johnson.' | incorrect | gold 未命中 |
| 162 | train | The Jodrell Bank Observatory was established in 1945 by what | Sir Alfred Charles Berna | 'John Bell.' | incorrect | gold 未命中 |
| 163 | train | Who is the mother of the princess who opened Middleton Grang | Princess Elizabeth | 'Queen Elizabeth II' | incorrect | gold 未命中 |
| 164 | test | Why does the City of Boston get their christmas tree from Ai | for their assistance aft | 'The City of Boston gets their Christmas tree from ' | incorrect | gold 未命中 |
| 165 | validation | Bobby Godsell held a senior position in which global company | AngloGold Ashanti | 'British Airways' | incorrect | gold 未命中 |
| 166 | train | What's the name of the differential equation that was develo | Lommel differential equa | 'The name of the differential equation developed by' | incorrect | gold 未命中 |
| 167 | validation | Iselin Solheim provided vocals in the song released on what  | 3 December | 'Iselin Solheim provided vocals in the song "The Mi' | incorrect | gold 未命中 |
| 168 | train | Which song, released on December 7, 2008 was co-written by L | White Horse | '"Hello"' | incorrect | 单 token 短答 '"Hello"'（疑似错答，人工留意 |
| 169 | train | An American who is a German literature translator and did a  | University of Vienna | 'Harvard University' | incorrect | gold 未命中 |
| 170 | test | The actress who played Laurie Keller in the episode "Pilot"  | Critics' Choice Televisi | 'The actress who played Laurie Keller in the episod' | incorrect | gold 未命中 |
| 171 | train | What was the air date of "The Simpsons" episode written by M | May 21, 2000 | 'The air date of "The Simpsons" episode written by ' | incorrect | gold 未命中 |
| 172 | test | What church was the college Marjorie Hass is the 20th presid | Presbyterian Church | 'The Episcopal Church.' | incorrect | gold 未命中 |
| 173 | train | The current coach of the Los Angeles Clippers was signed as  | 1994–95 NBA season | '2000-2001' | incorrect | 单 token 短答 '2000-2001'（疑似错答，人工 |
| 174 | validation | Who wrote the 1970 international hit song Murray Head is mos | Andrew Lloyd Webber and  | 'Murray Head.' | incorrect | gold 未命中 |
| 175 | train | What party does the House of Commons representative for Cong | British Conservative Par | 'The House of Commons representative for Congleton ' | incorrect | gold 未命中 |
| 176 | train | In the USA, gun powder is used in conjunction with this to s | Anvil firing | 'Fireworks' | incorrect | 单 token 短答 'Fireworks'（疑似错答，人工 |
| 177 | train | Inserra Supermarkets is a supermarket chain that is a member | Wakefern Food Corporatio | 'Inserra Supermarkets is a member of the New Jersey' | incorrect | gold 未命中 |
| 178 | test | Which car brand was one step above the brand started on Nove | Oakland | 'Cadillac' | incorrect | 单 token 短答 'Cadillac'（疑似错答，人工留 |
| 179 | train | Who is the author of the play that was adapted into a film a | William Shakespeare | 'The author of the play that was adapted into a fil' | correct | gold 命中（含等价/别名） |
| 180 | validation | The 2014–15 UEFA Champions League knockout phase lead to the | European Champion Clubs' | 'the European Cup' | incorrect | gold 未命中 |
| 181 | test | What languages is the journal that Michel Feher semi-regular | French, English and Span | 'The journal that Michel Feher semi-regularly blogs' | incorrect | gold 未命中 |
| 182 | train | Sum 41 and Passion Pit have what in common? | Passion Pit is an Americ | 'Sum 41 and Passion Pit are both American punk rock' | incorrect | gold 未命中 |
| 183 | validation | Are Sandy Mayer and Billy Martin both more successful at dou | yes | 'Yes, both Sandy Mayer and Billy Martin are more su' | correct | gold 命中（含等价/别名） |
| 184 | train | Which founding member drew critical acclaim as a bass guitar | Mike" Mills | ' Damon Albarn' | incorrect | gold 未命中 |
| 185 | train | Do Matthew Good Band and Sleep Room play the same type of mu | yes | 'No, Matthew Good Band and Sleep Room do not play t' | incorrect | gold 未命中 |
| 186 | train | Where is the usual main ingredient of Hákarl normally found? | North Atlantic Ocean and | 'Iceland.' | incorrect | 单 token 短答 'Iceland.'（疑似错答，人工留 |
| 187 | validation | What occupations do Charles Burnett and Alan J. Pakula have  | film director, film prod | 'Charles Burnett and Alan J. Pakula are both film d' | incorrect | gold 未命中 |
| 188 | train | What title did the actor who worked with Sivaji Ganesan in a | politician | 'actress' | incorrect | 单 token 短答 'actress'（疑似错答，人工留意 |
| 189 | train | Folie à Deux is a studio album by the American rock band for | Wilmette | 'Los Angeles' | incorrect | gold 未命中 |
| 190 | test | Les Patterson Saves the World was a comedy film starring the | My Gorgeous Life | 'Being Les.' | incorrect | gold 未命中 |
| 191 | train | Which author dedicated a 1985 romance novel to the author wh | Eva Ibbotson | 'Barbara Michaels.' | incorrect | gold 未命中 |
| 192 | validation | What Manchester United and Portuguese national winger scored | Nani | ' Cristiano Ronaldo' | incorrect | gold 未命中 |
| 193 | test | whats the famous bavagheet by arun date? | Shukratara | 'Zero.' | incorrect | 单 token 短答 'Zero.'（疑似错答，人工留意） |
| 194 | train | Swiss music duo Double released their best known single "The | 1986 | '1986' | correct | gold 命中（含等价/别名） |
| 195 | validation | Which American novelist was notable primarily for publishing | Philip Kindred Dick | 'Philip K. Dick' | format_failure | 输出为问句回显，无答案内容 |
| 196 | train | When was the college which Albert Simons taught at founded? | 1770 | '1854' | incorrect | 单 token 短答 '1854'（疑似错答，人工留意） |
| 197 | train | Which cast member of Alice Upside Down also stars in the ABC | Lucas Stephen Grabeel | 'Ashley Johnson.' | incorrect | gold 未命中 |
| 198 | train | What is the date of the reissue of one of Rhihanna's album t | June 2, 2008 | 'The date of the reissue of Rihanna\'s album "Fugees' | incorrect | gold 未命中 |
| 199 | test | Bobby Arora is the trading director of a retail chain that w | 1978 | "Bobby Arora is the trading director of McDonald's," | incorrect | gold 未命中 |
| 200 | train | The Swiss immigration referendum, February 2014 is an exampl | relations between Switze | 'The Swiss immigration referendum, February 2014 is' | incorrect | gold 未命中 |
| 201 | test | What is this group referred to as that this Russian composer | The Five | 'The Russian Five.' | incorrect | gold 未命中 |
| 202 | validation | Who has released more solo albums, Ozzy Osbourne or Curt Smi | John Michael "Ozzy" Osbo | 'Ozzy Osbourne' | correct | gold 命中（含等价/别名） |
| 203 | validation | What city was the band who "Evie" formed in? | Sydney, Australia | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 204 | train | What actor, who passed away in 1942 was also the producer of | George M. Cohan | 'Ralph Richardson.' | incorrect | gold 未命中 |
| 205 | train | What 1958 born American television writer and actress contri | Deborah "Deb" Lacusta | 'Jane Espenson' | incorrect | gold 未命中 |
| 206 | train | Are Trent Edwards and Lucy Saroyan both football players? | no | 'Yes, both Trent Edwards and Lucy Saroyan are footb' | incorrect | gold 未命中 |
| 207 | train | Who was the brother of the architect of Hook and Ladder No.  | Cuyler Reynolds | 'William Livingston.' | incorrect | gold 未命中 |
| 208 | train | Which magazine was founded first, Allure or Genre? | Allure is an American wo | 'Allure' | incorrect | 单 token 短答 'Allure'（疑似错答，人工留意） |
| 209 | train | Tedrow, Ohio lies close to which 241. 26 mi highway? | Ohio Turnpike | 'Tedrow, Ohio lies close to Interstate 70.' | incorrect | gold 未命中 |
| 210 | train | Who was the First Prophert to the sixth Pharaoh of the Eight | Khonsu | 'Yuya.' | incorrect | 单 token 短答 'Yuya.'（疑似错答，人工留意） |
| 211 | train | Which British engineering company is best known for its luxu | D. Napier & Son | 'Stanley' | incorrect | 单 token 短答 'Stanley'（疑似错答，人工留意 |
| 212 | train | Which 8-year old star of an epistolary novel turned musical  | Diamond White | 'Justin Paul.' | incorrect | gold 未命中 |
| 213 | train | The casino owner who was focused on the documentary Nobody S | American | 'American' | correct | gold 命中（含等价/别名） |
| 214 | test | Who beacme a star as a comic book character created by Gerry | Megalyn Echikunwoke | 'Spider-Man.' | incorrect | 单 token 短答 'Spider-Man.'（疑似错答， |
| 215 | train | Are Yingkou and Fuding the same level of city? | no | 'No, Yingkou and Fuding are not the same level of c' | correct | gold 命中（含等价/别名） |
| 216 | test | What is the nationality of the man who finished second for A | Russia | 'British' | incorrect | 单 token 短答 'British'（疑似错答，人工留意 |
| 217 | train | What award was won by the director who directed the eighth m | Tony Award | 'Academy Award' | incorrect | gold 未命中 |
| 218 | test | Geoffrey Serle wrote a biography about which Australian mili | John Monash | 'Geoffrey Serle wrote a biography about General Wil' | incorrect | gold 未命中 |
| 219 | test | The winner of the FIA World Endurance Championship in 2013 d | Mika Salo | 'Toyota Racing.' | incorrect | gold 未命中 |
| 220 | validation | What type of sport does Sergio Casal and Manuel Orantes have | tennis | 'Sergio Casal and Manuel Orantes are both tennis pl' | correct | gold 命中（含等价/别名） |
| 221 | test | What institution does 2017 Texas Tech Red Raiders baseball t | Texas Tech University | 'The 2017 Texas Tech Red Raiders baseball team and ' | correct | gold 命中（含等价/别名） |
| 222 | train | What science fantasy young adult series, told in first perso | Animorphs | 'The Expanse' | incorrect | gold 未命中 |
| 223 | train | Where did the designer of the Van de Graaff generator teach  | Princeton University and | 'Princeton University' | correct | gold 命中（含等价/别名） |
| 224 | train | Who won more academy awards, Joseph L. Mankiewicz or Tony Ka | Joseph Leo Mankiewicz | 'Joseph L. Mankiewicz' | format_failure | 输出为问句回显，无答案内容 |
| 225 | train | When was the son of Kingsley Amis born ? | 1949 | '1961' | incorrect | 单 token 短答 '1961'（疑似错答，人工留意） |
| 226 | test | Whose given first name is longer, Theo Angelopoulos and Budd | Theodoros "Theo" Angelop | 'Theo' | incorrect | 单 token 短答 'Theo'（疑似错答，人工留意） |
| 227 | test | Who is the former pentecostal preacher who released the come | Sam Kinison | 'Tom Jones.' | incorrect | gold 未命中 |
| 228 | train | Psycho-physical Awareness was developed into an original and | his most brilliant stude | 'The Master.' | incorrect | gold 未命中 |
| 229 | validation | Armageddon in Retrospect was written by the author who was b | Slaughterhouse-Five | 'Armageddon in Retrospect was written by Joseph Hel' | incorrect | gold 未命中 |
| 230 | train | Who was the director of 1935 American crime drama film, whic | Tim Whelan | 'The director of the 1935 American crime drama film' | incorrect | gold 未命中 |
| 231 | test | Pramod Bhasin was the former CEO of a company that provided  | IT | 'Pramod Bhasin was the former CEO of Tata Power.' | incorrect | gold 未命中 |
| 232 | train | Which British Indian novelist and essayist did Anthony Burge | Salman Rushdie | ' Salman Rushdie.' | correct | gold 命中（含等价/别名） |
| 233 | test | What topic does GeekDad cover that pertains to a line of pla | Lego | 'GeekDad covers the topic of LEGO bricks.' | correct | gold 命中（含等价/别名） |
| 234 | test | What character did James Byron Dean play in his final lead r | ranch hand Jett Rink | 'James Byron Dean played the character of James Dea' | incorrect | gold 未命中 |
| 235 | train | What other method of extending an ice hockey game exists oth | the shootout | 'The other method of extending an ice hockey game i' | correct | gold 命中（含等价/别名） |
| 236 | validation | Daniel Greene has created what for clients including sportsc | portrait | 'portraits' | incorrect | 单 token 短答 'portraits'（疑似错答，人工 |
| 237 | test | Which KaBoom! Entertainment Inc. film is based on a story by | The Jungle Book (1894) | 'The Jungle Book' | correct | gold 命中（含等价/别名） |
| 238 | train | What Friday night programming block included what collective | Cartoon Cartoon Fridays | 'Adult Swim' | incorrect | gold 未命中 |
| 239 | validation | What championship did the person who substituted for Simon P | Australian Supercars Cha | 'Formula One.' | incorrect | gold 未命中 |
| 240 | train | Are David O. Russell and Tony Gatlif from the same country? | no | 'No, David O. Russell and Tony Gatlif are not from ' | correct | gold 命中（含等价/别名） |
| 241 | train | What animation company produced the first season of an anima | Goldie & Bear | ' Cartoon Network.' | incorrect | gold 未命中 |
| 242 | train | In what century did this Native warrior and chief, whose bro | nineteenth | 'In the 19th century, this Native warrior and chief' | incorrect | gold 未命中 |
| 243 | train | Who was the ruler ousted by the 30th Prime Minister of Cambo | Prince of Cambodia Norod | 'The ruler ousted by the 30th Prime Minister of Cam' | incorrect | gold 未命中 |
| 244 | test | What Ruben Fleischer film did No One's Gonna Love You appear | Zombieland | "No One's Gonna Love You appeared in the film Dirty" | incorrect | gold 未命中 |
| 245 | validation | Were the films Tonka and 101 Dalmatians released in the same | 1958 Walt Disney Western | 'No, the films Tonka and 101 Dalmatians were not re' | incorrect | gold 未命中 |
| 246 | test | What number largest commercial airline in the United States  | 8th | 'third' | incorrect | 单 token 短答 'third'（疑似错答，人工留意） |
| 247 | validation | Where are schools in the athletic association Cardinal Hayes | New York City, Long Isla | 'Cardinal Hayes High School is part of the Kansas C' | incorrect | gold 未命中 |
| 248 | train | What literary style describes the 1968 book that features a  | the growing literary sty | 'The literary style that describes the 1968 book "T' | incorrect | gold 未命中 |
| 249 | train | What Australian Electoral Division in New South Wales create | Division of Cook | 'Division of Alexandria' | incorrect | gold 未命中 |
| 250 | train | Mazda's Mazda6 belongs to which country's car manufacturer? | Japanese | 'Japan' | incorrect | 单 token 短答 'Japan'（疑似错答，人工留意） |
| 251 | test | The original serialized story of the Bride of Re-Animator fi | horror fiction | 'The original serialized story of the Bride of Re-A' | incorrect | gold 未命中 |
| 252 | train | What technique does Cam Clarke and Akira have in common? | animation | 'Cam Clarke and Akira are both martial artists.' | incorrect | gold 未命中 |
| 253 | validation | What profession does Kazuyuki Fujita and Gilbert Yvel have i | martial artist | 'Kazuyuki Fujita and Gilbert Yvel are both film dir' | incorrect | gold 未命中 |
| 254 | test | Who directed a 2009 comedy released by BBC Films? | Debbie Isitt | 'Richard Curtis' | incorrect | gold 未命中 |
| 255 | train | Which port city lies approximately 25 km north of the Lingna | Keelung | 'Xiamen' | incorrect | 单 token 短答 'Xiamen'（疑似错答，人工留意） |
| 256 | train | Who created the series broadcast on the WB that Leigh-Allyn  | Constance M. Burge | 'David Solomon.' | incorrect | gold 未命中 |
| 257 | train | What country of origin does Shawnee Trail and Great Indian W | American | 'Shawnee Trail and Great Indian Warpath originate f' | incorrect | gold 未命中 |
| 258 | train | The university where Rolf Martin Theodor Dahlgren worked as  | 9,000 | 'Unknown' | format_failure | 规则检出拒答 |
| 259 | train | When was the star of the 1982 remake of The Spider's Web app | 2014 | '1985' | incorrect | 单 token 短答 '1985'（疑似错答，人工留意） |
| 260 | validation | Deckers Creek begins west of an unincorporated area in what  | Preston County | 'Deckers Creek begins west of an unincorporated are' | incorrect | gold 未命中 |
| 261 | train | Are Myles Kennedy and SafetySuit both associated with rock b | yes | 'Yes, both Myles Kennedy and SafetySuit are associa' | correct | gold 命中（含等价/别名） |
| 262 | train | House of Many Ways is a young adult fantasy novel set in the | Academy Award for Best A | 'House of Many Ways is a young adult fantasy novel ' | incorrect | gold 未命中 |
| 263 | test | Dost Mohammad Khan was killed by a ruler who became the thir | Afghanistan | 'Dost Mohammad Khan was killed by a ruler who becam' | correct | gold 命中（含等价/别名） |
| 264 | train | In what year was the Sayrevill, New Jersey rock band that Fr | 1983 | '1966' | incorrect | 单 token 短答 '1966'（疑似错答，人工留意） |
| 265 | test | What professional dancers twice turned on a lights festival  | Audrey Mossom | 'The Wanted.' | incorrect | gold 未命中 |
| 266 | train | Which tennis player is from a country closer to Canada, Ken  | Kenneth Eliot Flach | 'Ken Flach' | incorrect | gold 未命中 |
| 267 | test | What dance academy did the starring actress from The Glory o | Beijing Dance Academy | 'Beijing Dance Academy' | correct | gold 命中（含等价/别名） |
| 268 | test | What brother of Stanley Alan Van Gundy is a color commentato | Jeffrey William Van Gund | 'Jeff Van Gundy' | incorrect | gold 未命中 |
| 269 | test | What 1989-born Liverpool player was Jim Cassell responsible  | Daniel Sturridge | 'Jordan Henderson.' | incorrect | gold 未命中 |
| 270 | test | Are both Deerhunter and Nine Lashes American Christian rock  | no | 'Yes, both Deerhunter and Nine Lashes are American ' | incorrect | gold 未命中 |
| 271 | train | Not About Angels was used in the film adaptation of what nov | The Fault in Our Stars | 'Not About Angels was used in the film adaptation o' | incorrect | gold 未命中 |
| 272 | train | Which American-Canadian actor starred in the Disney Channel' | Eric Allan Kramer | 'Charlie Sheen' | incorrect | gold 未命中 |
| 273 | train | From which country is the largest known example of European  | Switzerland | 'The largest known example of European Iron Age sil' | incorrect | gold 未命中 |
| 274 | train | Where is the brand "Moe's Southwest Grill" owned based? | It is based in Sandy Spr | "Moe's Southwest Grill is owned by Yum! Brands." | incorrect | gold 未命中 |
| 275 | validation | Ruth Vollmer begins work designing window displays for which | Tiffany's | "Tiffany's" | correct | gold 命中（含等价/别名） |
| 276 | train | Who is the controlling shareholder of the world's fourth-lar | Jürgen M. Geissinger | "The controlling shareholder of the world's fourth-" | incorrect | gold 未命中 |
| 277 | test | During the Miss USA 2015, Olivia Jordan of Oklahoma was crow | Nia Sanchez | 'Jessica Alba' | incorrect | gold 未命中 |
| 278 | test | What American broadcasting company broadcasted the comedy sh | Sirius XM Holdings | 'NBC' | incorrect | 单 token 短答 'NBC'（疑似错答，人工留意） |
| 279 | test | Are University of Virginia and Massachusetts Institute of Te | yes | 'Yes, both the University of Virginia and Massachus' | correct | gold 命中（含等价/别名） |
| 280 | train | What type of activity does Owner earnings and Warren Buffett | business | 'Owner earnings and Warren Buffett are both related' | incorrect | gold 未命中 |
| 281 | train | The La Senza brand is currently owned by a fashion retailer  | Columbus | 'Cleveland' | incorrect | 单 token 短答 'Cleveland'（疑似错答，人工 |
| 282 | train | Orchard Gateway connects what shopping mall in singapore wit | Orchard Central | 'Orchard.' | incorrect | 单 token 短答 'Orchard.'（疑似错答，人工留 |
| 283 | train | Was Without the King and Italy in a Day directed by the same | no | 'Yes, Without the King and Italy in a Day were both' | incorrect | gold 未命中 |
| 284 | train | What continents are the Moneuptychia found in? | the Americas | 'Africa' | incorrect | 单 token 短答 'Africa'（疑似错答，人工留意） |
| 285 | train | Wade Watts is the uncle of a politican who played college fo | the Oklahoma Sooners | 'Wade Watts is the uncle of Chris Watts, who played' | incorrect | gold 未命中 |
| 286 | train | Which band formed first Cha Cha Cohen or Swervedriver? | Cha Cha Cohen were a ban | 'Swervedriver' | incorrect | 单 token 短答 'Swervedriver'（疑似错答 |
| 287 | validation | Which road borders both Pacific Mall and Splendid China Mall | Steeles Avenue | 'East Coast Road' | incorrect | gold 未命中 |
| 288 | train | A Hand Is on the Gate marked the Broadway directorial debut  | Roscoe Lee Browne | 'James Baldwin.' | incorrect | gold 未命中 |
| 289 | test | The mass killing that took place at Oakland, California on A | Oregon | 'The mass killing that took place at Oakland, Calif' | incorrect | gold 未命中 |
| 290 | validation | When was the father of the professional ice hockey player wi | June 13, 1960 | 'The father of the professional ice hockey player w' | incorrect | gold 未命中 |
| 291 | train | What career did the British actor born in 1965 and star of L | professional footballer | 'Comedian' | incorrect | 单 token 短答 'Comedian'（疑似错答，人工留 |
| 292 | train | John MacGregor, Baron MacGregor of Pulham Market was educate | King George IV | 'John MacGregor, Baron MacGregor of Pulham Market w' | incorrect | gold 未命中 |
| 293 | train | This British television series was adapted from one of the b | Household Words | 'The Strand Magazine' | incorrect | gold 未命中 |
| 294 | validation | Maryland Jockey Club operates a race track in the largest mu | Prince George's County | 'Baltimore County' | incorrect | gold 未命中 |
| 295 | test | Which river flows next to the German town where the music pr | Moselle | 'The Elbe River.' | incorrect | gold 未命中 |
| 296 | train | When was the younger brother of Farshid Karimi born ? | 8 November 1978 | 'The younger brother of Farshid Karimi was born in ' | incorrect | gold 未命中 |
| 297 | test | This annual event held in several major cities in Finland is | the summer solstice | 'Christmas' | incorrect | 单 token 短答 'Christmas'（疑似错答，人工 |
| 298 | test | Are Lycoris and Ammi both native to southern Asia? | yes | 'Yes, both Lycoris and Ammi are native to southern ' | correct | gold 命中（含等价/别名） |
| 299 | train | When William Gladstone successfully relaunched his political | Liberal Party | 'Liberal Party' | correct | gold 命中（含等价/别名） |
| 300 | train | Are Kenji Mizoguchi and David Wall from the same country? | no | 'No, Kenji Mizoguchi and David Wall are not from th' | correct | gold 命中（含等价/别名） |
| 301 | validation | Naseer & Shahab is a Pakistani band playing a genre that dom | 1970s | 'Naseer & Shahab is a Pakistani band playing a genr' | incorrect | gold 未命中 |
| 302 | test | In which branch of the U.S. military did the man who Robert  | Marine Corps | 'Air Force' | incorrect | gold 未命中 |
| 303 | train | What year was the man, who is credited for developing a Cres | 1858 | '1859' | incorrect | 单 token 短答 '1859'（疑似错答，人工留意） |
| 304 | train | Are Ferocactus and Silene both types of plant? | yes | 'Yes, both Ferocactus and Silene are types of plant' | correct | gold 命中（含等价/别名） |
| 305 | test | Murray Seafield St George Head most recognised for which son | One Night in Bangkok | '"Time"' | incorrect | 单 token 短答 '"Time"'（疑似错答，人工留意） |
| 306 | validation | Are the libretto of Tristan und Isolde and Ariane et Barbe-b | no | 'Yes, the libretto of Tristan und Isolde and Ariane' | incorrect | gold 未命中 |
| 307 | train | What was the specialization of an American naval officer who | feats of exploration | 'Aviator.' | incorrect | 单 token 短答 'Aviator.'（疑似错答，人工留 |
| 308 | test | Are Francis Ford Coppola and Jack Hill both American? | yes | 'Yes, both Francis Ford Coppola and Jack Hill are A' | correct | gold 命中（含等价/别名） |
| 309 | train | Which pistol was replaced by a pistol manufactured by Spreew | Luger P08 | 'The Luger.' | incorrect | gold 未命中 |
| 310 | test | Which American digital media company and news satire organiz | The Onion | 'The Onion.' | correct | gold 命中（含等价/别名） |
| 311 | test | What type of arts that have existed since ancient times did  | Graffiti | 'The Stieber Twins specialized in martial arts.' | incorrect | gold 未命中 |
| 312 | test | What song originally released by an American rock band activ | "Bad Moon Rising" | '"atisfaction"' | incorrect | 单 token 短答 '"atisfaction"'（疑似错 |
| 313 | validation | Where did King James reign during Samuel Parker's time as a  | James II and VII (14 Oct | 'King James I ruled in England during Samuel Parker' | incorrect | gold 未命中 |
| 314 | train | What was the setting for Raphael Coleman's best known film? | Victorian England | 'Chicago.' | incorrect | 单 token 短答 'Chicago.'（疑似错答，人工留 |
| 315 | train | Heikki Seppa studied metalsmith at Goldsmith's school in Hel | Georg Arthur Jensen | "Heikki Seppa studied metalsmith at Goldsmith's sch" | incorrect | gold 未命中 |
| 316 | validation | The 2006 NCAA Wrestling Championships crowned Jake Rosholt a | left | 'right hand' | incorrect | gold 未命中 |
| 317 | test | Where was the band who released Feeding the Wolves formed? | Knoxville, Tennessee | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 318 | test | Who directed the film Leigha Kayleen Hancock is best known f | Gary Ross | 'David Lynch.' | incorrect | gold 未命中 |
| 319 | validation | What is the legal name of Johnny Campbell's hometown? | Londonderry | 'Nashville' | incorrect | 单 token 短答 'Nashville'（疑似错答，人工 |
| 320 | train | What kind of species on the Indonesian island of java might  | Javan leopard | 'Elephants' | incorrect | 单 token 短答 'Elephants'（疑似错答，人工 |
| 321 | train | What type of film are both "500 Years Later" and "Manson"? | documentary | 'Both "500 Years Later" and "Manson" are horror fil' | incorrect | gold 未命中 |
| 322 | train | The runner-up in The Celebrity Apprentice 2 has written an a | "How I Raised, Folded, B | '"Raw"' | incorrect | 单 token 短答 '"Raw"'（疑似错答，人工留意） |
| 323 | validation | The Meadowbrook State Parkway connects to the Southern State | 12,272 | 'The Meadowbrook State Parkway connects to the Sout' | incorrect | gold 未命中 |
| 324 | train | The city where Alex Shevelev died is the capital of what reg | the Lazio region | 'Moscow' | incorrect | 单 token 短答 'Moscow'（疑似错答，人工留意） |
| 325 | train | What was Robert M. Fomon's connection to the New York Stock  | a governor | 'Robert M. Fomon was a prominent investment banker ' | incorrect | gold 未命中 |
| 326 | train | What park is just south of the location where the New York J | Central Park | 'Prospect Park' | incorrect | gold 未命中 |
| 327 | test | Where did the military engagements that Captain Lewis Cunnin | Mexico-United States bor | 'Captain Lewis Cunningham Broadus served during the' | incorrect | gold 未命中 |
| 328 | test | Whose former city palace did Erna Flegel work at? | Prince Antoni Radziwiłł | 'Erna Flegel worked at the former city palace of Vi' | incorrect | gold 未命中 |
| 329 | train | In what town is Suffolk county hamlet that was served by the | Town of Islip | 'Norwich' | incorrect | 单 token 短答 'Norwich'（疑似错答，人工留意 |
| 330 | test | Garth Richardson is the son of the producer who worked for w | Badfinger | 'Garth Richardson is the son of the producer who wo' | incorrect | gold 未命中 |
| 331 | train | Shenley Hall is a house at a parish how far from central Lon | 18.7 miles | 'Shenley Hall is approximately 10 miles from centra' | incorrect | gold 未命中 |
| 332 | test | What kind of game is The Park a spin-off of? | massively multiplayer on | 'The Park is a spin-off of The Sims.' | incorrect | gold 未命中 |
| 333 | validation | Do tennis players Kathy Jordan and Sergi Bruguera have the s | no | 'No, Kathy Jordan is American, while Sergi Bruguera' | correct | gold 命中（含等价/别名） |
| 334 | train | What type of music did Dave Wyndorf and Poly Styrene perform | rock | 'Dave Wyndorf and Poly Styrene performed progressiv' | correct | gold 命中（含等价/别名） |
| 335 | train | The movie "100 Million BC" continues the urban myth of an ex | Philadelphia Naval Shipy | 'The movie "100 Million BC" continues the urban myt' | incorrect | gold 未命中 |
| 336 | train | Robin Pingeton replaced Cindy Stein as head coach of which u | University of Missouri | 'Robin Pingeton replaced Cindy Stein as head coach ' | incorrect | gold 未命中 |
| 337 | test | Boulevardier and Earthquake are cocktails, one of which has  | The Tremblement de Terre | 'Boursier' | incorrect | 单 token 短答 'Boursier'（疑似错答，人工留 |
| 338 | test | What child starred in a Chicago production of Alice Walker's | Diamond White | 'Maya Angelou' | incorrect | gold 未命中 |
| 339 | test | From March 631 to April 631, Farrukhzad Khosrau V was the ki | the Parthian Empire | 'Farrukhzad Khosrau V was the king of the Sasanian ' | correct | gold 命中（含等价/别名） |
| 340 | validation | Who was the head promotor of the singer of "For The Good Tim | Rikki Farr's | 'Tom Jones.' | incorrect | gold 未命中 |
| 341 | test | Hairy Jeremy was a television show created in a style that,  | clay animation | 'Claymation.' | incorrect | 单 token 短答 'Claymation.'（疑似错答， |
| 342 | train | Who is the US Olympian and Christian evangelist did the 2010 | Louis "Louie" Zamperini | 'The 2010 non-fiction book by Laura Hillenbrand, ti' | incorrect | gold 未命中 |
| 343 | train | Are Giuseppe Verdi and Ambroise Thomas both Opera composers  | yes | 'Yes, both Giuseppe Verdi and Ambroise Thomas are o' | correct | gold 命中（含等价/别名） |
| 344 | train | Be Quick '28 football club is locayed in what province? | Overijssel | "Be Quick '28 football club is located in the provi" | incorrect | gold 未命中 |
| 345 | train | Are the films Gasland from 2010 and Pumping Iron from 1977 b | yes | 'Yes, both films are documentaries.' | correct | gold 命中（含等价/别名） |
| 346 | train | Who married a man who starred in Marcus Welby, M.D.? | Barbra Streisand | 'Nancy Travis.' | incorrect | gold 未命中 |
| 347 | test | ho is the brother of the American transgender actor known fo | Connor | 'James Franco.' | incorrect | gold 未命中 |
| 348 | validation | What is the name of the place in The Chronicles of Narnia wh | Lantern Waste | 'The wardrobe.' | incorrect | gold 未命中 |
| 349 | train | Were Thinking Fellers Union Local 282 and the Smiths, who ha | yes | 'Yes, both Thinking Fellers Union Local 282 and the' | correct | gold 命中（含等价/别名） |
| 350 | train | Which American comedian starred in the original cast of Satu | Garrett Morris | 'Martin Short.' | incorrect | gold 未命中 |
| 351 | test | What is a common feature of both the Iron Rattler's inversio | combination of a loop an | "A common feature of both the Iron Rattler's invers" | incorrect | gold 未命中 |
| 352 | train | Party of Syrian Unity was established in the wake of a publi | support for the establis | 'The Party of Syrian Unity was established in the w' | incorrect | gold 未命中 |
| 353 | train | How do the Peter Laufer books Forbidden Creatures and No Ani | his own opinions changed | '"Forbidden Creatures" by Peter Laufer focuses on t' | incorrect | gold 未命中 |
| 354 | train | In the 1962 German Grand Prix, a racer came second. What did | Surtees Racing Organisat | 'Gold.' | incorrect | 单 token 短答 'Gold.'（疑似错答，人工留意） |
| 355 | train | Jaroslav Seifert and John McGahern were both part of what sh | writer | 'Actors.' | incorrect | 单 token 短答 'Actors.'（疑似错答，人工留意 |
| 356 | validation | How many films were directed by the director of Wise Blood? | 37 | '2' | format_failure | 单 token 函数词/碎片 '2'，无答案内容 |
| 357 | train | Operation light house was an experiment by Wernher von Braun | 1895 | '1912' | incorrect | 单 token 短答 '1912'（疑似错答，人工留意） |
| 358 | train | Iola is a city along the Neosho River in a region of Kansas  | Bourbon County | 'Allen County' | incorrect | gold 未命中 |
| 359 | train | San Marco and Medina are both what type of game? | board | 'San Marco and Medina are both board games.' | correct | gold 命中（含等价/别名） |
| 360 | train | Ælfgifu of Exeter and Ælfgifu of Shaftesbury are both known  | saint | 'Ælfgifu of Exeter and Ælfgifu of Shaftesbury are b' | incorrect | gold 未命中 |
| 361 | test | Do Lush and P.O.D. both consist of four band members? | yes | 'Yes, both Lush and P.O.D. consist of four band mem' | correct | gold 命中（含等价/别名） |
| 362 | train | Insomniac Events is part of a partnership with a club founde | Iranian-American | 'Jewish' | incorrect | 单 token 短答 'Jewish'（疑似错答，人工留意） |
| 363 | validation | What was the English football club Tottenham Hotspur that Le | Spurs | 'Tottenham Hotspur is commonly referred to as Totte' | incorrect | gold 未命中 |
| 364 | train | The Trappist Abbey of Achel produces and sells what as an "A | Trappist beer | 'candy' | incorrect | 单 token 短答 'candy'（疑似错答，人工留意） |
| 365 | validation | Q:The 7.92×57mm Mauser rifle cartridge was used by which cou | German service cartridge | 'The 7.92×57mm Mauser rifle cartridge was used by G' | incorrect | gold 未命中 |
| 366 | test | Who did a new permanent member on the fourteenth season of S | Gabriella Montez | 'Ryan Evans' | incorrect | gold 未命中 |
| 367 | test | What was the budget of the film in which Kodi Smit-McPhee vo | $60 million | '$50 million' | incorrect | gold 未命中 |
| 368 | test | Who won the 2007 Copa America Final, with help from Julio Ba | Brazil | 'River Plate' | incorrect | gold 未命中 |
| 369 | test | Do both Lancaster Cathedral and Peel Cathedral belong to the | yes | 'No, both Lancaster Cathedral and Peel Cathedral be' | incorrect | gold 未命中 |
| 370 | test | where was the musician and stand up comedian who recorded an | Northampton, England | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 371 | train | Legends of the Fall was based on a novella by what poetry an | James Harrison | 'Stephen King.' | incorrect | gold 未命中 |
| 372 | train | Telescope Hill is near the hamlet that is in what Suffolk Co | Brookhaven | 'Telescope Hill is near the hamlet of Westbury in S' | incorrect | gold 未命中 |
| 373 | train | Not Richard, But Dick was an album by the band formed in wha | Philadelphia | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 374 | train | What is the birthdate of this American actor, director, and  | February 13, 1946 | 'September 17, 1964' | incorrect | gold 未命中 |
| 375 | train | Han Chae-young was in the 2009 drama that aired on what netw | KBS2 | 'Han Chae-young was in the 2009 drama that aired on' | incorrect | gold 未命中 |
| 376 | test | Which American swimmer, coached by Ray Looze, won a bronze m | Cody Miller | 'Michael Phelps' | incorrect | gold 未命中 |
| 377 | test | Are Harry Everett Smith and Vladimir Danilevich both from Ru | no | 'No, Harry Everett Smith and Vladimir Danilevich ar' | correct | gold 命中（含等价/别名） |
| 378 | train | 3TEETH was the debut album for the opening act for the2016 t | Los Angeles | 'San Diego' | incorrect | gold 未命中 |
| 379 | train | The producer of the Eric Church album "The Outsiders" was a  | In Pursuit | 'The Police' | incorrect | gold 未命中 |
| 380 | test | "Take Me" is a song recorded by which American singer, actor | Frank Sinatra | 'Tom Petty' | incorrect | gold 未命中 |
| 381 | train | Tui Flower and Julia child were both known for what? | Cooking | 'photography' | incorrect | 单 token 短答 'photography'（疑似错答， |
| 382 | train | how many films has the director of "Girl 6" produced since 1 | over 35 films | '6' | format_failure | 单 token 函数词/碎片 '6'，无答案内容 |
| 383 | train | Are Toshi and Warrel Dane both in the band Sanctuary? | no | 'Yes, Toshi and Warrel Dane are both in the band Sa' | incorrect | gold 未命中 |
| 384 | test | When was the football club founded in which Walter Otto Davi | 1885 | '1876' | incorrect | 单 token 短答 '1876'（疑似错答，人工留意） |
| 385 | train | What type of beliefs does Mount Ida and Rhea have in common? | Greek mythology | 'Mount Ida and Rhea are both associated with ancien' | correct | gold 命中（含等价/别名） |
| 386 | validation | Where was one of Sergei Prokofiev's most well-known operas f | Chicago, Illinois | 'London.' | incorrect | 单 token 短答 'London.'（疑似错答，人工留意 |
| 387 | test | The Church of England's Oxford Movement was opposed by a cle | devotional | 'Poetry.' | incorrect | 单 token 短答 'Poetry.'（疑似错答，人工留意 |
| 388 | train | About Time is a British romantic comedy-drama film that star | Dublin Institute of Tech | 'Dublin University' | incorrect | gold 未命中 |
| 389 | test | Who has won more awards, Dan Schneider or Helen Hunt? | Helen Elizabeth Hunt | 'Dan Schneider' | incorrect | gold 未命中 |
| 390 | train | Guy Pearce starred in which movie produced by Marvel Studios | Iron Man 3 | 'Guy Pearce starred in the movie "Deadpool" produce' | incorrect | gold 未命中 |
| 391 | train | What team competed in six competitions in their 116th season | Football Club Barcelona | 'Manchester United' | incorrect | gold 未命中 |
| 392 | test | Are Sunset Strip and American Hardcore both music documentar | no | 'Yes, both Sunset Strip and American Hardcore are m' | incorrect | gold 未命中 |
| 393 | test | Hivange is a village in a country that has how many official | three official languages | 'Hivange is a village in Belgium, which has three o' | correct | gold 命中（含等价/别名） |
| 394 | validation | What author wrote a three book series of memoirs that are st | Homer Hickam, Jr. | 'Anne Frank' | incorrect | gold 未命中 |
| 395 | test | Are Maro Ajemian and Patricia Field both pianists? | no | 'Yes, both Maro Ajemian and Patricia Field are pian' | incorrect | gold 未命中 |
| 396 | train | The movies Queen of Blood and Battle Beyond the Sun both con | Nebo Zovyot | 'The Mission.' | incorrect | gold 未命中 |
| 397 | validation | Gretchen Gotay graduated from what American public research  | The University of Georgi | 'Gretchen Gotay graduated from Georgia Tech.' | incorrect | gold 未命中 |
| 398 | train | Are Phlebodium and Pieris both species of ferns? | no | 'No, Phlebodium and Pieris are not both species of ' | correct | gold 命中（含等价/别名） |
| 399 | validation | Adam Fox was one of the first members of an informal literar | University of Oxford, En | 'Harvard University' | incorrect | gold 未命中 |
| 400 | train | Siegfriedstellung in the First World War was a defensive pos | German | 'Germany' | incorrect | 单 token 短答 'Germany'（疑似错答，人工留意 |
| 401 | train | From which phrase the name of the place where Hazina Towers  | Maasai phrase | 'The name of the place where Hazina Towers is under' | incorrect | gold 未命中 |
| 402 | test | Alex Yemenidjian is the CEO of the company that owns what La | Tropicana Las Vegas | 'Alex Yemenidjian is the CEO of Caesars Palace.' | incorrect | gold 未命中 |
| 403 | train | Were the films "Ten Who Dared" and "Tonka" distributed by th | yes | 'Yes, the films "Ten Who Dared" and "Tonka" were bo' | correct | gold 命中（含等价/别名） |
| 404 | train | What is the nationality of this company that services MS Mob | Danish | 'American' | incorrect | 单 token 短答 'American'（疑似错答，人工留 |
| 405 | test | What broadcasting company did both Andrew Collins and Stuart | BBC | 'ITV' | incorrect | 单 token 短答 'ITV'（疑似错答，人工留意） |
| 406 | train | What kind of musician does Robert Plant discography and John | drummer | 'Drummer' | correct | gold 命中（含等价/别名） |
| 407 | train | Which Croatian professional basketball player (a shooting gu | Dražen Petrović | 'Robert Beljan.' | incorrect | gold 未命中 |
| 408 | test | Who animated the TV anime adaptation of Dies irae? | studio A.C.G.T | 'MAPPA.' | incorrect | 单 token 短答 'MAPPA.'（疑似错答，人工留意） |
| 409 | train | In what year was Shin Hyun-joon in the successful South Kore | 2005 | 'Shin Hyun-joon starred in the successful South Kor' | incorrect | gold 未命中 |
| 410 | train | Bally's & Paris station is on the monorail that is of what l | 3.9 mi | "Bally's & Paris station is on the monorail that is" | incorrect | gold 未命中 |
| 411 | train | What actor starred in "Word of Honor" and "Miami Vice"? | Donald Wayne Johnson | 'Don Johnson.' | incorrect | gold 未命中 |
| 412 | test | What is the name of the Australian specialist electronic mus | Cyclic Defrost | 'Electronic Sound' | incorrect | gold 未命中 |
| 413 | test | What type of engine powered both the Saab 36 and the Avro Vu | British Bristol Olympus  | 'Jet turbine engines.' | incorrect | gold 未命中 |
| 414 | train | Does Bazhong or Kaiyuan, Liaoning have a higher population? | Bazhong () is a prefectu | 'Kaiyuan, Liaoning has a higher population than Baz' | incorrect | gold 未命中 |
| 415 | test | Following The Simple Things a featurette directed by Burny M | Mickey's Christmas Carol | 'Home.' | incorrect | 单 token 短答 'Home.'（疑似错答，人工留意） |
| 416 | train | What is the name of a member of the North Melbourne Football | Mark Andrew Brayshaw | 'Sam Johnson.' | incorrect | gold 未命中 |
| 417 | train | Vestfold and Telemark each border what other Norwegian count | Buskerud | 'Vestfold and Telemark each border the Norwegian co' | incorrect | gold 未命中 |
| 418 | validation | What game where a play must act as a night security guard wa | Five Nights at Freddy's | 'Overwatch' | incorrect | 单 token 短答 'Overwatch'（疑似错答，人工 |
| 419 | validation | What is another movie the director of Marvel Cinematic Unive | "Nanny McPhee" | 'Black Panther' | incorrect | gold 未命中 |
| 420 | train | Have Jelena Janković and Marat Safin both played tennis prof | yes | 'Yes, both Jelena Janković and Marat Safin have pla' | correct | gold 命中（含等价/别名） |
| 421 | train | Q: Who had more solo albums, Marty Raybon or Greg Graffin? | Gregory Walter Graffin | 'Greg Graffin' | incorrect | gold 未命中 |
| 422 | train | What type of profession do Dave Pirner and Les McKeown both  | singer | 'Dave Pirner and Les McKeown are both professional ' | incorrect | gold 未命中 |
| 423 | train | A Wind in the Door is part of a series written by who? | Madeleine L'Engle | 'A Wind in the Door is part of a series written by ' | incorrect | gold 未命中 |
| 424 | test | Mark Lawrence played for the Dallas Stars and which other NH | New York Islanders | 'Mark Lawrence played for the Dallas Stars and the ' | incorrect | gold 未命中 |
| 425 | test | Keene is an unincorporated community in Wabaunsee County, Ka | The United States of Ame | 'The United States of America.' | correct | gold 命中（含等价/别名） |
| 426 | test | Postal 2 has scenes that are used in a song that was release | June 2003 | '2011' | incorrect | 单 token 短答 '2011'（疑似错答，人工留意） |
| 427 | test | The Sanders-Brown Center on Aging was funded by a grant from | Kentucky Fried Chicken ( | 'The Sanders-Brown Center on Aging was funded by a ' | incorrect | gold 未命中 |
| 428 | test | Who did Muhummad Ali fight next, in Houston, after the so-ca | Jimmy Ellis | 'Joe Louis.' | incorrect | gold 未命中 |
| 429 | train | What kind of music do The Stone Roses and The Lemonheads pla | rock band | 'The Stone Roses and The Lemonheads play rock music' | incorrect | gold 未命中 |
| 430 | test | How many episodes were in the season of "Rick and Morty" tha | ten | '12' | format_failure | 单 token 函数词/碎片 '12'，无答案内容 |
| 431 | validation | Who was the biological father of the emperor who built the N | Germanicus | 'The biological father of the emperor who built the' | incorrect | gold 未命中 |
| 432 | test | Elizabeth Austin wrote for a fitness magazine founded by who | Christine MacIntyre | 'Richard Simmons.' | incorrect | gold 未命中 |
| 433 | train | The creators of the product designation TSR 2002 was the fir | role-playing game | 'Video game.' | incorrect | gold 未命中 |
| 434 | train | Lakshmi Shankar is the mother-in-law of an acclaimed Indian  | Hindustani classical voc | 'Lakshmi Shankar is the mother-in-law of  Ravi Shan' | incorrect | gold 未命中 |
| 435 | train | What was the estimated population of the city that Luis Vill | 102,984 | 'Luis Villalta Aquino was from Mexico.' | incorrect | gold 未命中 |
| 436 | validation | What country of origin does Dana Ivey and Two Weeks Notice h | American | 'Dana Ivey and Two Weeks Notice are both American p' | correct | gold 命中（含等价/别名） |
| 437 | train | Jasmin Geljo is known for his role in a 2005 post-apocalypti | George A. Romero | 'Jasmin Geljo is known for his role in the 2005 pos' | incorrect | gold 未命中 |
| 438 | validation | In what year was the scientific journal for which Danilo Err | 1952 | '1997' | incorrect | 单 token 短答 '1997'（疑似错答，人工留意） |
| 439 | validation | Where does Yannick Ferreira Carrasco play home games? | Wanda Metropolitano | 'Yannick Ferreira Carrasco plays home games at the ' | incorrect | gold 未命中 |
| 440 | test | Which is the busiest airport in the United Kingdom outside o | Gatwick Airport | 'Manchester Airport' | incorrect | gold 未命中 |
| 441 | train | What honor has been received by both a former NASA Astronaut | National Aviation Hall o | 'Aviation Hall of Fame' | correct | gold 命中（含等价/别名） |
| 442 | test | The 2017–18 Wigan Athletic F.C. season will be a year in whi | Carabao Cup | 'EFL Cup' | incorrect | gold 未命中 |
| 443 | train | U.S. Representative Mike Conaway is investigating interferen | 2016 United States elect | '2016' | incorrect | 单 token 短答 '2016'（疑似错答，人工留意） |
| 444 | test | Which actor/actress from Overnight Delivery was born in New  | Reese Witherspoon | 'Tom Arnold.' | incorrect | gold 未命中 |
| 445 | test | Are the writing from Maurice Level and Alice Hoffman focused | yes | 'Yes, the writing from Maurice Level and Alice Hoff' | correct | gold 命中（含等价/别名） |
| 446 | train | Which author influenced the animated Easter television speci | Margery Williams | 'Beatrix Potter' | incorrect | gold 未命中 |
| 447 | test | How many Golden Globe Awards did this English retired actres | two Golden Globe Awards | '2' | format_failure | 单 token 函数词/碎片 '2'，无答案内容 |
| 448 | train | What award did the writer of Never Let Me Go novel win in 19 | Man Booker Prize for Fic | 'The Booker Prize.' | incorrect | gold 未命中 |
| 449 | train | In which period was this German composer, pianist, organist  | early Romantic period | 'The German composer, pianist, organist, and conduc' | incorrect | gold 未命中 |
| 450 | train | The magazine that nominated George Rainsford for their Best  | Tuesday | 'Wednesday' | incorrect | 单 token 短答 'Wednesday'（疑似错答，人工 |
| 451 | train | George Borba was part of the team that competed at what 1970 | FIFA World Cup | 'Mexico.' | incorrect | 单 token 短答 'Mexico.'（疑似错答，人工留意 |
| 452 | train | What was the formative year for the company eventually repla | 1858 | 'The formative year for the company eventually repl' | incorrect | gold 未命中 |
| 453 | test | The world's greatest Super-Heroes anthology showcased one of | Captain Marvel | 'Superman' | incorrect | 单 token 短答 'Superman'（疑似错答，人工留 |
| 454 | train | Who had more of their English novels turned into Oscar-nomin | Two of his novels, "The  | 'Pat Conroy' | incorrect | gold 未命中 |
| 455 | train | On what part of U.S Route 56 can you listen to the KCTV? | The highway's eastern te | 'Texas' | incorrect | 单 token 短答 'Texas'（疑似错答，人工留意） |
| 456 | validation | Umaru Mutallab had a son who tried to detonate materials abo | December 25, 2009 | 'Umaru Mutallab had no son.' | incorrect | gold 未命中 |
| 457 | train | Barnstable County Hospital was the location of the autopsy o | Caroline Kennedy | 'Barnstable County Hospital was the location of the' | incorrect | gold 未命中 |
| 458 | train | Are both Duke Energy and Affiliated Managers Group based in  | no | 'No, both Duke Energy and Affiliated Managers Group' | correct | gold 命中（含等价/别名） |
| 459 | train | "Show 'Em (What You're Made Of)" is a song written by a grou | Kentucky Music Hall of F | '"Show \'Em (What You\'re Made Of)" is a song written' | incorrect | gold 未命中 |
| 460 | train | What party was the secretary of commerce and housing under t | Republican | 'The Democratic Party.' | incorrect | gold 未命中 |
| 461 | train | Before I Go to Sleep stars an Australian actress, producer a | singer | 'comedian' | incorrect | 单 token 短答 'comedian'（疑似错答，人工留 |
| 462 | train | WrestleMania XXX took place at the home venue of which Natio | New Orleans Saints | 'WrestleMania XXX took place at Giants Stadium.' | incorrect | gold 未命中 |
| 463 | test | Who was involved in the arrest of Dread Pirate Roberts? | Christopher "Chris" Tarb | 'Captain Hook.' | incorrect | gold 未命中 |
| 464 | validation | Let Mother Earth Speak's Native American activist was born w | Leech Lake Indian Reserv | 'Minnesota' | incorrect | 单 token 短答 'Minnesota'（疑似错答，人工 |
| 465 | train | What county is Keene High School located in? | Cheshire County | 'Keene High School is located in Cheshire County, N' | correct | gold 命中（含等价/别名） |
| 466 | train | Which British first-generation jet-powered medium bomber was | English Electric Canberr | 'The British first-generation jet-powered medium bo' | incorrect | gold 未命中 |
| 467 | test | Black Book starred the actress and writer of what heritage? | Dutch | 'Jewish' | incorrect | 单 token 短答 'Jewish'（疑似错答，人工留意） |
| 468 | train | Kingdom Hearts 358/2 Days was made by the company based in w | Shinjuku | 'Kingdom Hearts 358/2 Days was made by the company ' | incorrect | gold 未命中 |
| 469 | train | When was the novella written whose film adaptation was playe | 1843 | 'The novella "A Christmas Carol" by Charles Dickens' | correct | gold 命中（含等价/别名） |
| 470 | train | In what year was the British actress who starred in a film a | 9 November 1955 | 'The British actress who starred in a film adaptati' | incorrect | gold 未命中 |
| 471 | train | Riaz-Ur-Rehman Saghar wrote songs for the Pakistani singer w | The Kennedy Center | 'Riaz-Ur-Rehman Saghar wrote songs for the Pakistan' | incorrect | gold 未命中 |
| 472 | train | Jayaraj made the 2016 epic historical drama that is an adapt | Macbeth | 'Hamlet' | incorrect | 单 token 短答 'Hamlet'（疑似错答，人工留意） |
| 473 | test | Mexican Indignados Movement is a response to a war also know | Mexican War on Drugs | 'The Mexican Indignados Movement is a response to t' | incorrect | gold 未命中 |
| 474 | train | Both Hatter and March Hare are characters in which book? | Alice's Adventures in Wo | 'Both Hatter and March Hare are characters in "Alic' | correct | gold 命中（含等价/别名） |
| 475 | train | The Westchester Knicks are a basketball team in a minor leag | National Basketball Deve | 'The Westchester Knicks.' | format_failure | 输出为问句回显，无答案内容 |
| 476 | test | Lafe Pence was a member of which lower chamber of the United | United States House of R | 'Lafe Pence was a member of the United States House' | correct | gold 命中（含等价/别名） |
| 477 | test | Jimmy D'Arcy played in Northern Ireland for the team based i | Antrim | 'Antrim' | correct | gold 命中（含等价/别名） |
| 478 | train | What type of magazine is Eugene Habecker the chairman of? | evangelical Christian pe | 'Eugene Habecker is the chairman of Rolling Stone m' | incorrect | gold 未命中 |
| 479 | train | What does Age of Chance and Vector share in common? | was a rock band | 'They are both graphic novels.' | incorrect | gold 未命中 |
| 480 | train | What religion is the composer for India's first science fict | Hindi | 'Christian.' | incorrect | 单 token 短答 'Christian.'（疑似错答，人 |
| 481 | train | Why did the CEO of the football team based in Denver, Colora | due to the onset and pro | 'The CEO of the football team based in Denver, Colo' | incorrect | gold 未命中 |
| 482 | test | Were both Peter Duffell and Fred Niblo actors? | yes | 'Yes, both Peter Duffell and Fred Niblo were actors' | correct | gold 命中（含等价/别名） |
| 483 | train | A private university that beat Georgetown during a basketbal | Marietta | 'Philadelphia' | incorrect | 单 token 短答 'Philadelphia'（疑似错答 |
| 484 | train | Have Tionne Watkins and Park So-yeon both been members of a  | yes | 'Yes, Tionne Watkins and Park So-yeon have both bee' | correct | gold 命中（含等价/别名） |
| 485 | train | What is the name of the second largest car rental company, t | Hertz | 'Avis' | incorrect | 单 token 短答 'Avis'（疑似错答，人工留意） |
| 486 | test | What Minnesota county is the University of Minnesota in? | Hennepin County | 'The University of Minnesota is located in Twin Cou' | incorrect | gold 未命中 |
| 487 | test | In Ancient Egyptian religion how would a citizen be weighted | against the feather of t | 'In Ancient Egyptian religion, a citizen would be w' | correct | gold 命中（含等价/别名） |
| 488 | validation | The Death of Cook depicts the death of James Cook at a bay o | Kona coast | 'Pacific.' | incorrect | 单 token 短答 'Pacific.'（疑似错答，人工留 |
| 489 | test | Jamie Harris is best known for his role as The Hook-Handed M | Brad Silberling | 'Jamie Harris is best known for his role as The Hoo' | incorrect | gold 未命中 |
| 490 | validation | What area once connected Great Britain to continental Europe | Doggerland | 'The area that once connected Great Britain to cont' | incorrect | gold 未命中 |
| 491 | test | Muslim Mahammad oglu Magomayev is the grandfther of what Sov | Muslim Magometovich Mago | 'Mahmud Atayev' | incorrect | gold 未命中 |
| 492 | train | What is the name of the region that includes the cities Dove | Seacoast Region | 'New Hampshire Coast' | incorrect | gold 未命中 |
| 493 | test | What profession does John Landis and Gore Verbinski have in  | director | 'Film directors' | incorrect | gold 未命中 |
| 494 | test | Did the Sandy and Beaver Canal remain operational until a la | no | 'Yes, the Sandy and Beaver Canal remained operation' | incorrect | gold 未命中 |
| 495 | train | Which feature does the G-shock watch have that is tested by  | water resistance | 'The G-Shock watch has a water resistance feature t' | correct | gold 命中（含等价/别名） |
| 496 | train | National Strategy for Homeland Security was a response to th | Pentagon | 'The Pentagon.' | correct | gold 命中（含等价/别名） |
| 497 | train | What city was the capital of the Ostrogothic Kingdom and the | Ravenna (] , also locall | 'Savenna' | incorrect | 单 token 短答 'Savenna'（疑似错答，人工留意 |
| 498 | train | Shannon Purser played the role of June Acosta in a 2017 horr | John R. Leonetti | 'Shannon Purser played the role of June Acosta in t' | incorrect | gold 未命中 |
| 499 | train | Jim Atchison was the President of the theme park that had he | Orlando | 'Orlando.' | correct | gold 命中（含等价/别名） |
| 500 | validation | The 1966 Football League Cup Final was contested with which  | West Bromwich Albion Foo | 'Birmingham City' | incorrect | gold 未命中 |
| 501 | test | Channel 8 has broadcast which American sports series that pr | HBO World Championship B | 'ESPN.' | incorrect | 单 token 短答 'ESPN.'（疑似错答，人工留意） |
| 502 | train | What is the height of the player who won the 2015 AFL Rising | 1.95 m | 'The player who won the 2015 AFL Rising Star award ' | incorrect | gold 未命中 |
| 503 | train | Driven To Perform has a sponsor that includes the electronic | Canada | 'Germany' | incorrect | 单 token 短答 'Germany'（疑似错答，人工留意 |
| 504 | test | The 1966–67 NHL season ended with a win in the Stanley Cup b | Atlantic | 'Atlantic' | correct | gold 命中（含等价/别名） |
| 505 | test | which league is the 121th season of top-tier competitive foo | 2017–18 Swiss Super Leag | 'The 121st season of top-tier competitive football ' | incorrect | gold 未命中 |
| 506 | test | What is the National Grape Cooperative Association classifie | An agricultural cooperat | 'The National Grape Cooperative Association is clas' | incorrect | gold 未命中 |
| 507 | train | What date was the person born that Samuel Flores Borrego was | 1 August 1971 | 'March 14, 1928' | incorrect | gold 未命中 |
| 508 | train | Are both Alabama Slammer and Yorsh non alcoholic drinks? | no | 'Yes, both Alabama Slammer and Yorsh are non-alcoho' | incorrect | gold 未命中 |
| 509 | validation | What series did William Hopke play in for the Detroit Tigers | 1909 Cuban-American Majo | 'William Hopke played in the 1934 World Series for ' | incorrect | gold 未命中 |
| 510 | test | Hey Ya is a song performed on The Ed Sullivan Show on CBS by | is a song written and pr | 'Eminem' | incorrect | 单 token 短答 'Eminem'（疑似错答，人工留意） |
| 511 | test | What is the name of the murder victim that worked in a resta | Ron Goldman | 'Frank Sin.' | incorrect | gold 未命中 |
| 512 | train | Ambrose Mendy has managed and/or advised a British professio | "The Ring" magazine | 'Ambrose Mendy has managed and/or advised Anthony J' | incorrect | gold 未命中 |
| 513 | train | Immanuel Lutheran School is affiliated with the denomination | 2.1 million | 'Immanuel Lutheran School is affiliated with the Lu' | incorrect | gold 未命中 |
| 514 | test | What was the manager for the 1891 Cincinnati Kelly's Killers | $10,000 Kelly | 'Jim Kelly.' | incorrect | gold 未命中 |
| 515 | train | What organization does Rosyth Dockyard and Queen Elizabeth-c | Navy | 'Royal Navy' | correct | gold 命中（含等价/别名） |
| 516 | train | Erving Goffman was cited as higher than a literary critic on | The Times Higher Educati | 'The Harvard Guide' | incorrect | gold 未命中 |
| 517 | train | What genre did the writer whose novel was based on "I'll Tak | romance genre | 'Science Fiction' | incorrect | gold 未命中 |
| 518 | train | Who was the founder of a chain of supermarkets that is now h | Joseph E. Grosberg | 'Ralph Meyer.' | incorrect | gold 未命中 |
| 519 | validation | Fred Mace played for which English football club in 1919? | Stalybridge Celtic Footb | 'Fred Mace played for Manchester City in 1919.' | incorrect | gold 未命中 |
| 520 | train | Who was the recipient of a prize also given to a player for  | Rivaldo of Milan | 'David Beckham.' | incorrect | gold 未命中 |
| 521 | train | Reveille Park is the eighth album by which American rapper b | South Park Mexican | 'Reveille Park is the eighth album by Eminem.' | incorrect | gold 未命中 |
| 522 | test | In which city were the olympic games held in which Willi Meu | Berlin, Germany | 'Rome.' | incorrect | 单 token 短答 'Rome.'（疑似错答，人工留意） |
| 523 | train | What actor played the male lead in a teen comedy about a hig | Patrick Dempsey | 'Chris Evans' | incorrect | gold 未命中 |
| 524 | train | Is The Devils of Loudun and Maskarade both operas? | yes | 'Yes, The Devils of Loudun and Maskarade are both o' | correct | gold 命中（含等价/别名） |
| 525 | train | Faces is a mixtape that features guest appearances from an A | Country Thuggin | 'Faces.' | incorrect | 单 token 短答 'Faces.'（疑似错答，人工留意） |
| 526 | test | In the 2011 census what was the population of suburban area  | 26,788 | 'In the 2011 census, the population of Watford was ' | incorrect | gold 未命中 |
| 527 | test | What collaboration with DJ Muggs did Gary Grice participate  | Grandmasters | 'No answer.' | incorrect | gold 未命中 |
| 528 | validation | Both the Pulandian District and Hailar District are located  | China | 'India' | incorrect | 单 token 短答 'India'（疑似错答，人工留意） |
| 529 | test | The Companions were the first of what type of cavalry? | Shock troops | 'The Companions were the first Roman light cavalry.' | incorrect | gold 未命中 |
| 530 | train | Who was a Christian Evangelist and US prisoner of war surviv | Louis "Louie" Zamperini | 'Tom Clark' | incorrect | gold 未命中 |
| 531 | train | Which Oxford University graduate did Midge Mackenzie intervi | Kate Millett | 'Margaret Thatcher.' | incorrect | gold 未命中 |
| 532 | train | How many laps did Harry Prowell run during the 10,000 metres | 25 laps | 'Harry Prowell ran 20 laps during the 10,000 metres' | incorrect | gold 未命中 |
| 533 | train | The host of PokerFace is from where? | Newcastle upon Tyne, Eng | 'Canada' | incorrect | 单 token 短答 'Canada'（疑似错答，人工留意） |
| 534 | train | Aleksandras Stulginskis' successor held office between what  | 7 June 1926 to 17 Decemb | "Aleksandras Stulginskis' successor held office bet" | incorrect | gold 未命中 |
| 535 | validation | What is the nickname of the singer with which Castor McCord  | Satchmo | ' Bessie Smith' | incorrect | gold 未命中 |
| 536 | test | Gül Mosque and Hippodrome of Constantinople are both located | Istanbul, Turkey | 'Gül Mosque and Hippodrome of Constantinople are bo' | correct | gold 命中（含等价/别名） |
| 537 | train | Are Danie Visser and Oliver Marach both Grand Slam tennis to | no | 'Yes, Danie Visser and Oliver Marach are both Grand' | incorrect | gold 未命中 |
| 538 | train | What year was the bank famously opposed by Brendan Bracken f | 1694 | 'The bank famously opposed by Brendan Bracken for c' | incorrect | gold 未命中 |
| 539 | validation | What movie did John Gavin Malkovich play in with Matt Damon  | Rounders | 'Fight Club.' | incorrect | gold 未命中 |
| 540 | validation | which Australian politician represented Electoral district o | Jane Goward | 'Tony Smith' | incorrect | gold 未命中 |
| 541 | test | Where did the hijacked plane rammed by Heather Penney crash? | Pennsylvania | 'The hijacked plane rammed by Heather Penney crashe' | correct | gold 命中（含等价/别名） |
| 542 | validation | What is in both the Lithocarpus and Duranta species? | trees | 'Fruits' | incorrect | 单 token 短答 'Fruits'（疑似错答，人工留意） |
| 543 | validation | Jordan's Furniture is a furniture retailer with a location i | the junction with Inters | 'Dallas.' | incorrect | 单 token 短答 'Dallas.'（疑似错答，人工留意 |
| 544 | train | Is it correct to state that Tetrapanax is an evergreen shrub | yes | 'Yes, that is correct. Tetrapanax is an evergreen s' | correct | gold 命中（含等价/别名） |
| 545 | train | Chantal Thomas wrote a book that was turned into a 2012 film | Benoît Jacquot | 'David Mackenzie.' | incorrect | gold 未命中 |
| 546 | train | Which of the actress starred in Zombie Night appeared in the | Jennifer Taylor | 'Jennifer Grey.' | incorrect | gold 未命中 |
| 547 | train | What is the gross leasable area of the shopping mall served  | 1800000 sqft | 'Not available.' | incorrect | gold 未命中 |
| 548 | validation | Are Euptelea and Muehlenbeckia both genuses? | yes | 'Yes, both Euptelea and Muehlenbeckia are plant gen' | correct | gold 命中（含等价/别名） |
| 549 | train | Which of Mabel Keyes Babcock's distant relatives wrote "Of P | William Bradford | 'William Bradford' | correct | gold 命中（含等价/别名） |
| 550 | train | What Albanian department is reasonbile for an international  | Ministry of European Int | 'The Albanian department responsible for an interna' | incorrect | gold 未命中 |
| 551 | validation | Pajottenland has historically provided beers that include ar | Zenne | 'The Po Valley' | incorrect | gold 未命中 |
| 552 | train | Luke Null is an actor who was on the program that premiered  | September 30, 2017 | 'September 21, 2019' | incorrect | gold 未命中 |
| 553 | train | Alexander S. Wadsworth served during the war that was faught | United States, the Unite | 'Alexander S. Wadsworth served during the American ' | incorrect | gold 未命中 |
| 554 | train | Baltic Neopaganism was a religious movement that included wh | Vilius Storostas-Vydūnas | 'Eero Laine' | incorrect | gold 未命中 |
| 555 | train | Which composer was wrote his music most recently, Michael Ti | Michael Kemp Tippett | 'Michael Tippett' | incorrect | gold 未命中 |
| 556 | train | What did both Karel Bossart and Sergei Korolev design? | rocket | 'Both Karel Bossart and Sergei Korolev designed spa' | incorrect | gold 未命中 |
| 557 | train | The man known as the voice of "Elgar" voices the English cha | Love Hina | 'Dragon Ball Z' | incorrect | gold 未命中 |
| 558 | test | Which actor does American Beauty and American Beauty have in | Kevin Spacey | 'Tom Cruise.' | incorrect | gold 未命中 |
| 559 | test | The Hip Hop Republican was credited with giving blacks empha | 2008 | 'The Hip Hop Republican was credited with giving bl' | correct | gold 命中（含等价/别名） |
| 560 | train | Camp Modin moved to the Belgrade Lakes region of Maine from  | Somerset County | 'Camp Modin moved to the Belgrade Lakes region of M' | incorrect | gold 未命中 |
| 561 | test | Michael J. Hunter replaced the lawyer who became the adminis | EPA | 'Michael J. Hunter replaced the lawyer who became t' | correct | gold 命中（含等价/别名） |
| 562 | test | What is the primary role of the position played by Viktor Ra | prevent the opposing tea | 'Viktor Raychev primarily plays as a forward for Lo' | incorrect | gold 未命中 |
| 563 | test | Stephen Joseph Bercik was mayer of a city that had a populat | 129,007 | 'Stephen Joseph Bercik was the mayor of the city of' | incorrect | gold 未命中 |
| 564 | train | who is a British physicist and also a British government's c | Frederick Alexander | 'Sir Brian Cox' | incorrect | gold 未命中 |
| 565 | test | Who were the stars of the 2008 South Korean movie that was l | Kim Yoon-seok and Ha Jun | 'The stars of the 2008 South Korean movie "Three Br' | incorrect | gold 未命中 |
| 566 | train | What genre was the movie that Austin Nichols was in with Kir | romantic comedy | 'Comedy' | incorrect | 单 token 短答 'Comedy'（疑似错答，人工留意） |
| 567 | test | One of the actors in the film Dhruva Natchathiram was awarde | 2011 | '2011' | correct | gold 命中（含等价/别名） |
| 568 | test | where is the American professional basketball team which Jal | Louisiana. | 'The Golden State Warriors are based in Oakland, Ca' | incorrect | gold 未命中 |
| 569 | test | The M1919 and the M1 was used by what military? | U.S. | 'The M1919 and the M1 were used by the United State' | incorrect | gold 未命中 |
| 570 | validation | What is the name of the person that named Moltke Nunatak aft | Second German Antarctic  | ' Ernest Shackleton' | incorrect | gold 未命中 |
| 571 | test | Which town is the venue, in which the APRA Music Awards of 2 | New South Wales | 'Melbourne' | incorrect | 单 token 短答 'Melbourne'（疑似错答，人工 |
| 572 | train | Gorgoroth is a band based in which Norwegian county? | Hordaland | 'Gorgoroth is a band based in the Norwegian county ' | incorrect | gold 未命中 |
| 573 | validation | When did the mother of Joseph Ferdinand Leopold of Bavaria d | 1692 | 'The mother of Joseph Ferdinand Leopold of Bavaria,' | incorrect | gold 未命中 |
| 574 | validation | Is The Stuff of Legend and Babes in Toyland both entertainme | by | 'Yes, both The Stuff of Legend and Babes in Toyland' | incorrect | gold 未命中 |
| 575 | train | Carroll County, Ohio is named after the only Catholic signat | Charles Carroll of Carro | 'Charles Carroll of Carrollton' | correct | gold 命中（含等价/别名） |
| 576 | test | Who was a member of "Cheney", who won 'Song of the Year' in  | Christopher John Cheney | 'Mikael Åkerfeldt' | incorrect | gold 未命中 |
| 577 | train | In what corner of Missouri is radio station WMBH located? | southwestern | 'WMBH is located in the northeast corner of Missour' | incorrect | gold 未命中 |
| 578 | train | Are the Laleli Mosque and Esma Sultan Mansion located in the | no | 'No, the Laleli Mosque and Esma Sultan Mansion are ' | correct | gold 命中（含等价/别名） |
| 579 | validation | The Cleveland Thyagaraja Festival is a type of festival that | Telugu | 'The Cleveland Thyagaraja Festival honors Carnatic ' | incorrect | gold 未命中 |
| 580 | train | In which county does the 8th Military Police Brigade of the  | Honolulu | "The 8th Military Police Brigade's Barracks is loca" | incorrect | gold 未命中 |
| 581 | train | When was one of the teacher of Nikolai Lugansky died who was | 1924November 22, 1993 | '1941' | incorrect | 单 token 短答 '1941'（疑似错答，人工留意） |
| 582 | train | What IBF Light Flyweight Championship winner was related to  | Ricardo “El Finito” Lópe | 'The IBF Light Flyweight Championship winner relate' | incorrect | gold 未命中 |
| 583 | validation | American Blues included the drummer from which American rock | ZZ Top | 'The Who' | incorrect | gold 未命中 |
| 584 | train | When was one of the science fiction survival horror video ga | 22 September 2015 | '2007' | incorrect | 单 token 短答 '2007'（疑似错答，人工留意） |
| 585 | validation | What nationality is the singer who recorded "Who I Was Born  | Scottish | 'American' | incorrect | 单 token 短答 'American'（疑似错答，人工留 |
| 586 | validation | What cartel drug lord with the reputation as "The King of Co | Pablo Escobar | 'The cartel drug lord with the reputation as "The K' | correct | gold 命中（含等价/别名） |
| 587 | test | Are both Cypress and Ajuga genera? | no | 'Yes, both Cypress and Ajuga are genera.' | incorrect | gold 未命中 |
| 588 | train | The 2014 All-Pac-12 Conference football team featured player | Mark Helfrich | 'Tim Hawkins' | incorrect | gold 未命中 |
| 589 | train | Where will the student which pass the exam for which Le Rêve | secondary school study | 'Paris.' | incorrect | 单 token 短答 'Paris.'（疑似错答，人工留意） |
| 590 | train | Fodder on My Wings is an album by a singer/pianist/songwrite | 1933 | '1961' | incorrect | 单 token 短答 '1961'（疑似错答，人工留意） |
| 591 | train | Which organization has been led by the overseer of the Renew | Northern Ireland Assembl | 'The organization led by the overseer of the Renewa' | incorrect | gold 未命中 |
| 592 | test | Which amusement park at Coney Island, Brooklyn, New York Cit | Steeplechase Park | 'The amusement park at Coney Island, Brooklyn, New ' | incorrect | gold 未命中 |
| 593 | train | David Sinclair is a fictional character in "Numb3rs", a crim | CBS Corporation | 'David Sinclair is a fictional character in "Numb3r' | incorrect | gold 未命中 |
| 594 | validation | The Actaea genus is native to what continent that the Onocle | Europe | 'Europe' | correct | gold 命中（含等价/别名） |
| 595 | test | Where in London was the 2012 Olympic event featuring athlete | ExCeL Exhibition Centre | 'The 2012 Olympic event featuring athletes such as ' | incorrect | gold 未命中 |
| 596 | test | La Yesca Dam was inaugurated by which Mexican politiician an | Felipe de Jesús Calderón | 'Felipe Calderón' | incorrect | gold 未命中 |
| 597 | validation | What made the man who abolished the Consell in 1718 resume t | upon his son's death | 'The man who abolished the Consell in 1718, King Ge' | incorrect | gold 未命中 |
| 598 | train | Socialist conferences were held with what countries that opp | The Allies of World War  | 'Allied Powers' | incorrect | gold 未命中 |
| 599 | validation | In what city is the mortgage lending company, founded by Dan | Detroit, Michigan | 'Dallas, Texas' | incorrect | gold 未命中 |
| 600 | train | The Secret of Moonacre was directed by the founder of which  | Klasky Csupo | 'The Secret of Moonacre was directed by the founder' | incorrect | gold 未命中 |
| 601 | test | What novel imagines the true story of a character based on a | Shohola Falls | 'The novel that imagines the true story of a charac' | incorrect | gold 未命中 |
| 602 | test | What film directed by David Greene did Merrell Jackson play  | Godspell | 'Merrell Jackson played an apostle in the film "The' | incorrect | gold 未命中 |
| 603 | validation | the movie "A Cure for Wellness" was a science fiction? | is a 2016 science fictio | 'No.' | format_failure | 单 token 函数词/碎片 'No.'，无答案内容 |
| 604 | train | Brindisi, the city where Louis-Jean-Nicolas Lejoille died, i | Italy | 'Brindisi is located in Italy.' | correct | gold 命中（含等价/别名） |
| 605 | train | How did the chairman of the Luthuanian Union of Actors discr | one of Lithuania's most  | 'The chairman of the Lithuanian Union of Actors,' | incorrect | gold 未命中 |
| 606 | train | Cherie Currie and Steve Augeri were both what? | American musician | 'Cherie Currie and Steve Augeri were both American ' | incorrect | gold 未命中 |
| 607 | train | What was the occupation of the man who published an individu | American schoolteacher a | 'Writer.' | incorrect | 单 token 短答 'Writer.'（疑似错答，人工留意 |
| 608 | test | What type of product is the sponsor of the Premiership Rugby | pale lager | 'Alcohol.' | incorrect | 单 token 短答 'Alcohol.'（疑似错答，人工留 |
| 609 | train | In what year was the uprising that marred John P. Buchanan's | 1891 | "The uprising that marred John P. Buchanan's term a" | incorrect | gold 未命中 |
| 610 | validation | Which areas of the United States were still able to deny sam | American Samoa, but not  | 'None' | incorrect | 单 token 短答 'None'（疑似错答，人工留意） |
| 611 | validation | How old was Virginia Bruce when she starred in Let Freedom R | 29 | 'Virginia Bruce was 21 years old when she starred i' | incorrect | gold 未命中 |
| 612 | train | Manchester, New Hampshire is a part of the Northeast megalop | Boston, Providence, Hart | 'Boston and New York' | incorrect | gold 未命中 |
| 613 | train | My Neighbor Totoro was produced by a Japanese animation film | 1985 | 'My Neighbor Totoro was produced by a Japanese anim' | incorrect | gold 未命中 |
| 614 | train | The Kansas City Wizards have had three home venues in Kansas | Arrowhead Stadium | "The Kansas City Wizards' first home venue was Kemp" | incorrect | gold 未命中 |
| 615 | train | Gérald Genta, a Swiss jewelllery designer, worked with what  | International Watch Co. | 'Gérald Genta worked with Peter Jones.' | incorrect | gold 未命中 |
| 616 | validation | WSCV's transmitter is located near this stadium located in w | Miami Gardens, Florida, | "WSCV's transmitter is located near the suburb of C" | incorrect | gold 未命中 |
| 617 | test | What two singers who worked together on the song I Would Lik | Johnny Cash, Waylon Jenn | 'The two singers who worked together on the song "I' | incorrect | gold 未命中 |
| 618 | train | what is the english name of Émile Verdets editorial? | Annals of Chemistry and  | 'Le Monde' | incorrect | gold 未命中 |
| 619 | test | What screenplay was worked on by both Edward Carfagno and Mi | Julius Caesar | 'Unknown.' | format_failure | 规则检出拒答 |
| 620 | train | The infantry rifle regiment of the British Army that Talaias | 1881 | 'The answer is 1899.' | incorrect | gold 未命中 |
| 621 | train | Thirukkalacherry is a village in which Indian town? | Tharangambadi | 'Thirukkalacherry is a village in the Indian town o' | incorrect | gold 未命中 |
| 622 | train | Northland Mall was the first directionally-named shopping ce | Westland Mall | 'Southland Mall' | incorrect | gold 未命中 |
| 623 | train | What band did both Delores Holmes and an inductee to the Roc | E Street Band | 'The Hollies.' | incorrect | gold 未命中 |
| 624 | train | Muz-TV was launched before the 24-hour music channel that wa | Prof Media | 'Muz-TV was launched before MTV.' | incorrect | gold 未命中 |
| 625 | validation | Are Water dropwort and Costus both in the family Apiaceae? | no | 'Yes, both Water dropwort and Costus are in the fam' | incorrect | gold 未命中 |
| 626 | test | What genre of music was played by both Tappi Tíkarrass and I | rock | 'Hard Rock' | correct | gold 命中（含等价/别名） |
| 627 | train | What apartment complex originally constructed in 1927 is inc | Tudor City | 'The Village.' | incorrect | gold 未命中 |
| 628 | validation | Lost in Time includes the theme song for a French/Japanese a | Savin Yeatman-Eiffel | 'Jean Pierrot.' | incorrect | gold 未命中 |
| 629 | train | Which guitar brand was endorsed by the band centered by Ann  | Kramer Guitars | 'Fender' | incorrect | 单 token 短答 'Fender'（疑似错答，人工留意） |
| 630 | test | How long is the bridge in the Öresund Region that connect Co | 8 km | 'The bridge in the Öresund Region that connects Cop' | incorrect | gold 未命中 |
| 631 | validation | What company headquartered in Whitley, Coventry, United King | Jaguar Land Rover | 'Volkswagen' | incorrect | 单 token 短答 'Volkswagen'（疑似错答，人 |
| 632 | train | When did the University, of which The Dove Marine Laboratory | 1963 | '1964' | incorrect | 单 token 短答 '1964'（疑似错答，人工留意） |
| 633 | train | Mehdi Hashemi was thought to be guilty of opposition to the  | Reagan | 'Mehdi Hashemi was thought to be guilty of oppositi' | incorrect | gold 未命中 |
| 634 | test | RL-83 Blindicide was an improved derivative of a wea[on laun | the United States Army | 'Israeli Army' | incorrect | gold 未命中 |
| 635 | train | Who was the fourth son of the lord of the Seventeen Province | Diego Félix of Austria | 'The fourth son of the lord of the Seventeen Provin' | incorrect | gold 未命中 |
| 636 | validation | Dutch-born American businessman, Harry Koch, fathered a son  | Koch Industries | 'Koch Industries' | correct | gold 命中（含等价/别名） |
| 637 | train | High School Confidential, an eight part documentary followed | #364 | '10' | format_failure | 单 token 函数词/碎片 '10'，无答案内容 |
| 638 | test | Where does the founder of The International Grenfell Associa | Newfoundland and Labrado | 'The founder of The International Grenfell Associat' | incorrect | gold 未命中 |
| 639 | train | What is the birthday of the actress who was the Duchess in " | 23 November 1946 | 'July 15, 1925' | incorrect | gold 未命中 |
| 640 | test | What is the birthday of the Earl of Merioneth? | 10 June 1921 | 'The Earl of Merioneth was born on October 10, 1947' | incorrect | gold 未命中 |
| 641 | train | Who wrote the novel that the movie directed by Stanley Kubri | Stephen King | 'Stephen King.' | correct | gold 命中（含等价/别名） |
| 642 | train | What other two divisions of Argentine forces were involved i | Army, Navy | 'The First and Second divisions.' | incorrect | gold 未命中 |
| 643 | test | Morgan Paull played Dave Holden in a 1982 film loosely adapt | Philip K. Dick | 'Stephen King.' | incorrect | gold 未命中 |
| 644 | train | When was the German actress born who is best known for her r | February 22, 1968 | 'The German actress Susanna Armin was born in 1961.' | incorrect | gold 未命中 |
| 645 | train | What movie did Pitof direct which had an action-adventure ti | Catwoman | 'Shrek' | incorrect | 单 token 短答 'Shrek'（疑似错答，人工留意） |
| 646 | validation | Jennifer Ventimilia co-wrote the teleplay of the episode tha | sixth season | 'Season Seven' | incorrect | gold 未命中 |
| 647 | train | When was the rock band to which Pre-Creedence name was chang | 1960s and early 1970s | 'The rock band to which Pre-Creedence name was chan' | incorrect | gold 未命中 |
| 648 | train | Jal Pari, which translated in another language refers to whi | A mermaid | 'Jal Pari, also known as "Water Serpent" or "Sea Se' | incorrect | gold 未命中 |
| 649 | test | Roger O. Egeberg was Assistant Secretary for Health and Scie | 1969 until 1974 | 'Roger O. Egeberg was Assistant Secretary for Healt' | incorrect | gold 未命中 |
| 650 | train | Which avant-garde Japanese composer studied with John Cage a | Toshi Ichiyanagi | 'Yoko Ono' | incorrect | gold 未命中 |
| 651 | train | The American restaurant chain, the Original House of Pies, i | orange juice | 'The Original Juice.' | incorrect | gold 未命中 |
| 652 | train | Did Qionghai or Suining have a population of 658,798 in 2002 | In 2002, Suining had a p | 'Suining' | incorrect | 单 token 短答 'Suining'（疑似错答，人工留意 |
| 653 | test | What son of Larry Johnson was born on November 19, 1979? | Larry Alphonso Johnson J | 'Magic Johnson' | incorrect | gold 未命中 |
| 654 | test | Rocket Rods was a high-speed thrill attraction opened in 199 | August 21, 1995 | '2006' | incorrect | 单 token 短答 '2006'（疑似错答，人工留意） |
| 655 | test | A Pair of Brown Eyes and Wild Mountain Thyme is based from w | Francis McPeake | 'Bob Dylan.' | incorrect | gold 未命中 |
| 656 | test | Are Benjamin Britten and Béla Bartók from the same country? | no | 'No, Benjamin Britten and Béla Bartók are not from ' | correct | gold 命中（含等价/别名） |
| 657 | train | Love Thy Neighbor starred an AMerican actor who was best kno | Three's Company | 'Love Thy Neighbor starred Jack Lemmon.' | incorrect | gold 未命中 |
| 658 | train | Astro Boy and The Secret of Kells share which genre of film? | Animation | 'Astro Boy and The Secret of Kells share the genre ' | incorrect | gold 未命中 |
| 659 | train | Both Tim Conlon and Kehinde Wiley have what type of occupati | artist | 'Artists.' | incorrect | 单 token 短答 'Artists.'（疑似错答，人工留 |
| 660 | train | Which American singer-songwriter toured with J.P. Doherty in | Debbie Harry | 'Amy Winehouse' | incorrect | gold 未命中 |
| 661 | test | Berk Communication and Marketing Group best known for repres | New York Yankees | 'Berk Communication and Marketing Group is best kno' | incorrect | gold 未命中 |
| 662 | train | How many records did Shane Lynch sell as a member of Boyzone | 25 million | 'Shane Lynch sold over 100 million records as a mem' | incorrect | gold 未命中 |
| 663 | train | Who was the lead character designer on "Pepper Ann", and the | Thomas Warburton | 'Tim Hill.' | incorrect | gold 未命中 |
| 664 | test | What platinum selling track was included on the album "The W | I'm Shipping Up to Bosto | '"Americanrie"' | incorrect | 单 token 短答 '"Americanrie"'（疑似错 |
| 665 | train | What production company is owned by the director of "She Hat | 40 Acres and a Mule Film | 'Free Range Productions' | incorrect | gold 未命中 |
| 666 | train | When is the election held for the position former policy dir | November 6, 2018 | 'The election for the position is not yet determine' | incorrect | gold 未命中 |
| 667 | train | When did the UVF Mid-Ulster Brigade conducted the attack The | 31 July 1975 | 'The UVF Mid-Ulster Brigade conducted the attack Th' | incorrect | gold 未命中 |
| 668 | train | In what year was the writer of "The Bet" born? | 1964 | 'The writer of "The Bet" was born in 1961.' | incorrect | gold 未命中 |
| 669 | train | Which university Founded as a college in 1881 is Janet Beer  | The University of Liverp | 'Janet Beer is the Vice-Chancellor of the Universit' | incorrect | gold 未命中 |
| 670 | test | What was the other Los Angeles team that the 1999 Clippers t | Los Angeles Lakers | 'The 1999 Clippers top draft pick, Klay Thompson, w' | correct | gold 命中（含等价/别名） |
| 671 | train | Who did President Franklin Roosevelt appoint that was respon | Robert Digges Wimberly C | 'Robert Weaver.' | incorrect | gold 未命中 |
| 672 | test | When did former Yugoslav which Patricia Hy-Boulais eventuall | in 1994 | '1992' | incorrect | 单 token 短答 '1992'（疑似错答，人工留意） |
| 673 | train | Which CEO of FedEx becked Value America | Frederick Wallace "Fred" | 'Fred Smith' | correct | gold 命中（含等价/别名） |
| 674 | test | Which football player that topped the 10,000-yard career rus | Curtis James Martin Jr. | 'Tom Brady' | incorrect | gold 未命中 |
| 675 | test | What is the population of the town that starts with the lett | 15,023 | 'The population of the town that starts with the le' | incorrect | gold 未命中 |
| 676 | train | Charles Scribner's Sons publishes the books of what author w | Donald Richard "Don" DeL | 'Richard Powers' | incorrect | gold 未命中 |
| 677 | train | What is the name of the record label owned by one of the thr | Dolly Records | 'RCA Records' | incorrect | gold 未命中 |
| 678 | validation | Are Parents and Madame Figaro published in the same country? | no | 'No, Parents and Madame Figaro are not published in' | correct | gold 命中（含等价/别名） |
| 679 | test | When is the national league which the Manchester United is p | 13 May 2018 | 'May' | incorrect | 单 token 短答 'May'（疑似错答，人工留意） |
| 680 | train | Which Canadian heavy metal band is Safe the second EP by | Kittie | 'Mastodon' | incorrect | 单 token 短答 'Mastodon'（疑似错答，人工留 |
| 681 | train | What was the 2010 population of the town where Black Crescen | 310 | 'The 2010 population of the town where Black Cresce' | incorrect | gold 未命中 |
| 682 | train | in 1992 Spengler Cup all matches were played at the home are | HC Davos | 'HC Davos' | correct | gold 命中（含等价/别名） |
| 683 | validation | When was the American actor, film director which Dana Brunet | July 26, 1959 | 'September 17, 1944' | incorrect | gold 未命中 |
| 684 | train | Which former American football player had a part in the movi | Terry Crews | 'Tom Brady.' | incorrect | gold 未命中 |
| 685 | train | Charlie McDermott plays Axl Heck on a tv show that premiered | September 30, 2009 | 'Charlie McDermott plays Axl Heck on the TV show "F' | incorrect | gold 未命中 |
| 686 | test | Which historical drama filmed in the Winter Palace of the Ru | Russian Ark | 'The Catherine.' | incorrect | gold 未命中 |
| 687 | test | Typically how many pages were in the fiction magazine in whi | 128 pages | '32 pages' | incorrect | gold 未命中 |
| 688 | train | What reward did the founder of Chick-Fil-A receive? | Call to Service Award | 'Golden Plate Award.' | incorrect | gold 未命中 |
| 689 | train | In which year was this public research university in which B | 1874 | '1855' | incorrect | 单 token 短答 '1855'（疑似错答，人工留意） |
| 690 | test | GamesMaster has a sister publicantion that is published how  | 13 | 'Four times per year.' | incorrect | gold 未命中 |
| 691 | validation | Are both Frank Lloyd and Olivier Assayas American film direc | no | 'Yes, both Frank Lloyd and Olivier Assayas are Amer' | incorrect | gold 未命中 |
| 692 | train | What English campaigner for the suffragette movement did Ang | Sylvia Pankhurst | 'Pankhurst' | incorrect | 单 token 短答 'Pankhurst'（疑似错答，人工 |
| 693 | train | What month did the an online adult website whose last print  | January | 'June' | incorrect | 单 token 短答 'June'（疑似错答，人工留意） |
| 694 | train | What did Phuture begin that spread to the United Kingdom and | acid-house | 'Phuture began' | incorrect | gold 未命中 |
| 695 | test | What city has a football team and had a player from Pago Pag | He is from Pago Pago, Am | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 696 | test | Are Peter Balakian and James Der Derian both teachers? | yes | 'Yes, both Peter Balakian and James Der Derian are ' | correct | gold 命中（含等价/别名） |
| 697 | test | Which author was a dentist, Zane Grey or Bhabananda Deka? | Pearl Zane Grey | 'Zane Grey' | correct | gold 命中（含等价/别名） |
| 698 | train | When was the University established where Laura Landweber is | 1754 | '1851' | incorrect | 单 token 短答 '1851'（疑似错答，人工留意） |
| 699 | test | What was the name of the 1996 loose adaptation of William Sh | Tromeo and Juliet | 'Hamlet.' | incorrect | 单 token 短答 'Hamlet.'（疑似错答，人工留意 |
| 700 | validation | When did the the Antonine who was known as the third of the  | 24 January 76 – 10 July  | 'The Antonine Pius lived from 138-161 AD.' | incorrect | gold 未命中 |
| 701 | train | Chandamama and Kajal Aggarwal are both associated with which | Telugu and Tamil | 'Chandamama and Kajal Aggarwal are both associated ' | incorrect | gold 未命中 |
| 702 | train | Which Russian figure skating coach was a former competitive  | Nikolai Morozov | 'Alexander Morozov.' | incorrect | gold 未命中 |
| 703 | train | The Column of Saint Zanobi is a monumental marble column loc | a minor basilica | 'The Column of Saint Zanobi is located just north o' | incorrect | gold 未命中 |
| 704 | test | Thomas Tull produced the comedy movie The Hangover, which wa | Las Vegas | 'Los Angeles' | incorrect | gold 未命中 |
| 705 | train | The 1991–92 NBA season included an Achilles tendon injury to | Jacques Dominique Wilkin | 'Michael Jordan' | incorrect | gold 未命中 |
| 706 | test | When was the album released for which Lady Gaga used for mat | October 21, 2016 | 'January 19, 2018' | incorrect | gold 未命中 |
| 707 | train | Are the genera Gordonia and Osbeckia in the same family? | no | 'Yes, the genera Gordonia and Osbeckia are both in ' | incorrect | gold 未命中 |
| 708 | train | In between Hymenosporum and Agrostemma which one is closely  | Hymenosporum flavum | 'Agrostemma' | incorrect | 单 token 短答 'Agrostemma'（疑似错答，人 |
| 709 | test | Are Ian Brown and Dee Snider both actors? | no | 'Yes, both Ian Brown and Dee Snider are actors.' | incorrect | gold 未命中 |
| 710 | test | Who had a perfect game against The Ignitor's team in 1998? | David Wells | 'Tim Wakefield.' | incorrect | gold 未命中 |
| 711 | test | The author of Sexual Politics attended which British Univers | Oxford | 'University of London' | incorrect | gold 未命中 |
| 712 | train | How many people did the South Korean spree killer which NICS | 32 people | '13' | format_failure | 单 token 函数词/碎片 '13'，无答案内容 |
| 713 | train | How many records has the singer which Robert Gale tour with  | 140 million records | '2' | format_failure | 单 token 函数词/碎片 '2'，无答案内容 |
| 714 | train | Who recorded the song written by Johnny Russell | Buck Owens | 'Tom Petty' | incorrect | gold 未命中 |
| 715 | train | Which former mill town is near Rivington Hall Barn? | Bolton | 'Bradford' | incorrect | 单 token 短答 'Bradford'（疑似错答，人工留 |
| 716 | train | Which American popular music and country music singer record | Linda Maria Ronstadt | 'olly Parton' | incorrect | gold 未命中 |
| 717 | train | Are both Stephen R. Donaldson and Michael Moorcock science f | yes | 'Yes, both Stephen R. Donaldson and Michael Moorcoc' | correct | gold 命中（含等价/别名） |
| 718 | train | What airport serviced by American Airlines Shuttle, is also  | Logan International Airp | 'Boston International Airport' | incorrect | gold 未命中 |
| 719 | train | Where is the group of islands named after Purdue University' | the northwest tip of Can | 'The group of islands named after Purdue University' | incorrect | gold 未命中 |
| 720 | train | What is the name of the film directed by Alex Cox adapted fr | Revengers Tragedy | 'The Dutchess' | incorrect | gold 未命中 |
| 721 | train | "Twenty Two" is an episode of the series "The Twilight Zone. | What's My Line | 'Match Game.' | incorrect | gold 未命中 |
| 722 | test | Tommy's Honour was a drama film that included the actor who  | War & Peace | 'Broadchurch' | incorrect | 单 token 短答 'Broadchurch'（疑似错答， |
| 723 | train | The creek of which Paradise Creek is a tributary is a tribut | Delaware River | 'The Colorado River' | incorrect | gold 未命中 |
| 724 | train | Who created the show with Wendy Schaal doing the voice of Fr | Seth MacFarlane | 'Tim Brown.' | incorrect | gold 未命中 |
| 725 | test | What type of veterinary specialist is the star veterinarian  | neuro-orthopaedic | 'Orthopedic surgeon' | incorrect | gold 未命中 |
| 726 | train | Sporobolus and Zea are in the same what? | family | 'Sporobolus and Zea are in the same family.' | correct | gold 命中（含等价/别名） |
| 727 | train | Which of the campaign that brought out the term Vichy Republ | presidential campaign of | 'The campaign that brought out the term "Vichy Repu' | format_failure | 输出为问句回显，无答案内容 |
| 728 | train | What county was Matt Herr raised in? | Bergen | 'Matt Herr was raised in Travis County, Texas.' | incorrect | gold 未命中 |
| 729 | validation | When is the football club which Stan Spinks played for found | in 1902 | '1885' | incorrect | 单 token 短答 '1885'（疑似错答，人工留意） |
| 730 | train | Who is the Chief Executive Officer of the corporation that o | Fatih Ozmen | 'Tim Cook.' | incorrect | gold 未命中 |
| 731 | train | Which Disneyland attraction is Matterhorn Bobsleds roller co | Autopia | 'The Matterhorn Bobsleds roller coaster is an expan' | incorrect | gold 未命中 |
| 732 | validation | In what basketball position does the brother of Saulius Kuzm | small forward | 'Point guard' | incorrect | gold 未命中 |
| 733 | test | What player was the first overall pick in the 2004 NFL draft | Eli Manning | 'Elton Manning' | incorrect | gold 未命中 |
| 734 | test | Which star of The Human Stain was born in 1937? | Anthony Hopkins | 'James Woods.' | incorrect | gold 未命中 |
| 735 | test | Who is the father of the king who attempted to have Eardwulf | Æthelwald Moll | 'The father of the king who attempted to have Eardw' | incorrect | gold 未命中 |
| 736 | train | Michaël Llodra of France, called "the best volleyer on tour" | Argentinian | 'Argentina' | incorrect | 单 token 短答 'Argentina'（疑似错答，人工 |
| 737 | train | The Sentinelese language is the language of people of one of | Andaman Islands | 'North Sentinel Island' | incorrect | gold 未命中 |
| 738 | train | Name an American actress who starred both in High School Hig | Tia Carrere | 'Jessica Simpson.' | incorrect | gold 未命中 |
| 739 | train | What was Thomas Boutflower Bennet's role at The Collegiate S | schoolmaster at J. L. Yo | 'Thomas Boutflower Bennet was the Principal of The ' | incorrect | gold 未命中 |
| 740 | validation | What South Australian capital held UFC Fight Night 65 in May | Adelaide | 'Adelaide' | correct | gold 命中（含等价/别名） |
| 741 | train | When was the club formed, for which Adam Johnson played as w | 1919 | '1887' | incorrect | 单 token 短答 '1887'（疑似错答，人工留意） |
| 742 | train | Who manages the Laboratory that ran the Aurora Generator Tes | Battelle Energy Alliance | 'The University of Chicago.' | incorrect | gold 未命中 |
| 743 | test | When was the English rock band formed that's first recording | June 1975 | 'The English rock band was formed in 1964.' | incorrect | gold 未命中 |
| 744 | test | What year was the major Roman road built that connects to th | 95 AD | 'The major Roman road that connects to the port tha' | incorrect | gold 未命中 |
| 745 | validation | When was the company that produced rectangular crackers that | 1853 | '1926' | incorrect | 单 token 短答 '1926'（疑似错答，人工留意） |
| 746 | test | What was the other name for the war between the Cherokee peo | Chickamauga Wars | 'The other name for the war between the Cherokee pe' | incorrect | gold 未命中 |
| 747 | validation | What is the population of the city in Colombia where Carlos  | 3.7 million | 'Carlos Vieco Ortiz was born in Santiago, Colombia.' | incorrect | gold 未命中 |
| 748 | train | Which British music producer and engineer is notable for wor | Gareth Jones | 'Alan Parsons.' | incorrect | gold 未命中 |
| 749 | train | Which character does this protagonist, who secretly loves an | Tybalt | 'Mercutio' | incorrect | 单 token 短答 'Mercutio'（疑似错答，人工留 |
| 750 | validation | The subject of the biography "Name Dropper" was born in what | 1961 | 'The subject of the biography "Name Dropper" was bo' | incorrect | gold 未命中 |
| 751 | train | Bridgewater Trustees major source of income came from a cana | Francis Egerton | "The Bridgewater Trustees' major source of income c" | incorrect | gold 未命中 |
| 752 | train | What was Sophia Dallas' husbands name who served under the 1 | Vice President George | 'James Monroe.' | incorrect | gold 未命中 |
| 753 | train | Carl Barks is best known for his comics about the cartoon ch | 1934 | 'Carl Barks is best known for his comics about the ' | incorrect | gold 未命中 |
| 754 | train | This aircraft carrier served as a recovery ship for this fli | three | '7' | format_failure | 单 token 函数词/碎片 '7'，无答案内容 |
| 755 | train | Which Eminem album included vocals from a singer who had an  | "The Marshall Mathers LP | 'Encore' | incorrect | 单 token 短答 'Encore'（疑似错答，人工留意） |
| 756 | train | The Bart the Fink episode of The Simpsons aired in February  | The Itchy & Scratchy Sho | 'Bart the Kid' | incorrect | gold 未命中 |
| 757 | train | The revue Putting It Together was devised by Stephen Sondhei | Julia McKenzie | 'Agatha Christie' | incorrect | gold 未命中 |
| 758 | train | YouPorn was surpassed, in 2013, by competitor sites xHamster | XVideos | 'RedTube' | incorrect | 单 token 短答 'RedTube'（疑似错答，人工留意 |
| 759 | test | An Austrian-British psychoanalyst born in 1882 and innovativ | Morita therapy | 'behavioral therapy' | incorrect | gold 未命中 |
| 760 | test | Kam Heskin plays Paige Morgan in a 2004 film directed by who | Martha Coolidge | 'Kam Heskin plays Paige Morgan in the 2004 film "Th' | incorrect | gold 未命中 |
| 761 | train | What was the given name of the singer who is most closely as | William Howard Ashton, | 'Tom Petty.' | incorrect | gold 未命中 |
| 762 | test | Father Jean-Pierre Aulneau de le Touche was killed before he | North Dakota | 'North Dakota' | correct | gold 命中（含等价/别名） |
| 763 | train | What single was released by a American country singer, songw | Feels Like Love | '"American Pie"' | incorrect | gold 未命中 |
| 764 | train | The Church of the Guanche People was founded in the city tha | Macaronesia | 'The Church of the Guanche People was founded in th' | incorrect | gold 未命中 |
| 765 | validation | Who was President of the United States when Jennifer Hunt se | Barack Obama | 'Barack Obama' | correct | gold 命中（含等价/别名） |
| 766 | train | When was the track from which a sample was featured in "Take | 16 March 1987 | 'The track from which a sample was featured in "Tak' | incorrect | gold 未命中 |
| 767 | test | Isabella Kelly was born at a ruined castle characterized as  | The Changing Scottish La | 'Isabella Kelly was born at Dunster Castle.' | incorrect | gold 未命中 |
| 768 | test | What 1876 battle featured the Other Magpie? | Battle of the Rosebud | 'The Battle of the Magpie.' | incorrect | gold 未命中 |
| 769 | test | What type of music features Geetam, created by a devotee of  | Carnatic | 'The type of music that features Geetam, created by' | incorrect | gold 未命中 |
| 770 | train | What was the highest grossing movie of 2010? | Toy Story 3 | 'The highest grossing movie of 2010 was Avatar.' | incorrect | gold 未命中 |
| 771 | train | English economist and physician Nicholas Barbon helped to pi | Fire insurance | 'Life insurance.' | incorrect | gold 未命中 |
| 772 | test | Mount Lascar is in which South American country? | Chile | 'Mount Lascar is in Chile.' | correct | gold 命中（含等价/别名） |
| 773 | train | Which country suspended its annual Antarctic Whale Hunt in F | Japan | 'Japan' | correct | gold 命中（含等价/别名） |
| 774 | validation | Mistral, chinook, zonda, and willy-willy are types of which  | Winds | 'Wind.' | correct | gold 别名命中 |
| 775 | validation | The white pinwheel shaped Tiare is the national flower of wh | French Polynesia | 'Samoa' | incorrect | 单 token 短答 'Samoa'（疑似错答，人工留意） |
| 776 | test | In humans, alopecia is the loss of what? | Hair | 'Hair.' | correct | gold 命中（含等价/别名） |
| 777 | validation | A popular 1960s TV cowboy series, what is a cutaneous coveri | Rawhide | 'Buckskin' | incorrect | 单 token 短答 'Buckskin'（疑似错答，人工留 |
| 778 | train | A Gay Girl in Damascus is the title of a hoax blog by fictio | Syria | 'Syria' | correct | gold 命中（含等价/别名） |
| 779 | train | French for an additive, and a Venezuelan liberator of Ecuado | Sucre | 'The currency of Ecuador before adopting the US dol' | correct | gold 命中（含等价/别名） |
| 780 | validation | Sukhoi and Tupolev are aircraft manufacturers of what nation | Russia | 'Sukhoi and Tupolev are aircraft manufacturers of R' | correct | gold 命中（含等价/别名） |
| 781 | test | What is the international telephone dialling code for German | 49 | 'The international telephone dialling code for Germ' | incorrect | gold 未命中 |
| 782 | validation | A Tale of Two Cities? | Charles Dickens | '"A Tale of Two Cities" is a novel by Charles Dicke' | correct | gold 命中（含等价/别名） |
| 783 | test | Whose father wrote and sang the popular 'Secret Lemonade Dri | Elvis Costello | 'Tom Jones.' | incorrect | gold 未命中 |
| 784 | train | As at 2012 Goulburn Correctional Centre is considered the hi | Australia | 'Australia' | correct | gold 命中（含等价/别名） |
| 785 | train | What is the main metallic element in the core of the moon? | Iron | 'The main metallic element in the core of the moon ' | correct | gold 命中（含等价/别名） |
| 786 | train | The medical term bariatric refers (increasingly politically  | Obesity | 'The medical term bariatric refers to the human con' | correct | gold 命中（含等价/别名） |
| 787 | train | A period of Northern Hemisphere climatic extremes occurring  | Ice Age | 'Ice Age' | correct | gold 命中（含等价/别名） |
| 788 | train | A harquebus/arquebus is an early form of? | Gun | 'A harquebus/arquebus is an early form of a musket.' | incorrect | gold 未命中 |
| 789 | train | Lysergic Acid Diethylamide is better known by what abbreviat | LSD | 'LSD' | correct | gold 命中（含等价/别名） |
| 790 | test | What cartoon character featured on a $100,000 auctioned post | Mickey Mouse | 'Batman' | incorrect | 单 token 短答 'Batman'（疑似错答，人工留意） |
| 791 | train | What is confit meat cooked and preserved in? | Fat | 'Oil.' | incorrect | 单 token 短答 'Oil.'（疑似错答，人工留意） |
| 792 | train | A ewer is a large? | Jug | 'A ewer is a large bowl.' | incorrect | gold 未命中 |
| 793 | test | What Olympic event entails disqualification if both feet of  | Racewalking | 'Triple jump' | incorrect | gold 未命中 |
| 794 | train | The rights to which famous character were sold by creators J | Superman | 'Superman' | correct | gold 命中（含等价/别名） |
| 795 | validation | The UK political Labour Party's famously controversial 1995  | Nationalization | 'Social democracy.' | incorrect | gold 未命中 |
| 796 | test | "The Duke of Wellington's suggestion of ""Sparrowhawks"" to  | Crystal Palace | 'Buckingham Palace' | incorrect | gold 未命中 |
| 797 | validation | What red fruit-juice-based drink whose name alludes to energ | Vimto | 'Energy.' | incorrect | 单 token 短答 'Energy.'（疑似错答，人工留意 |
| 798 | train | What characteristic of Borneo ranks it among the largest fiv | Island | 'Borneo is the third-largest island in the world.' | correct | gold 命中（含等价/别名） |
| 799 | validation | In physics, what is a substance that continually deforms/flo | Fluid | 'In physics, a substance that continually deforms/f' | correct | gold 命中（含等价/别名） |
| 800 | validation | In what year was Band-Aid's Do They Know It's Christmas the  | 1984 | 'Band Aid\'s "Do They Know It\'s Christmas" was the U' | correct | gold 命中（含等价/别名） |
| 801 | test | Suya, Puff Puff, and Moin Moin (or Moyi-Moyi) are well-known | Foods | 'dancers' | incorrect | 单 token 短答 'dancers'（疑似错答，人工留意 |
| 802 | validation | In team ball games such as football, a pass to a team-mate w | Hospital | 'Screen.' | incorrect | 单 token 短答 'Screen.'（疑似错答，人工留意 |
| 803 | validation | Matthias Sammer, Ronaldo, Zinedine Zidane, Rivaldo, and Luis | European Footballer of t | 'Matthias Sammer, Ronaldo, Zinedine Zidane, Rivaldo' | incorrect | gold 未命中 |
| 804 | train | What in the human body is the calcaneum? | Heel bone | 'The calcaneum is the largest bone in the human bod' | correct | gold 别名命中 |
| 805 | train | What mountain's peak is the farthest point from Earth's cent | Chimborazo | 'Denali' | incorrect | 单 token 短答 'Denali'（疑似错答，人工留意） |
| 806 | test | Name the four terrestrial planets of the Solar System? | Mercury, Venus, Earth, M | 'The four terrestrial planets of the Solar System a' | incorrect | gold 未命中 |
| 807 | train | The Erythraean Sea, lying between Africa and Asia is more co | Red Sea | 'Red Sea' | correct | gold 命中（含等价/别名） |
| 808 | train | US veterinary pathologist Daniel Salmon (1850-1914) oversaw  | Salmonella | 'Salmonella.' | correct | gold 命中（含等价/别名） |
| 809 | train | American businessman and philanthropist Solomon Guggenheim ( | Museums | 'art museums' | correct | gold 命中（含等价/别名） |
| 810 | train | To what does the portmanteau word Grexit refer? | Greece Exit | 'Brexit refers to the United Kingdom leaving the Eu' | incorrect | gold 未命中 |
| 811 | train | JP Morgan, Barclays, RBS, Citigroup, Bank of America, and UB | Foreign Exchange | 'Forex.' | incorrect | 单 token 短答 'Forex.'（疑似错答，人工留意） |
| 812 | validation | Name the pioneering Game Theory US mathematician featured in | John Nash | 'John Nash' | correct | gold 命中（含等价/别名） |
| 813 | validation | What famous road began in Chicago, Illinois, ending at Santa | Route 66 | 'The Lincoln Highway.' | incorrect | gold 未命中 |
| 814 | train | Dermalogica, Olay, Clearasil, and Nutrogena are brands of? | Skincare | 'Dermalogica, Olay, Clearasil, and Nutrogena are br' | correct | gold 命中（含等价/别名） |
| 815 | train | The fictitious South American city/country El Dorado was abu | Gold | 'Gold.' | correct | gold 命中（含等价/别名） |
| 816 | train | Traditional Latin pluralization of Latin-originating words e | i | 'i' | correct | gold 命中（含等价/别名） |
| 817 | train | Five ninths of three fifths is a? | Third | 'Fraction' | incorrect | 单 token 短答 'Fraction'（疑似错答，人工留 |
| 818 | validation | Which Gilbert and Sullivan operetta is sub-titled The Slave  | The Pirates of Penzance | 'The Mikado' | incorrect | gold 未命中 |
| 819 | test | Feugo, Yangin, Brand, and Pozar are Spanish, Turkish, Dutch  | Fire | 'Wine.' | incorrect | 单 token 短答 'Wine.'（疑似错答，人工留意） |
| 820 | train | What gas, symbol F, is the most reactive of all chemical ele | Fluorine | 'Fluorine' | correct | gold 命中（含等价/别名） |
| 821 | train | In 2015 Japan lowered its voting age from what to what? | 20 to 18 | '20 to 18' | correct | gold 命中（含等价/别名） |
| 822 | test | What African nation is known in parts of Asia by the local n | Morocco | 'Morocco' | correct | gold 命中（含等价/别名） |
| 823 | test | Which country occupying 47% of South America has states incl | Brazil | 'Brazil' | correct | gold 命中（含等价/别名） |
| 824 | validation | Leicester City FC's owners are (at 2016) what nationality? | Thailand | 'American' | incorrect | 单 token 短答 'American'（疑似错答，人工留 |
| 825 | train | A warm sunny period in Autumn (Fall) in the northern hemisph | Indian Summer | 'Autumn.' | incorrect | 单 token 短答 'Autumn.'（疑似错答，人工留意 |
| 826 | train | Born Henry John Deutschendorf Junior, which American singer  | John Denver | 'John Denver.' | correct | gold 命中（含等价/别名） |
| 827 | test | Name the ballet dancer who requested asylum in France while  | Rudolph Nureyev | 'Nina Batalova' | incorrect | gold 未命中 |
| 828 | train | The cult TV series Lost which began in 2004 features 'Oceani | 815 | 'Seven.' | incorrect | 单 token 短答 'Seven.'（疑似错答，人工留意） |
| 829 | train | Which country won the 2007 FIFA Women's World Cup? | Germany | 'China' | incorrect | 单 token 短答 'China'（疑似错答，人工留意） |
| 830 | train | Who became the new French president in 2007? | Nicolas Sarkozy | ' Nicolas Sarkozy became the new French president i' | correct | gold 命中（含等价/别名） |
| 831 | train | Who wrote and had a hit with the instrumental Classical Gas? | Mason Williams | 'Tom Jones.' | incorrect | gold 未命中 |
| 832 | train | In which year did Captain Scott reach the South Pole? | 1912 | '1912' | correct | gold 命中（含等价/别名） |
| 833 | train | The NASA spacecraft Messenger reached what planet destinatio | Mercury | 'Mercury' | correct | gold 命中（含等价/别名） |
| 834 | train | What colour is the inner ring of an Olympic archery target? | Gold | 'The inner ring of an Olympic archery target is red' | incorrect | gold 未命中 |
| 835 | test | In the human body what is the Axilla commonly known as? | The armpit | 'The axilla is commonly known as the armpit.' | correct | gold 命中（含等价/别名） |
| 836 | train | Jimmy Wales and Larry Sanger founded which website in 2001? | Wikipedia | 'Wikipedia' | correct | gold 命中（含等价/别名） |
| 837 | validation | Which US lead singer's real name is William Baily? | Axl Rose | 'Tom Petty' | incorrect | gold 未命中 |
| 838 | train | In which English county is the Dickens World Theme Park? | Kent | 'Dickens World Theme Park is located in Staffordshi' | incorrect | gold 未命中 |
| 839 | train | Which fashion designer introduced the Polo label in 1967? | Ralph Lauren | 'Ralph Lauren.' | correct | gold 命中（含等价/别名） |
| 840 | train | According to legend who killed the lion represented by the c | Hercules | 'Hercules' | correct | gold 命中（含等价/别名） |
| 841 | test | What merchant bank collapsed in 1995 due to unauthorised deb | Barings | 'Barings.' | correct | gold 命中（含等价/别名） |
| 842 | train | What is the Japanese martial art, similar to judo, which use | Aikido | 'Kendo' | incorrect | 单 token 短答 'Kendo'（疑似错答，人工留意） |
| 843 | validation | Which French prime minister was executed for treason in 1945 | Pierre Laval | 'Pierre Pétain.' | incorrect | gold 未命中 |
| 844 | train | Herman Van Rompuy became first Permanent President of what? | The European Council | 'Herman Van Rompuy became the first Permanent Presi' | correct | gold 命中（含等价/别名） |
| 845 | train | The Bell Rock Lighthouse, said to be the oldest surviving of | Scotland | 'England' | incorrect | 单 token 短答 'England'（疑似错答，人工留意 |
| 846 | train | The Collegiate Church of St Peter in London is more popularl | Westminster Abbey | ' Westminster Abbey.' | correct | gold 命中（含等价/别名） |
| 847 | train | The fortified wine drink Sherry is named after what town? | Jerez | 'Sherry' | incorrect | 单 token 短答 'Sherry'（疑似错答，人工留意） |
| 848 | train | In 1725 Catherine the First succeeded which Russian emperor, | Peter the First | 'Peter I' | incorrect | gold 未命中 |
| 849 | validation | How many triangles are on a backgammon board? | Twenty-four | 'There are no triangles on a backgammon board.' | incorrect | gold 未命中 |
| 850 | test | Ireland is known as The 'what' Isle? | Emerald | 'Green' | incorrect | 单 token 短答 'Green'（疑似错答，人工留意） |
| 851 | train | Originating in early central American culture, where on the  | Foot | 'A huarache would be worn on the head.' | incorrect | gold 未命中 |
| 852 | train | Name the head of the 'whistleblowing' website Wikileaks, in  | Julian Assange | 'Julian Assange' | correct | gold 命中（含等价/别名） |
| 853 | train | Which English public school shares it's name with a farm imp | Harrow | 'Harrow School' | correct | gold 命中（含等价/别名） |
| 854 | train | Who played Clayton Farlowe in Dallas | Howard Keel | 'David Jason.' | incorrect | gold 未命中 |
| 855 | test | Which millionaire's daughter married Imran Khan in 1995 | Sir James Goldsmith | 'Shahid Khan' | incorrect | gold 未命中 |
| 856 | train | Which musical instrument was Jelly Roll Morton associated wi | Piano | 'Jelly Roll Morton was associated with the piano.' | correct | gold 命中（含等价/别名） |
| 857 | train | What is the largest natural lake in Wales | Lake Bala | 'The largest natural lake in Wales is Lake Conwy.' | incorrect | gold 未命中 |
| 858 | validation | What was the name of Catherine Zeta Jones character in The D | Mariette | 'Jane Darling.' | incorrect | gold 未命中 |
| 859 | train | In which country was Queen Elizabeth 11 when she heard of he | Kenya | 'Canada' | incorrect | 单 token 短答 'Canada'（疑似错答，人工留意） |
| 860 | train | What was bandleader Joe Loss's signature tune | In The Mood | 'Joe Loss\'s signature tune was "The Big Hit."' | incorrect | gold 未命中 |
| 861 | test | What nationality is singer Vanessa Paradis | French | 'Vanessa Paradis is a French singer.' | correct | gold 命中（含等价/别名） |
| 862 | train | Which cup competition was founded by Charles William Alcock  | The FA Cup | 'The FA Cup' | correct | gold 命中（含等价/别名） |
| 863 | train | Who played the title role in the TV western series Bronco | Ty Hardin | 'James Arness' | incorrect | gold 未命中 |
| 864 | train | How was Monday October 19, 1987 known in the world of financ | Black Monday | 'Monday, October 19, 1987, is known as "Black Monda' | correct | gold 命中（含等价/别名） |
| 865 | test | On which river is the city of Ely | The Ouse | 'The city of Ely is located on the River Ouse.' | incorrect | gold 未命中 |
| 866 | train | Which Oscar winning song came from the film Pocahontas | Colours of the Wind | 'The Wind.' | correct | gold 命中（含等价/别名） |
| 867 | test | What is the title of Max Bygraves autobiography | I Wanna Tell You a Story | 'The Game.' | incorrect | gold 未命中 |
| 868 | train | What country singer's duets with Loretta Lynn ended when he  | Conway Twitty | 'olly Parton' | incorrect | gold 未命中 |
| 869 | test | What flower was named after the Duke of Cumberland | Sweet William | 'Cumbine' | incorrect | 单 token 短答 'Cumbine'（疑似错答，人工留意 |
| 870 | train | Whose autobiography was titled 1966 And All That | Geoff Hurst | 'Bob Dylan' | incorrect | gold 未命中 |
| 871 | train | Which English town's Anglo Saxon name was Gipeswic pronounce | Ipswich | 'Greenwich' | incorrect | 单 token 短答 'Greenwich'（疑似错答，人工 |
| 872 | train | Made in Scotland what type of beverage is Rock Rose | Gin | 'Rock Rose is a Scotch whisky.' | incorrect | gold 未命中 |
| 873 | test | What is vellum parchment made from | Calfskin | 'Vellum parchment is made from animal skin.' | incorrect | gold 未命中 |
| 874 | train | Who wrote the poems If, Gunga Din, Mandalay, and The Female  | Rudyard Kipling | 'Alfred Owen' | incorrect | gold 未命中 |
| 875 | train | Which British submarine sank the General Belgrano in the Fal | HMS Conqueror | 'HMS Exeter' | incorrect | gold 未命中 |
| 876 | validation | What was the name of the building destroyed in the Oklahoma  | Alfred Murrah Federal Bu | 'The Oklahoma Federal Building' | incorrect | gold 未命中 |
| 877 | test | During a penalty shoot out in soccer where should the non pa | In the centre circle | 'During a penalty shootout in soccer, the non-parti' | incorrect | gold 未命中 |
| 878 | train | What was the former name of The Home Guard | Local Defence Volunteers | 'The former name of The Home Guard was the Local De' | incorrect | gold 未命中 |
| 879 | train | What was the name of the character played by Bonnie Langford | Violet Elizabeth Bott | 'Mary.' | incorrect | 单 token 短答 'Mary.'（疑似错答，人工留意） |
| 880 | validation | What used to be bought at Spitalfields market apart from fru | Flowers | 'Fish.' | incorrect | 单 token 短答 'Fish.'（疑似错答，人工留意） |
| 881 | test | Which Australian prime minister was said to have tweaked the | Paul Keating | 'John Howard' | incorrect | gold 未命中 |
| 882 | validation | "Which famous children's novel begins with the words ""The m | The Wind in the Willows | "The famous children's novel that begins with the w" | incorrect | gold 未命中 |
| 883 | test | Who were the first League Cup winners | Aston Villa | 'The first League Cup winners were Manchester City.' | incorrect | gold 未命中 |
| 884 | test | What nationality was Aristotle Onassis originally | Turkish | 'Aristotle Onassis was originally Greek.' | incorrect | gold 未命中 |
| 885 | train | Which female singer had a top ten hit in 1998 with My Favour | Sheryl Crow | 'Alicia Keys' | incorrect | gold 未命中 |
| 886 | train | Who in verse sailed to the land where the bong tree grows | The owl and the pussycat | 'Christopher Columbus' | incorrect | gold 未命中 |
| 887 | train | On which game show was Bobby Charlton once a contestant and  | Double Your Money | 'Bobby Charlton was a contestant and winner on the ' | incorrect | gold 未命中 |
| 888 | train | Which wild life quiz show was hosted by Henry Kelly | Monkey Business | 'Wild World' | incorrect | gold 未命中 |
| 889 | train | What award is given for a wound in the American forces | Purple Heart | 'The Purple Heart' | correct | gold 命中（含等价/别名） |
| 890 | train | Which boxer broke Muhammed Ali's jaw | Ken Norton | 'Joe Frazier' | incorrect | gold 未命中 |
| 891 | train | What nationality was Che Guevara | Argentinean | 'Che Guevara was Argentine.' | incorrect | gold 未命中 |
| 892 | train | Born in 1970, which female has been a presenter on the TV sh | Zoë Ball | 'Amanda Holden' | incorrect | gold 未命中 |
| 893 | test | Which torture chamber was invented by George Orwell? | Room 101 | 'None.' | incorrect | 单 token 短答 'None.'（疑似错答，人工留意） |
| 894 | train | Which 1949 film was set on the Scottish island of Todday? | Whisky Galore | 'The Island.' | incorrect | gold 未命中 |
| 895 | train | Red Grant was a villain in which James Bond movie? | From Russia With Love | 'Red Grant was a villain in the James Bond movie "D' | incorrect | gold 未命中 |
| 896 | train | The Conservation of Energy is the first ……..what? | Law of Thermodynamics | 'The Conservation of Energy is the first law of the' | correct | gold 命中（含等价/别名） |
| 897 | train | Whose “left hand” rule can predict the direction of motion o | John Ambrose Fleming | 'Michael Faraday' | incorrect | gold 未命中 |
| 898 | validation | What is the name of the O’Haras’ plantation in ‘Gone with th | TARA | 'Big Tara.' | correct | gold 命中（含等价/别名） |
| 899 | train | Clyde Tombaugh discovered which celestial object in our sola | PLUTO | 'Pluto' | correct | gold 命中（含等价/别名） |
| 900 | train | In a 1763 swap, what expanse of land did Britain gain from S | FLORIDA | 'Spanish Florida' | correct | gold 命中（含等价/别名） |
| 901 | test | What is the official march of the Royal Navy? | Heart of Oak | 'The official march of the Royal Navy is "The Royal' | incorrect | gold 未命中 |
| 902 | train | Which crop is attacked by the Colorado Beetle? | Potato | 'Corn' | incorrect | 单 token 短答 'Corn'（疑似错答，人工留意） |
| 903 | train | Who had a hit in 1966 with When a Man Loves a Woman? | Percy Sledge | 'Tom Jones.' | incorrect | gold 未命中 |
| 904 | test | From what illness did Mary II die in 1694? | Smallpox | 'Smallpox.' | correct | gold 命中（含等价/别名） |
| 905 | train | Which football team are nicknamed the Blaugrana? | Barcelona | 'Real Madrid' | incorrect | gold 未命中 |
| 906 | validation | Which is the highest position in the Metropolitan Police? | Commissioner | 'The highest position in the Metropolitan Police is' | incorrect | gold 未命中 |
| 907 | test | What bird did Good Queen Bess decree should be eaten at Chri | GOOSE | 'Good Queen Bess decreed that a peacock should be e' | incorrect | gold 未命中 |
| 908 | train | Which Michael Frayn play features a ‘play within a play’ ent | Noises Off | 'The Hours' | incorrect | gold 未命中 |
| 909 | train | What is measured by a Bourdon Gauge? | Pressure | 'A Bourdon Gauge measures pressure.' | correct | gold 命中（含等价/别名） |
| 910 | train | At which battle of 2 December 1805 did Napoleon defeat a com | Battle of Austerlitz | 'Ulm.' | incorrect | 单 token 短答 'Ulm.'（疑似错答，人工留意） |
| 911 | validation | What is the symbol for the chemical element protactinium, at | Pa | 'The symbol for the chemical element protactinium i' | correct | gold 命中（含等价/别名） |
| 912 | validation | 'Nobody puts Baby in a corner.' is a line from which 1987 fi | Dirty Dancing | "'Nobody puts Baby in a corner.' is a line from the" | incorrect | gold 未命中 |
| 913 | train | Mrs Darrell Waters books were translated into 120 languages. | Enid Blyton | 'Anne Perry.' | incorrect | gold 未命中 |
| 914 | train | Sidney Poitier, Eartha Kitt, Val Doonican and Ferenc Puskas  | 1927 | 'Sidney Poitier, Eartha Kitt, Val Doonican, and Fer' | incorrect | gold 未命中 |
| 915 | train | Who is widely credited with introducing his former wife Whit | BOBBY BROWN | 'James Brown' | incorrect | gold 未命中 |
| 916 | train | Captain of the Flying Dustman, what was the name of Captain  | Cut-throat Jake | 'Captain Flint.' | incorrect | gold 未命中 |
| 917 | train | Weighing-in at up 48 stone, who wrestled under the ring-name | Martin Ruane | 'Mike Graham' | incorrect | gold 未命中 |
| 918 | train | Which woman was voted BBC Sports Personality of the Year in  | PRINCESS ANNE | 'Mary Peters.' | incorrect | gold 未命中 |
| 919 | test | What do 4 roods equal? | An Acre | '4 roods equal 1 yard.' | incorrect | gold 未命中 |
| 920 | train | The bumblebee or hog-nosed is the smallest mammal in the wor | Bat | 'The bumblebee.' | incorrect | gold 未命中 |
| 921 | train | What do we call the selfless and virtuous practice of concer | ALTRUISM | 'Altruism.' | correct | gold 命中（含等价/别名） |
| 922 | test | The SI unit the ohm is often represented by the upper-case f | OMEGA | 'Ω' | format_failure | 单 token 函数词/碎片 'Ω'，无答案内容 |
| 923 | test | As well as municipalities, which country is made up of 26 st | BRAZIL | 'Mexico' | incorrect | 单 token 短答 'Mexico'（疑似错答，人工留意） |
| 924 | train | In which city did the gangland St Valentine’s Day Massacre t | CHICAGO | 'New York City' | incorrect | gold 未命中 |
| 925 | test | Which bird is the international symbol for happiness? | Bluebird | 'The bluebird is the international symbol for happi' | correct | gold 命中（含等价/别名） |
| 926 | train | Who wrote the BBC tv serial drama ‘The Singing Detective’ (1 | DENNIS POTTER | 'John le.' | incorrect | gold 未命中 |
| 927 | train | What is Britain’s bestselling breakfast cereal? | Weetabix | "Britain's bestselling breakfast cereal is Crunchie" | incorrect | gold 未命中 |
| 928 | train | The bestselling children’s book “Grandpa’s great escape” is  | David Walliams | 'Peter Brown.' | incorrect | gold 未命中 |
| 929 | train | Tintern Abbey, made famous by Wordsworth’s poetry, stands on | Wye | 'Tintern Abbey stands on the River Wye.' | correct | gold 命中（含等价/别名） |
| 930 | test | What was Her Majesty's Prison Manchester called until 1990? | Strangeways | 'Manchester HM Prison.' | correct | gold 别名命中 |
| 931 | test | What was Margot’s surname in “The Good Life” TV series? | Leadbetter | 'Taylor.' | incorrect | 单 token 短答 'Taylor.'（疑似错答，人工留意 |
| 932 | validation | In humans ribs are divided into three types. True, False and | Floating | 'False' | incorrect | 单 token 短答 'False'（疑似错答，人工留意） |
| 933 | test | Which is the most southerly of the Shipping Forecast areas? | Trafalgar | 'South Atlantic' | incorrect | gold 未命中 |
| 934 | test | The disease blossom end rot is most frequently found in whic | Tomatoes | 'Tomatoes.' | correct | gold 命中（含等价/别名） |
| 935 | train | According to several early Old Testament books, who led the  | JOSHUA | 'Joshua' | correct | gold 命中（含等价/别名） |
| 936 | test | ‘When Will You Marry?’ became the world’s most expensive wor | Paul GAUGUIN | "'When Will You Marry?' became the world's most exp" | incorrect | gold 未命中 |
| 937 | train | The prominent headland known as the Great Orme is close to w | LLANDUDNO | 'Cardiff' | incorrect | 单 token 短答 'Cardiff'（疑似错答，人工留意 |
| 938 | train | What dark brown food paste is the Australian version of Marm | VEGEMITE | 'Vegemite' | correct | gold 命中（含等价/别名） |
| 939 | test | Which planet did Gustav Holst describe as the ‘Winged Messen | Mercury | 'Mercury' | correct | gold 命中（含等价/别名） |
| 940 | train | Which early sixties singer was backed by The Bruvvers? | Joe Brown | 'Tom Jones.' | incorrect | gold 未命中 |
| 941 | test | Merton Pride and Williams are varieties of which fruit? | Pear | 'Merton Pride and Williams are varieties of apples.' | incorrect | gold 未命中 |
| 942 | train | Which city in the USA suffered a huge fire in 1871 allegedly | Chicago | 'The city in the USA that suffered a huge fire in 1' | incorrect | gold 未命中 |
| 943 | train | “Dreams from my father, a story of race and heritance” is ab | Barack Obama | 'Barack Obama' | correct | gold 命中（含等价/别名） |
| 944 | train | Created in 1662, In which city is Phoenix Park? | Dublin | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 945 | train | Which character was played by John Inman in “Are you being s | Mr. Humphries | 'Johnno' | incorrect | 单 token 短答 'Johnno'（疑似错答，人工留意） |
| 946 | test | Which two countries took part in the short Kargil War in 199 | India and Pakistan | 'India and Pakistan.' | correct | gold 命中（含等价/别名） |
| 947 | test | From the Greek for ‘artificial’, what was the first synthesi | Technetium | 'Radium' | incorrect | 单 token 短答 'Radium'（疑似错答，人工留意） |
| 948 | train | Who presented the 1980 blockbuster documentary series, Cosmo | Carl Sagan | 'Carl Sagan' | correct | gold 命中（含等价/别名） |
| 949 | train | The Analects are the writings of which Eastern philosopher? | Confucius | 'The Analects are the writings of the Eastern philo' | correct | gold 命中（含等价/别名） |
| 950 | test | Which 1987 US film was based on the 1985 French film ‘Trois  | THREE MEN AND A BABY | 'Three Men' | correct | gold 命中（含等价/别名） |
| 951 | train | What are the last six words of Rudyard Kipling’s ‘If’? | YOU’LL BE A MAN, MY SON | 'And so would I.' | incorrect | gold 未命中 |
| 952 | train | Which motor scooter had a name meaning ‘wasp’? | Vespa | 'Volpi' | incorrect | 单 token 短答 'Volpi'（疑似错答，人工留意） |
| 953 | train | The Wasp Factory was the debut novel of which author who die | Iain Banks | 'Roald Dahl' | incorrect | gold 未命中 |
| 954 | train | The Most Noble Order of the Garter was established during th | Edward III | 'The Most Noble Order of the Garter was established' | correct | gold 命中（含等价/别名） |
| 955 | validation | Which duo created the “Dagenham dialogues”? | Peter Cook and Dudley Mo | 'John Lennon and Paul McCartney.' | incorrect | gold 未命中 |
| 956 | validation | Swinley Bottom forms part of the track on which famous racec | Ascot | 'Cheltenham.' | incorrect | 单 token 短答 'Cheltenham.'（疑似错答， |
| 957 | train | If you were performing an orison what would you be doing? | Praying | 'If you were performing an orison, you would be sin' | incorrect | gold 未命中 |
| 958 | train | What type of food or drink is a macchiato? | COFFEE | 'A macchiato is a type of coffee drink.' | correct | gold 命中（含等价/别名） |
| 959 | train | Amanuensis is an archaic word for what profession? | Secretary | 'Amanuensis is an archaic word for a physician.' | incorrect | gold 未命中 |
| 960 | train | Who did Claus von Stauffenberg plot to kill? | Adolf Hitler | 'Claus von Stauffenberg plotted to kill Adolf Hitle' | correct | gold 命中（含等价/别名） |
| 961 | validation | What does the French word noir mean in English? | Black | 'The French word "noir" means "black" in English.' | correct | gold 命中（含等价/别名） |
| 962 | train | "What country's ""Kingdom Tower"" is planned to be more than | Saudi Arabia | 'Saudi Arabia' | correct | gold 命中（含等价/别名） |
| 963 | test | What country does Waterford crystal come from? | Ireland | 'Ireland' | correct | gold 命中（含等价/别名） |
| 964 | train | What country is the largest oil producer in Africa? | Nigeria | 'Nigeria' | correct | gold 命中（含等价/别名） |
| 965 | train | What company is the world's largest auction house? | Christie's | "Christie's" | correct | gold 命中（含等价/别名） |
| 966 | train | What movie starred Michael Jordan? | Space Jam | 'Space Jam.' | correct | gold 命中（含等价/别名） |
| 967 | test | Hafidh are people who have memorized what? | The Quran | 'The Quran.' | correct | gold 命中（含等价/别名） |
| 968 | validation | If I sail on the Neva river past the Hermitage Museum, what  | St. Petersburg | 'Russia.' | incorrect | 单 token 短答 'Russia.'（疑似错答，人工留意 |
| 969 | test | Where would a Viking warrior hope to go if he died in battle | Valhalla | 'Valhalla' | correct | gold 命中（含等价/别名） |
| 970 | train | What is the most common phobia in the United States, accordi | Fear of Public Speaking | 'The most common phobia in the United States, accor' | incorrect | gold 未命中 |
| 971 | test | What city will host the 2016 Olympics? | Rio de Janeiro | 'Rio de Janeiro, Brazil.' | correct | gold 命中（含等价/别名） |
| 972 | validation | Followers of what cult leader committed mass suicide by drin | Jim Jones | 'Jim David Jones' | incorrect | gold 未命中 |
| 973 | train | What is Brazil's most widely-spoken language? | Portuguese | 'Portuguese.' | correct | gold 命中（含等价/别名） |
| 974 | test | In alphabetical order, what is the last U.S. state? | Wyoming | 'The last U.S. state in alphabetical order is Wyomi' | correct | gold 命中（含等价/别名） |
| 975 | train | What is the number 17 in binary? | 10001 | 'The number 17 in binary is 100001.' | incorrect | gold 未命中 |
| 976 | validation | "In the ""Peanuts"" comic strip, who is Lucy's brother?" | Linus | 'Augustus' | incorrect | 单 token 短答 'Augustus'（疑似错答，人工留 |
| 977 | train | What Olympics-like event is for athletes with physical disab | Paralympics | 'The Paralympic Games.' | correct | gold 别名命中 |
| 978 | train | What movie takes place at Shermer High School's detention? | The Breakfast Club | 'Felon' | incorrect | 单 token 短答 'Felon'（疑似错答，人工留意） |
| 979 | train | What musician formed a singing duo with Art Garfunkel in 196 | Paul Simon | 'Paul Simon' | correct | gold 命中（含等价/别名） |
| 980 | train | What religious text was recently adapted into a hit Broadway | The Book of Mormon | 'The Bible' | incorrect | gold 未命中 |
| 981 | test | What Carl Sagan television series was resurrected in 2014 wi | Cosmos | 'The Carl Sagan television series resurrected in 20' | correct | gold 命中（含等价/别名） |
| 982 | test | What is Paris's largest airport? | Charles de Gaulle | "Paris's largest airport is Orly Airport." | incorrect | gold 未命中 |
| 983 | train | What notorious leader had a similar style mustache to Charli | Adolf Hitler | 'Adolf Hitler' | correct | gold 命中（含等价/别名） |
| 984 | train | What Pakistani river valley was home to one of the world's m | Indus Valley | 'The Indus River Valley.' | correct | gold 别名命中 |
| 985 | train | "The song ""Sunday Bloody Sunday"" was about a massacre on w | Ireland | 'Northern Ireland' | correct | gold 命中（含等价/别名） |
| 986 | train | What is the name of the vast hall where the Norse gods live? | Valhalla | 'Glimellir' | incorrect | 单 token 短答 'Glimellir'（疑似错答，人工 |
| 987 | test | On what body of water did Jesus supposedly walk? | Sea of Galilee | 'The Dead Sea.' | incorrect | gold 未命中 |
| 988 | test | What was abolished by the Supreme Court in 1972, but reinsta | Death Penalty | 'The death penalty.' | correct | gold 命中（含等价/别名） |
| 989 | train | What bridge connects the two peninsulas of Michigan? | Mackinac Bridge | 'The Lilac Bridge connects the two peninsulas of Mi' | incorrect | gold 未命中 |
| 990 | train | Grozny is the capital of what war-torn Russian republic? | Chechnya | 'Grozny is the capital of the war-torn Russian repu' | correct | gold 命中（含等价/别名） |
| 991 | train | What are the two major European cities that start with the l | Belfast | 'Belgium and Berlin.' | incorrect | gold 未命中 |
| 992 | test | What is the tallest kind of tree? | Coast Redwood | 'The tallest kind of tree is the redwood tree.' | incorrect | gold 未命中 |
| 993 | train | What was the last name of brothers Chico, Harpo, Groucho, Ze | Marx | 'Harp.' | incorrect | 单 token 短答 'Harp.'（疑似错答，人工留意） |
| 994 | test | "What play is about ""star-crossed lovers""?" | Romeo and Juliet | 'Romeo and Juliet' | correct | gold 命中（含等价/别名） |
| 995 | train | What comes next in the sequence kilo, mega, giga? | Tera | 'Tera' | correct | gold 命中（含等价/别名） |
| 996 | test | David Jason starred as Inspector Frost, but who played his b | BRUCE ALEXANDER | 'Peter Cook' | incorrect | gold 未命中 |
| 997 | train | The Habit of Art is a play by Alan Bennett about a fictional | W H AUDEN | 'T.S. Eliot' | incorrect | gold 未命中 |
| 998 | train | Which river runs through York? | OUSE | 'The Ouse runs through York.' | correct | gold 命中（含等价/别名） |
| 999 | train | Who played 'Captain Corelli' in the film 'Captain Corelli's  | NICOLAS CAGE | 'Anthony Hopkins.' | incorrect | gold 未命中 |
| 1000 | train | The 2013 G8 Summit was held at Lough Erne Resort in Northern | FERMANAGH | 'Lough Erne Resort is located in County Down, North' | incorrect | gold 未命中 |
| 1001 | train | In which British city is the Mitchell Library | Glasgow | 'The Mitchell Library is located in London, England' | incorrect | gold 未命中 |
| 1002 | train | The Wolfe Noel Cup is awarded to the winners of the woman's  | Squash | 'Tennis' | incorrect | 单 token 短答 'Tennis'（疑似错答，人工留意） |
| 1003 | train | Which artist was famed for his paintings of the water lilies | CLAUDE MONET | 'Claude Monet' | correct | gold 命中（含等价/别名） |
| 1004 | train | Octavian, who became Augustus, and Marcus Aemilius Lepidus w | MARK ANTONY | 'Mark Antony' | correct | gold 命中（含等价/别名） |
| 1005 | train | In which Italian city is the newspaper 'La Stampa' published | TURIN | 'Naples' | incorrect | 单 token 短答 'Naples'（疑似错答，人工留意） |
| 1006 | train | Which is the largest city on the Caspian Sea? | BAKU | 'The largest city on the Caspian Sea is Baku, Azerb' | correct | gold 命中（含等价/别名） |
| 1007 | train | Which island was home to Odysseus? | ITHACA | 'Troya' | incorrect | 单 token 短答 'Troya'（疑似错答，人工留意） |
| 1008 | test | Which boxer fought Mohammed Ali in the fight known as 'The T | JOE FRAZIER | 'Joe Frazier' | correct | gold 命中（含等价/别名） |
| 1009 | train | 'Original Pirate Material' was the 2002 debut album of which | 'THE STREETS' | 'Coldplay' | incorrect | 单 token 短答 'Coldplay'（疑似错答，人工留 |
| 1010 | train | Who was the head of the German Ministry of Public Enlightenm | JOSEPH GOEBBELS | 'The head of the German Ministry of Public Enlighte' | correct | gold 命中（含等价/别名） |
| 1011 | test | Who won a Best Actress Oscar for the 1940 film 'Kitty Foyle' | Ginger Rogers | 'Bette Davis' | incorrect | gold 未命中 |
| 1012 | train | Which precious gem is the birthstone for May? | Emerald | 'Diamond.' | incorrect | 单 token 短答 'Diamond.'（疑似错答，人工留 |
| 1013 | train | 'Whom we invite to see us crowned at Scone' is a line from w | MacBeth | 'Macbeth' | correct | gold 命中（含等价/别名） |
| 1014 | train | In which novel does Flora Poste move to live with her relati | Cold Comfort Farm | 'Flora Poste moves to live with her relatives, the ' | correct | gold 别名命中 |
| 1015 | train | In 2006 Orhan Pamuk became the first Nobel Laureate from whi | Turkey | 'Turkey' | correct | gold 命中（含等价/别名） |
| 1016 | validation | Which European city is served by Domodedovo Airport? | Moscow | 'Moscow' | correct | gold 命中（含等价/别名） |
| 1017 | train | Albacore, bigeye and longtail are species of what type of fi | TUNA | 'Albacore, bigeye, and longtail are species of tuna' | correct | gold 命中（含等价/别名） |
| 1018 | test | "Complete the name of the group for whom Young Girl was a Nu | PUCKETT | 'Glitter' | incorrect | 单 token 短答 'Glitter'（疑似错答，人工留意 |
| 1019 | validation | Luzon and Mindanao are the two largest islands in which coun | PHILIPPINES | 'Luzon and Mindanao are the two largest islands in ' | correct | gold 命中（含等价/别名） |
| 1020 | train | Interflug used the AN-2 and AN-24 aircraft - manufactured by | ANTONOV | 'Antonov' | correct | gold 命中（含等价/别名） |
| 1021 | test | Han of Iceland, Oedipus in Athens & The Ballet of Unhatched  | (Modest) Mussorgsky | 'Benjamin Britten.' | incorrect | gold 未命中 |
| 1022 | test | OJ presenter Stephen Fry stepped down earlier this year, who | (Sandi) Toksvig | 'Lucy Montgomery.' | incorrect | gold 未命中 |
| 1023 | train | For which 1960 film did Billy Wilder become the first person | The Apartment | 'The Apartment.' | correct | gold 命中（含等价/别名） |
| 1024 | train | Which fashion designer wrote the book, 'Men Without Ties'? | GIANNI VERSACE | 'Ralph Lauren.' | incorrect | gold 未命中 |
| 1025 | validation | Dame Judi Dench and which other actress played the Widdingto | Maggie Smith | 'Nicole Kidman' | incorrect | gold 未命中 |
| 1026 | validation | What is the most famous work of the architect James Hoban? | The Whitehouse | "James Hoban's most famous work is the Sydney Opera" | incorrect | gold 未命中 |
| 1027 | validation | The childhood disease 'Rickets' is caused by a lack of which | VITAMIN D | 'Vitamin D' | correct | gold 命中（含等价/别名） |
| 1028 | train | Cassiterite is the main ore of which metal? | Tin | 'Cassiterite is the main ore of tin.' | correct | gold 命中（含等价/别名） |
| 1029 | train | Complete the title of the novel that won the 2001 Booker Pri | Kelly | 'New York' | incorrect | gold 未命中 |
| 1030 | train | Who was the last British athlete to compete in the Olympic 1 | DWAYNE CHAMBERS | 'Andy Griffith.' | incorrect | gold 未命中 |
| 1031 | validation | Which company produces the 'Magentis' car model? | KIA | 'Volkswagen' | incorrect | 单 token 短答 'Volkswagen'（疑似错答，人 |
| 1032 | test | What mission was the fifth human space flight of 'Project Ap | APOLLO 11 | 'Apollo 11' | correct | gold 命中（含等价/别名） |
| 1033 | train | Who was the British monarch when Theodore Roosevelt was the  | EDWARD VII | 'King Edward VII' | correct | gold 命中（含等价/别名） |
| 1034 | train | 'London Is The Place For Me' which was sung by Lord Kitchene | CALYPSO | 'Pop song' | incorrect | gold 未命中 |
| 1035 | test | Which philosopher, 1872 - 1970, co-wrote 'Principia Mathemat | BERTRAND RUSSELL | 'Bertrand Russell' | correct | gold 命中（含等价/别名） |
| 1036 | train | Which hymn, based on Psalm 90, by Isaac Watts to a tune by W | 'OH GOD OUR HELP IN AGES | '"Amazing Grace"' | incorrect | gold 未命中 |
| 1037 | train | Which capital city is served by Arlanda Airport | Stockholm | 'Stockholm' | correct | gold 命中（含等价/别名） |
| 1038 | train | Who wrote 'The Legend Of Sleepy Hollow'? | WASHINGTON IRVING | "George Washington Irving wrote 'The Legend of Slee" | correct | gold 命中（含等价/别名） |
| 1039 | test | Which daily newspaper was merged with the daily Mail in 1971 | DAILY SKETCH | 'The Daily Telegraph' | incorrect | gold 未命中 |
| 1040 | validation | Which group had UK top ten hits in 1987 with 'Sweet Little M | 'WET WET WET' | 'The Cure' | incorrect | gold 未命中 |
| 1041 | train | Which island of just over 30 square miles lies between North | Benbecula | 'Iona.' | incorrect | 单 token 短答 'Iona.'（疑似错答，人工留意） |
| 1042 | train | 'Whole Lotta Love', 'Yellow Pearl', 'The Wizard', and 'Get O | 'TOP OF THE POPS' | 'Doctor Who' | incorrect | gold 未命中 |
| 1043 | train | What nationality is singer Rhianna? | BARBADIAN | 'Rhianna is an American singer.' | incorrect | gold 未命中 |
| 1044 | train | What word can mean loose broken rocks or someone who is vulg | Brash | 'pebble.' | incorrect | 单 token 短答 'pebble.'（疑似错答，人工留意 |
| 1045 | validation | The largest region in New Zealand is Canterbury. Which city  | CHRISTCHURCH | 'Christchurch' | correct | gold 命中（含等价/别名） |
| 1046 | train | Which band, formed in Salford in 1976, contained Ian Curtis, | 'JOY DIVISION' | 'Joy Division' | correct | gold 命中（含等价/别名） |
| 1047 | train | According to figures released by the ONS what was the most p | HARRY | 'Jack' | incorrect | 单 token 短答 'Jack'（疑似错答，人工留意） |
| 1048 | train | Who is the current World Snooker Champion? | Stuart Bingham | 'The current World Snooker Champion is Neil Roberts' | incorrect | gold 未命中 |
| 1049 | train | On which Italian track was the Formula One San Marino Grand  | Imola | 'The Formula One San Marino Grand Prix was held at ' | incorrect | gold 未命中 |
| 1050 | train | In which 1996 film were there characters known as Rent Boy,  | Trainspotting | 'Rent.' | incorrect | 单 token 短答 'Rent.'（疑似错答，人工留意） |
| 1051 | train | In music how many quavers make a minim? | Four (4) | '4' | format_failure | 单 token 函数词/碎片 '4'，无答案内容 |
| 1052 | train | Which US state is called 'Old Dominion'? | VIRGINIA | 'Virginia' | correct | gold 命中（含等价/别名） |
| 1053 | train | Which Liverpool player scored two goals in both the semi-fin | IAN RUSH | 'Allan Rush' | incorrect | gold 未命中 |
| 1054 | test | Which word is missing from this music hall song ‘When father | PARLOUR | 'wall' | incorrect | 单 token 短答 'wall'（疑似错答，人工留意） |
| 1055 | validation | Which car manufacturer made models called 'Ensign' and 'Vang | STANDARD | 'Honda' | incorrect | 单 token 短答 'Honda'（疑似错答，人工留意） |
| 1056 | validation | By what first name was the actor brother of Vanessa and Lynn | CORIN | 'Michael' | incorrect | 单 token 短答 'Michael'（疑似错答，人工留意 |
| 1057 | train | Which writer created the detective Charlie Chan? | EARL DERR BIGGERS | 'Raymond Chandler.' | incorrect | gold 未命中 |
| 1058 | train | Which of the 'Classic' horse races, run at Epsom for three y | 'THE OAKS' | 'The Oaks' | correct | gold 命中（含等价/别名） |
| 1059 | train | Which country defeated the Ivory Coast to win football's Afr | ZAMBIA | 'Egypt.' | incorrect | 单 token 短答 'Egypt.'（疑似错答，人工留意） |
| 1060 | train | In which sport did the future King Olav V of Norway in 1928  | SAILING | 'The future King Olav V of Norway won an Olympic Go' | incorrect | gold 未命中 |
| 1061 | test | With which common fish is Gooseberry sauce most often served | MACKEREL | 'Gooseberry sauce is most often served with salmon.' | incorrect | gold 未命中 |
| 1062 | train | From which country does 'Manchego' cheese come? | SPAIN | 'Spain' | correct | gold 命中（含等价/别名） |
| 1063 | validation | The 'Vuvuzela' is traditionally made from the horn of which  | KUDU | "The 'Vuvuzela' is traditionally made from the horn" | incorrect | gold 未命中 |
| 1064 | train | Which Hollywood actor was married to Uma Thurman 1998 - 2004 | ETHAN HAWKE | 'Brad Pitt.' | incorrect | gold 未命中 |
| 1065 | train | What name is shared by the capital city of Newfoundland and  | St Johns | "Saint John's" | correct | gold 别名命中 |
| 1066 | train | Livorno, Pisa and Siena are three of the largest cities in w | TUSCANY | 'Tuscany' | correct | gold 命中（含等价/别名） |
| 1067 | train | The 1999 film, 'The Green Mile' was directed by whom? | FRANK DARABONT | 'Peter Yates.' | incorrect | gold 未命中 |
| 1068 | validation | In the late 60's, Owen Finlay Maclaren pioneered what aid to | BABY BUGGY | 'In the late 1960s, Owen Finlay Maclaren pioneered ' | incorrect | gold 未命中 |
| 1069 | train | "What is the literal meaning of the French expression ""Son  | """SOUND AND LIGHT""" | 'The literal meaning of the French expression "Son ' | correct | gold 命中（含等价/别名） |
| 1070 | train | Tommy Bolin, who died of a heroin overdose in 1976, was the  | DEEP PURPLE | 'Tommy Bolin was the lead guitarist with the band T' | incorrect | gold 未命中 |
| 1071 | train | Donald Neilson was a notorious figure in the 1970's, but how | 'THE BLACK PANTHER' | 'Donald Neilson was better known as Charles Manson.' | incorrect | gold 未命中 |
| 1072 | validation | What is the meteorological name of the clouds commonly known | CIRRUS | 'Cirrus clouds' | correct | gold 命中（含等价/别名） |
| 1073 | train | Who wrote the Buddy Holly hit 'It Doesn't Matter Anymore'? | PAUL ANKA | 'Tom Petty.' | incorrect | gold 未命中 |
| 1074 | test | Which Shakespeare play centres around a novice nun called 'I | 'MEASURE FOR MEASURE' | 'Twelfth Night' | incorrect | gold 未命中 |
| 1075 | validation | The trade union Unison was formed by a merger of NALGO, NUPE | COHSE | 'GMB' | incorrect | 单 token 短答 'GMB'（疑似错答，人工留意） |
| 1076 | train | The second act, set in the Land of Sweets, of which ballet b | THE NUTCRACKER SUITE | 'The Nutcracker' | correct | gold 命中（含等价/别名） |
| 1077 | train | In the human body, what is the common name for the 'Talus bo | ANKLE | "The common name for the 'Talus bone' is the 'ankle" | correct | gold 命中（含等价/别名） |
| 1078 | validation | Which director won the 'Oscar' for best Director for the pic | RON HOWARD | 'Ron Howard.' | correct | gold 命中（含等价/别名） |
| 1079 | train | In which town or city would you find the 'Caledonian Brewery | EDINBURGH | 'Edinburgh' | correct | gold 命中（含等价/别名） |
| 1080 | train | Who was the youngest ever Pope? | BENEDICT IX | 'The youngest ever Pope was Pope Alexander VI.' | incorrect | gold 未命中 |
| 1081 | validation | What name is given to a substance that accelerates a chemica | CATALYST | 'Catalyst.' | correct | gold 命中（含等价/别名） |
| 1082 | train | In 1932 which British physicist discovered the part of the n | (James) CHADWICK | 'James Chadwick' | correct | gold 命中（含等价/别名） |
| 1083 | train | Which Puccini opera begins with 'Rodolfo' finishing writing  | 'LA BOHEME' | 'Madama Butterfly' | incorrect | gold 未命中 |
| 1084 | train | The painting 'Faithful Unto Death' can be found in Liverpool | SIR EDWARD JOHN POYNTER | 'Francis Bacon.' | incorrect | gold 未命中 |
| 1085 | validation | Which motor company owns the truck maker, Scania? | SAAB | 'Volvo' | incorrect | 单 token 短答 'Volvo'（疑似错答，人工留意） |
| 1086 | test | What type of animal, according to its alternative name, is t | TASMANIAN WOLF | 'The Thylacine, also known as the Tasmanian Tiger, ' | correct | gold 别名命中 |
| 1087 | train | "Who famously said after the 'Dunblane Massacre', ""If a cri | DUKE OF EDINBURGH | 'David Cameron' | incorrect | gold 未命中 |
| 1088 | validation | Which artist, a member of the Order of Merit, was born in Br | DAVID HOCKNEY | 'Barbara Hepworth' | incorrect | gold 未命中 |
| 1089 | train | Which type of roof is pitched at two different angles, the l | Mansard | 'Gabled roof.' | incorrect | gold 未命中 |
| 1090 | train | Whose picture is on the US 20 dollar note? | Andrew Jackson | 'Alexander Hamilton' | incorrect | gold 未命中 |
| 1091 | train | What name is given to a line on a map joining places of equa | ISOHYET | 'Isohyet.' | correct | gold 命中（含等价/别名） |
| 1092 | test | Who played the part of 'herman' in the 1960's TV series 'The | FRED GWYNNE | 'Eddie Munster' | incorrect | gold 未命中 |
| 1093 | validation | Which is the sixth book of the New Testament, following Acts | EPISTLE TO THE ROMANS | 'Romans' | incorrect | 单 token 短答 'Romans'（疑似错答，人工留意） |
| 1094 | test | rtve is the state broadcaster in which country? | SPAIN | 'Spain' | correct | gold 命中（含等价/别名） |
| 1095 | train | Who is the only Rugby League player to win two consecutive L | Paul Wellens | 'Andrew Johns.' | incorrect | gold 未命中 |
| 1096 | train | The Cerval is one of the more uncommon members of which fami | CAT | 'The Cerval is one of the more uncommon members of ' | incorrect | gold 未命中 |
| 1097 | validation | Terry Scott starred as middle-aged, suburban husband, Terry  | 'HAPPY EVER AFTER' | 'Family Matters' | incorrect | gold 未命中 |
| 1098 | validation | What is the general term for the seed-bearing part of a flow | PISTIL | 'Gyn.' | incorrect | 单 token 短答 'Gyn.'（疑似错答，人工留意） |
| 1099 | test | "In British history, who was nicknamed ""The Sailor King""?" | WILLIAM IV | 'Lord Nelson.' | incorrect | gold 未命中 |
| 1100 | test | In Shakespeare's 'Hamlet', what was the name of 'Hamlet's' m | 'GERTRUDE' | 'Gertrude' | correct | gold 命中（含等价/别名） |
| 1101 | validation | Which country is the world's largest producer of copper? | CHILE | 'China' | incorrect | 单 token 短答 'China'（疑似错答，人工留意） |
| 1102 | test | What may be described as a 'red earthworm with rings of a br | BRANDLING | 'The Redworm.' | incorrect | gold 未命中 |
| 1103 | train | For which film did Tatum O'Neal receive the Best Supporting  | 'PAPER MOON' | "Tatum O'Neal received the Best Supporting Actress " | incorrect | gold 未命中 |
| 1104 | train | The Leverhulme Stand and 1539 Restaurant and Bar are facilit | Chester | 'The Leverhulme Stand and 1539 Restaurant and Bar a' | incorrect | gold 未命中 |
| 1105 | train | In Greek mythology, Heracles' Twelfth Labour (final) was to  | 'CERBERUS' | 'Golden Hind' | incorrect | gold 未命中 |
| 1106 | train | Which film starring Will Smith, Bill Pullman and Jeff Goldbl | 'INDEPENDENCE DAY' | 'Ghostbusters' | incorrect | 单 token 短答 'Ghostbusters'（疑似错答 |
| 1107 | train | In which country is the most northerly point on mainland Afr | TUNISIA | 'Libya' | incorrect | 单 token 短答 'Libya'（疑似错答，人工留意） |
| 1108 | train | The ancient Egyptian goddess Serket took the form of which c | SCORPION | 'Cat.' | incorrect | 单 token 短答 'Cat.'（疑似错答，人工留意） |
| 1109 | train | The adjective “buccal” refers to which part of the body? | Cheek | 'Mouth' | incorrect | 单 token 短答 'Mouth'（疑似错答，人工留意） |
| 1110 | train | Belonging to Indonesia, Irian Jaya is the western portion of | New Guinea | 'Irian Jaya is the western portion of the large isl' | correct | gold 命中（含等价/别名） |
| 1111 | train | How many wheels are there on a sulky? | 2 | 'A sulky typically has two wheels.' | correct | gold 别名命中 |
| 1112 | train | At the beginning of 'Two Towers', the second book in 'The Lo | 'GANDALF' | 'Legolas' | incorrect | 单 token 短答 'Legolas'（疑似错答，人工留意 |
| 1113 | train | Octavian, who became Augustus, and Lepidus were two of the ' | MARK ANTONY | 'Mark Antony' | correct | gold 命中（含等价/别名） |
| 1114 | test | What was the name of the British nurse who was shot by a Ger | EDITH CAVELL | 'Barbara Barton.' | incorrect | gold 未命中 |
| 1115 | train | Who coached New Zealand when they won the 2011 Rugby Union W | GRAHAM HENRY | 'Steve Hansen.' | incorrect | gold 未命中 |
| 1116 | validation | What name is given to the temperature of -273.15 degrees Cel | ABSOLUTE ZERO | 'Absolute zero.' | correct | gold 命中（含等价/别名） |
| 1117 | validation | By what name are the Essex one-day cricket team known? | 'EAGLES' | 'The Essex one-day cricket team is known as the Ess' | correct | gold 命中（含等价/别名） |
| 1118 | test | What first name is shared by Turner Prize winning artists Wa | MARK | 'Mark' | correct | gold 命中（含等价/别名） |
| 1119 | validation | Complete the name of the MLB (Baseball) team based in Arling | '..RANGERS' | 'The Texas Rangers.' | correct | gold 命中（含等价/别名） |
| 1120 | train | Which now defunct newspaper was originally owned by Eddy Sha | Today | 'The Daily Times' | incorrect | gold 未命中 |
| 1121 | train | Until the introduction of the Euro, what is the unit of curr | Schilling | 'Until the introduction of the Euro, the unit of cu' | incorrect | gold 未命中 |
| 1122 | test | Pipistrellus is a genus of which mammal? | BAT | 'Pipistrellus is a genus of bats.' | incorrect | gold 未命中 |
| 1123 | train | How many sides did the pre-decimal British threepence have a | TWELVE | 'The pre-decimal British threepence had eight sides' | incorrect | gold 未命中 |
| 1124 | train | What in Sikhism, is a Kanga? | COMB | 'In Sikhism, a Kanga is a wooden comb.' | correct | gold 命中（含等价/别名） |
| 1125 | test | With what area of manufacturing are the names 'Audemars Pigu | WATCHMAKING | 'Watchmaking.' | correct | gold 命中（含等价/别名） |
| 1126 | test | Complete the sequence: Johnson, Nixon, Ford....? | JIMMY CARTER | ' Carter.' | incorrect | 单 token 短答 ' Carter.'（疑似错答，人工留 |
| 1127 | test | In which game could you be faced with a 'Simple or Double Sq | BRIDGE | 'Monopoly' | incorrect | 单 token 短答 'Monopoly'（疑似错答，人工留 |
| 1128 | train | Which prominent Irish Nationalist was hung for treason in 19 | Roger Casement | 'Michael Collins.' | incorrect | gold 未命中 |
| 1129 | train | Which American University is situated in Ithaca, New York? | CORNELL | 'Cornell University' | correct | gold 命中（含等价/别名） |
| 1130 | validation | Who according to the title of a 1992 novel was 'Count Lazzio | 'THE ENGLISH PATIENT' | 'James Bond.' | incorrect | gold 未命中 |
| 1131 | train | Who wrote the children's books 'Pigeon Post' and 'Coot Club' | ARTHUR RANSOME | 'Richard Adams.' | incorrect | gold 未命中 |
| 1132 | train | The traditional gift for a ninth anniversary should be made  | POTTERY | 'Gold' | incorrect | 单 token 短答 'Gold'（疑似错答，人工留意） |
| 1133 | train | How many 'Oscars' did the film 'Slumdog Millionaire' win? | 8 | '8' | correct | gold 命中（含等价/别名） |
| 1134 | train | In 1986, whilst facing England which West Indian batsman sco | VIV RICHARDS | ' Vivian Richards' | correct | gold 别名命中 |
| 1135 | validation | Which former US boxer is referred to as the ‘Poet laureate o | Floyd Mayweather Sr | 'Joe Frazier' | incorrect | gold 未命中 |
| 1136 | test | The UK television drama series ‘Boys From the Black Stuff’ w | Liverpool | 'Manchester' | incorrect | 单 token 短答 'Manchester'（疑似错答，人 |
| 1137 | train | Who became the host of the UK television game show Blankety  | Les Dawson | 'Richard Hammond' | incorrect | gold 未命中 |
| 1138 | train | Acmeism relates to poetry from the early 20th Century in whi | Russia | 'France' | incorrect | 单 token 短答 'France'（疑似错答，人工留意） |
| 1139 | train | Who does the commentary in the UK tv programme ‘Come Dine Wi | Dave Lamb | 'Richard Hammond.' | incorrect | gold 未命中 |
| 1140 | test | Which country was invaded by Iraq in 1990? | Kuwait | 'Kuwait' | correct | gold 命中（含等价/别名） |
| 1141 | train | In Greek mythology, Amphitrite, queen of the sea, was the wi | Poseidon | 'Amphitrite was the wife of Poseidon.' | correct | gold 命中（含等价/别名） |
| 1142 | train | Maria Fitzherbert was ‘married’ to which British monarch? | George IV | "Maria Fitzherbert was 'married' to King George IV." | correct | gold 命中（含等价/别名） |
| 1143 | validation | Henry Blake, Charles Winchester and Father Mulcahy are all c | M*A*S*H | 'Henry Blake, Charles Winchester, and Father Mulcah' | incorrect | gold 未命中 |
| 1144 | test | ‘Obey your thirst’ is the advertising slogan for which soft  | Sprite | 'Pepsi.' | incorrect | 单 token 短答 'Pepsi.'（疑似错答，人工留意） |
| 1145 | train | What did fictional detective Sherlock Holmes keep in the toe | Tobacco | 'Sherlock Holmes kept a small key in the toe of his' | incorrect | gold 未命中 |
| 1146 | train | Which creatures are used as croquet balls in the novel ‘Alic | Hedgehogs | 'Cats.' | incorrect | 单 token 短答 'Cats.'（疑似错答，人工留意） |
| 1147 | train | Which Spanish artist painted the series known as ‘Fantasy an | Francisco Goya | 'Franc Goya' | correct | gold 别名命中 |
| 1148 | train | In the 2005 Julian Barnes novel ‘Arthur and George’, who is  | Arthur Conan Doyle | "In the 2005 Julian Barnes novel 'Arthur and George" | incorrect | gold 未命中 |
| 1149 | test | The UEFA (Union of European Football Associations) was found | Switzerland | 'France.' | incorrect | 单 token 短答 'France.'（疑似错答，人工留意 |
| 1150 | test | The ‘La Scala Opera House’ is in which European city? | Milan | 'Milan, Italy.' | correct | gold 命中（含等价/别名） |
| 1151 | test | In medicine, algology is the study of what? | Pain | 'Algae.' | incorrect | 单 token 短答 'Algae.'（疑似错答，人工留意） |
| 1152 | validation | The meibomian gland is found in which part of the human body | Eyelid | 'The meibomian gland is found in the eyelid.' | correct | gold 命中（含等价/别名） |
| 1153 | train | Which British swimmer won Olympic Gold Medals in 2008 in the | Rebecca Adlington | 'David Phelps' | incorrect | gold 未命中 |
| 1154 | train | The Cuatro Torres Business Area is in which European city? | Madrid | 'The Cuatro Torres Business Area is in Madrid, Spai' | correct | gold 命中（含等价/别名） |
| 1155 | test | In the poem ‘Monday’s Child’, what is Wednesday’s child full | Woe | 'Hope.' | incorrect | 单 token 短答 'Hope.'（疑似错答，人工留意） |
| 1156 | test | Which clothing chain was founded by brothers Clemens and Aug | C&A | 'H&M.' | incorrect | 单 token 短答 'H&M.'（疑似错答，人工留意） |
| 1157 | validation | Which fictional character is the subject of George Frampton’ | Peter Pan | 'Sherlock Holmes' | incorrect | gold 未命中 |
| 1158 | train | In which London street does fictional character Sweeney Todd | Fleet Street | 'Old Bond Street' | incorrect | gold 未命中 |
| 1159 | train | The Nullarbor Plain is in which country? | Australia | 'The Nullarbor Plain is in Australia.' | correct | gold 命中（含等价/别名） |
| 1160 | train | Who was the first Hanover King of England? | George I | 'The first Hanover King of England was George I.' | correct | gold 命中（含等价/别名） |
| 1161 | validation | The 1981 film ‘Chariots of Fire’ was based on the stories of | Harold Abrahams and Eric | "The 1981 film 'Chariots of Fire' was based on the " | incorrect | gold 未命中 |
| 1162 | test | What is the US state capital of Kansas? | Topeka | 'The US state capital of Kansas is Kansas City.' | correct | gold 别名命中 |
| 1163 | train | Who wrote the novel ‘Seven Pillars of Wisdom’? | T E Lawrence | 'Ken Follett.' | incorrect | gold 未命中 |
| 1164 | validation | Which British-American actress died on 23rd March 2011, aged | Elizabeth Taylor | 'Margaret Lockwood' | incorrect | gold 未命中 |
| 1165 | train | Who became US President John Kennedy’s Vice President in 196 | Lyndon B Johnson | 'Lyndon B. Johnson' | correct | gold 命中（含等价/别名） |
| 1166 | train | Blinky, Mr Teeny and Jub-Jub are all animals in which US ani | The Simpsons | 'Blinky, Mr. Teeny, and Jub-Jub are all characters ' | incorrect | gold 未命中 |
| 1167 | test | What is the name of the steam locomotive which set the world | Mallard | 'The Blue Bird' | incorrect | gold 未命中 |
| 1168 | train | What type of creature is a bananaquit? | Bird | 'A bananaquit is a type of bird.' | correct | gold 命中（含等价/别名） |
| 1169 | train | What is the art of hand-making cricket bats called? | Podshaving | 'Bat making.' | incorrect | gold 未命中 |
| 1170 | test | In the Charles Dickens novel ‘Oliver Twist’ what is the name | Bulls Eye | ' Dodger' | incorrect | 单 token 短答 ' Dodger'（疑似错答，人工留意 |
| 1171 | validation | Elliot Carver is the villain in which James Bond film? | Tomorrow Never Dies | 'Elliot Carver is the villain in the James Bond fil' | correct | gold 别名命中 |
| 1172 | train | What is the system of raised dots called which blind people  | Braille | 'Braille.' | correct | gold 命中（含等价/别名） |
| 1173 | validation | In the nursery rhyme ‘Oranges and Lemons’, the bells of whic | St Martins | 'London.' | incorrect | 单 token 短答 'London.'（疑似错答，人工留意 |
| 1174 | train | In the US, which state lies to the west of New Hampshire? | Vermont | 'Massachusetts' | incorrect | 单 token 短答 'Massachusetts'（疑似错 |
| 1175 | train | Which Radio 2 DJ christened ‘Dallas’ character Lucy Ewing ‘T | Terry Wogan | 'Richard Bacon' | incorrect | gold 未命中 |
| 1176 | test | What was the name of the band, featuring members of Thin Liz | The Greedies (originally | 'The Clash' | incorrect | gold 未命中 |
| 1177 | train | What is the nickname of the great bell of the clock at the n | Big Ben | 'Big Ben' | correct | gold 命中（含等价/别名） |
| 1178 | test | In June 1978, who became the first cricketer to score a cent | Ian Botham | 'Brian Lara.' | incorrect | gold 未命中 |
| 1179 | train | On a standard dartboard, which number lies between 12 and 20 | 5 | '15' | format_failure | 单 token 函数词/碎片 '15'，无答案内容 |
| 1180 | train | In Ian Fleming’s novel ‘Moonraker’, Sir Hugo Drax is suspect | Bridge | 'Darts' | incorrect | 单 token 短答 'Darts'（疑似错答，人工留意） |
| 1181 | train | What was the name of the Cunard ocean liner which was launch | Mauretania | 'Titanic' | incorrect | 单 token 短答 'Titanic'（疑似错答，人工留意 |
| 1182 | train | In which James Bond film does actress Jane Seymour play Soli | Live and Let Die | 'Jane Seymour plays Solitaire in the James Bond fil' | incorrect | gold 未命中 |
| 1183 | train | To ‘Defenestrate’ is to throw something or someone out of wh | A window | 'A window.' | correct | gold 命中（含等价/别名） |
| 1184 | train | During which year was Washington DC declared the capital of  | 1790 | '1800' | incorrect | 单 token 短答 '1800'（疑似错答，人工留意） |
| 1185 | test | Who played boxer Jim Braddock in the 2005 film ‘Cinderella m | Russell Crowe | 'Tom Hardy.' | incorrect | gold 未命中 |
| 1186 | train | In the UK, the LTA is the governing body of which sport? | Tennis | 'Table Tennis' | correct | gold 命中（含等价/别名） |
| 1187 | validation | Who played Brad Pitt’s wife Theresa Mills in the film ‘Seven | Gwyneth Paltrow | 'Julia Roberts.' | incorrect | gold 未命中 |
| 1188 | test | St Joseph’s Day is celebrated during which month of the year | March -19th | 'March' | incorrect | 单 token 短答 'March'（疑似错答，人工留意） |
| 1189 | train | Which is the largest state in the US? | Alaska | 'The largest state in the US is Alaska.' | correct | gold 命中（含等价/别名） |
| 1190 | train | Which English Rugby Union team play their home games at Adam | London Wasps | 'Worcester Warriors' | incorrect | gold 未命中 |
| 1191 | test | Apart from white, what colour are the other two ‘triangles’  | Blue | "The other two 'triangles' on the BMW logo are red." | incorrect | gold 未命中 |
| 1192 | validation | How many US Presidents have been impeached? | Two | '2' | correct | gold 别名命中 |
| 1193 | test | Arturo Frondizi became president of which South American cou | Argentina | 'Uruguay' | incorrect | 单 token 短答 'Uruguay'（疑似错答，人工留意 |
| 1194 | train | On 7th July 2011 which UK tabloid was closed down because jo | News of the World | 'The Sun' | incorrect | gold 未命中 |
| 1195 | train | Which island group became known as The Friendly Islands? | Tonga | 'The Cook Islands.' | incorrect | gold 未命中 |
| 1196 | train | ‘Probably the best lager in the world’ is the advertising sl | Carlsberg | 'Guinness' | incorrect | 单 token 短答 'Guinness'（疑似错答，人工留 |
| 1197 | test | Who won the 1989 Ladies Singles Wimbledon Championship? | Steffi Graf | 'Andre Agassi.' | incorrect | gold 未命中 |
| 1198 | validation | Which American car manufacturer has a logo which features th | Buick | 'Ford.' | incorrect | 单 token 短答 'Ford.'（疑似错答，人工留意） |
| 1199 | train | The Museum of Bags and Purses is in which European city? | Amsterdam | 'The Museum of Bags and Purses is in Amsterdam, Net' | correct | gold 命中（含等价/别名） |
| 1200 | test | How many times did Actress Zsa Zsa Gabor marry? | Nine | 'Zsa Zsa Gabor married three times.' | incorrect | gold 未命中 |
| 1201 | train | American singer Al, late British television host Hughie and  | Green | 'Greene' | incorrect | 单 token 短答 'Greene'（疑似错答，人工留意） |
| 1202 | train | Who wrote the 1975 novel ‘The History Man’? | Malcolm Bradbury | 'Robert Harris.' | incorrect | gold 未命中 |
| 1203 | validation | In the 1965 film ‘Those Magnificent Men in Their Flying Mach | 10,000 | '500' | incorrect | 单 token 短答 '500'（疑似错答，人工留意） |
| 1204 | validation | Who directed the 1969 film ‘Women in Love’, starring Oliver  | Ken Russell | 'Oliver Reed.' | incorrect | gold 未命中 |
| 1205 | train | Which country invaded the Falkland Islands in April 1982? | Argentina | 'Argentina' | correct | gold 命中（含等价/别名） |
| 1206 | test | A group of which fish is called a Lap? | Cod | 'Sharks' | incorrect | 单 token 短答 'Sharks'（疑似错答，人工留意） |
| 1207 | test | What is the title of the 18th Century novel by Lawrence Ster | (The Life and Opinions o | 'Rasselas' | incorrect | 单 token 短答 'Rasselas'（疑似错答，人工留 |
| 1208 | test | The Aviva Sports Stadium is in which European country? | Ireland | 'The Aviva Sports Stadium is in London, England.' | incorrect | gold 未命中 |
| 1209 | train | Who played Gomez Addams in the 1993 film ‘Addams Family Valu | Raul Julia | 'Tom Arnold.' | incorrect | gold 未命中 |
| 1210 | validation | In which UK city is Headingley railway station? | Leeds | 'Headingley railway station is located in Leeds, We' | correct | gold 命中（含等价/别名） |
| 1211 | train | Which, then fictional, award is mentioned in the opening sce | The Sarah Siddons Award | 'The Academy Award' | incorrect | gold 未命中 |
| 1212 | test | What disease was Robert the Bruce, King of Scotland, said to | Leprosy | 'Robert the Bruce, King of Scotland, was said to ha' | incorrect | gold 未命中 |
| 1213 | train | In humans, the medical condition Hyposmia affects which of t | Smell | 'The sense of smell.' | correct | gold 命中（含等价/别名） |
| 1214 | validation | Which London football club won the last FA cup final held at | Chelsea FC | 'Arsenal' | incorrect | 单 token 短答 'Arsenal'（疑似错答，人工留意 |
| 1215 | train | Which is the only US state to begin with the letter ‘U’? | Utah | 'Utah' | correct | gold 命中（含等价/别名） |
| 1216 | train | Who played Thelma in the UK television series ‘The Likely La | Brigit Forsyth | 'Barbara Windsor.' | incorrect | gold 未命中 |
| 1217 | train | In Greek mythology, how many heads does Cerberus, the dog wh | Three | 'Three.' | correct | gold 命中（含等价/别名） |
| 1218 | train | Breve, Mocha and Americano are all types of which drink? | Coffee | 'Breve, Mocha, and Americano are all types of coffe' | correct | gold 命中（含等价/别名） |
| 1219 | test | Sound engineer Peter Lodge first announced which phrase on t | Mind the gap | 'London Underground Network.' | incorrect | gold 未命中 |
| 1220 | test | Who did Germany defeat to win the 1990 FIFA World Cup? | Argentina | 'Germany defeated Italy to win the 1990 FIFA World ' | incorrect | gold 未命中 |
| 1221 | test | What is the name of the life-size plastic dummies in the tel | Autons | 'The life-size plastic dummies in the television se' | incorrect | gold 未命中 |
| 1222 | train | Who designed the red telephone box, which first appeared in  | Sir Giles Gilbert Scott | 'Sir Gilbert Scott' | incorrect | gold 未命中 |
| 1223 | train | Strangles is a bacterial infection of the respiratory tract  | Horse | 'Cattle' | incorrect | 单 token 短答 'Cattle'（疑似错答，人工留意） |
| 1224 | train | Saint Fidelis Church, otherwise known as The Cathedral of th | Kansas | 'Saint Fidelis Church, also known as The Cathedral ' | correct | gold 命中（含等价/别名） |
| 1225 | train | In March 1951, which comic strip character first appeared in | Dennis the Menace | 'Peanuts' | incorrect | 单 token 短答 'Peanuts'（疑似错答，人工留意 |
| 1226 | test | The Formula One Sepang International Circuit is in which cou | Malaysia | 'Malaysia' | correct | gold 命中（含等价/别名） |
| 1227 | train | The Paragons originally recorded which 1980 hit single by Bl | The Tide is High | 'The Paragons originally recorded "Call Me".' | incorrect | gold 未命中 |
| 1228 | train | Arkansas Black is a variety of which fruit? | Apple | 'Arkansas Black is a variety of grape.' | incorrect | gold 未命中 |
| 1229 | train | What was is the name of Penelope Pitstop’s car in the childr | Compact Pussycat | 'Penelope' | incorrect | 单 token 短答 'Penelope'（疑似错答，人工留 |
| 1230 | train | The discovery of what in Australia in February 1851 is tradi | Gold | 'Gold.' | correct | gold 命中（含等价/别名） |
| 1231 | test | How is the year 1994 depicted in Roman Numerals? | MCMXCIV | 'The year 1994 is depicted in Roman Numerals as MCM' | correct | gold 命中（含等价/别名） |
| 1232 | train | The 1995 autobiography ‘Dreams From My Father’ is by which U | Barack Obama | 'Michelle Obama' | correct | gold 别名命中 |
| 1233 | train | 8Â Fort Ville-Marie was the original name of which Canadian  | Montreal | 'Fort Ville-Marie was the original name of Montreal' | correct | gold 命中（含等价/别名） |
| 1234 | train | Which was Disney's second animated film? | Pinocchio | 'Pinocchio' | correct | gold 命中（含等价/别名） |
| 1235 | train | What would a Scotsman do with a spurtle? | Eat porridge | 'A Scotsman would eat a spurtle.' | incorrect | gold 未命中 |
| 1236 | train | When running around the athletics track, what does the sound | The last lap | 'The sound of a bell indicates the end of a lap.' | incorrect | gold 未命中 |
| 1237 | validation | Who played 'Chief Inspector Dreyfus' in the 'Pink Panther' f | Herbert Lom | 'Peter Sellers' | incorrect | gold 未命中 |
| 1238 | train | Who played Dr Richard Kimble in the 1993 film The Fugitive? | Harrison Ford | 'Tom Cruise.' | incorrect | gold 未命中 |
| 1239 | test | In 1967, who was the first DJ on Radio 1? | Tony Blackburn | 'Alan Freeman.' | incorrect | gold 未命中 |
| 1240 | test | Patusnaya and mallasol are types of what? | Caviar | 'Patusnaya and mallasol are types of Russian bread.' | incorrect | gold 未命中 |
| 1241 | train | In a petrol engine what component mixes fuel and air? | The carburettor | 'Combustor' | incorrect | 单 token 短答 'Combustor'（疑似错答，人工 |
| 1242 | train | Ascorbic acid is usually known as what? | Vitamin C | 'Ascorbic acid is usually known as Vitamin C.' | correct | gold 命中（含等价/别名） |
| 1243 | train | Until 1796, there was a state in the United States called Fr | Tennessee! | 'Georgia' | incorrect | 单 token 短答 'Georgia'（疑似错答，人工留意 |
| 1244 | train | The Southern Alps can be found in which country? | New Zealand | 'The Southern Alps can be found in Australia.' | incorrect | gold 未命中 |
| 1245 | train | Beaufort who created The Wind Scale had which profession ? | Sailor | 'Engineer' | incorrect | 单 token 短答 'Engineer'（疑似错答，人工留 |
| 1246 | train | Who played the role of George Carter in The Sweeney? | Dennis Waterman | 'Peter Cook' | incorrect | gold 未命中 |
| 1247 | train | 'Diva' released in 1992 was the first solo album for who? | Annie Lennox | 'Mariah Carey' | incorrect | gold 未命中 |
| 1248 | validation | 'Roquefort Cheese' is made from what sort of milk? | Ewe's Milk | "Roquefort cheese is made from cow's milk." | incorrect | gold 未命中 |
| 1249 | train | Which King reigned for only 325 days? | Edward 8th | 'King Edward VIII' | correct | gold 别名命中 |
| 1250 | train | In British Wrestling who was Shirley Crabtree? | Big Daddy | 'Shirley Crabtree was a British female wrestler.' | incorrect | gold 未命中 |
| 1251 | train | What was Britain called - before it was Britain? | Albion | 'Romania' | incorrect | 单 token 短答 'Romania'（疑似错答，人工留意 |
| 1252 | train | What is Africa's most populated country? | Nigeria | 'Nigeria' | correct | gold 命中（含等价/别名） |
| 1253 | test | Which comedy duo were born Bartholomew and Wiseman? | Morecambe and Wise | 'Barbe and Wise' | incorrect | gold 未命中 |
| 1254 | validation | Who founded the Jaguar motor company? | William Lyons | 'Jaguar was founded by William Lyons in 1924.' | correct | gold 命中（含等价/别名） |
| 1255 | validation | What was Billy Connolly's only No. 1 hit? | D-I-V-O-R-C-E | '"Rich Girl"' | incorrect | gold 未命中 |
| 1256 | train | Which fashion craze was made popular by the film 'Flashdance | Legwarmers | "The fashion craze made popular by the film 'Flashd" | incorrect | gold 未命中 |
| 1257 | train | The rivers Trent and Ouse flow into which estuary? | Humber | 'The rivers Trent and Ouse flow into the Humber Est' | correct | gold 命中（含等价/别名） |
| 1258 | train | Aviemore, in Scotland is at the heart of which National Park | The Cairngorms National  | 'Aviemore is at the heart of Cairngorms National Pa' | correct | gold 别名命中 |
| 1259 | train | Which is the largest cat in the world? | Siberian Tiger | 'The largest cat in the world is the snow leopard.' | incorrect | gold 未命中 |
| 1260 | validation | Who had an August 1969 No.1 with 'In The Year 2525 (Exordium | Zager & Evans | 'The Who.' | incorrect | gold 未命中 |
| 1261 | validation | Founded in 1775, George Washington was the Commander-in-Chie | Continental Army | 'The Continental Army.' | correct | gold 命中（含等价/别名） |
| 1262 | test | What boxer was stripped of his heavyweight boxing titles whe | Muhammed Ali | 'Muhammad Ali' | correct | gold 别名命中 |
| 1263 | train | According to Arthurian legend, Arthur's wife Guinevere, had  | Lancelot | 'Lancelot' | correct | gold 命中（含等价/别名） |
| 1264 | test | In which city would you find the International Court of Just | The Hague, Netherlands | 'The International Court of Justice, also known as ' | correct | gold 命中（含等价/别名） |
| 1265 | train | What noted film director and producer, born on May 14, 1944, | George Lucas | 'George Lucas' | correct | gold 命中（含等价/别名） |
| 1266 | train | May 15, 1940 saw what fast food chain get started in San Ber | McDonald's | "Wendy's" | incorrect | gold 未命中 |
| 1267 | validation | Also known as the Roland Garros, what is the Grand Slam Tenn | French Open | 'The French Open.' | correct | gold 命中（含等价/别名） |
| 1268 | train | In 2001: A Space Odyssey, what was the name of the computer  | HAL 9000 | 'HAL' | incorrect | 单 token 短答 'HAL'（疑似错答，人工留意） |
| 1269 | validation | Portrayed by James Doohan, what was the actual name of the e | Montgomery Scott | 'Montgomery Scott' | correct | gold 命中（含等价/别名） |
| 1270 | test | Who flew a kite in a storm on June 15, 1750, proving that li | Benjamin Franklin | 'Benjamin Franklin' | correct | gold 命中（含等价/别名） |
| 1271 | train | The first civilians executed for espionage in the United Sta | Julius and Ethel Rosenbe | 'Ethel and Julius Rosenberg' | correct | gold 别名命中 |
| 1272 | train | June 17, 1994 saw a low speed chase up Interstate 405 as OJ  | White Ford Bronco | 'Motorcycle' | incorrect | 单 token 短答 'Motorcycle'（疑似错答，人 |
| 1273 | train | Used as an alloy in making high-speed cutting tools, mo is t | Molybdenum | 'Molybdenum' | correct | gold 命中（含等价/别名） |
| 1274 | validation | What do you practice in a dojo? | Martial Arts | ' Martial arts.' | correct | gold 命中（含等价/别名） |
| 1275 | train | The 1999 Spike Lee film Summer of Sam focuses on the crimes  | David Berkowitz | 'Sam Harris.' | incorrect | gold 未命中 |
| 1276 | train | Named after an abduction at the Japanese Embassy in a South  | Lima Syndrome | 'The Japanese Embassy Syndrome.' | incorrect | gold 未命中 |
| 1277 | train | By what name are Rontgen rays more commonly known? | X-Rays | 'Rontgen rays are more commonly known as X-rays.' | correct | gold 命中（含等价/别名） |
| 1278 | test | Which Apollo mission, which was launched on July 16, 1969, w | 11 | 'Apollo 11' | correct | gold 命中（含等价/别名） |
| 1279 | train | In the Tour de France who wears the polka dot jersey? | The king of the mountain | 'The race leader wears the polka dot jersey.' | incorrect | gold 未命中 |
| 1280 | train | On July 21, 1969, who became the first man to set foot on th | Neil Armstrong | 'Neil Armstrong' | correct | gold 命中（含等价/别名） |
| 1281 | train | Anchored by the star Polaris, the constellation ursa minor r | bear | 'a bear' | correct | gold 命中（含等价/别名） |
| 1282 | train | What Latin phrase, which translates as Out of many, one, is  | E Pluribus Unum | 'E pluribus' | correct | gold 命中（含等价/别名） |
| 1283 | test | The Sharks face off against what gang in Leonard Bernsteins  | The Jets | 'The Sharks face off against the Jets.' | correct | gold 命中（含等价/别名） |
| 1284 | train | What ice cream company produces flavors such as Everything B | Ben & Jerry's | 'Blue Bell.' | incorrect | gold 未命中 |
| 1285 | train | The gravesite of what American writer, buried in Baltimore,  | Edgar Allen Poe | ' Edgar Allan Poe' | correct | gold 别名命中 |
| 1286 | validation | What type of rain did Prince sing about in 1984? | Purple Rain | 'Purple Rain' | correct | gold 命中（含等价/别名） |
| 1287 | validation | The Dukes of Hazzard, the CBS TV series that debuted on Jan  | Bo and Luke Duke | 'Bo and Luke Duke' | correct | gold 命中（含等价/别名） |
| 1288 | test | What synthetic opioid is used to help treat heroin addiction | Methadone | 'Suboxone' | incorrect | 单 token 短答 'Suboxone'（疑似错答，人工留 |
| 1289 | train | Who broke Lou Gehrig's record by playing in his 2131st conse | Cal Ripken, Jr | "Randy Johnson broke Lou Gehrig's record by playing" | incorrect | gold 未命中 |
| 1290 | train | What magician-turned-actor portrayed a recurring role as a t | Harry Anderson | 'David Copperfield' | incorrect | gold 未命中 |
| 1291 | train | On Sept 18, 1947, which branch of the US Military became an  | US Air Force | 'Air Force' | correct | gold 命中（含等价/别名） |
| 1292 | train | The journal of which Amsterdam schoolgirl was first publishe | Anne Frank | 'Anne Frank' | correct | gold 命中（含等价/别名） |
| 1293 | train | Name the 1998 movie from the IMDB plot summary: "A former ne | American History X | 'Felix' | incorrect | 单 token 短答 'Felix'（疑似错答，人工留意） |
| 1294 | train | Commonly known as nipplegate, whose wardrobe malfunction dur | Janet Jackson | 'Christina Applegate' | incorrect | gold 未命中 |
| 1295 | train | What is the 3rd largest car rental company in the United Sta | Alamo | 'Avis' | incorrect | 单 token 短答 'Avis'（疑似错答，人工留意） |
| 1296 | validation | What Arizona national park was formed over millions of years | The Grand Canyon | 'Grand Canyon National Park.' | correct | gold 别名命中 |
| 1297 | train | On Oct 28, 1886, the rotund one himself, Grover Cleveland, o | The Statue of Liberty | 'The Washington Monument' | incorrect | gold 未命中 |
| 1298 | validation | Used primarily to talk to the dead (and the scare the snot o | Ouija Board | 'The Parker Brothers game is called Ouija.' | correct | gold 别名命中 |
| 1299 | train | What company advertised itself with the slogan “We’ll leave  | Motel 6 | 'GE Appliances' | incorrect | gold 未命中 |
| 1300 | train | First put on sale last week, Decision Points, currently rank | George W. Bush | 'John McCain' | incorrect | gold 未命中 |
| 1301 | train | What planets orbit takes it the furthest away from the sun? | Neptune | 'Neptune' | correct | gold 命中（含等价/别名） |
| 1302 | train | Although it ended up being very ineffective, what was the na | Maginot Line | 'The name for the interconnected series of concrete' | correct | gold 命中（含等价/别名） |
| 1303 | train | What is the name for the flexible, connective tissue found i | Cartilage | 'Cartilage' | correct | gold 命中（含等价/别名） |
| 1304 | validation | What radio station do you find at 90.3 on your FM dial? | KEXP | 'NPR' | incorrect | 单 token 短答 'NPR'（疑似错答，人工留意） |
| 1305 | train | The sinking of what battleship in Havana harbor on Feb 15, 1 | USS Maine | 'The sinking of the USS Maine in Havana harbor on F' | correct | gold 命中（含等价/别名） |
| 1306 | train | In what card game do you need the queen of spades to shoot t | Hearts | 'Uno' | incorrect | 单 token 短答 'Uno'（疑似错答，人工留意） |
| 1307 | train | Who's missing: Bashful, Doc, Dopey, Grumpy, Happy, Sleepy | Sneezy | 'Sleepy' | incorrect | 单 token 短答 'Sleepy'（疑似错答，人工留意） |
| 1308 | train | What was the name of two tyrants who ruled Syracuse in the 2 | Dionysius | 'Hieron and Dionysius.' | correct | gold 命中（含等价/别名） |
| 1309 | test | Which ocean is closest to the capital of the USA? | Atlantic | 'The Atlantic Ocean.' | correct | gold 命中（含等价/别名） |
| 1310 | train | Which river flows through Cologne? | Rhine | 'The Moselle River flows through Cologne.' | incorrect | gold 未命中 |
| 1311 | train | "Who has hosted the US series ""Power of 10"", ""Whose Line  | Drew Carey | ' Drew Carey' | correct | gold 命中（含等价/别名） |
| 1312 | train | What name has been used on Irish postage stamps since 1922,  | ire | 'Éire' | incorrect | 单 token 短答 'Éire'（疑似错答，人工留意） |
| 1313 | train | Where, in 2011 and since, is a major gathering place in Egyp | Tahrir Square | 'Tahrir Square' | correct | gold 命中（含等价/别名） |
| 1314 | train | What is the surname of sisters and singers Dannii and Kylie? | Minogue | 'Minogue' | correct | gold 命中（含等价/别名） |
| 1315 | train | What is the name of Tony and Cherie Blair's daughter? | Kathryn | 'Lori Blair' | incorrect | gold 未命中 |
| 1316 | train | What term is used for the actress that has the main part in  | Leading lady | 'Lead actress.' | incorrect | gold 未命中 |
| 1317 | validation | Dishes prepared with spinach can be referred to as what? | la Florentine | 'Spinach dishes.' | incorrect | gold 未命中 |
| 1318 | train | "John Wayne appeared as a centurion in the film ""The Greate | Truly this man was the s | '" Hail, Caesar!"' | incorrect | gold 未命中 |
| 1319 | test | Whose alter ego is Sasha Fierce? | Beyonc | 'Sasha Fierce is the alter ego of Beyoncé.' | incorrect | gold 未命中 |
| 1320 | train | What is a mosquito-borne virus, also known as breakbone feve | Dengue fever | 'Dengue fever.' | correct | gold 命中（含等价/别名） |
| 1321 | validation | Christmas Island is administered by which country? | Australia | 'Australia' | correct | gold 命中（含等价/别名） |
| 1322 | train | Who is the next in this series: John L. Sullivan, James J. C | Tommy Burns | 'hammad Ali.' | incorrect | gold 未命中 |
| 1323 | validation | What was the name of the operation whereby 1,373 U.S. citize | Operation Frequent Wind | 'Operationrequent.' | incorrect | 单 token 短答 'Operationrequent.' |
| 1324 | train | "Literally, what old French word translates approximately as | Blancmange | 'Blanc.' | incorrect | 单 token 短答 'Blanc.'（疑似错答，人工留意） |
| 1325 | train | Who was the only Prime Minister of Great Britain born outsid | Andrew Bonar Law | 'William Pitt' | incorrect | gold 未命中 |
| 1326 | validation | What is a legislative or executive act by which a state rest | Amnesty | 'Pardon' | incorrect | 单 token 短答 'Pardon'（疑似错答，人工留意） |
| 1327 | train | Quadrille, a popular card game in the 18th century, is for f | 40 | 'Quadrille is for four players with a deck of 52 ca' | incorrect | gold 未命中 |
| 1328 | test | On the buttons of a VCR or DVD player, what does the sign in | Fast forward | 'Rewind' | incorrect | 单 token 短答 'Rewind'（疑似错答，人工留意） |
| 1329 | train | The composer Frdric Chopin had a decade-long affair with whi | George Sand | 'Answer: George Sand.' | correct | gold 命中（含等价/别名） |
| 1330 | train | The Australian Tennis Open is played in what city? | Melbourne | 'The Australian Tennis Open is played in Melbourne,' | correct | gold 命中（含等价/别名） |
| 1331 | validation | He was the fourth of 6 children and the oldest surviving, wa | Adolf Hitler | 'William Shakespeare.' | incorrect | gold 未命中 |
| 1332 | train | What is a name for the abstract study of topics such as quan | Mathematics | 'Mathematics.' | correct | gold 命中（含等价/别名） |
| 1333 | test | "Which German was deprived of his nationality in 1938 mainly | Erich Maria Remarque | 'Erich Maria Remar' | incorrect | gold 未命中 |
| 1334 | train | "What is the first line of ""Walk on the Wild Side"" by Lou  | Holly came from Miami F  | '"Walk on the wild side"' | format_failure | 输出为问句回显，无答案内容 |
| 1335 | train | What is the name of the scientific discipline that deals wit | Geodesy | 'Geodesy' | correct | gold 命中（含等价/别名） |
| 1336 | train | In the books by A A Milne, what was Eeyore? | Donkey | 'A donkey' | correct | gold 命中（含等价/别名） |
| 1337 | test | Which pigment is named after an Italian city? | Sienna | 'Sienna.' | correct | gold 命中（含等价/别名） |
| 1338 | train | What is someone allergic to if they have coeliac disease? | Gluten | 'Gluten.' | correct | gold 命中（含等价/别名） |
| 1339 | train | Yelena Isinbayeva broke her first World record in 2003 and c | Women's Pole Vault | 'Yelena Isinbayeva broke her first World record in ' | incorrect | gold 未命中 |
| 1340 | validation | The ship Andrea Gail features in which 1997 book and 2000 fi | The Perfect Storm | 'The ship Andrea Gail features in the 1997 book and' | incorrect | gold 未命中 |
| 1341 | test | Which 19th century American poet wrote over 1,000 poems whic | Emily Dickinson | 'Emily Dickinson' | correct | gold 命中（含等价/别名） |
| 1342 | train | Who was crowned MotoGP World Champion after he finished thir | Jorge Lorenzo | 'Dani Moda' | incorrect | gold 未命中 |
| 1343 | validation | What was the name of the 1976 film that told the story of Wo | Bound for Glory | 'Woody' | incorrect | 单 token 短答 'Woody'（疑似错答，人工留意） |
| 1344 | validation | The main international cricket competitions are Test matches | Twenty20 Internationals | 'T20' | incorrect | 单 token 短答 'T20'（疑似错答，人工留意） |
| 1345 | test | Marat, Robespierre, Danton are names associated with what ev | The French Revolution | 'The French Revolution.' | correct | gold 命中（含等价/别名） |
| 1346 | validation | Cayenne, after which the spicy condiment is named, is a city | French Guiana | 'France' | incorrect | 单 token 短答 'France'（疑似错答，人工留意） |
| 1347 | train | Where is the homeland of Queen Boudica (also Boudicca or Boa | East Anglia | 'Scotland.' | incorrect | 单 token 短答 'Scotland.'（疑似错答，人工 |
| 1348 | train | In a film script, what do the letters ECU mean? | Extreme Close Up | 'Emergency Care Unit' | incorrect | gold 未命中 |
| 1349 | train | Since the Association of Tennis Professionals (ATP) World To | Rafael Nadal | 'Andre Agassi' | incorrect | gold 未命中 |
| 1350 | train | What is the name given to a bone fracture when one part of i | Impacted | 'Puncture fracture' | incorrect | gold 未命中 |
| 1351 | test | What year did the cable television network ESPN made its deb | 1979 | '1992' | incorrect | 单 token 短答 '1992'（疑似错答，人工留意） |
| 1352 | train | "Which British composer wrote ""The Dam Busters March""?" | Eric Coates | 'Ralph Vaughan Williams' | incorrect | gold 未命中 |
| 1353 | validation | Which of Queen Elizabeth's children is the lowest in success | Anne | 'Prince Harry' | incorrect | gold 未命中 |
| 1354 | train | A synonym for french kissing would be what? | Cataglottis | 'French lips' | incorrect | gold 未命中 |
| 1355 | train | "The book ""Dirty Sexy Politics"", released in 2010, was abo | John McCain | 'The book "Dirty Sexy Politics" was about Hillary C' | incorrect | gold 未命中 |
| 1356 | test | Macao Special Administrative Region of the People's Republic | Textile and garment manu | 'Manufacturing.' | incorrect | 单 token 短答 'Manufacturing.'（疑似 |
| 1357 | validation | In which country was Saddam Hussein President 1979-2003, bei | Iraq | 'Saddam Hussein was President of Iraq.' | correct | gold 命中（含等价/别名） |
| 1358 | train | Calvados apple brandy is traditionally produced in which cou | France | 'France' | correct | gold 命中（含等价/别名） |
| 1359 | train | In which country did Queen Isabella secure the throne when h | Spain | 'Queen Isabella secured the throne in Spain.' | correct | gold 命中（含等价/别名） |
| 1360 | train | What game, created in 1904 by a quaker, Elizabeth (Lizzie) P | Monopoly | 'Monopoly' | correct | gold 命中（含等价/别名） |
| 1361 | test | The first Paralympic Games to officially tie in with the Sum | Rome | 'The first Paralympic Games to officially tie in wi' | correct | gold 命中（含等价/别名） |
| 1362 | train | What is the name for a large circular stained glass window f | Rose window | 'Rose window' | correct | gold 命中（含等价/别名） |
| 1363 | train | What is the name of the son of Pete Wentz and Ashlee Simpson | Bronx Mowgli | 'Jackson.' | incorrect | 单 token 短答 'Jackson.'（疑似错答，人工留 |
| 1364 | train | "Which 19th century English writer wrote ""Swallows and Amaz | Arthur Ransome | ' Jules Verne' | incorrect | gold 未命中 |
| 1365 | train | In which country did Juan Domingo Peron seize power in 1943, | Argentina | 'Argentina' | correct | gold 命中（含等价/别名） |
| 1366 | train | The U.S. Masters, one of the four major championships in pro | Augusta National Golf Cl | 'The U.S. Masters has been played at Augusta Nation' | correct | gold 命中（含等价/别名） |
| 1367 | train | On 12 September 1995, the Belarusian air force shot down a g | Gordon Bennett Cup | 'The World Cup' | incorrect | gold 未命中 |
| 1368 | validation | The highest mountain in North America is part of which mount | Alaska Range | 'The highest mountain in North America, Denali, is ' | correct | gold 命中（含等价/别名） |
| 1369 | train | Which conflict began in England in 1455 after King Henry VI, | The Wars of the Roses | 'The Wars of the Roses.' | correct | gold 命中（含等价/别名） |
| 1370 | test | "Which 16th century Venetian, born Jacopo Robusti, studied u | Tintoretto | 'Tiziano' | incorrect | 单 token 短答 'Tiziano'（疑似错答，人工留意 |
| 1371 | test | Which group of around 200 Greek islands in the Aegean Sea in | Cyclades | 'The Cyclades.' | correct | gold 命中（含等价/别名） |
| 1372 | train | "Which German social economist of Jewish descent, expelled f | Karl Marx | 'Karl Marx' | correct | gold 命中（含等价/别名） |
| 1373 | test | The English cities of Gloucester and Worcester are on which  | River Severn | 'The English cities of Gloucester and Worcester are' | correct | gold 命中（含等价/别名） |
| 1374 | train | Which British comedy-drama series (1979 to 1994) starred Geo | Minder | 'Blackadder' | incorrect | 单 token 短答 'Blackadder'（疑似错答，人 |
| 1375 | train | Prince Philip, Duke of Edinburgh, was born on which island? | Corfu | 'Prince Philip, Duke of Edinburgh, was born on the ' | incorrect | gold 未命中 |
| 1376 | train | Who was the leader of the Peasant's Revolt in 1381 who, afte | Wat Tyler | "The leader of the Peasant's Revolt in 1381 was Wat" | correct | gold 命中（含等价/别名） |
| 1377 | test | Australian Shane Warne is associated with which sport? | Cricket | 'Cricket' | correct | gold 命中（含等价/别名） |
| 1378 | train | What was the name of the computer in Stanley Kubricks 2001:  | HAL | "The name of the computer in Stanley Kubrick's 2001" | correct | gold 命中（含等价/别名） |
| 1379 | train | What is a popular name for the North American bison? | Buffalo | 'A popular name for the North American bison is the' | correct | gold 命中（含等价/别名） |
| 1380 | test | Badminton debuted at the 1992 Summer Olympics. How many diff | 5 | '4' | format_failure | 单 token 函数词/碎片 '4'，无答案内容 |
| 1381 | validation | What name was given to a series of thirty evening radio spee | Fireside chats | 'fireside chats' | correct | gold 命中（含等价/别名） |
| 1382 | train | The final carrier of the Olympic flame in the Olympic Torch  | A sports celebrity of th | 'The final carrier of the Olympic flame in the Olym' | incorrect | gold 未命中 |
| 1383 | validation | What was the first name of de Gaulle, the first President of | Charles | 'Charles' | correct | gold 命中（含等价/别名） |
| 1384 | train | Measuring from the closest point of each of these countries  | Canada | 'Russia' | incorrect | 单 token 短答 'Russia'（疑似错答，人工留意） |
| 1385 | validation | "What is the setting for the Alfred Hitchcock film ""The Bir | Bodega Bay, California | 'The setting for the Alfred Hitchcock film "The Bir' | incorrect | gold 未命中 |
| 1386 | test | After sporadic visits by European explorers and merchants fr | Australia | 'The eastern half of Australia.' | correct | gold 命中（含等价/别名） |
| 1387 | train | Lee Kuan Yew and Goh Chok Tong were the first two Prime Mini | The Republic of Singapor | 'Lee Kuan Yew and Goh Chok Tong were the first two ' | correct | gold 别名命中 |
| 1388 | train | Farthings were in use in England as coinage from the 13th ce | 960 | '40' | format_failure | 单 token 函数词/碎片 '40'，无答案内容 |
| 1389 | train | What was the Mississippi State Penitentiary formerly called? | Parchman Farm | 'The Mississippi State Penitentiary was formerly ca' | correct | gold 别名命中 |
| 1390 | train | What name is given to the syndrome which involves a delusion | Clinical lycanthropy | ' metamorphosis.' | incorrect | 单 token 短答 ' metamorphosis.'（疑 |
| 1391 | test | "Where would one find ""Bachmann's bundle""?" | The human heart | "Bachmann's bundle is a mathematical concept." | incorrect | gold 未命中 |
| 1392 | train | In 1848, Mexico ratified the Treaty of Guadalupe Hidalgo, of | Land | 'Texas.' | incorrect | 单 token 短答 'Texas.'（疑似错答，人工留意） |
| 1393 | train | The Great Sphinx of Giza in Egypt is a statue of a reclining | Human | 'Human.' | correct | gold 命中（含等价/别名） |
| 1394 | validation | What is the disease that Stephen Hawking has? | Motor neuron disease | 'Stephen Hawking has amyotrophic lateral sclerosis.' | incorrect | gold 未命中 |
| 1395 | train | Formula 1 driver Ayrton Senna died while leading the 1994 Sa | Imola | 'Ayrton Senna died while leading the 1994 San Marin' | incorrect | gold 未命中 |
| 1396 | test | In which novel does Michael Henchard sell his wife and child | The Mayor of Casterbridg | 'David Copperfield' | incorrect | gold 未命中 |
| 1397 | train | The capital of Brazil was moved from Rio de Janeiro to the p | 1960 | '1960' | correct | gold 命中（含等价/别名） |
| 1398 | test | Who won the gold medal for the 100m at the 1992 Olympics at  | Linford Christie | 'Michael Johnson.' | incorrect | gold 未命中 |
| 1399 | train | Cricketer W G Grace, who played first-class cricket from 186 | Lawn bowls | 'Football.' | incorrect | 单 token 短答 'Football.'（疑似错答，人工 |
| 1400 | train | Who invaded Europe from Mongolia and Turkey over 300 years,  | Tartars | 'The Mongols.' | incorrect | gold 未命中 |
| 1401 | test | What is the name of Madonna's proposed chain of fitness club | Hard Candy Fitness | 'Madonna Fitness.' | incorrect | gold 未命中 |
| 1402 | validation | What is a group of jellyfish called? | Smack | 'A group of jellyfish is called a swarm.' | incorrect | gold 未命中 |
| 1403 | validation | Which shipping passage was closed from 1967 to 1975? | Suez Canal | 'The Panama Canal.' | incorrect | gold 未命中 |
| 1404 | test | "In Victorian England, what was a ""reticule""?" | Bag | 'In Victorian England, a "reticule" was a type of f' | incorrect | gold 未命中 |
| 1405 | validation | The Limpopo River separates Zimbabwe and Botswana from what  | South Africa | 'The Limpopo River separates Zimbabwe and Botswana ' | correct | gold 命中（含等价/别名） |
| 1406 | validation | "In the 19th century, the term ""penny dreadful"" applied to | Book | 'In the 19th century, the term "penny dreadful" app' | incorrect | gold 未命中 |
| 1407 | train | "The ""Three Laws of Motion"" are named after which scientis | Isaac Newton | 'Isaac Newton' | correct | gold 命中（含等价/别名） |
| 1408 | train | Who was the first US president to succeed to the Presidency  | Andrew Johnson | 'Andrew Johnson' | correct | gold 命中（含等价/别名） |
| 1409 | train | "Which American vocalist (described by the British newspaper | Eva Cassidy | 'The American vocalist described by the British new' | format_failure | 规则检出拒答 |
| 1410 | test | What name is given to describes the phenomenon of the gradua | Diffusion | 'Diffusion.' | correct | gold 命中（含等价/别名） |
| 1411 | train | Maine Coon, Munchkin, Oriental Shorthair, Persian, Ragamuffi | Cat | 'Cats.' | correct | gold 别名命中 |
| 1412 | train | In which year was the first robbery for which it is known th | 1869 | '1876' | incorrect | 单 token 短答 '1876'（疑似错答，人工留意） |
| 1413 | train | "In what sport are the ""stones"" aimed at the ""house""?" | Curling | 'Curling.' | correct | gold 命中（含等价/别名） |
| 1414 | validation | Who married Heidi Klum in May 2005? | Seal | 'Holger Hauer married Heidi Klum in May 2005.' | incorrect | gold 未命中 |
| 1415 | test | How many US states border Lake Superior? | 3 | 'Three US states border Lake Superior.' | correct | gold 别名命中 |
| 1416 | test | Where was the world's tallest road bridge opened in December | France | "The world's tallest road bridge was opened in Shan" | incorrect | gold 未命中 |
| 1417 | test | What was the UK #1 single released by the band Stereophonics | Dakota | '"Home"' | incorrect | 单 token 短答 '"Home"'（疑似错答，人工留意） |
| 1418 | train | Which member of the British royal family was born on 8/8/88? | Princess Beatrice of Yor | 'Prince Harry.' | incorrect | gold 未命中 |
| 1419 | train | What is traditionally written in a ledger? | Accounts | 'Financial records are traditionally written in a l' | incorrect | gold 未命中 |
| 1420 | train | Which 20th century American composer wrote the American Fest | William Schuman | 'Aaron Copland' | incorrect | gold 未命中 |
| 1421 | test | What is the maximum number of points that can be scored from | 3 | 'The maximum number of points that can be scored fr' | correct | gold 命中（含等价/别名） |
| 1422 | train | "Who wrote the poem ""Daffodils""?" | William Wordsworth | 'The poem "Daffodils" was written by William Wordsw' | correct | gold 命中（含等价/别名） |
| 1423 | test | Where was the first permanent European settlement establishe | Florida | 'The first permanent European settlement was establ' | incorrect | gold 未命中 |
| 1424 | validation | Which famous painter's surname was Harmenzoon van Rijn which | Rembrandt | 'Rembrandt' | correct | gold 命中（含等价/别名） |
| 1425 | train | From which animal does Haggis come? | Sheep | 'Haggis comes from a sheep.' | correct | gold 命中（含等价/别名） |
| 1426 | test | Which King did Guy Fawkes attempt to kill with his gunpowder | James I | 'Guy Fawkes attempted to kill King James I with his' | correct | gold 命中（含等价/别名） |
| 1427 | test | Which animal has the longest gestation period at around 22 m | The elephant | 'Elephant' | incorrect | 单 token 短答 'Elephant'（疑似错答，人工留 |
| 1428 | train | Which famous book features the character of Bob Cratchit? | A Christmas Carol | 'A Christmas Carol by Charles Dickens.' | correct | gold 命中（含等价/别名） |
| 1429 | train | Which actress married Dennis Quaid on Valentine's Day in 199 | Meg Ryan | 'Jennifer Aniston' | incorrect | gold 未命中 |
| 1430 | train | How many pieces are there in a standard set of dominoes? | 28 | 'A standard set of dominoes contains 28 pieces.' | correct | gold 命中（含等价/别名） |
| 1431 | test | What is the acronym for the agency which provides co-operati | Interpol | 'INTERPOL' | correct | gold 命中（含等价/别名） |
| 1432 | validation | The Ducati is manufactured in which city and what country? | Bologna, Italy | 'The Ducati is manufactured in Bologna, Italy.' | correct | gold 命中（含等价/别名） |
| 1433 | train | Who presented Family Fortunes in the two years between Bob M | Max Bygraves | 'Alan Freeman' | incorrect | gold 未命中 |
| 1434 | train | Which planet has moons named after Shakespearean characters? | Uranus | 'Saturn' | incorrect | 单 token 短答 'Saturn'（疑似错答，人工留意） |
| 1435 | train | Which movie starred Michael Caine as a murderous transvestit | Dressed To Kill | 'M.' | format_failure | 单 token 函数词/碎片 'M.'，无答案内容 |
| 1436 | train | Meryl Streep's character, Miranda, in the 2006 film The Devi | Vogue | 'Vogue' | correct | gold 命中（含等价/别名） |
| 1437 | train | Who won the 2010 Giro D'Italia? | Ivan Basso | ' Alberto Contador.' | incorrect | gold 未命中 |
| 1438 | train | In the Commonwealth games in Delhi, which British athlete wo | Leon Baptiste | 'Usain Bolt' | incorrect | gold 未命中 |
| 1439 | train | Who sang the theme song for the TV show 'Rawhide'? | Frankie Laine | 'Tom Jones.' | incorrect | gold 未命中 |
| 1440 | validation | Which constellation contains many bright shining stars, such | Leo. | 'The constellation that contains many bright shinin' | correct | gold 命中（含等价/别名） |
| 1441 | train | For what novel did J. K. Rowling win the 1999 Whitbread Chil | Harry Potter and the Pri | "J. K. Rowling won the 1999 Whitbread Children's bo" | incorrect | gold 未命中 |
| 1442 | test | Which company were responsible for the production of the Spi | Supermarine | 'Supermarine.' | correct | gold 命中（含等价/别名） |
| 1443 | train | 1986 film starring Goldie Hawn as a High School football coa | Wildcats | 'Fame.' | incorrect | 单 token 短答 'Fame.'（疑似错答，人工留意） |
| 1444 | test | Which Italian explorer had ships named Nina, Pinta and Santa | Christopher COLUMBUS | 'Christopher Columbus' | correct | gold 命中（含等价/别名） |
| 1445 | test | Which famous resident resides at Highgrove House? | The Prince of Wales | 'Harry Potter.' | incorrect | gold 未命中 |
| 1446 | validation | Rarely is the question asked: Is our children learning? | George W Bush | 'No' | format_failure | 单 token 函数词/碎片 'No'，无答案内容 |
| 1447 | train | Mel Gibson (1990) and Kenneth Branagh (1996) have both playe | Hamlet | 'Richard III.' | incorrect | gold 未命中 |
| 1448 | validation | Which Holiday movie favourite featured a character called Ke | Home Alone | 'Home Alone' | correct | gold 命中（含等价/别名） |
| 1449 | train | What year did E.T. Hit the cinema screen? | 1982 | '1982' | correct | gold 命中（含等价/别名） |
| 1450 | test | Which singer played the Goblin King Jareth in the film Laby | David Bowie | 'David Bowie.' | correct | gold 命中（含等价/别名） |
| 1451 | train | Who created the Miss World pageant? | Eric Morley. | 'The Miss World pageant was created by Eric Morley ' | correct | gold 命中（含等价/别名） |
| 1452 | train | What dish, especially popular in parts of Wales and the Engl | Faggots | 'Rabbit' | incorrect | 单 token 短答 'Rabbit'（疑似错答，人工留意） |
| 1453 | train | What was the name of Shari Lewis' sassy sock puppet? | Lamb Chop. | 'Sassy' | incorrect | 单 token 短答 'Sassy'（疑似错答，人工留意） |
| 1454 | train | What is the southernmost city in USA | Honolulu | 'The southernmost city in the USA is Miami, Florida' | incorrect | gold 未命中 |
| 1455 | test | In Vladimir Nabokov's book "Lolita", what is Lolita's real n | Dolores HAZE | "Lolita's real name is Dolores Humbert." | correct | gold 别名命中 |
| 1456 | test | What animal did Reggie Perrin think of every time his Mother | A Hippopotamus. | 'A cow' | incorrect | gold 未命中 |
| 1457 | validation | More commonly known as the thigh bone, what is the medical n | The Femur | 'The medical name for the longest bone in the human' | correct | gold 命中（含等价/别名） |
| 1458 | train | What is being built in the Olympic Park, that will be the wo | A slide | 'The National Stadium.' | incorrect | gold 未命中 |
| 1459 | train | What was the name of the Liverpool nightclub where the Beatl | The Cavern | 'The Cavern Club' | correct | gold 命中（含等价/别名） |
| 1460 | test | How many US states are prefixed by the word New? | 4 | '2' | format_failure | 单 token 函数词/碎片 '2'，无答案内容 |
| 1461 | train | Which ITV magazine style show ran from 1968 to 1980 and feat | Magpie | 'Panorama' | incorrect | 单 token 短答 'Panorama'（疑似错答，人工留 |
| 1462 | train | In which New York borough would you find Hell’s Kitchen? | Manhattan | "Hell's Kitchen is located in the borough of Manhat" | correct | gold 命中（含等价/别名） |
| 1463 | train | The melody for which famous song was written by sisters and  | Happy Birthday | 'Happy Birthday.' | correct | gold 命中（含等价/别名） |
| 1464 | test | What do we call the vegetable called the rutabaga in America | Swede | 'Turnip.' | incorrect | 单 token 短答 'Turnip.'（疑似错答，人工留意 |
| 1465 | train | In which city in the UK is the National Railways Museum? | York | 'The National Railways Museum is located in York, E' | correct | gold 命中（含等价/别名） |
| 1466 | test | Which boxer was the first to defeat Mike Tyson in a professi | "James (""Buster"") Doug | 'Joe Louis.' | incorrect | gold 未命中 |
| 1467 | train | Who has been Archbishop of York since 2005? | John Sentamu | 'Justin Williams' | incorrect | gold 未命中 |
| 1468 | train | In the Muslim religion what name is given to an invisible sp | DJINN | 'Jinn' | correct | gold 别名命中 |
| 1469 | test | As a figure of speech, what is a statement made in exaggerat | HYPERBOLE | 'Hyperbole.' | correct | gold 命中（含等价/别名） |
| 1470 | test | Which 'literary' nickname has been given to the extinct spec | Hobbits | 'Little Man' | incorrect | gold 未命中 |
| 1471 | train | Which character from a comic strip had the real name Marmadu | Lord Snooty | 'Fancy Brown' | incorrect | gold 未命中 |
| 1472 | validation | Who, according to legend, cut the Gordian Knot? | Alexander the Great | 'Homer.' | incorrect | 单 token 短答 'Homer.'（疑似错答，人工留意） |
| 1473 | train | In Greek mythology which king of Corinth was compelled to et | Sisyphus | 'Syleus' | incorrect | 单 token 短答 'Syleus'（疑似错答，人工留意） |
| 1474 | train | What is the name of Long John Silver's parrot in Treasure Is | Captain Flint | 'Silver.' | incorrect | 单 token 短答 'Silver.'（疑似错答，人工留意 |
| 1475 | validation | What consumer electronics product shares its name with the c | BLACKBERRY | 'Raspberry' | incorrect | 单 token 短答 'Raspberry'（疑似错答，人工 |
| 1476 | train | The Corryvreckan whirlpool lies to the north of which Scotti | JURA | 'The Corryvreckan whirlpool lies to the north of th' | incorrect | gold 未命中 |
| 1477 | train | Which Hollywood film star advertises 'Qantas' airlines and i | JOHN TRAVOLTA | 'Tom Hanks' | incorrect | gold 未命中 |
| 1478 | test | 'The Castle of Otranto' often called the first gothic novel, | HORACE WALPOLE | 'Horace Walpole' | correct | gold 命中（含等价/别名） |
| 1479 | train | Which group became the first to reach Number One with their  | THE SPICE GIRLS | 'The Beatles' | incorrect | gold 未命中 |
| 1480 | train | The flag of which European country is a blue-white-red horiz | Serbia | 'Spain' | incorrect | 单 token 短答 'Spain'（疑似错答，人工留意） |
| 1481 | train | Who, in May 2006 when aged 17 years and 75 days, became the  | Theo Walcott | 'Wayne Rooney' | incorrect | gold 未命中 |
| 1482 | train | Blinky, Pinky, Inky, and Clyde are four ghosts in which arca | Pac-Man | 'Blinky, Pinky, Inky, and Clyde are four ghosts in ' | correct | gold 命中（含等价/别名） |
| 1483 | test | 2012 is the Chinese year of which creature? | DRAGON | 'Monkey' | incorrect | 单 token 短答 'Monkey'（疑似错答，人工留意） |
| 1484 | validation | What was the code name for the British retreat from Dunkirk  | Dynamo | 'Operation Dynamo' | correct | gold 命中（含等价/别名） |
| 1485 | train | In Greek Mythology who was the princess rescued from the Sea | ANDROMEDA | 'Athena' | incorrect | 单 token 短答 'Athena'（疑似错答，人工留意） |
| 1486 | train | The term 'the fourth wall' would be used for an imaginary wa | Theatre | 'Theater' | correct | gold 别名命中 |
| 1487 | test | According to ancient Greek philosophers the universe was mad | Ether | 'ether' | correct | gold 命中（含等价/别名） |
| 1488 | validation | Which tree has the Lath name Taxus? | YEW | 'The yew.' | correct | gold 命中（含等价/别名） |
| 1489 | test | Who hit six sixes in one over at 2007 Cricket World Cup in t | (Herschelle) GIBBS | 'Brian Lara.' | incorrect | gold 未命中 |
| 1490 | train | "Who played Luke Skywalker in the 1977 original ""Star Wars" | (Mark) HAMILL | 'Mark Hamill' | correct | gold 命中（含等价/别名） |
| 1491 | train | Which car company manufacturers the Corolla model? | Toyota | 'Toyota' | correct | gold 命中（含等价/别名） |
| 1492 | test | What name is given to the nine square mile area of West York | THE RHUBARB TRIANGLE | 'Broadfield.' | incorrect | 单 token 短答 'Broadfield.'（疑似错答， |
| 1493 | train | Pearl is composed of minute crystals of which compound? | Calcium Carbonate | 'Calcium carbonate.' | correct | gold 命中（含等价/别名） |
| 1494 | train | Who was the last British male to reach the final of a Grand  | Greg Rusedski | 'Andy Murray.' | incorrect | gold 未命中 |
| 1495 | test | The folk song Johnny Todd is the signature tune for which 60 | Z Cars | 'The Lieutenant.' | incorrect | gold 未命中 |
| 1496 | train | Britain's first jet fighter, The Meteor was made by which co | GLOSTER | ' Gloster Meteor' | correct | gold 命中（含等价/别名） |
| 1497 | test | What is the name of the strong fibrous tissue that joins one | Ligament | 'Ligament.' | correct | gold 命中（含等价/别名） |
| 1498 | test | Who was housekeeper to Sherlock Holmes? | Mrs Hudson | 'Mary Hudson.' | incorrect | gold 未命中 |
| 1499 | train | Which European country's flag is a blue cross on a white bac | Finland | 'Sweden.' | incorrect | 单 token 短答 'Sweden.'（疑似错答，人工留意 |
| 1500 | train | Who is the oldest person to have a number one hit in Britain | LOUIS ARMSTRONG | 'Tom Jones.' | incorrect | gold 未命中 |
| 1501 | validation | What is the name of the whirlpool in the Hebrides between Sc | Corryvreckan | 'The Ness.' | incorrect | gold 未命中 |
| 1502 | validation | If you were to fly due east out of Rio de Janeiro, which cou | Namibia | 'Argentina' | incorrect | 单 token 短答 'Argentina'（疑似错答，人工 |
| 1503 | train | Which country joined the G7 government forum which then beca | Russia | 'Russia' | correct | gold 命中（含等价/别名） |
| 1504 | train | In which activity are banderillas used? | BULLFIGHTING | 'Banderillas are used in boxing.' | incorrect | gold 未命中 |
| 1505 | test | In radio technology, what does the 'A' represent in 'DAB'? | AUDIO | 'Analog' | incorrect | 单 token 短答 'Analog'（疑似错答，人工留意） |
| 1506 | train | Made in Cornwall, Yarg cheese is wrapped in what? | NETTLES | 'Cotton' | incorrect | 单 token 短答 'Cotton'（疑似错答，人工留意） |
| 1507 | train | Which Norwegian firm supposedly produced the first fleece fa | Helly Hansen | 'Stoltex' | incorrect | 单 token 短答 'Stoltex'（疑似错答，人工留意 |
| 1508 | train | In the cartoon series, what kind of dog is Scooby Doo? | Great Dane | 'Scooby Doo is a Great Dane dog.' | correct | gold 命中（含等价/别名） |
| 1509 | test | What was the name of Gary Puckett's backing group? | The Union Gap | 'The Firm.' | incorrect | gold 未命中 |
| 1510 | validation | "Which English comedian had a minor hit in 1958 with his cov | CHARLIE DRAKE | 'Peter Sellers.' | incorrect | gold 未命中 |
| 1511 | train | In which Indian city is Eden Gardens, the second largest tes | KOLKATA | 'Eden Gardens is located in Kolkata, India.' | correct | gold 命中（含等价/别名） |
| 1512 | test | Which opera star was born Claire Mary Teresa Rawstron in 194 | KIRI TE KANAWA | 'Claire Smith.' | incorrect | gold 未命中 |
| 1513 | validation | The Melrose Cup is awarded in which ball sport? | RUGBY SEVENS | 'The Melrose Cup is awarded in soccer.' | incorrect | gold 未命中 |
| 1514 | validation | "Which make of car is advertised under the slogan ""Vorsprun | Audi | 'BMW' | incorrect | 单 token 短答 'BMW'（疑似错答，人工留意） |
| 1515 | train | In Pride and Prejudice what was the first name of Mr Darcy? | Fitzwilliam | 'William' | incorrect | 单 token 短答 'William'（疑似错答，人工留意 |
| 1516 | validation | Name the French artist (1839-1906) whose painting 'The Card  | Paul Cézanne | 'Pierre Degas.' | incorrect | gold 未命中 |
| 1517 | train | Which famous conductor conducted the very first performance  | Sir Adrian Boult | 'Richard Strauss.' | incorrect | gold 未命中 |
| 1518 | test | Which man won a record 26 Academy Award 'Oscars'? | Walt Disney | 'James Stewart.' | incorrect | gold 未命中 |
| 1519 | train | Who played the part of 'Fitz' in the TV series 'Cracker'? | Robbie Coltrane | 'Stephen Fry.' | incorrect | gold 未命中 |
| 1520 | train | The flag of the Great Socialist People's Libyan Arab Jamahir | Green | "The flag of the Great Socialist People's Libyan Ar" | correct | gold 命中（含等价/别名） |
| 1521 | train | Who was born at Villa Mon Repos, Corfu, in 1921? | Prince Philip | 'Winston Churchill.' | incorrect | gold 未命中 |
| 1522 | train | In which children's TV series does Shaggy appear? | SCOOBY DOO | 'Shaggy appears in the children\'s TV series "Muppet' | incorrect | gold 未命中 |
| 1523 | train | Which of England's 1966 World Cup winning footballers played | George Cohen | 'Bobby Moore' | incorrect | gold 未命中 |
| 1524 | validation | At what age does an individual first become entitled to a fr | 75 | '16' | format_failure | 单 token 函数词/碎片 '16'，无答案内容 |
| 1525 | train | In which sport is the Vince Lombardi awarded? | American Football | 'The Vince Lombardi Award is awarded in American fo' | correct | gold 命中（含等价/别名） |
| 1526 | train | Which island nation lost a day in Dec. 2011 by moving the In | Samoa | 'New Zealand' | incorrect | gold 未命中 |
| 1527 | train | Which Roman Emperor succeeded his father Vespasian in 79? | Titus | 'Domit' | incorrect | 单 token 短答 'Domit'（疑似错答，人工留意） |
| 1528 | train | The bones of King Richard III have been discovered under a c | LEICESTER | 'York.' | incorrect | 单 token 短答 'York.'（疑似错答，人工留意） |
| 1529 | test | Which Briton won the Nobel Prize for Literature in the 1980s | WILLIAM GOLDING | 'William Morrison' | incorrect | gold 未命中 |
| 1530 | train | Which Scotsman became the first European to reach the River  | Mungo Park | 'James Bruce' | incorrect | gold 未命中 |
| 1531 | train | On which West Indian island did the Calypso originate? | TRINIDAD | 'Jamaica' | incorrect | 单 token 短答 'Jamaica'（疑似错答，人工留意 |
| 1532 | train | Which American motor manufacturer's logo is the head of a ra | Dodge | 'Ford' | incorrect | 单 token 短答 'Ford'（疑似错答，人工留意） |
| 1533 | train | Who was the first President to be an American citizen from b | Martin Van Buren | 'George Washington' | incorrect | gold 未命中 |
| 1534 | test | Which Pacific nation consists of over 800 islands and islets | FIJI | 'Fiji' | correct | gold 命中（含等价/别名） |
| 1535 | train | Which April fool's joke did Richard Dimbleby report on in 19 | THE SPAGHETTI TREE | 'Richard Dimbleby reported on the spaghetti man hoa' | incorrect | gold 未命中 |
| 1536 | train | Which English county is Bletchley Park, the WW II code-break | BUCKINGHAMSHIRE | 'Bletchley Park is located in the English county of' | correct | gold 命中（含等价/别名） |
| 1537 | train | According to the late Dr Robert Atkins, what kind of nutrien | Carbohydrates | 'Carbohydrates' | correct | gold 命中（含等价/别名） |
| 1538 | train | "What does the Latin phrase ""primus inter pares "" mean?" | First Amongst Equals | 'The Latin phrase "primus inter pares" means "first' | correct | gold 别名命中 |
| 1539 | train | Sir William Herschel discovered which planet, calling it 'Ge | Uranus | 'Sir William Herschel discovered Uranus, calling it' | correct | gold 命中（含等价/别名） |
| 1540 | train | What is added to white wine to make a Kir? | Cassis | 'Sugar.' | incorrect | 单 token 短答 'Sugar.'（疑似错答，人工留意） |
| 1541 | train | In Imperial measurement, how many pounds are there in a hund | 112 | 'There are 20 pounds in a hundredweight.' | incorrect | gold 未命中 |
| 1542 | train | The most southerly part of mainland Australia is in which st | VICTORIA | 'The most southerly part of mainland Australia is i' | incorrect | gold 未命中 |
| 1543 | train | Which female country and Western singer died in a plane cras | PATSY CLINE | 'Joni James' | incorrect | gold 未命中 |
| 1544 | validation | In the 1920s by what name did Angelo Siciliano become better | CHARLES ATLAS | 'Charo.' | incorrect | 单 token 短答 'Charo.'（疑似错答，人工留意） |
| 1545 | test | Which 1980s TV sitcom starred Keith Barron and Gwen Taylor a | Duty Free | 'Relax!' | incorrect | 单 token 短答 'Relax!'（疑似错答，人工留意） |
| 1546 | test | The painting A Dance to the Music of Time 1634 - 1635 displa | Nicholas Poussin | 'Vermeer' | incorrect | 单 token 短答 'Vermeer'（疑似错答，人工留意 |
| 1547 | train | Which adjective is used when pertaining to the fox? | VULPINE | 'Foxy' | incorrect | 单 token 短答 'Foxy'（疑似错答，人工留意） |
| 1548 | validation | Euclid of Alexandria established the foundations of which br | Geometry | 'Geometry' | correct | gold 命中（含等价/别名） |
| 1549 | train | Alfred Munnings was famous for his paintings of what? | HORSES | 'Alfred Munnings was famous for his paintings of la' | incorrect | gold 未命中 |
| 1550 | train | Who is the most famous cartoon creation of Al Capp? | Li'l Abner | 'Popeye' | incorrect | 单 token 短答 'Popeye'（疑似错答，人工留意） |
| 1551 | train | Juba is the capital of which country? | South Sudan | 'Juba is the capital of Sudan.' | incorrect | gold 未命中 |
| 1552 | validation | What is the French name for the English channel? | La Manche | 'The French name for the English Channel is the Man' | correct | gold 别名命中 |
| 1553 | validation | Which European country has Switzerland to the west Austria t | Lichtenstein | 'Germany' | incorrect | 单 token 短答 'Germany'（疑似错答，人工留意 |
| 1554 | train | Who composed the 'War Requiem'? | Benjamin Britten | 'Richard Strauss.' | incorrect | gold 未命中 |
| 1555 | train | Who founded the Body Shop, in the UK, in 1976? | Anita Roddick | 'John Burton.' | incorrect | gold 未命中 |
| 1556 | test | Which literary location did John Jarndyce own? | Bleak House | 'John Jarndyce owned Morok Hall.' | correct | gold 别名命中 |
| 1557 | train | Under what pseudonym did JK Rowling publish the book 'The Cu | Robert Galbraith | 'Galbraith' | incorrect | 单 token 短答 'Galbraith'（疑似错答，人工 |
| 1558 | train | Who won the first ever boxing gold for women? She shares her | Nicola Adams | 'Helen Douglas.' | incorrect | gold 未命中 |
| 1559 | train | What was the Christian name of the wife of composer Robert S | CLARA | 'Clara' | correct | gold 命中（含等价/别名） |
| 1560 | test | Which comic strip character was created in the early fifties | DAN DARE | 'Tom Brown' | incorrect | gold 未命中 |
| 1561 | validation | In which TV 'quiz' show was the consolation prize a dustbin? | 3-2-1 | 'The Chase.' | incorrect | gold 未命中 |
| 1562 | train | The books 'The Edge of Reason' and 'Mad About The Boy' are s | Bridget Jones' Diary | "The books 'The Edge of Reason' and 'Mad About The " | incorrect | gold 未命中 |
| 1563 | train | St John's is the capital of which Canadian Province? | NEWFOUNDLAND | "St. John's is the capital of the Canadian province" | correct | gold 命中（含等价/别名） |
| 1564 | train | 'We Will Stand Together' is a song to music from which class | Nimrod | 'The Ninth Symphony.' | incorrect | gold 未命中 |
| 1565 | train | 'Eureka', the National Children's Museum is in which town? | Halifax | 'Manchester.' | incorrect | 单 token 短答 'Manchester.'（疑似错答， |
| 1566 | train | The first session of the United Nations General Assembly was | London | 'New York City' | incorrect | gold 未命中 |
| 1567 | test | Broxtowe District Council is in which English county? | Nottinghamshire | 'Broxtowe District Council is in the English county' | correct | gold 命中（含等价/别名） |
| 1568 | train | Where does Rupert Bear live? | NUTWOOD | 'Rupert Bear lives in Ontario, Canada.' | incorrect | gold 未命中 |
| 1569 | test | Which Shakespeare comedy is set in Messina, Italy? | MUCH ADO ABOUT NOTHING | 'Twelfth Night' | incorrect | gold 未命中 |
| 1570 | train | Which organisation was founded in Ontario, Canada in 1897 by | WOMEN'S INSTITUTE | 'The Canadian Red Cross.' | incorrect | gold 未命中 |
| 1571 | test | Forbes Magazine named which author as the top earner between | E L JAMES | 'Stephen King.' | incorrect | gold 未命中 |
| 1572 | validation | Which is the largest island in Canada? | Baffin Island | 'The largest island in Canada is Vancouver Island.' | incorrect | gold 未命中 |
| 1573 | train | Which company produced the Hastings and Herald aircraft? | Handley-Page | 'Hawker Hunter' | incorrect | gold 未命中 |
| 1574 | test | The Carnegie family fortune was built around Andrew Carnegie | Steel | 'Steel' | correct | gold 命中（含等价/别名） |
| 1575 | test | In 1986 the prime minister of which European country was ass | Sweden | 'Italy.' | incorrect | 单 token 短答 'Italy.'（疑似错答，人工留意） |
| 1576 | test | Which member of the cabinet is MP for Maidenhead? | THERESA MAY | 'Liz Truss' | incorrect | gold 未命中 |
| 1577 | train | Who wrote the opera A Masked Ball? | Giuseppe Verdi | 'Johann Strauss.' | incorrect | gold 未命中 |
| 1578 | train | Who, c1819, wrote the poem Ode to the West Wind? | PERCY BYSSHE SHELLY | 'William Wordsworth' | incorrect | gold 未命中 |
| 1579 | train | Which island is named after the world's largest bear? | Kodiak | 'Polar bear Island' | incorrect | gold 未命中 |
| 1580 | train | Mount Elbrus, arguably Europe's highest peak, is in which mo | Caucasus | 'Mount Elbrus is in the Caucasus mountain range.' | correct | gold 命中（含等价/别名） |
| 1581 | train | Which popular dessert was invented at the Hungry Monk in Alf | SUSSEX POND | 'Chocolate Wellington.' | incorrect | gold 未命中 |
| 1582 | test | The disease pertussis is more commonly known by what name? | Whooping Cough | 'Whooping cough.' | correct | gold 命中（含等价/别名） |
| 1583 | test | In anatomy, what is a ganglion? | Nerve Cell Cluster | 'A ganglion is a cluster of nerve cells.' | incorrect | gold 未命中 |
| 1584 | train | Which indoor sport includes a side wall, front wall, and a t | Squash | 'Bowling.' | incorrect | 单 token 短答 'Bowling.'（疑似错答，人工留 |
| 1585 | train | HRH Princess Anne?s Gloucestershire country home is called w | Gatcombe Park | 'Highgrove.' | incorrect | 单 token 短答 'Highgrove.'（疑似错答，人 |
| 1586 | train | What is the derived SI unit of pressure? | Pascal | 'The derived SI unit of pressure is the Pascal (Pa)' | correct | gold 命中（含等价/别名） |
| 1587 | test | Who captained the England rugby union team 59 times between  | Will Carling | 'John Wilkinson' | incorrect | gold 未命中 |
| 1588 | test | Which standard orchestral instrument has a name which derive | Oboe | 'Flute' | incorrect | 单 token 短答 'Flute'（疑似错答，人工留意） |
| 1589 | train | Which Mexican dish is a steamed corn husk filled with meat o | Tamale | 'Tamale' | correct | gold 命中（含等价/别名） |
| 1590 | test | Which mountain range stretches for 1500 miles and has Mount  | Appalachians | 'The Appalachian Mountains.' | correct | gold 别名命中 |
| 1591 | test | In which 1816 novel do we meet the characters Anne Elliot an | Persuasion | 'Persuasion' | correct | gold 命中（含等价/别名） |
| 1592 | train | Which chemical element is named after a university in Oaklan | Berkelium | 'Americium' | incorrect | 单 token 短答 'Americium'（疑似错答，人工 |
| 1593 | train | Under what name did Dr Brooke Magnanti write her blog about  | Belle du Jour | 'Dr Brooke.' | incorrect | gold 未命中 |
| 1594 | train | Who won the .1995 Best Actress Oscar for her role as Sister  | SUSAN SARANDON | 'Anne Hathaway won the 1995 Best Actress Oscar for ' | incorrect | gold 未命中 |
| 1595 | train | Jose Mourinho was appointed manager of which football club S | BENFICA | 'Porto.' | incorrect | 单 token 短答 'Porto.'（疑似错答，人工留意） |
| 1596 | train | "Who according to the Book of Genesis was described as ""A m | NIMROD | 'Cain' | incorrect | 单 token 短答 'Cain'（疑似错答，人工留意） |
| 1597 | train | What does the Greek word Mesopotamia mean? | Between two rivers | 'The Greek word "Mesopotamia" means "land between t' | incorrect | gold 未命中 |
| 1598 | test | in which century was St Bartholomew's Hospital located in We | 12th century | "St Bartholomew's Hospital was founded in the 12th " | correct | gold 命中（含等价/别名） |
| 1599 | train | Who was King of England in the year 1300? | Edward I | 'Edward I' | correct | gold 命中（含等价/别名） |
| 1600 | train | Which musical instrument is Albert Schweitzer known to have  | Organ | 'Albert Schweitzer is known to have played the pian' | incorrect | gold 未命中 |
| 1601 | test | In the acronym DEFRA, for what does the A stand? | Affairs | 'Agriculture' | incorrect | 单 token 短答 'Agriculture'（疑似错答， |
| 1602 | test | In an electrical circuit what is measured by a Wheatstone Br | Resistance | 'Resistance.' | correct | gold 命中（含等价/别名） |
| 1603 | train | In which country are the wine producing regions Huasco Valle | Chile | 'The Huasco Valley and Choapa Valley are wine-produ' | incorrect | gold 未命中 |
| 1604 | train | According to the rhyme, what is Wednesday’s child? | Full of woe | 'Thursday' | incorrect | 单 token 短答 'Thursday'（疑似错答，人工留 |
| 1605 | test | What sport do you associate with Francesco Molinari? | Golf | 'Francesco Molinari is an Italian professional foot' | incorrect | gold 未命中 |
| 1606 | train | jhe BBC2 production of Wolf Hal! was based on the novels by  | Bring Up the Bodies | 'Wolf Hall' | incorrect | gold 未命中 |
| 1607 | train | Who wrote the opera Faust in 1859? | Charles Gounod | 'Charles Gounod wrote the opera Faust in 1859.' | correct | gold 命中（含等价/别名） |
| 1608 | test | Who penned his own epitaph ‘Here lies one whose name was wri | John Keats | 'John Milton' | incorrect | gold 未命中 |
| 1609 | test | Which flower is also known as the Lent Lily? | Daffodil | 'The Easter Lily.' | incorrect | gold 未命中 |
| 1610 | validation | What is the name of me political party, led by Alexis Tsipra | SYRIZA | 'New Democracy' | incorrect | gold 未命中 |
| 1611 | train | Who was known as 'The Great One' in North American ice hocke | WAYNE GRETZKY | ' Bobby Orr.' | incorrect | gold 未命中 |
| 1612 | test | Oswald Cobblepot is a devious crime-boss who is seldom seen  | PENGUIN | 'Oswald Cobblepot is better known as the Penguin.' | correct | gold 命中（含等价/别名） |
| 1613 | train | Raphanus Sativus is the Latin name of what vegetable, which  | Radish | 'Raphanus Sativus is the Latin name of the vegetabl' | correct | gold 命中（含等价/别名） |
| 1614 | train | What nationality is former Liverpool FC footballer Jan Molby | Danish | 'Jan Molby is Danish.' | correct | gold 命中（含等价/别名） |
| 1615 | train | Who wrote the 20th century verse play Murder in the Cathedra | T S ELIOT | 'ylan Thomas.' | incorrect | gold 未命中 |
| 1616 | train | When hallmarking articles made of platinum, what pictorial m | AN ORB | 'P' | format_failure | 单 token 函数词/碎片 'P'，无答案内容 |
| 1617 | train | As SNCF is the French railway system, what are the initials  | DB | 'DB' | correct | gold 命中（含等价/别名） |
| 1618 | validation | Which British 2012 Olympic Gold medallist won two events at  | MO FARAH | 'Greg Rutherford' | incorrect | gold 未命中 |
| 1619 | test | What was the name of the flying island in Gulliver’s Travels | LAPUTA | "The name of the flying island in Gulliver's Travel" | incorrect | gold 未命中 |
| 1620 | test | Which US city began as a trading post on the Chisholm Trail  | WICHITA | 'ichita' | incorrect | 单 token 短答 'ichita'（疑似错答，人工留意） |
| 1621 | validation | In which war did the battles of Crecy and Poitiers take plac | HUNDRED YEARS WAR | 'The battles of Crecy and Poitiers took place durin' | correct | gold 命中（含等价/别名） |
| 1622 | test | Koh-I-Noor, as in the diamond, means what in English? | MOUNTAIN of LIGHT | 'Koh-I-Noor means "Mountain of Light" in English.' | correct | gold 命中（含等价/别名） |
| 1623 | validation | Of what does the usual base of a Florentine biscuit consist? | CHOCOLATE | 'The usual base of a Florentine biscuit consists of' | incorrect | gold 未命中 |
| 1624 | train | Actor John Hewer died early in 2008 aged 86; under what name | Captain Birdseye | 'Johnnie' | incorrect | 单 token 短答 'Johnnie'（疑似错答，人工留意 |
| 1625 | train | “Tis Herself’ published in 2005 was the autobiography of whi | MAUREEN O’HARA | 'Jennifer Aniston' | incorrect | gold 未命中 |
| 1626 | train | Which King of England is buried in Gloucester Cathedral? | EDWARD II | 'Edward III' | incorrect | gold 未命中 |
| 1627 | train | The storyline of which 1994 Disney animated film is based on | THE LION KING | 'Hercules' | incorrect | 单 token 短答 'Hercules'（疑似错答，人工留 |
| 1628 | validation | In which country is the Sierra Madre mountain range, with it | Mexico | 'The Sierra Madre mountain range, with its highest ' | correct | gold 命中（含等价/别名） |
| 1629 | validation | Canaletto is famous for his landscapes of Venice and which o | London | 'Rome.' | incorrect | 单 token 短答 'Rome.'（疑似错答，人工留意） |
| 1630 | validation | In which European city is Kurtfurstendamm the main shopping  | BERLIN | 'Kturfurstendamm is the main shopping street in Ber' | correct | gold 命中（含等价/别名） |
| 1631 | train | Harvard University is situated in which American State? | MASSACHUSETTS | 'Harvard University is situated in the American sta' | correct | gold 命中（含等价/别名） |
| 1632 | train | Which popular garden flower is the national flower of Mexico | THE DAHLIA | 'The national flower of Mexico is the Sunflower.' | incorrect | gold 未命中 |
| 1633 | train | Which illness caused Edward VII's coronation to be delayed b | APPENDICITIS | 'aryngitis.' | incorrect | 单 token 短答 'aryngitis.'（疑似错答，人 |
| 1634 | validation | Which piece of laboratory equipment consists of a vertical c | A BURETTE. | 'Pipette' | incorrect | 单 token 短答 'Pipette'（疑似错答，人工留意 |
| 1635 | validation | "Who produces the perfumes ""Opium"" and ""Rive Gauche""?" | Yves Saint Laurent | 'Lancô produces the perfumes "Opium" and "Rive Gauc' | incorrect | gold 未命中 |
| 1636 | test | Botswana was known by what name until 1966? | Bechuanaland | 'Bechuanaland' | correct | gold 命中（含等价/别名） |
| 1637 | train | What do the Americans call what we call a 'sofa'? | DAVENPORT | 'Couch.' | incorrect | 单 token 短答 'Couch.'（疑似错答，人工留意） |
| 1638 | train | In which English city is the HQ of the Ordnance Survey? | Southampton | 'London.' | incorrect | 单 token 短答 'London.'（疑似错答，人工留意 |
| 1639 | train | Which singer had a number 1 hit album in 2008 entitled 'Hard | Madonna | 'Britney Spears' | incorrect | gold 未命中 |
| 1640 | test | Which Irish politician was known as 'The Liberator'? | Daniel O'Connell | 'McConnell' | incorrect | 单 token 短答 'McConnell'（疑似错答，人工 |
| 1641 | validation | Which device, now a plaything, has a lift end, a dingle end  | Boomerang | 'A broom.' | incorrect | gold 未命中 |
| 1642 | validation | Which is the only property on a traditional UK Monopoly boar | OLD KENT ROAD | 'Mayfair' | incorrect | 单 token 短答 'Mayfair'（疑似错答，人工留意 |
| 1643 | validation | In the context of UK government, for what does the C stand i | Cabinet | 'Counter.' | incorrect | 单 token 短答 'Counter.'（疑似错答，人工留 |
| 1644 | train | Which island in the Grenadines of St. Vincent was bought by  | MUSTIQUE | 'Birds Island' | incorrect | gold 未命中 |
| 1645 | test | The Aran Islands are located at the mouth of which bay? | Galway Bay | 'The Aran Islands are located at the mouth of the B' | incorrect | gold 未命中 |
| 1646 | test | The former Queen Mother, Elizabeth Bowes-Lyon, married the D | Durham | 'Cornwall' | incorrect | 单 token 短答 'Cornwall'（疑似错答，人工留 |
| 1647 | train | Who wrote much of King George V's first Christmas broadcast, | Rudyard Kipling | 'Richard Greene.' | incorrect | gold 未命中 |
| 1648 | train | In terms of tonnage of cargo handled, which is the world's l | Rotterdam | 'Shanghai.' | incorrect | 单 token 短答 'Shanghai.'（疑似错答，人工 |
| 1649 | train | By what name was Peggy Hookham DBE better known? | Margot Fonteyn | 'Peggy Hookham DBE was better known as Peggy Sue.' | correct | gold 别名命中 |
| 1650 | train | General James Wolfe was killed at which battle in 1759? | Quebec | 'General James Wolfe was killed at the Battle of Qu' | correct | gold 命中（含等价/别名） |
| 1651 | train | What is the perfect score in ten pin bowling? | 300 | 'The perfect score in ten pin bowling is 300.' | correct | gold 命中（含等价/别名） |
| 1652 | train | Which Alpine peak is known in Italy as Monte Cervino? | The Matterhorn | 'Monte Cervino' | correct | gold 别名命中 |
| 1653 | test | What is the largest state in Brazil? | AMAZONAS | 'The largest state in Brazil is Pará.' | incorrect | gold 未命中 |
| 1654 | test | Which official residence is No.12 Downing Street? | GOVERNMENT CHIEF WHIP | 'No. 12 Downing Street is the official residence of' | incorrect | gold 未命中 |
| 1655 | train | In the Lake District which is the only body of water to actu | Bassenthwaite Lake | 'Lake District.' | incorrect | gold 未命中 |
| 1656 | train | What is the imperial distance of a marathon race? | 26 miles, 385 yards | 'The imperial distance of a marathon race is 26.219' | incorrect | gold 未命中 |
| 1657 | validation | What kind of aircraft gave the space shuttle a piggy-back pr | BOEING 747 | 'Airplane.' | incorrect | 单 token 短答 'Airplane.'（疑似错答，人工 |
| 1658 | test | As at November 2007, who is the Shadow Home Secretary? | David Davis | 'Michael Howard' | incorrect | gold 未命中 |
| 1659 | test | Aglaia, Thalia and. Euphrosyne were known as what? | THREE GRACES | 'Aglaia, Thalia, and Euphrosyne were known as the T' | correct | gold 命中（含等价/别名） |
| 1660 | train | What is the name for a female bear? | A sow | 'The name for a female bear is a sow.' | correct | gold 命中（含等价/别名） |
| 1661 | train | On which island in the North Sea did both St Aidan and St Cu | LINDISFARNE | 'Farne Island' | incorrect | gold 未命中 |
| 1662 | test | Who played the part of companion Martha Jones in the 2007 se | FREEMA AGYEMAN | 'William Piper.' | incorrect | gold 未命中 |
| 1663 | train | Which large American bird (Gymnogyps) has been reintroduced  | (California) Condor | 'The California Condor.' | correct | gold 命中（含等价/别名） |
| 1664 | train | Whose portrait (apart from the Queen) appeared on the now de | ISAAC NEWTON | 'Sir Winston Churchill' | incorrect | gold 未命中 |
| 1665 | train | By what name is the garden flowering plant hypericum commonl | ST JOHN'S WORT | 'Wort.' | incorrect | 单 token 短答 'Wort.'（疑似错答，人工留意） |
| 1666 | train | Which well known 1987 film, featured a character named Priva | FULL METAL JACKET | 'Top Gun.' | incorrect | gold 未命中 |
| 1667 | train | The 2010 Winter Olympics will be held where? | Vancouver | 'The 2010 Winter Olympics will be held in Vancouver' | correct | gold 命中（含等价/别名） |
| 1668 | train | The name of which Chinese dish translates as 'bits and piece | Chop Suey | 'Dim sum' | incorrect | gold 未命中 |
| 1669 | train | In GB Shaw's Major Barbara in which army was Barbara a major | SALVATION ARMY | 'British Army' | incorrect | gold 未命中 |
| 1670 | train | "The novel, ""Birdsong"", by Sebastian Faulks, is mainly set | WORLD WAR I | 'The novel "Birdsong" by Sebastian Faulks is mainly' | incorrect | gold 未命中 |
| 1671 | test | "What was the sequel to 'Tom Brown's Schooldays""?" | Tom Brown at Oxford | "The sequel to 'Tom Brown's Schooldays' is 'Tom Bro" | incorrect | gold 未命中 |
| 1672 | validation | Which British Prime Ministers death is commemorated on 19th  | Benjamin Disraeli | 'Winston Churchill' | incorrect | gold 未命中 |
| 1673 | test | "Which English comedian/actor said ""Girls are like pianos.  | Benny Hill | 'Stephen Fry.' | incorrect | gold 未命中 |
| 1674 | train | Who in 1476 brought his painting press from Bruges to London | WILLIAM CAXTON | ' Johannes Gutenberg' | incorrect | gold 未命中 |
| 1675 | test | Which American city has districts called Financial, Mission, | San Francisco | 'San Francisco' | correct | gold 命中（含等价/别名） |
| 1676 | train | Which river flows from northern Moscow to the Caspian Sea? | Volga | 'The Volga River flows from northern Moscow to the ' | correct | gold 命中（含等价/别名） |
| 1677 | train | Which actor was the fifth Doctor Who from 1982-1984, and in  | PETER DAVISON | 'Paul McGann' | incorrect | gold 未命中 |
| 1678 | test | Which post in England and Wales is held by Anne Owers? | (CHIEF) INSPECTOR OF PRI | 'Chief Justice.' | incorrect | gold 未命中 |
| 1679 | train | In what year was the Battle of Stamford Bridge? | 1066 | 'The Battle of Stamford Bridge took place in 1066.' | correct | gold 命中（含等价/别名） |
| 1680 | train | Born in 1947, James Jewel Osterberg is a rock/punk pop singe | Iggy Pop | 'Tom Petty' | incorrect | gold 未命中 |
| 1681 | validation | How many faces has an icosahedron? | 20 | 'An icosahedron has 20 faces.' | correct | gold 命中（含等价/别名） |
| 1682 | train | Which boxer was portrayed b Robert De Niro in the film 'Ragi | Jake La Motta | 'Robert De Niro portrayed the boxer Rocky Balboa in' | incorrect | gold 未命中 |
| 1683 | train | Which 20th Century U.S. President was a Peanut Farmer? | JIMMY CARTER | 'Jimmy Carter.' | correct | gold 命中（含等价/别名） |
| 1684 | train | In Greek mythology what was the name of the goatlike man wit | A SATYR | 'Cronus' | incorrect | 单 token 短答 'Cronus'（疑似错答，人工留意） |
| 1685 | train | The axilla is the anatomical name for which part of the body | Armpit | 'The axilla is the anatomical name for the arm pit.' | correct | gold 别名命中 |
| 1686 | train | Give any year in the life of the painter Raphael. | 1483-1520 | 'Raphael was born in 1483.' | incorrect | gold 未命中 |
| 1687 | test | In 2002, Chechen terrorists took more than 700 people as hos | Theatre | 'A theater.' | correct | gold 别名命中 |
| 1688 | train | What is the surname of the father and son who rode Grand Nat | Carberry | 'The surname of the father and son who rode Grand N' | incorrect | gold 未命中 |
| 1689 | train | At which school was Billy Bunter a pupil | GREYFRIARS | 'Billy Bunter was a pupil at Watford Grammar School' | incorrect | gold 未命中 |
| 1690 | train | The two wives of King John of England shared which forename? | Isabella | 'Margaret' | incorrect | 单 token 短答 'Margaret'（疑似错答，人工留 |
| 1691 | train | "Give the name of the character played by James Stewart in t | George Bailey | 'George Bailey.' | correct | gold 命中（含等价/别名） |
| 1692 | train | In January 2010, who became the first mother to win the Aust | Kim Clijsters | ' Serena Williams.' | incorrect | gold 未命中 |
| 1693 | validation | "Who created the fictional character ""Tilly Trotter'?" | Catherine Cookson | 'Tilly Trotter was created by author Jacqueline Wil' | correct | gold 别名命中 |
| 1694 | train | Which UK international airport has the code PIK? | Prestwick | ' Gatwick Airport' | incorrect | gold 未命中 |
| 1695 | test | Who judged Aphrodite more beautiful than Hera or Athena? | Paris | 'Athena' | incorrect | 单 token 短答 'Athena'（疑似错答，人工留意） |
| 1696 | test | What was the name of the second wife of Johnny Cash, who he  | June Carter | 'Janene Carter' | incorrect | gold 未命中 |
| 1697 | train | KHI is the international code for which Asian airport? | Karachi | 'KHI is the international code for Hiro Internation' | incorrect | gold 未命中 |
| 1698 | train | In 1842, what was ceded to Britain by the Treaty of Nanking? | HONG KONG | 'Hong Kong.' | correct | gold 命中（含等价/别名） |
| 1699 | test | Hawley Harvey were the first names of which criminal? | Dr. Crippen | 'Hawley and Harvey were the first names of the crim' | incorrect | gold 未命中 |
| 1700 | train | If the Staten Island Ferry is to New York, the Star Ferry th | Hong Kong | 'Hong Kong' | correct | gold 命中（含等价/别名） |
| 1701 | train | Which city in Egypt has been characterised as the 'world's g | Luxor | 'The city in Egypt that has been characterized as t' | correct | gold 命中（含等价/别名） |
| 1702 | train | The Battle of Kadesh in 1274 BC that took place between the  | Chariots | 'The Battle of Kadesh in 1274 BC is best known for ' | correct | gold 命中（含等价/别名） |
| 1703 | train | A fictional species of great apes called 'Mangani' are respo | Tarzan | 'Tarzan' | correct | gold 命中（含等价/别名） |
| 1704 | train | The Miller-Urey experiment conducted in 1953 that simulated  | Chemical origins of life | 'The Miller-Urey experiment aimed to investigate th' | incorrect | gold 未命中 |
| 1705 | train | "The name of what tennis star was used by a commentator for  | Anna Kournikova | 'Andre Agassi' | incorrect | gold 未命中 |
| 1706 | train | What American city has suffered two (separate) outcomes of w | Cleveland | 'Detroit.' | incorrect | 单 token 短答 'Detroit.'（疑似错答，人工留 |
| 1707 | validation | What type of 'helpful' businesses operate on the basis of th | Co-operatives | 'Co-operatives' | correct | gold 命中（含等价/别名） |
| 1708 | train | A tourist attraction near Alliance, Nebraska created by Jim  | Stonehenge | 'The Lincoln Memorial.' | incorrect | gold 未命中 |
| 1709 | train | What 2009 hit that rewarded a woman director opens with the  | The Hurt Locker | 'The 2009 hit that rewarded a woman director opens ' | incorrect | gold 未命中 |
| 1710 | validation | Mammy Two Shoes, a recurring character in MGM's Tom and Jerr | Hattie McDaniel | 'Fay Williams' | incorrect | gold 未命中 |
| 1711 | train | What is the second-largest day for U.S. food consumption, af | Super Bowl Sunday | 'The second-largest day for U.S. food consumption, ' | incorrect | gold 未命中 |
| 1712 | train | Which crop that was of great nutritional importance in pre-C | Quinoa | 'Quinoa' | correct | gold 命中（含等价/别名） |
| 1713 | train | Used to describe US citizens who attempted to foment insurre | Filibuster | 'filibuster' | correct | gold 命中（含等价/别名） |
| 1714 | train | In 1914 a paleontologist suggested that what legend might ha | Cyclops | 'In 1914, a paleontologist suggested that the legen' | incorrect | gold 未命中 |
| 1715 | validation | After USA, what is the largest country in the world named af | Saudi Arabia | 'Canada' | incorrect | 单 token 短答 'Canada'（疑似错答，人工留意） |
| 1716 | train | Beloved in 1999 was whose first movie since The Color Purple | Oprah Winfrey | 'Toni Morrison' | incorrect | gold 未命中 |
| 1717 | train | Which sitcom star appeared on the big screening The Object o | Jennifer Aniston | 'Matthew Perry.' | incorrect | gold 未命中 |
| 1718 | train | Nigel Hawthorne was Oscar nominated for The Madness of which | George | 'George III' | correct | gold 命中（含等价/别名） |
| 1719 | train | Which Oscar-nominated film had You Sexy Thing as its theme s | The Full Monty | 'Dirty Dancing' | incorrect | gold 未命中 |
| 1720 | train | Who was the male star of the movie The Man of La Mancha? | Peter O'Toole | 'The male star of the movie The Man of La Mancha wa' | incorrect | gold 未命中 |
| 1721 | test | Which sports event was first held at Worcester, Massachusett | Ryder Cup | 'The Boston Marathon.' | incorrect | gold 未命中 |
| 1722 | train | In which European city is the Belvederen Gallery? | Vienna | 'The Belvederen Gallery is located in Amsterdam, Ne' | incorrect | gold 未命中 |
| 1723 | train | Who's home runs record did Mark McGwire break in the 1998 se | Roger Maris | "Mark McGwire broke Hank Aaron's home run record in" | incorrect | gold 未命中 |
| 1724 | train | Which future Hollywood star got her break as Wonder Girl, Wo | Debra Winger | 'Barbara Eden.' | incorrect | gold 未命中 |
| 1725 | train | In Hanna and Barbera's TV cartoons base on The Addams Family | John Astin | 'Barbara Goodson' | incorrect | gold 未命中 |
| 1726 | train | Which grand slam did Pete Sampras not win in the 20th centur | French | 'Pete Sampras did not win the Australian Open in th' | incorrect | gold 未命中 |
| 1727 | train | Which European town gave its name to a Treaty which symboliz | Maastricht | 'The European town that gave its name to the Treaty' | incorrect | gold 未命中 |
| 1728 | train | Which home of champagne in France was also where the German  | Reims | 'Reims.' | correct | gold 命中（含等价/别名） |
| 1729 | train | What color golf balls are used on the golf course in Antarct | Orange | 'White' | incorrect | 单 token 短答 'White'（疑似错答，人工留意） |
| 1730 | train | "Who said, To err is human but it feels divine?""" | Mae West | 'Alexander Pope' | incorrect | gold 未命中 |
| 1731 | train | In WWII, who was the head of the Nazi party's security servi | Reinhard Heidrich | 'Heinzrich.' | incorrect | 单 token 短答 'Heinzrich.'（疑似错答，人 |
| 1732 | train | In what year was the first in-flight movie shown on an inter | 1929 | '1952' | incorrect | 单 token 短答 '1952'（疑似错答，人工留意） |
| 1733 | train | In which city was John Lennon murdered? | New York | 'John Lennon was murdered in New York City.' | correct | gold 命中（含等价/别名） |
| 1734 | train | How was President Kennedy assassinated? | Shot | 'President John F. Kennedy was assassinated by a bu' | incorrect | gold 未命中 |
| 1735 | train | Of which African country is Niamey the capital? | Niger | 'Niamey is the capital of Niger.' | correct | gold 命中（含等价/别名） |
| 1736 | train | Which Syrian city is said to be the oldest continually inhab | Damascus | 'Aleppo' | incorrect | 单 token 短答 'Aleppo'（疑似错答，人工留意） |
| 1737 | train | Which wife of Henry VIII had already married twice before sh | Catherine Parr | 'Jane Seymour' | incorrect | gold 未命中 |
| 1738 | test | Which builder of steam engines formed a successful partnersh | James Watt | 'James Watt' | correct | gold 命中（含等价/别名） |
| 1739 | validation | What is the name of the strong material found in plant cell  | Cellulose | 'Cellulose.' | correct | gold 命中（含等价/别名） |
| 1740 | train | What is the most abundant substance in the plant kingdom, wh | Cellulose | 'The most abundant substance in the plant kingdom t' | correct | gold 命中（含等价/别名） |
| 1741 | train | What has a central vein called a midrib? | Leaf | 'Leaves have a central vein called a midrib.' | correct | gold 别名命中 |
| 1742 | train | Which 90s sci fi series with James Belushi was based on Bruc | Wild Palms | 'The Tick' | incorrect | gold 未命中 |
| 1743 | train | What is the Milky Way? | The local galaxy | 'The Milky Way is a galaxy.' | correct | gold 别名命中 |
| 1744 | test | If I Were A Rich Man Was a big hit from which stage show? | Fiddler on the Roof | 'If I Were A Rich Man was a big hit from the stage ' | incorrect | gold 未命中 |
| 1745 | train | Kagoshima international airport is in which country? | Japan | 'Kagoshima International Airport is in Japan.' | correct | gold 命中（含等价/别名） |
| 1746 | train | Kim Carnes' nine weeks at No 1 with Bette Davis Eyes was int | Stars on 45 medley | 'Private Eyes' | incorrect | gold 未命中 |
| 1747 | train | Which musician founded the Red Hot Peppers? | Jelly Roll Morton | 'Flea.' | incorrect | 单 token 短答 'Flea.'（疑似错答，人工留意） |
| 1748 | train | Who was the first US-born winner of golf's British Open? | Walter Hagen | ' Arnold Palmer.' | incorrect | gold 未命中 |
| 1749 | train | Who was the youngest brother in the Beach Boys? | Carl Wilson | 'Dennis Wilson' | incorrect | gold 未命中 |
| 1750 | train | Who first hosted Family Feud? | Richard Dawson | 'Bob Stewart.' | incorrect | gold 未命中 |
| 1751 | train | What did the Lone Ranger's title Kemo Sabe mean in Apache? | White Shirt | 'I know.' | incorrect | gold 未命中 |
| 1752 | test | The Nazi regime was Germany's Third Reich; which was the fir | HOLY ROMAN EMPIRE | 'The first Reich was the German Empire.' | correct | gold 别名命中 |
| 1753 | train | Which county won the County Cricket Championship in 1959, af | YORKSHIRE | 'Essex' | incorrect | 单 token 短答 'Essex'（疑似错答，人工留意） |
| 1754 | test | The magic lantern was an early form of what item of photogra | SLIDE PROJECTOR | 'Projector.' | incorrect | 单 token 短答 'Projector.'（疑似错答，人 |
| 1755 | train | What was the name of the USAAF B-17 Flying Fortress whose ai | MEMPHIS BELLE | 'The name of the USAAF B-17 Flying Fortress whose a' | incorrect | gold 未命中 |
| 1756 | test | Although not the state capital, which is the largest city in | OMAHA | 'Omaha' | correct | gold 命中（含等价/别名） |
| 1757 | train | In which Lake District town would you find the Cumberland Pe | KESWICK | 'The Cumberland Pencil Museum is located in the Lak' | incorrect | gold 未命中 |
| 1758 | train | Created in 1952, which is Britain's only coastal National Pa | PEMBROKESHIRE COAST NATI | 'Norfolk Coast National Park' | incorrect | gold 未命中 |
| 1759 | train | Who directed the Noughties films One Day in September, The L | KEVIN MACDONALD | 'David Lynch.' | incorrect | gold 未命中 |
| 1760 | train | """Because I'm worth it"" was the advertising slogan for whi | L'OREAL | 'Pepsi' | incorrect | 单 token 短答 'Pepsi'（疑似错答，人工留意） |
| 1761 | test | Traditionally served in a tall glass, what name is given to  | KNICKERBOCKER GLORY | 'Fruit Tart.' | incorrect | gold 未命中 |
| 1762 | train | "What was the name of the Jester in Shakespeare's ""As You L | TOUCHSTONE | 'Jaques' | incorrect | 单 token 短答 'Jaques'（疑似错答，人工留意） |
| 1763 | train | "Which famous western movie ends with the line :- ""Oh good, | BUTCH CASSIDY AND THE SU | 'The famous western movie that ends with the line "' | incorrect | gold 未命中 |
| 1764 | validation | Near which village in North Wales were the rowing events hel | LLANBERIS | 'Bangor.' | incorrect | 单 token 短答 'Bangor.'（疑似错答，人工留意 |
| 1765 | train | "In Italy, if you were served ""Mortadella"", what foodstuff | SAUSAGE | 'Sausage.' | correct | gold 命中（含等价/别名） |
| 1766 | train | A Lemur is a small primate found only on which island? | MADAGASCAR | 'Madagascar' | correct | gold 命中（含等价/别名） |
| 1767 | train | Formula 1 - On which racetrack was the World Champion Ayrton | IMOLA | 'Ayrton Senna was killed at the Brazilian Grand Pri' | incorrect | gold 未命中 |
| 1768 | test | Which famous sporting figure was the subject of attention by | STEVEN GERARD | 'David Beckham' | incorrect | gold 未命中 |
| 1769 | validation | Which British band reached number one in the UK pop charts i | POLICE | 'U2' | format_failure | 单 token 函数词/碎片 'U2'，无答案内容 |
| 1770 | test | Ridden by jockey Brian Fletcher, which horse won the 1968 Gr | RED ALLIGATOR | 'Citation.' | incorrect | 单 token 短答 'Citation.'（疑似错答，人工 |
| 1771 | train | Alternatively known as Austrpphlebia Costalis, what type of  | DRAGONFLY | 'The Southern Giant Darner is a type of dragonfly.' | correct | gold 命中（含等价/别名） |
| 1772 | train | Which political party, founded in 1967, has its headquarters | NATIONAL FRONT | 'Labour Party' | incorrect | gold 未命中 |
| 1773 | test | Darwin is the capital of which Australian state ? | NORTHERN TERRITORY | 'Darwin is the capital of the Australian state of N' | correct | gold 命中（含等价/别名） |
| 1774 | train | What is the largest island in the Mediterrainean Sea? | SICILY | 'The largest island in the Mediterranean Sea is Sic' | correct | gold 命中（含等价/别名） |
| 1775 | validation | Which film of 1988 sees the lead male character, named Dan G | FATAL ATTRACTION | 'The film of 1988 where the lead male character, na' | incorrect | gold 未命中 |
| 1776 | train | Which tennis player played in three consecutive men's single | FRED STOLLE | 'Rod Laver' | incorrect | gold 未命中 |
| 1777 | train | Ailurophobia is the abnormal fear of what? | CATS | 'Ailurophobia is the abnormal fear of cats.' | correct | gold 命中（含等价/别名） |
| 1778 | validation | Which German word meaning 'armour' was applied to certain ar | PANZER | 'Panzer' | correct | gold 命中（含等价/别名） |
| 1779 | test | Name the town in the vicinity of Versailles famous for its h | SEVRES | 'Chantilly' | incorrect | 单 token 短答 'Chantilly'（疑似错答，人工 |
| 1780 | train | In which part of the human body can you find the Malleus or  | THE EAR | 'The Malleus or Hammer bone is found in the middle ' | incorrect | gold 未命中 |
| 1781 | train | In Indian cookery, dishes known as 'tandoori' are so named b | AN OVEN | 'A tandoor is a type of clay oven used in Indian co' | correct | gold 别名命中 |
| 1782 | train | What is the name of the island that separates the two larges | GOAT ISLAND | 'Niagara Island' | incorrect | gold 未命中 |
| 1783 | train | Some Americans claim to have seen a Sasquatch; by what name  | BIGFOOT | 'The Sasquatch is better known as the Bigfoot.' | correct | gold 命中（含等价/别名） |
| 1784 | train | What was the surname of the 19th president of the USA who ha | HAYES | 'The surname of the 19th president of the USA is Wi' | incorrect | gold 未命中 |
| 1785 | train | Which two word named plant, also known as Dionaea Muscipala  | VENUS FLYTRAP | 'The two-word named plant, also known as Dionaea Mu' | correct | gold 命中（含等价/别名） |
| 1786 | train | Which is the most southerly Irish city ? | CORK | 'Cork' | correct | gold 命中（含等价/别名） |
| 1787 | train | In which year was the ten shilling note withdrawn in the UK  | 1970 | 'The ten shilling note was withdrawn in the UK in 1' | incorrect | gold 未命中 |
| 1788 | validation | What nationality was the pointillist artist MONDRIAN? | DUTCH | 'French' | incorrect | 单 token 短答 'French'（疑似错答，人工留意） |
| 1789 | test | Who was the first Republican President of the United States  | ABRAHAM LINCOLN | 'The first Republican President of the United State' | correct | gold 命中（含等价/别名） |
| 1790 | test | Which national anthem was originally called the 'War Song fo | MARSELLAISE | 'The German national anthem was originally called t' | incorrect | gold 未命中 |
| 1791 | train | "The opera ""Duke Bluebeard's Castle"" and the ballet ""The  | BARTOK | ' Maurice Ravel.' | incorrect | gold 未命中 |
| 1792 | validation | Which superhero film, produced by Marvel Studios and written | THE AVENGERS | 'The Avengers' | correct | gold 命中（含等价/别名） |
| 1793 | validation | Which Italian liqueur is a key ingredient of the well known  | GALLIANO | 'Chartreuse' | incorrect | 单 token 短答 'Chartreuse'（疑似错答，人 |
| 1794 | test | Which rider won the ladies European Three Day event Champion | PRINCESS ANNE | 'Mary Moody.' | incorrect | gold 未命中 |
| 1795 | validation | "Which product was promoted with the slogan ""Full of Easter | FRY'S TURKISH DELIGHT | 'Milk' | incorrect | 单 token 短答 'Milk'（疑似错答，人工留意） |
| 1796 | train | Which opera by Borodin features the Polovtsian Dances? | PRINCE IGOR | 'The Igor.' | incorrect | gold 未命中 |
| 1797 | validation | What was the name of the British teacher jailed in Sudan in  | GILLIAN GIBBONS | 'Janeani.' | incorrect | 单 token 短答 'Janeani.'（疑似错答，人工留 |
| 1798 | train | Which city in Saxony was known as Karl-Marx-Stadt from 1953  | CHEMNITZ | 'Leipzig' | incorrect | 单 token 短答 'Leipzig'（疑似错答，人工留意 |
| 1799 | train | David Tyler is the current chairman of which leading superma | SAINSBURY'S | 'Asda' | incorrect | 单 token 短答 'Asda'（疑似错答，人工留意） |
| 1800 | train | "Which snooker player had the nickname ""The Thunder from Do | NEIL ROBERTSON | 'Steve Davis' | incorrect | gold 未命中 |
