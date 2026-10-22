# 签核复核表（draft，human_reviewed=false）

规则：`src/signoff_rule.py`（已对 pilot200 400/400 复现）；题单：`data/raw_qa/subsets/pool2000_v1.jsonl`

## dream（1800 条；correct 521）

| # | split | question | gold | prediction | 判定 | 说明 |
|---|---|---|---|---|---|---|
| 1 | validation | What is the name of Bruce Willis's character in Unbreakable? | David Dunn | 'David Dunn' | correct | gold 命中（含等价/别名） |
| 2 | test | Which "Blackzilians" fighter is currently competing in the M | Vitor Belfort | 'Alex Costa' | incorrect | gold 未命中 |
| 3 | test | Drisheen is what type of product made in Ireland and other p | Black pudding | 'food' | incorrect | 单 token 短答 'food'（疑似错答，人工留意） |
| 4 | test | What heritage site, known for a British explorer, is listed  | Captain Cook's Landing P | 'James Cook' | incorrect | gold 未命中 |
| 5 | train | Kevin Wayne Durant was named what ?(An Award initiated follo | The National Basketball  | 'NBA Most MVP' | incorrect | gold 未命中 |
| 6 | test | Seal Harris was born in what county? | Polk County | 'H County' | incorrect | gold 未命中 |
| 7 | train | When was the king that started coin production in Copenhagen | 2 February 1455 | '1533' | incorrect | 单 token 短答 '1533'（疑似错答，人工留意） |
| 8 | train | How many people live in the County serviced by The Collier A | 321,520 | '100,000' | incorrect | gold 未命中 |
| 9 | test | The creator of "Wallace and Gromit" also created what animat | Creature Comforts | 'Homeoo' | incorrect | 单 token 短答 'Homeoo'（疑似错答，人工留意） |
| 10 | train | Who was the architect of a Dutch museum dedicated to the art | Petrus Josephus Hubertus | 'Mies van' | incorrect | gold 未命中 |
| 11 | train | What Finnish Christmas figure, which eventually become more  | The Yule goat | 'Joulas' | incorrect | 单 token 短答 'Joulas'（疑似错答，人工留意） |
| 12 | test | Who is the son of the author of the short story "The Enormou | Benjamin Hale Cheever | 'John King' | incorrect | gold 未命中 |
| 13 | train | What airline holding company located in Solna Municipality,  | SAS Group | 'Sw Airlines' | incorrect | gold 未命中 |
| 14 | train | Which of Kylian Hazard's older brothers plays for the German | Thorgan Ganael Francis H | 'Eden Hazard' | incorrect | gold 未命中 |
| 15 | train | What is the character's name for which Anna Leonidovna Koval | Chief Detective Maria Sh | 'Anna' | incorrect | 单 token 短答 'Anna'（疑似错答，人工留意） |
| 16 | test | Who was born first, Samantha Cristoforetti or Jean-Loup Chré | Jean-Loup Jacques Marie  | 'Jean-Loup Chrétien' | incorrect | gold 未命中 |
| 17 | validation | Indie studio Jumpship developed what puzzle-platform video g | Limbo | 'B' | format_failure | 单 token 函数词/碎片 'B'，无答案内容 |
| 18 | test | Which star of Zork was also the voice of Pac-Man? | Martin Ingerman | 'Don West' | incorrect | gold 未命中 |
| 19 | train | Which football club appeared in the 2015 FA Community Shield | Chelsea | 'Manchester City' | incorrect | gold 未命中 |
| 20 | test | Who was convicted of murdering the director of Schoolboy Cru | Harlow Cuadra and Joseph | 'John Smith' | incorrect | gold 未命中 |
| 21 | train | What is the birth name of the woman that "A Woman Called Mos | Araminta Ross | 'Mary Moses' | incorrect | gold 未命中 |
| 22 | train | Which player signed to Bayern Munich before the 2012-2013 se | Dante | 'Davidm' | incorrect | 单 token 短答 'Davidm'（疑似错答，人工留意） |
| 23 | validation | The large subunit and small subunit that use two types of RN | Ribosomes | 'ribosome' | incorrect | 单 token 短答 'ribosome'（疑似错答，人工留 |
| 24 | test | Piers Bizony has written articles for which magazine based i | BBC Focus | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 25 | train | Gaia is a space observatory of the European Space Agency, wh | India's first dedicated  | 'Astrosat is an Indian space observatory' | incorrect | gold 未命中 |
| 26 | train | What type of bank organization is Pondicherry Gramin Bank th | Regional Rural Bank | 'Pondicherry Gramin Bank is a cooperative bank.' | incorrect | gold 未命中 |
| 27 | train | When the two Coldplay songs U.F.O and Princess of China were | was written by all four  | 'same' | incorrect | 单 token 短答 'same'（疑似错答，人工留意） |
| 28 | test | Thomas Henry Moray Followed work down on nuclear batteries i | Henry Moseley | 'Lord Tesla' | incorrect | gold 未命中 |
| 29 | test | Lady Elizabeth Delmé and Her Children (1779) is a portrait g | Washington, D.C. | 'DC' | format_failure | 单 token 函数词/碎片 'DC'，无答案内容 |
| 30 | test | Fantasy Records is know for recordings of comedian Lenny Bru | Vincent Anthony Guaraldi | 'Charles Mingus' | incorrect | gold 未命中 |
| 31 | train | In which city are Anadoluhisarı and Church of St. Mary of Bl | Istanbul | 'Anadoluhisarı and Church of St. Mary of Blachernae' | correct | gold 命中（含等价/别名） |
| 32 | train | Was Atom Egoyans biggest commercial success on stage or on f | erotic thriller film | 'Film' | incorrect | 单 token 短答 'Film'（疑似错答，人工留意） |
| 33 | validation | What country is home to both Guadarrama National Park and Do | Spain | 'Spain' | correct | gold 命中（含等价/别名） |
| 34 | train | Mount Austin Barracks is located near the Peak Tram terminus | Victoria Peak | 'Peak Peak' | incorrect | gold 未命中 |
| 35 | train | Alex Haley wrote what novel about a man that was born in 175 | Roots: The Saga of an Am | 'Roots' | incorrect | 单 token 短答 'Roots'（疑似错答，人工留意） |
| 36 | train | What actress starred in "The Golden Girls" and was an animal | Bea Arthur | 'Jane Arthur' | incorrect | gold 未命中 |
| 37 | test | What company claims to manufacture one out of every three ob | Crown Holdings Incorpora | 'General' | incorrect | 单 token 短答 'General'（疑似错答，人工留意 |
| 38 | train | After coaching the red raiders to several winning seasons, w | Washington State | 'Washington State University' | correct | gold 命中（含等价/别名） |
| 39 | test | What song was created by the group consisting of Jeffrey Jey | Blue | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 40 | validation | Who was the husband of the prominent Walton family member wh | Sam Walton | 'John Walton' | incorrect | gold 未命中 |
| 41 | train | BOTH Skyang Kangri and Pumari Chhish are both what? | subrange of the Karakora | 'mountains' | incorrect | 单 token 短答 'mountains'（疑似错答，人工 |
| 42 | validation | W. Tresper Clarke High School is in what county? | Nassau County | 'Mar County' | incorrect | gold 未命中 |
| 43 | validation | How many members does the Tennessee Volunteers football team | fourteen members | '14' | format_failure | 单 token 函数词/碎片 '14'，无答案内容 |
| 44 | test | What retailer in ABQ Uptown is headquarted in Poole, Dorset, | Lush Ltd. | 'Hark' | incorrect | 单 token 短答 'Hark'（疑似错答，人工留意） |
| 45 | validation | When was the father of Princess Mafalda of Savoy born ? | 11 November 1869 | '1936' | incorrect | 单 token 短答 '1936'（疑似错答，人工留意） |
| 46 | train | What Russian ballet choreographer restaged a play based on a | Alexander Gorsky | 'Alexander Fokine' | incorrect | gold 未命中 |
| 47 | train | Which 1962 film starring Tom Courtenay is based on a short s | The Loneliness of the Lo | 'The Long Man' | incorrect | gold 未命中 |
| 48 | test | What is the title of the person who is Head of the Departmen | Doctor | 'Professor' | incorrect | 单 token 短答 'Professor'（疑似错答，人工 |
| 49 | train | What Hindi thriller directed by Deepak SHivdasani features c | Julie 2 | 'K' | format_failure | 单 token 函数词/碎片 'K'，无答案内容 |
| 50 | test | Július Satinský was born in a city that has a current popula | about 450,000 | '1 million' | incorrect | gold 未命中 |
| 51 | train | The Northern Chamber Orchestra gives concerts at what estate | Tatton Park | 'Bham Castle' | incorrect | gold 未命中 |
| 52 | train | What league, which is also known as the Barclays Premier Lea | The 2013–14 Premier Leag | 'the Barclays Premier League' | format_failure | 输出为问句回显，无答案内容 |
| 53 | test | Which team's 2013-2014 season had players including a Sloven | the Phoenix Suns | 'Chicago Heat' | incorrect | gold 未命中 |
| 54 | test | Robert Jan van Pelt testified for the defense in this "Churc | David Irving | 'David Churchill' | incorrect | gold 未命中 |
| 55 | train | What indigenous American ethnic group that inhabits land in  | Odawa | 'Choux' | incorrect | 单 token 短答 'Choux'（疑似错答，人工留意） |
| 56 | test | Which actress played a character that dated Mark Brendanawic | Rashida Jones | 'Erin Davis' | incorrect | gold 未命中 |
| 57 | train | Alfred Balk served as the secretary of the Committee on the  | Nelson Rockefeller | 'Richard Nixon' | incorrect | gold 未命中 |
| 58 | train | Was the famous opera comique that was based on a Prosper Mer | "Carmen", perhaps the mo | 'comedy' | incorrect | 单 token 短答 'comedy'（疑似错答，人工留意） |
| 59 | train | Which American spy thriller TV series, which was developed b | Homeland | 'Homeland' | correct | gold 命中（含等价/别名） |
| 60 | train | The Stone Book series is set in what country? | North West England | 'I' | format_failure | 单 token 函数词/碎片 'I'，无答案内容 |
| 61 | train | What else was Baghdad known as during the Abbasid Caliphate? | the City of Peace | 'Bag' | incorrect | 单 token 短答 'Bag'（疑似错答，人工留意） |
| 62 | train | Who was born in Ireland and has coached the captain of MLS c | Des McAleenan | 'John Arena' | incorrect | gold 未命中 |
| 63 | test | Kate Ashfield plays what role in the 2004 British horror com | Liz | 'J' | format_failure | 单 token 函数词/碎片 'J'，无答案内容 |
| 64 | train | What actor from Northern Ireland born in 1983 starred in Who | Martin "Marty" McCann | 'James James' | incorrect | gold 未命中 |
| 65 | validation | What is the name of a Sri Lankan political party associated  | The Sri Lanka Freedom Pa | 'United National Party' | incorrect | gold 未命中 |
| 66 | train | What is the name of the English poet who wrote a poem titled | Lord Byron | 'George Gordon Byron' | incorrect | gold 未命中 |
| 67 | validation | What is the mascot of the oldest private university in Georg | The Bears | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 68 | train | What race track in the midwest hosts a 500 mile race eavery  | Indianapolis Motor Speed | 'Indianapolis Motor Speedway' | correct | gold 命中（含等价/别名） |
| 69 | train | What former two-weight world champion is represented by boxi | Tomasz Adamek | 'Mike Taylor' | incorrect | gold 未命中 |
| 70 | train | What 1991 Disney film is also a 1946 French romantic fantasy | Beauty and the Beast | 'The Little Mermaid' | incorrect | gold 未命中 |
| 71 | train | St Anne's Academy is an 11–18 mixed comprehensive academy is | 42,972 | '10,000' | incorrect | gold 未命中 |
| 72 | train | Which jazz singer has a 2003 album entitled The Boy Next Doo | Stacey Kent | 'John G' | incorrect | gold 未命中 |
| 73 | train | What is the species of animal which the town of Antelope, Ka | Antilocapra americana | 'antelope' | incorrect | 单 token 短答 'antelope'（疑似错答，人工留 |
| 74 | train | Which band formed in England, Of Montreal or Vib Gyor? | Vib Gyor was a band that | 'Of Montreal' | incorrect | gold 未命中 |
| 75 | train | What is the birthplace of the musician responsible for creat | Tennessee | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 76 | train | What scientist as well as a practising Roman Cathloic descri | Konstantīns Raudive | 'Ed Brown' | incorrect | gold 未命中 |
| 77 | test | Which group did Masta Kill released Selling My Soul under? | Wu-Tang Clan | 'Public' | incorrect | 单 token 短答 'Public'（疑似错答，人工留意） |
| 78 | test | Jacques Coghen is a direct ancestor to the spouse of which B | Queen Mathilde | 'Queenatrix' | incorrect | 单 token 短答 'Queenatrix'（疑似错答，人 |
| 79 | test | The channel that has interviewed players such as the forward | YouTube | 'YouTube' | correct | gold 命中（含等价/别名） |
| 80 | train | Between two scientists Ernst Messerschmid and Philippe Perri | Ernst Willi Messerschmid | 'Ernst Messerschmid' | incorrect | gold 未命中 |
| 81 | train | Orange is the New Black, starring Annie Golden as Norma Roma | FCI Danbury | 'Federal' | incorrect | 单 token 短答 'Federal'（疑似错答，人工留意 |
| 82 | test | What is the birthday of the oldest among Vicente García and  | March 30, 1983 | '10 August 1952' | incorrect | gold 未命中 |
| 83 | train | What military formation were participated in by both Oscar W | Third Army | 'World War I' | incorrect | gold 未命中 |
| 84 | train | What is the country of origin of the film Dui Purush and the | Bengali | 'India' | incorrect | 单 token 短答 'India'（疑似错答，人工留意） |
| 85 | test | What age was Georgia Middleman when she started singing in t | ten | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 86 | validation | Former race car driver Jeff Wood made his CART debut at whic | Caesars Palace Grand Pri | 'Indianapolis' | incorrect | 单 token 短答 'Indianapolis'（疑似错答 |
| 87 | test | The Church at Hoxne was dedicated to Edmund the Martyr who w | king of East Anglia | 'England' | incorrect | 单 token 短答 'England'（疑似错答，人工留意 |
| 88 | train | Which two occupations does Ronnie Dunn and Annie Lennox have | singer, songwriter | 'singers' | incorrect | 单 token 短答 'singers'（疑似错答，人工留意 |
| 89 | validation | This man who was born on April 25th, 1947, was a member of t | Robert "Bobby" Bunda | 'House House' | incorrect | gold 未命中 |
| 90 | train | Who was the final champion of the Thailand Masters that was  | Marco Fu | 'Michael Chau' | incorrect | gold 未命中 |
| 91 | train | In what California city was the first Torrid location opened | Brea, California | 'Los Angeles' | incorrect | gold 未命中 |
| 92 | train | In what part of Scotland is Bass Rock located? | the Firth of Forth in th | 'Edinburgh' | incorrect | 单 token 短答 'Edinburgh'（疑似错答，人工 |
| 93 | validation | Bobby Bowden coached which former Toronto Blue Jays minor le | Chris Weinke | 'John Johnson' | incorrect | gold 未命中 |
| 94 | train | New Jersey politicians Linda Stender and Leonard Lance were  | 1952 | '1940' | incorrect | 单 token 短答 '1940'（疑似错答，人工留意） |
| 95 | train | What Danish eurodance group had a single called "Barbie Girl | Aqua | 'Aqua' | correct | gold 命中（含等价/别名） |
| 96 | train | How many times has the driver who placed third in the 2003 I | 11 | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 97 | train | Which of the starting pitchers for Team USA in the Baseball  | Ben Sheets | 'Mike' | incorrect | 单 token 短答 'Mike'（疑似错答，人工留意） |
| 98 | validation | When did Henrietta Ponsonby's father die? | 31 October 1783 | "Henrietta Ponsonby's father died in 1790." | incorrect | gold 未命中 |
| 99 | train | The Swallow Bluff Island Mounds is a Mississippian culture a | the Cherokee River | 'Missoto River' | incorrect | gold 未命中 |
| 100 | train | What is the birthday of the author of "She Walks These Hills | February 26, 1948 | 'June 6, 1925' | incorrect | gold 未命中 |
| 101 | train | What is the river that Sangin is found in the valley of the  | Sistan Basin | 'Sangin River' | incorrect | gold 未命中 |
| 102 | train | Which Arab World's car was used in a American action film di | Lykan Hypersport | 'F' | format_failure | 单 token 函数词/碎片 'F'，无答案内容 |
| 103 | train | What type of media do Peter Filkins and The New Criterion ha | journal | 'Print' | incorrect | 单 token 短答 'Print'（疑似错答，人工留意） |
| 104 | train | WHAT WAS THE NAME OF THE BOOK MADE INTO THE 2015 SOUTH KOREA | "Murder Request" | 'The Deal' | incorrect | gold 未命中 |
| 105 | train | What is the altitude of the town in England that has Leadgat | about 1,000 ft above sea | '0' | format_failure | 单 token 函数词/碎片 '0'，无答案内容 |
| 106 | train | The "civic rally cross" was sold alongside what other model  | Honda Ballade | 'Honda CivicX' | incorrect | gold 未命中 |
| 107 | test | Beena Sarwar is the editor of a peace initiative sponsored b | Karachi, Pakistan | 'Beena Sarwar is the editor of a peace initiative s' | incorrect | gold 未命中 |
| 108 | validation | What current state is the location of unrecognized and auton | Tennessee | 'T' | format_failure | 单 token 函数词/碎片 'T'，无答案内容 |
| 109 | train | What is the fourth most populous urban area in the Republic  | Galway | 'Gal' | incorrect | 单 token 短答 'Gal'（疑似错答，人工留意） |
| 110 | test | Johnny Edwards and Ian Anderson are singers, who had joined  | John Douglas "Johnny" Ed | 'Ian Anderson' | incorrect | gold 未命中 |
| 111 | validation | What award won by only twelve people has a man who Ted Koosh | EGOT | 'Tony Prize' | incorrect | gold 未命中 |
| 112 | test | What man is linked to both Johnny Tremain and Magic Kingdom? | Walt Disney | 'Walt Disney' | correct | gold 命中（含等价/别名） |
| 113 | train | Who did the player nicknamed "The Human Highlight Film" play | Boston Celtics | 'New York Knicks' | incorrect | gold 未命中 |
| 114 | train | How many assists did the Bosnian football player account for | 20 assists | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 115 | validation | What type of industry does Tony Bill and Flyboys have in com | film | 'Av industry' | incorrect | gold 未命中 |
| 116 | train | Blank Check and Air Bud are both examples of what type of mo | American comedy | 'comedy' | incorrect | 单 token 短答 'comedy'（疑似错答，人工留意） |
| 117 | test | What is the year of the event which orrurred first, Beecher' | 1907 | '1979' | incorrect | 单 token 短答 '1979'（疑似错答，人工留意） |
| 118 | train | The William Ulmer Brewery is located in a neighborhood that  | NYPD's 83rd Precinct | 'The Los Angeles Police Department' | incorrect | gold 未命中 |
| 119 | test | Milo Parker starred in which 2014 movie alongside Gillian An | Robot Overlords | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 120 | train | In what town does the one-time star of "And There's More" no | Rochdale | 'Los Angeles, California' | incorrect | gold 未命中 |
| 121 | test | Mr. Wilson's Cabinet of Wonder: Pronged Ants, Horned Humans, | Los Angeles | 'Los Angeles' | correct | gold 命中（含等价/别名） |
| 122 | validation | Luther: The Calling is based on the BBC crime drama comprisi | 2010 | '2016' | incorrect | 单 token 短答 '2016'（疑似错答，人工留意） |
| 123 | train | Howard Bilerman produced an album for which songwriter from  | Vic Chesnutt | 'Wilco' | incorrect | 单 token 短答 'Wilco'（疑似错答，人工留意） |
| 124 | test | Which dog is considered a giant dog breed, the Leonberger or | The Leonberger is a gian | 'The Leonberger is considered a giant dog breed.' | incorrect | gold 未命中 |
| 125 | train | Which actress does this Netflix's project by Nick Bernardone | Ellie Kemper | 'Tina Fey' | incorrect | gold 未命中 |
| 126 | train | The American short horror The sub stars which American actre | Heather Langenkamp | 'Sarah Bell' | incorrect | gold 未命中 |
| 127 | test | What ABC television series was inspired by a 2011 film and c | Agent Carter | 'Iron' | incorrect | 单 token 短答 'Iron'（疑似错答，人工留意） |
| 128 | validation | What was the address of the penitentiary where Jimmy Elliot  | 2027 Fairmount Avenue | 'San Quentin, California' | incorrect | gold 未命中 |
| 129 | train | What is the year of the event that occured first, Skeeter st | 1979 | '1940' | incorrect | 单 token 短答 '1940'（疑似错答，人工留意） |
| 130 | train | Who played the crime boss considered the father of modern or | Andy García | 'Al Pacino' | incorrect | gold 未命中 |
| 131 | train | The was the album with the song Unbelievable by American rap | September 13, 1994 | '1994' | incorrect | 单 token 短答 '1994'（疑似错答，人工留意） |
| 132 | test | Who was born first Burton Cummings or Sharleen Spiteri? | Burton Lorne Cummings | 'Burton Cummings' | incorrect | gold 未命中 |
| 133 | train | The Shrewsbury & Newport Canals Trust promotes the restorati | Shropshire Union Canal | 'Canal' | incorrect | 单 token 短答 'Canal'（疑似错答，人工留意） |
| 134 | train | What year was the midfielder who shot the winning goal in th | 1988 | '1986' | incorrect | 单 token 短答 '1986'（疑似错答，人工留意） |
| 135 | train | In what country does the director of Shirin in Love, live? | Iranian | 'Iran' | incorrect | 单 token 短答 'Iran'（疑似错答，人工留意） |
| 136 | train | What concert hall is located on the northern edge or South K | Royal Albert Hall | 'Bigmore Hall' | incorrect | gold 未命中 |
| 137 | validation | Which ocean would the ingredients likely come from for the S | Atlantic Ocean | 'Atlantic Ocean' | correct | gold 命中（含等价/别名） |
| 138 | test | Which Russian professional ice hockey player, known as the M | Pavel Valerievich Datsyu | 'Yuri Ivanov' | incorrect | gold 未命中 |
| 139 | test | Both Bishop Carroll Catholic High School and Kapaun Mt. Carm | Wichita | 'Kansasrence' | incorrect | 单 token 短答 'Kansasrence'（疑似错答， |
| 140 | train | Metro West Ambulance serves event support for the building i | Rose Garden | 'Portland Hall' | incorrect | gold 未命中 |
| 141 | test | What current NHL team owner played for the team that won the | Mario Lemieux | 'Ed Wilson' | incorrect | gold 未命中 |
| 142 | train | Myron F. Diduryk's exploits were described in a book by an a | lieutenant general | 'Majorel' | incorrect | 单 token 短答 'Majorel'（疑似错答，人工留意 |
| 143 | train | The first book in the Sprawl Trilogy won what three awards? | Nebula Award, the Philip | 'H' | format_failure | 单 token 函数词/碎片 'H'，无答案内容 |
| 144 | train | Who is younger, Billy Idol or Ray Wilson? | Raymond Wilson | 'Billy Idol is younger than Ray Wilson.' | incorrect | gold 未命中 |
| 145 | train | Daddy was an American Pit Bull who was integral to the work  | Cesar Millan | 'Cesar Milan' | incorrect | gold 未命中 |
| 146 | train | What was the other name of the textile mill on which The Mil | Styal Mill | 'Theley Mill' | incorrect | gold 未命中 |
| 147 | train | In what year did Farda Amiga win a race at the Saratoga Race | (foaled February 1, 1999 | 'Farda Amiga won a race at the Saratoga Race course' | incorrect | gold 未命中 |
| 148 | test | The St. Louis Bay Bridge runs between Bay St. Louis and a ci | Harrison County, Mississ | 'H County' | incorrect | gold 未命中 |
| 149 | train | In the 2012-13 FC Sion they brought in Gennaro Gattuso and a | Scottish Premiership clu | 'Rangers' | incorrect | 单 token 短答 'Rangers'（疑似错答，人工留意 |
| 150 | train | The Hindmarsh Stadium is sponsored by a brewery that sold ho | 69.7 million litres | '10 million' | incorrect | gold 未命中 |
| 151 | train | Which Hells Angel member stabbed and beat an attendant of th | Alan Passaro | 'John Thompson' | incorrect | gold 未命中 |
| 152 | test | WHICH GROUP OF PEOPLE NICKNAMED THE US ARMYS REGIMENT "BUFFA | Native American tribes | 'Native Americans' | incorrect | gold 未命中 |
| 153 | train | Are Bangkok Girl and Home both horror movies? | no | 'No' | correct | gold 命中（含等价/别名） |
| 154 | train | Which professional baseball player and National 1993 Basebal | Reginald Martinez "Reggi | 'David Rose' | incorrect | gold 未命中 |
| 155 | train | St. John's College, Belize offers an education in a traditio | Grammar, logic, and rhet | 'Latin, science, and mathematics' | incorrect | gold 未命中 |
| 156 | test | What was the author of Freeway Warrior's original occupation | Originally a musician | 'law' | incorrect | 单 token 短答 'law'（疑似错答，人工留意） |
| 157 | train | Who co-wrote The Hidden History of the Human Race with a man | Richard L. Thompson | 'John White' | incorrect | gold 未命中 |
| 158 | test | The actress who played Clementine Churchill in "The Crown" j | Paula D'Alessandris | 'David Shakespeare' | incorrect | gold 未命中 |
| 159 | train | The terminology of algebraic geometry changed drastically wi | German | 'French' | incorrect | 单 token 短答 'French'（疑似错答，人工留意） |
| 160 | train | The term snake eyes is used in a particular casino game that | a pair of dice | 'dice' | incorrect | 单 token 短答 'dice'（疑似错答，人工留意） |
| 161 | train | Whom was the cofounder of Orange County Choppers and appeare | Paul Teutul Jr. | 'Mike Smith' | incorrect | gold 未命中 |
| 162 | train | The Jodrell Bank Observatory was established in 1945 by what | Sir Alfred Charles Berna | 'Fred Ryle' | incorrect | gold 未命中 |
| 163 | train | Who is the mother of the princess who opened Middleton Grang | Princess Elizabeth | 'Queen Elizabeth II' | incorrect | gold 未命中 |
| 164 | test | Why does the City of Boston get their christmas tree from Ai | for their assistance aft | 'Tradition' | incorrect | 单 token 短答 'Tradition'（疑似错答，人工 |
| 165 | validation | Bobby Godsell held a senior position in which global company | AngloGold Ashanti | 'Google' | incorrect | 单 token 短答 'Google'（疑似错答，人工留意） |
| 166 | train | What's the name of the differential equation that was develo | Lommel differential equa | 'Stusion equation' | incorrect | gold 未命中 |
| 167 | validation | Iselin Solheim provided vocals in the song released on what  | 3 December | '17 October 2015' | incorrect | gold 未命中 |
| 168 | train | Which song, released on December 7, 2008 was co-written by L | White Horse | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 169 | train | An American who is a German literature translator and did a  | University of Vienna | 'Prale University' | incorrect | gold 未命中 |
| 170 | test | The actress who played Laurie Keller in the episode "Pilot"  | Critics' Choice Televisi | 'Golden' | incorrect | 单 token 短答 'Golden'（疑似错答，人工留意） |
| 171 | train | What was the air date of "The Simpsons" episode written by M | May 21, 2000 | 'March 16, 2000' | incorrect | gold 未命中 |
| 172 | test | What church was the college Marjorie Hass is the 20th presid | Presbyterian Church | 'Methodist Church' | incorrect | gold 未命中 |
| 173 | train | The current coach of the Los Angeles Clippers was signed as  | 1994–95 NBA season | '2003' | incorrect | 单 token 短答 '2003'（疑似错答，人工留意） |
| 174 | validation | Who wrote the 1970 international hit song Murray Head is mos | Andrew Lloyd Webber and  | 'John' | incorrect | 单 token 短答 'John'（疑似错答，人工留意） |
| 175 | train | What party does the House of Commons representative for Cong | British Conservative Par | 'Conservative' | incorrect | 单 token 短答 'Conservative'（疑似错答 |
| 176 | train | In the USA, gun powder is used in conjunction with this to s | Anvil firing | 'gunder' | incorrect | 单 token 短答 'gunder'（疑似错答，人工留意） |
| 177 | train | Inserra Supermarkets is a supermarket chain that is a member | Wakefern Food Corporatio | 'Food cooperative' | incorrect | gold 未命中 |
| 178 | test | Which car brand was one step above the brand started on Nove | Oakland | 'A' | format_failure | 单 token 函数词/碎片 'A'，无答案内容 |
| 179 | train | Who is the author of the play that was adapted into a film a | William Shakespeare | 'William Shakespeare' | correct | gold 命中（含等价/别名） |
| 180 | validation | The 2014–15 UEFA Champions League knockout phase lead to the | European Champion Clubs' | 'European European Cup' | incorrect | gold 未命中 |
| 181 | test | What languages is the journal that Michel Feher semi-regular | French, English and Span | 'English' | incorrect | 单 token 短答 'English'（疑似错答，人工留意 |
| 182 | train | Sum 41 and Passion Pit have what in common? | Passion Pit is an Americ | 'rock' | incorrect | 单 token 短答 'rock'（疑似错答，人工留意） |
| 183 | validation | Are Sandy Mayer and Billy Martin both more successful at dou | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 184 | train | Which founding member drew critical acclaim as a bass guitar | Mike" Mills | 'Mike Buck' | incorrect | gold 未命中 |
| 185 | train | Do Matthew Good Band and Sleep Room play the same type of mu | yes | 'No' | format_failure | 单 token 函数词/碎片 'No'，无答案内容 |
| 186 | train | Where is the usual main ingredient of Hákarl normally found? | North Atlantic Ocean and | 'the Atlantic' | incorrect | gold 未命中 |
| 187 | validation | What occupations do Charles Burnett and Alan J. Pakula have  | film director, film prod | 'filmors' | incorrect | 单 token 短答 'filmors'（疑似错答，人工留意 |
| 188 | train | What title did the actor who worked with Sivaji Ganesan in a | politician | 'actor' | incorrect | 单 token 短答 'actor'（疑似错答，人工留意） |
| 189 | train | Folie à Deux is a studio album by the American rock band for | Wilmette | 'Los' | incorrect | 单 token 短答 'Los'（疑似错答，人工留意） |
| 190 | test | Les Patterson Saves the World was a comedy film starring the | My Gorgeous Life | 'Les Patterson' | incorrect | gold 未命中 |
| 191 | train | Which author dedicated a 1985 romance novel to the author wh | Eva Ibbotson | 'James King' | incorrect | gold 未命中 |
| 192 | validation | What Manchester United and Portuguese national winger scored | Nani | 'David Ronaldo' | incorrect | gold 未命中 |
| 193 | test | whats the famous bavagheet by arun date? | Shukratara | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 194 | train | Swiss music duo Double released their best known single "The | 1986 | '1998' | incorrect | 单 token 短答 '1998'（疑似错答，人工留意） |
| 195 | validation | Which American novelist was notable primarily for publishing | Philip Kindred Dick | 'Philip K. Dick' | format_failure | 输出为问句回显，无答案内容 |
| 196 | train | When was the college which Albert Simons taught at founded? | 1770 | '1887' | incorrect | 单 token 短答 '1887'（疑似错答，人工留意） |
| 197 | train | Which cast member of Alice Upside Down also stars in the ABC | Lucas Stephen Grabeel | 'Gina Rodriguez' | incorrect | gold 未命中 |
| 198 | train | What is the date of the reissue of one of Rhihanna's album t | June 2, 2008 | 'November 9, 2010' | incorrect | gold 未命中 |
| 199 | test | Bobby Arora is the trading director of a retail chain that w | 1978 | '1999' | incorrect | 单 token 短答 '1999'（疑似错答，人工留意） |
| 200 | train | The Swiss immigration referendum, February 2014 is an exampl | relations between Switze | 'refer referendum' | incorrect | gold 未命中 |
| 201 | test | What is this group referred to as that this Russian composer | The Five | 'Russian Five' | incorrect | gold 未命中 |
| 202 | validation | Who has released more solo albums, Ozzy Osbourne or Curt Smi | John Michael "Ozzy" Osbo | 'Ozzy Osbourne has released more solo albums.' | incorrect | gold 未命中 |
| 203 | validation | What city was the band who "Evie" formed in? | Sydney, Australia | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 204 | train | What actor, who passed away in 1942 was also the producer of | George M. Cohan | 'John Grant' | incorrect | gold 未命中 |
| 205 | train | What 1958 born American television writer and actress contri | Deborah "Deb" Lacusta | 'Linda Thomas' | incorrect | gold 未命中 |
| 206 | train | Are Trent Edwards and Lucy Saroyan both football players? | no | 'No' | correct | gold 命中（含等价/别名） |
| 207 | train | Who was the brother of the architect of Hook and Ladder No.  | Cuyler Reynolds | 'John' | incorrect | 单 token 短答 'John'（疑似错答，人工留意） |
| 208 | train | Which magazine was founded first, Allure or Genre? | Allure is an American wo | 'Genre' | incorrect | 单 token 短答 'Genre'（疑似错答，人工留意） |
| 209 | train | Tedrow, Ohio lies close to which 241. 26 mi highway? | Ohio Turnpike | 'US5' | incorrect | 单 token 短答 'US5'（疑似错答，人工留意） |
| 210 | train | Who was the First Prophert to the sixth Pharaoh of the Eight | Khonsu | 'Ahmose' | incorrect | 单 token 短答 'Ahmose'（疑似错答，人工留意） |
| 211 | train | Which British engineering company is best known for its luxu | D. Napier & Son | 'Roll' | incorrect | 单 token 短答 'Roll'（疑似错答，人工留意） |
| 212 | train | Which 8-year old star of an epistolary novel turned musical  | Diamond White | 'Bella Song' | incorrect | gold 未命中 |
| 213 | train | The casino owner who was focused on the documentary Nobody S | American | 'American' | correct | gold 命中（含等价/别名） |
| 214 | test | Who beacme a star as a comic book character created by Gerry | Megalyn Echikunwoke | 'Spider-Man' | incorrect | 单 token 短答 'Spider-Man'（疑似错答，人 |
| 215 | train | Are Yingkou and Fuding the same level of city? | no | 'No' | correct | gold 命中（含等价/别名） |
| 216 | test | What is the nationality of the man who finished second for A | Russia | 'French' | incorrect | 单 token 短答 'French'（疑似错答，人工留意） |
| 217 | train | What award was won by the director who directed the eighth m | Tony Award | 'Tony' | incorrect | 单 token 短答 'Tony'（疑似错答，人工留意） |
| 218 | test | Geoffrey Serle wrote a biography about which Australian mili | John Monash | 'John Monash' | correct | gold 命中（含等价/别名） |
| 219 | test | The winner of the FIA World Endurance Championship in 2013 d | Mika Salo | 'James' | incorrect | 单 token 短答 'James'（疑似错答，人工留意） |
| 220 | validation | What type of sport does Sergio Casal and Manuel Orantes have | tennis | 'tennis' | correct | gold 命中（含等价/别名） |
| 221 | test | What institution does 2017 Texas Tech Red Raiders baseball t | Texas Tech University | 'Texas Tech University' | correct | gold 命中（含等价/别名） |
| 222 | train | What science fantasy young adult series, told in first perso | Animorphs | 'Staren' | incorrect | 单 token 短答 'Staren'（疑似错答，人工留意） |
| 223 | train | Where did the designer of the Van de Graaff generator teach  | Princeton University and | 'Harvard University' | incorrect | gold 未命中 |
| 224 | train | Who won more academy awards, Joseph L. Mankiewicz or Tony Ka | Joseph Leo Mankiewicz | 'Joseph L. Mankiewicz' | format_failure | 输出为问句回显，无答案内容 |
| 225 | train | When was the son of Kingsley Amis born ? | 1949 | '1958' | incorrect | 单 token 短答 '1958'（疑似错答，人工留意） |
| 226 | test | Whose given first name is longer, Theo Angelopoulos and Budd | Theodoros "Theo" Angelop | 'Theo Angelopoulos' | correct | gold 命中（含等价/别名） |
| 227 | test | Who is the former pentecostal preacher who released the come | Sam Kinison | 'Bill Rock' | incorrect | gold 未命中 |
| 228 | train | Psycho-physical Awareness was developed into an original and | his most brilliant stude | 'Method' | incorrect | 单 token 短答 'Method'（疑似错答，人工留意） |
| 229 | validation | Armageddon in Retrospect was written by the author who was b | Slaughterhouse-Five | 'Catch-22' | incorrect | 单 token 短答 'Catch-22'（疑似错答，人工留 |
| 230 | train | Who was the director of 1935 American crime drama film, whic | Tim Whelan | 'John Hawks' | incorrect | gold 未命中 |
| 231 | test | Pramod Bhasin was the former CEO of a company that provided  | IT | 'financial services' | incorrect | gold 未命中 |
| 232 | train | Which British Indian novelist and essayist did Anthony Burge | Salman Rushdie | ' Salman Rushdie' | correct | gold 命中（含等价/别名） |
| 233 | test | What topic does GeekDad cover that pertains to a line of pla | Lego | 'LEego' | incorrect | 单 token 短答 'LEego'（疑似错答，人工留意） |
| 234 | test | What character did James Byron Dean play in his final lead r | ranch hand Jett Rink | 'Tom' | incorrect | 单 token 短答 'Tom'（疑似错答，人工留意） |
| 235 | train | What other method of extending an ice hockey game exists oth | the shootout | 'overtime' | incorrect | 单 token 短答 'overtime'（疑似错答，人工留 |
| 236 | validation | Daniel Greene has created what for clients including sportsc | portrait | 'bios' | incorrect | 单 token 短答 'bios'（疑似错答，人工留意） |
| 237 | test | Which KaBoom! Entertainment Inc. film is based on a story by | The Jungle Book (1894) | 'The Book' | incorrect | gold 未命中 |
| 238 | train | What Friday night programming block included what collective | Cartoon Cartoon Fridays | 'Friday Night Live' | incorrect | gold 未命中 |
| 239 | validation | What championship did the person who substituted for Simon P | Australian Supercars Cha | 'IndyCar Championship' | incorrect | gold 未命中 |
| 240 | train | Are David O. Russell and Tony Gatlif from the same country? | no | 'No' | correct | gold 命中（含等价/别名） |
| 241 | train | What animation company produced the first season of an anima | Goldie & Bear | 'Animation' | incorrect | 单 token 短答 'Animation'（疑似错答，人工 |
| 242 | train | In what century did this Native warrior and chief, whose bro | nineteenth | '19th century' | incorrect | gold 未命中 |
| 243 | train | Who was the ruler ousted by the 30th Prime Minister of Cambo | Prince of Cambodia Norod | 'Lon Nol' | incorrect | gold 未命中 |
| 244 | test | What Ruben Fleischer film did No One's Gonna Love You appear | Zombieland | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 245 | validation | Were the films Tonka and 101 Dalmatians released in the same | 1958 Walt Disney Western | 'Yes' | incorrect | 单 token 短答 'Yes'（疑似错答，人工留意） |
| 246 | test | What number largest commercial airline in the United States  | 8th | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 247 | validation | Where are schools in the athletic association Cardinal Hayes | New York City, Long Isla | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 248 | train | What literary style describes the 1968 book that features a  | the growing literary sty | 'children' | incorrect | 单 token 短答 'children'（疑似错答，人工留 |
| 249 | train | What Australian Electoral Division in New South Wales create | Division of Cook | 'Alex Sydney' | incorrect | gold 未命中 |
| 250 | train | Mazda's Mazda6 belongs to which country's car manufacturer? | Japanese | 'Japan' | incorrect | 单 token 短答 'Japan'（疑似错答，人工留意） |
| 251 | test | The original serialized story of the Bride of Re-Animator fi | horror fiction | 'horror fiction' | correct | gold 命中（含等价/别名） |
| 252 | train | What technique does Cam Clarke and Akira have in common? | animation | 'S' | format_failure | 单 token 函数词/碎片 'S'，无答案内容 |
| 253 | validation | What profession does Kazuyuki Fujita and Gilbert Yvel have i | martial artist | 'Kazuyuki Fujita and Gilbert Yvel are both football' | incorrect | gold 未命中 |
| 254 | test | Who directed a 2009 comedy released by BBC Films? | Debbie Isitt | 'Mark Smith' | incorrect | gold 未命中 |
| 255 | train | Which port city lies approximately 25 km north of the Lingna | Keelung | 'Shenzhen' | incorrect | 单 token 短答 'Shenzhen'（疑似错答，人工留 |
| 256 | train | Who created the series broadcast on the WB that Leigh-Allyn  | Constance M. Burge | 'David Thomas' | incorrect | gold 未命中 |
| 257 | train | What country of origin does Shawnee Trail and Great Indian W | American | 'United States' | incorrect | gold 未命中 |
| 258 | train | The university where Rolf Martin Theodor Dahlgren worked as  | 9,000 | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 259 | train | When was the star of the 1982 remake of The Spider's Web app | 2014 | '1999' | incorrect | 单 token 短答 '1999'（疑似错答，人工留意） |
| 260 | validation | Deckers Creek begins west of an unincorporated area in what  | Preston County | 'F' | format_failure | 单 token 函数词/碎片 'F'，无答案内容 |
| 261 | train | Are Myles Kennedy and SafetySuit both associated with rock b | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 262 | train | House of Many Ways is a young adult fantasy novel set in the | Academy Award for Best A | 'Oscar' | incorrect | 单 token 短答 'Oscar'（疑似错答，人工留意） |
| 263 | test | Dost Mohammad Khan was killed by a ruler who became the thir | Afghanistan | 'Sghan' | incorrect | 单 token 短答 'Sghan'（疑似错答，人工留意） |
| 264 | train | In what year was the Sayrevill, New Jersey rock band that Fr | 1983 | '1976' | incorrect | 单 token 短答 '1976'（疑似错答，人工留意） |
| 265 | test | What professional dancers twice turned on a lights festival  | Audrey Mossom | 'Professional dancers' | incorrect | gold 未命中 |
| 266 | train | Which tennis player is from a country closer to Canada, Ken  | Kenneth Eliot Flach | 'Lucie Šafářová' | incorrect | gold 未命中 |
| 267 | test | What dance academy did the starring actress from The Glory o | Beijing Dance Academy | 'Be York Dance Academy' | incorrect | gold 未命中 |
| 268 | test | What brother of Stanley Alan Van Gundy is a color commentato | Jeffrey William Van Gund | 'Jeff Van Gundy' | incorrect | gold 未命中 |
| 269 | test | What 1989-born Liverpool player was Jim Cassell responsible  | Daniel Sturridge | 'Jordan Alexander' | incorrect | gold 未命中 |
| 270 | test | Are both Deerhunter and Nine Lashes American Christian rock  | no | 'No' | correct | gold 命中（含等价/别名） |
| 271 | train | Not About Angels was used in the film adaptation of what nov | The Fault in Our Stars | 'The Fault in Our Stars' | correct | gold 命中（含等价/别名） |
| 272 | train | Which American-Canadian actor starred in the Disney Channel' | Eric Allan Kramer | 'Jake Justice' | incorrect | gold 未命中 |
| 273 | train | From which country is the largest known example of European  | Switzerland | 'Denmark' | incorrect | 单 token 短答 'Denmark'（疑似错答，人工留意 |
| 274 | train | Where is the brand "Moe's Southwest Grill" owned based? | It is based in Sandy Spr | 'United States' | incorrect | gold 未命中 |
| 275 | validation | Ruth Vollmer begins work designing window displays for which | Tiffany's | 'Saks Fifth' | incorrect | gold 未命中 |
| 276 | train | Who is the controlling shareholder of the world's fourth-lar | Jürgen M. Geissinger | 'Generalelin' | incorrect | 单 token 短答 'Generalelin'（疑似错答， |
| 277 | test | During the Miss USA 2015, Olivia Jordan of Oklahoma was crow | Nia Sanchez | 'Tyra Trump' | incorrect | gold 未命中 |
| 278 | test | What American broadcasting company broadcasted the comedy sh | Sirius XM Holdings | 'ABC' | incorrect | 单 token 短答 'ABC'（疑似错答，人工留意） |
| 279 | test | Are University of Virginia and Massachusetts Institute of Te | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 280 | train | What type of activity does Owner earnings and Warren Buffett | business | 'Investing' | incorrect | 单 token 短答 'Investing'（疑似错答，人工 |
| 281 | train | The La Senza brand is currently owned by a fashion retailer  | Columbus | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 282 | train | Orchard Gateway connects what shopping mall in singapore wit | Orchard Central | 'Somerset' | incorrect | 单 token 短答 'Somerset'（疑似错答，人工留 |
| 283 | train | Was Without the King and Italy in a Day directed by the same | no | 'No' | correct | gold 命中（含等价/别名） |
| 284 | train | What continents are the Moneuptychia found in? | the Americas | 'South' | incorrect | 单 token 短答 'South'（疑似错答，人工留意） |
| 285 | train | Wade Watts is the uncle of a politican who played college fo | the Oklahoma Sooners | 'LS State' | incorrect | gold 未命中 |
| 286 | train | Which band formed first Cha Cha Cohen or Swervedriver? | Cha Cha Cohen were a ban | 'Cha Cha Cohen' | correct | gold 命中（含等价/别名） |
| 287 | validation | Which road borders both Pacific Mall and Splendid China Mall | Steeles Avenue | 'New Pacific Road' | incorrect | gold 未命中 |
| 288 | train | A Hand Is on the Gate marked the Broadway directorial debut  | Roscoe Lee Browne | 'Paul Washington' | incorrect | gold 未命中 |
| 289 | test | The mass killing that took place at Oakland, California on A | Oregon | 'Oregon' | correct | gold 命中（含等价/别名） |
| 290 | validation | When was the father of the professional ice hockey player wi | June 13, 1960 | '1960' | incorrect | 单 token 短答 '1960'（疑似错答，人工留意） |
| 291 | train | What career did the British actor born in 1965 and star of L | professional footballer | 'music' | incorrect | 单 token 短答 'music'（疑似错答，人工留意） |
| 292 | train | John MacGregor, Baron MacGregor of Pulham Market was educate | King George IV | 'St I' | incorrect | gold 未命中 |
| 293 | train | This British television series was adapted from one of the b | Household Words | 'Blackunch' | incorrect | 单 token 短答 'Blackunch'（疑似错答，人工 |
| 294 | validation | Maryland Jockey Club operates a race track in the largest mu | Prince George's County | 'Bford' | incorrect | 单 token 短答 'Bford'（疑似错答，人工留意） |
| 295 | test | Which river flows next to the German town where the music pr | Moselle | 'Eline' | incorrect | 单 token 短答 'Eline'（疑似错答，人工留意） |
| 296 | train | When was the younger brother of Farshid Karimi born ? | 8 November 1978 | '1980' | incorrect | 单 token 短答 '1980'（疑似错答，人工留意） |
| 297 | test | This annual event held in several major cities in Finland is | the summer solstice | 'midnight' | incorrect | 单 token 短答 'midnight'（疑似错答，人工留 |
| 298 | test | Are Lycoris and Ammi both native to southern Asia? | yes | 'No' | format_failure | 单 token 函数词/碎片 'No'，无答案内容 |
| 299 | train | When William Gladstone successfully relaunched his political | Liberal Party | 'Liberal Party' | correct | gold 命中（含等价/别名） |
| 300 | train | Are Kenji Mizoguchi and David Wall from the same country? | no | 'No' | correct | gold 命中（含等价/别名） |
| 301 | validation | Naseer & Shahab is a Pakistani band playing a genre that dom | 1970s | '1970s' | correct | gold 命中（含等价/别名） |
| 302 | test | In which branch of the U.S. military did the man who Robert  | Marine Corps | 'USavy' | incorrect | 单 token 短答 'USavy'（疑似错答，人工留意） |
| 303 | train | What year was the man, who is credited for developing a Cres | 1858 | '1831' | incorrect | 单 token 短答 '1831'（疑似错答，人工留意） |
| 304 | train | Are Ferocactus and Silene both types of plant? | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 305 | test | Murray Seafield St George Head most recognised for which son | One Night in Bangkok | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 306 | validation | Are the libretto of Tristan und Isolde and Ariane et Barbe-b | no | 'No' | correct | gold 命中（含等价/别名） |
| 307 | train | What was the specialization of an American naval officer who | feats of exploration | 'aviography' | incorrect | 单 token 短答 'aviography'（疑似错答，人 |
| 308 | test | Are Francis Ford Coppola and Jack Hill both American? | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 309 | train | Which pistol was replaced by a pistol manufactured by Spreew | Luger P08 | 'Puger' | incorrect | 单 token 短答 'Puger'（疑似错答，人工留意） |
| 310 | test | Which American digital media company and news satire organiz | The Onion | 'The Onion' | correct | gold 命中（含等价/别名） |
| 311 | test | What type of arts that have existed since ancient times did  | Graffiti | 'martial arts' | incorrect | gold 未命中 |
| 312 | test | What song originally released by an American rock band activ | "Bad Moon Rising" | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 313 | validation | Where did King James reign during Samuel Parker's time as a  | James II and VII (14 Oct | 'England' | incorrect | 单 token 短答 'England'（疑似错答，人工留意 |
| 314 | train | What was the setting for Raphael Coleman's best known film? | Victorian England | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 315 | train | Heikki Seppa studied metalsmith at Goldsmith's school in Hel | Georg Arthur Jensen | 'Johan Ericman' | incorrect | gold 未命中 |
| 316 | validation | The 2006 NCAA Wrestling Championships crowned Jake Rosholt a | left | 'left' | correct | gold 命中（含等价/别名） |
| 317 | test | Where was the band who released Feeding the Wolves formed? | Knoxville, Tennessee | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 318 | test | Who directed the film Leigha Kayleen Hancock is best known f | Gary Ross | 'John Lee' | incorrect | gold 未命中 |
| 319 | validation | What is the legal name of Johnny Campbell's hometown? | Londonderry | 'San Antonio, Texas' | incorrect | gold 未命中 |
| 320 | train | What kind of species on the Indonesian island of java might  | Javan leopard | 'monkeys' | incorrect | 单 token 短答 'monkeys'（疑似错答，人工留意 |
| 321 | train | What type of film are both "500 Years Later" and "Manson"? | documentary | 'hor' | incorrect | 单 token 短答 'hor'（疑似错答，人工留意） |
| 322 | train | The runner-up in The Celebrity Apprentice 2 has written an a | "How I Raised, Folded, B | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 323 | validation | The Meadowbrook State Parkway connects to the Southern State | 12,272 | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 324 | train | The city where Alex Shevelev died is the capital of what reg | the Lazio region | 'U' | format_failure | 单 token 函数词/碎片 'U'，无答案内容 |
| 325 | train | What was Robert M. Fomon's connection to the New York Stock  | a governor | 'member' | incorrect | 单 token 短答 'member'（疑似错答，人工留意） |
| 326 | train | What park is just south of the location where the New York J | Central Park | 'Cwood Park' | incorrect | gold 未命中 |
| 327 | test | Where did the military engagements that Captain Lewis Cunnin | Mexico-United States bor | 'United' | incorrect | 单 token 短答 'United'（疑似错答，人工留意） |
| 328 | test | Whose former city palace did Erna Flegel work at? | Prince Antoni Radziwiłł | 'Berlinenna' | incorrect | 单 token 短答 'Berlinenna'（疑似错答，人 |
| 329 | train | In what town is Suffolk county hamlet that was served by the | Town of Islip | 'Hport' | incorrect | 单 token 短答 'Hport'（疑似错答，人工留意） |
| 330 | test | Garth Richardson is the son of the producer who worked for w | Badfinger | 'The Iies' | incorrect | gold 未命中 |
| 331 | train | Shenley Hall is a house at a parish how far from central Lon | 18.7 miles | '10 miles' | incorrect | gold 未命中 |
| 332 | test | What kind of game is The Park a spin-off of? | massively multiplayer on | 'a video game' | incorrect | gold 未命中 |
| 333 | validation | Do tennis players Kathy Jordan and Sergi Bruguera have the s | no | 'No' | correct | gold 命中（含等价/别名） |
| 334 | train | What type of music did Dave Wyndorf and Poly Styrene perform | rock | 'rock' | correct | gold 命中（含等价/别名） |
| 335 | train | The movie "100 Million BC" continues the urban myth of an ex | Philadelphia Naval Shipy | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 336 | train | Robin Pingeton replaced Cindy Stein as head coach of which u | University of Missouri | 'George State University' | incorrect | gold 未命中 |
| 337 | test | Boulevardier and Earthquake are cocktails, one of which has  | The Tremblement de Terre | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 338 | test | What child starred in a Chicago production of Alice Walker's | Diamond White | 'A Obama' | incorrect | gold 未命中 |
| 339 | test | From March 631 to April 631, Farrukhzad Khosrau V was the ki | the Parthian Empire | 'Sasanian Empire' | incorrect | gold 未命中 |
| 340 | validation | Who was the head promotor of the singer of "For The Good Tim | Rikki Farr's | 'David Jackson' | incorrect | gold 未命中 |
| 341 | test | Hairy Jeremy was a television show created in a style that,  | clay animation | 'stop-motion' | incorrect | 单 token 短答 'stop-motion'（疑似错答， |
| 342 | train | Who is the US Olympian and Christian evangelist did the 2010 | Louis "Louie" Zamperini | 'Steve Lewis' | incorrect | gold 未命中 |
| 343 | train | Are Giuseppe Verdi and Ambroise Thomas both Opera composers  | yes | 'yes' | correct | gold 命中（含等价/别名） |
| 344 | train | Be Quick '28 football club is locayed in what province? | Overijssel | 'Be' | format_failure | 单 token 函数词/碎片 'Be'，无答案内容 |
| 345 | train | Are the films Gasland from 2010 and Pumping Iron from 1977 b | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 346 | train | Who married a man who starred in Marcus Welby, M.D.? | Barbra Streisand | 'Elizabeth Taylor' | incorrect | gold 未命中 |
| 347 | test | ho is the brother of the American transgender actor known fo | Connor | 'Alex' | incorrect | 单 token 短答 'Alex'（疑似错答，人工留意） |
| 348 | validation | What is the name of the place in The Chronicles of Narnia wh | Lantern Waste | 'The Stone Wood' | incorrect | gold 未命中 |
| 349 | train | Were Thinking Fellers Union Local 282 and the Smiths, who ha | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 350 | train | Which American comedian starred in the original cast of Satu | Garrett Morris | 'Bill Martin' | incorrect | gold 未命中 |
| 351 | test | What is a common feature of both the Iron Rattler's inversio | combination of a loop an | 'in' | format_failure | 单 token 函数词/碎片 'in'，无答案内容 |
| 352 | train | Party of Syrian Unity was established in the wake of a publi | support for the establis | 'in' | format_failure | 单 token 函数词/碎片 'in'，无答案内容 |
| 353 | train | How do the Peter Laufer books Forbidden Creatures and No Ani | his own opinions changed | 'Forbidden Creatures' | incorrect | gold 未命中 |
| 354 | train | In the 1962 German Grand Prix, a racer came second. What did | Surtees Racing Organisat | 'F' | format_failure | 单 token 函数词/碎片 'F'，无答案内容 |
| 355 | train | Jaroslav Seifert and John McGahern were both part of what sh | writer | 'po' | format_failure | 单 token 函数词/碎片 'po'，无答案内容 |
| 356 | validation | How many films were directed by the director of Wise Blood? | 37 | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 357 | train | Operation light house was an experiment by Wernher von Braun | 1895 | '1912' | incorrect | 单 token 短答 '1912'（疑似错答，人工留意） |
| 358 | train | Iola is a city along the Neosho River in a region of Kansas  | Bourbon County | 'Scott County' | incorrect | gold 未命中 |
| 359 | train | San Marco and Medina are both what type of game? | board | 'board games' | correct | gold 命中（含等价/别名） |
| 360 | train | Ælfgifu of Exeter and Ælfgifu of Shaftesbury are both known  | saint | 'que' | incorrect | 单 token 短答 'que'（疑似错答，人工留意） |
| 361 | test | Do Lush and P.O.D. both consist of four band members? | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 362 | train | Insomniac Events is part of a partnership with a club founde | Iranian-American | 'J' | format_failure | 单 token 函数词/碎片 'J'，无答案内容 |
| 363 | validation | What was the English football club Tottenham Hotspur that Le | Spurs | 'Tottenham' | incorrect | 单 token 短答 'Tottenham'（疑似错答，人工 |
| 364 | train | The Trappist Abbey of Achel produces and sells what as an "A | Trappist beer | 'beer' | incorrect | 单 token 短答 'beer'（疑似错答，人工留意） |
| 365 | validation | Q:The 7.92×57mm Mauser rifle cartridge was used by which cou | German service cartridge | 'Germany' | incorrect | 单 token 短答 'Germany'（疑似错答，人工留意 |
| 366 | test | Who did a new permanent member on the fourteenth season of S | Gabriella Montez | 'Sharp Evans' | incorrect | gold 未命中 |
| 367 | test | What was the budget of the film in which Kodi Smit-McPhee vo | $60 million | '$' | format_failure | 单 token 函数词/碎片 '$'，无答案内容 |
| 368 | test | Who won the 2007 Copa America Final, with help from Julio Ba | Brazil | 'Argentina' | incorrect | 单 token 短答 'Argentina'（疑似错答，人工 |
| 369 | test | Do both Lancaster Cathedral and Peel Cathedral belong to the | yes | 'No' | format_failure | 单 token 函数词/碎片 'No'，无答案内容 |
| 370 | test | where was the musician and stand up comedian who recorded an | Northampton, England | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 371 | train | Legends of the Fall was based on a novella by what poetry an | James Harrison | 'James London' | incorrect | gold 未命中 |
| 372 | train | Telescope Hill is near the hamlet that is in what Suffolk Co | Brookhaven | 'Sayport' | incorrect | 单 token 短答 'Sayport'（疑似错答，人工留意 |
| 373 | train | Not Richard, But Dick was an album by the band formed in wha | Philadelphia | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 374 | train | What is the birthdate of this American actor, director, and  | February 13, 1946 | 'March 10, 1980' | incorrect | gold 未命中 |
| 375 | train | Han Chae-young was in the 2009 drama that aired on what netw | KBS2 | 'SBS' | incorrect | 单 token 短答 'SBS'（疑似错答，人工留意） |
| 376 | test | Which American swimmer, coached by Ray Looze, won a bronze m | Cody Miller | 'Ryan Phelps' | incorrect | gold 未命中 |
| 377 | test | Are Harry Everett Smith and Vladimir Danilevich both from Ru | no | 'No' | correct | gold 命中（含等价/别名） |
| 378 | train | 3TEETH was the debut album for the opening act for the2016 t | Los Angeles | 'Los Angeles' | correct | gold 命中（含等价/别名） |
| 379 | train | The producer of the Eric Church album "The Outsiders" was a  | In Pursuit | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 380 | test | "Take Me" is a song recorded by which American singer, actor | Frank Sinatra | 'Elvis Presley' | incorrect | gold 未命中 |
| 381 | train | Tui Flower and Julia child were both known for what? | Cooking | 'cooking' | correct | gold 命中（含等价/别名） |
| 382 | train | how many films has the director of "Girl 6" produced since 1 | over 35 films | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 383 | train | Are Toshi and Warrel Dane both in the band Sanctuary? | no | 'No' | correct | gold 命中（含等价/别名） |
| 384 | test | When was the football club founded in which Walter Otto Davi | 1885 | '1887' | incorrect | 单 token 短答 '1887'（疑似错答，人工留意） |
| 385 | train | What type of beliefs does Mount Ida and Rhea have in common? | Greek mythology | 'Greek beliefs' | incorrect | gold 未命中 |
| 386 | validation | Where was one of Sergei Prokofiev's most well-known operas f | Chicago, Illinois | 'Moscow' | incorrect | 单 token 短答 'Moscow'（疑似错答，人工留意） |
| 387 | test | The Church of England's Oxford Movement was opposed by a cle | devotional | 'poels' | incorrect | 单 token 短答 'poels'（疑似错答，人工留意） |
| 388 | train | About Time is a British romantic comedy-drama film that star | Dublin Institute of Tech | 'Trbridge University' | incorrect | gold 未命中 |
| 389 | test | Who has won more awards, Dan Schneider or Helen Hunt? | Helen Elizabeth Hunt | 'Helen Hunt' | incorrect | gold 未命中 |
| 390 | train | Guy Pearce starred in which movie produced by Marvel Studios | Iron Man 3 | 'The Man' | incorrect | gold 未命中 |
| 391 | train | What team competed in six competitions in their 116th season | Football Club Barcelona | 'Manchester United' | incorrect | gold 未命中 |
| 392 | test | Are Sunset Strip and American Hardcore both music documentar | no | 'Yes' | incorrect | 单 token 短答 'Yes'（疑似错答，人工留意） |
| 393 | test | Hivange is a village in a country that has how many official | three official languages | 'two' | incorrect | 单 token 短答 'two'（疑似错答，人工留意） |
| 394 | validation | What author wrote a three book series of memoirs that are st | Homer Hickam, Jr. | 'Elie W' | incorrect | gold 未命中 |
| 395 | test | Are Maro Ajemian and Patricia Field both pianists? | no | 'Yes' | incorrect | 单 token 短答 'Yes'（疑似错答，人工留意） |
| 396 | train | The movies Queen of Blood and Battle Beyond the Sun both con | Nebo Zovyot | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 397 | validation | Gretchen Gotay graduated from what American public research  | The University of Georgi | 'Georgia State University' | incorrect | gold 未命中 |
| 398 | train | Are Phlebodium and Pieris both species of ferns? | no | 'No' | correct | gold 命中（含等价/别名） |
| 399 | validation | Adam Fox was one of the first members of an informal literar | University of Oxford, En | 'Harvard University' | incorrect | gold 未命中 |
| 400 | train | Siegfriedstellung in the First World War was a defensive pos | German | 'Germany' | incorrect | 单 token 短答 'Germany'（疑似错答，人工留意 |
| 401 | train | From which phrase the name of the place where Hazina Towers  | Maasai phrase | 'Englishina' | incorrect | 单 token 短答 'Englishina'（疑似错答，人 |
| 402 | test | Alex Yemenidjian is the CEO of the company that owns what La | Tropicana Las Vegas | 'The Mirage' | incorrect | gold 未命中 |
| 403 | train | Were the films "Ten Who Dared" and "Tonka" distributed by th | yes | 'No' | format_failure | 单 token 函数词/碎片 'No'，无答案内容 |
| 404 | train | What is the nationality of this company that services MS Mob | Danish | 'British' | incorrect | 单 token 短答 'British'（疑似错答，人工留意 |
| 405 | test | What broadcasting company did both Andrew Collins and Stuart | BBC | 'BBC' | correct | gold 命中（含等价/别名） |
| 406 | train | What kind of musician does Robert Plant discography and John | drummer | 'rockian' | incorrect | 单 token 短答 'rockian'（疑似错答，人工留意 |
| 407 | train | Which Croatian professional basketball player (a shooting gu | Dražen Petrović | 'Mark' | incorrect | 单 token 短答 'Mark'（疑似错答，人工留意） |
| 408 | test | Who animated the TV anime adaptation of Dies irae? | studio A.C.G.T | 'Madhouse' | incorrect | 单 token 短答 'Madhouse'（疑似错答，人工留 |
| 409 | train | In what year was Shin Hyun-joon in the successful South Kore | 2005 | '2014' | incorrect | 单 token 短答 '2014'（疑似错答，人工留意） |
| 410 | train | Bally's & Paris station is on the monorail that is of what l | 3.9 mi | '3.5 miles' | incorrect | gold 未命中 |
| 411 | train | What actor starred in "Word of Honor" and "Miami Vice"? | Donald Wayne Johnson | 'Don Johnson' | incorrect | gold 未命中 |
| 412 | test | What is the name of the Australian specialist electronic mus | Cyclic Defrost | 'The Magazine' | incorrect | gold 未命中 |
| 413 | test | What type of engine powered both the Saab 36 and the Avro Vu | British Bristol Olympus  | 'jet' | incorrect | 单 token 短答 'jet'（疑似错答，人工留意） |
| 414 | train | Does Bazhong or Kaiyuan, Liaoning have a higher population? | Bazhong () is a prefectu | 'Kaiyuan, Liaoning' | incorrect | gold 未命中 |
| 415 | test | Following The Simple Things a featurette directed by Burny M | Mickey's Christmas Carol | 'The Simple Things' | format_failure | 输出为问句回显，无答案内容 |
| 416 | train | What is the name of a member of the North Melbourne Football | Mark Andrew Brayshaw | 'Rob' | incorrect | 单 token 短答 'Rob'（疑似错答，人工留意） |
| 417 | train | Vestfold and Telemark each border what other Norwegian count | Buskerud | 'Apland' | incorrect | 单 token 短答 'Apland'（疑似错答，人工留意） |
| 418 | validation | What game where a play must act as a night security guard wa | Five Nights at Freddy's | 'Overwatch' | incorrect | 单 token 短答 'Overwatch'（疑似错答，人工 |
| 419 | validation | What is another movie the director of Marvel Cinematic Unive | "Nanny McPhee" | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 420 | train | Have Jelena Janković and Marat Safin both played tennis prof | yes | 'Yes, Jelena Janković and Marat Safin have both pla' | correct | gold 命中（含等价/别名） |
| 421 | train | Q: Who had more solo albums, Marty Raybon or Greg Graffin? | Gregory Walter Graffin | 'Greg Graffin' | incorrect | gold 未命中 |
| 422 | train | What type of profession do Dave Pirner and Les McKeown both  | singer | 'Dave Pirner and Les McKeown are both musicians.' | incorrect | gold 未命中 |
| 423 | train | A Wind in the Door is part of a series written by who? | Madeleine L'Engle | "L'Engle" | correct | gold 命中（含等价/别名） |
| 424 | test | Mark Lawrence played for the Dallas Stars and which other NH | New York Islanders | 'Chicago Wild' | incorrect | gold 未命中 |
| 425 | test | Keene is an unincorporated community in Wabaunsee County, Ka | The United States of Ame | 'United States' | correct | gold 命中（含等价/别名） |
| 426 | test | Postal 2 has scenes that are used in a song that was release | June 2003 | '2003' | incorrect | 单 token 短答 '2003'（疑似错答，人工留意） |
| 427 | test | The Sanders-Brown Center on Aging was funded by a grant from | Kentucky Fried Chicken ( | 'The Sanders-Brown Center on Aging was funded by a ' | incorrect | gold 未命中 |
| 428 | test | Who did Muhummad Ali fight next, in Houston, after the so-ca | Jimmy Ellis | 'Joeman' | incorrect | 单 token 短答 'Joeman'（疑似错答，人工留意） |
| 429 | train | What kind of music do The Stone Roses and The Lemonheads pla | rock band | 'rock' | incorrect | 单 token 短答 'rock'（疑似错答，人工留意） |
| 430 | test | How many episodes were in the season of "Rick and Morty" tha | ten | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 431 | validation | Who was the biological father of the emperor who built the N | Germanicus | 'Nus' | incorrect | 单 token 短答 'Nus'（疑似错答，人工留意） |
| 432 | test | Elizabeth Austin wrote for a fitness magazine founded by who | Christine MacIntyre | 'Jack Johnson' | incorrect | gold 未命中 |
| 433 | train | The creators of the product designation TSR 2002 was the fir | role-playing game | 'role-playing game' | correct | gold 命中（含等价/别名） |
| 434 | train | Lakshmi Shankar is the mother-in-law of an acclaimed Indian  | Hindustani classical voc | 'vi' | format_failure | 单 token 函数词/碎片 'vi'，无答案内容 |
| 435 | train | What was the estimated population of the city that Luis Vill | 102,984 | '100,000' | incorrect | gold 未命中 |
| 436 | validation | What country of origin does Dana Ivey and Two Weeks Notice h | American | 'United States' | incorrect | gold 未命中 |
| 437 | train | Jasmin Geljo is known for his role in a 2005 post-apocalypti | George A. Romero | 'George Rodriguez' | incorrect | gold 未命中 |
| 438 | validation | In what year was the scientific journal for which Danilo Err | 1952 | '1968' | incorrect | 单 token 短答 '1968'（疑似错答，人工留意） |
| 439 | validation | Where does Yannick Ferreira Carrasco play home games? | Wanda Metropolitano | 'W' | format_failure | 单 token 函数词/碎片 'W'，无答案内容 |
| 440 | test | Which is the busiest airport in the United Kingdom outside o | Gatwick Airport | 'Ededs Airport' | incorrect | gold 未命中 |
| 441 | train | What honor has been received by both a former NASA Astronaut | National Aviation Hall o | 'Gold' | incorrect | 单 token 短答 'Gold'（疑似错答，人工留意） |
| 442 | test | The 2017–18 Wigan Athletic F.C. season will be a year in whi | Carabao Cup | 'TheFL Cup' | incorrect | gold 未命中 |
| 443 | train | U.S. Representative Mike Conaway is investigating interferen | 2016 United States elect | 'US elections' | incorrect | gold 未命中 |
| 444 | test | Which actor/actress from Overnight Delivery was born in New  | Reese Witherspoon | 'John Long' | incorrect | gold 未命中 |
| 445 | test | Are the writing from Maurice Level and Alice Hoffman focused | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 446 | train | Which author influenced the animated Easter television speci | Margery Williams | 'Peteratrix' | incorrect | 单 token 短答 'Peteratrix'（疑似错答，人 |
| 447 | test | How many Golden Globe Awards did this English retired actres | two Golden Globe Awards | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 448 | train | What award did the writer of Never Let Me Go novel win in 19 | Man Booker Prize for Fic | 'Man Booker Prize' | correct | gold 命中（含等价/别名） |
| 449 | train | In which period was this German composer, pianist, organist  | early Romantic period | 'Romantic' | incorrect | 单 token 短答 'Romantic'（疑似错答，人工留 |
| 450 | train | The magazine that nominated George Rainsford for their Best  | Tuesday | 'Thursday' | incorrect | 单 token 短答 'Thursday'（疑似错答，人工留 |
| 451 | train | George Borba was part of the team that competed at what 1970 | FIFA World Cup | 'World Cup' | correct | gold 命中（含等价/别名） |
| 452 | train | What was the formative year for the company eventually repla | 1858 | '1859' | incorrect | 单 token 短答 '1859'（疑似错答，人工留意） |
| 453 | test | The world's greatest Super-Heroes anthology showcased one of | Captain Marvel | 'Captain Marvel' | correct | gold 命中（含等价/别名） |
| 454 | train | Who had more of their English novels turned into Oscar-nomin | Two of his novels, "The  | 'Raja Rao' | incorrect | gold 未命中 |
| 455 | train | On what part of U.S Route 56 can you listen to the KCTV? | The highway's eastern te | 'Kansas' | incorrect | 单 token 短答 'Kansas'（疑似错答，人工留意） |
| 456 | validation | Umaru Mutallab had a son who tried to detonate materials abo | December 25, 2009 | 'December 25, 2009' | correct | gold 命中（含等价/别名） |
| 457 | train | Barnstable County Hospital was the location of the autopsy o | Caroline Kennedy | 'Robert F Kennedy' | incorrect | gold 未命中 |
| 458 | train | Are both Duke Energy and Affiliated Managers Group based in  | no | 'No' | correct | gold 命中（含等价/别名） |
| 459 | train | "Show 'Em (What You're Made Of)" is a song written by a grou | Kentucky Music Hall of F | 'Country Music Hall of Fame' | incorrect | gold 未命中 |
| 460 | train | What party was the secretary of commerce and housing under t | Republican | 'Republican' | correct | gold 命中（含等价/别名） |
| 461 | train | Before I Go to Sleep stars an Australian actress, producer a | singer | 'cominger' | incorrect | 单 token 短答 'cominger'（疑似错答，人工留 |
| 462 | train | WrestleMania XXX took place at the home venue of which Natio | New Orleans Saints | 'Chicago Bears' | incorrect | gold 未命中 |
| 463 | test | Who was involved in the arrest of Dread Pirate Roberts? | Christopher "Chris" Tarb | 'The FBI' | incorrect | gold 未命中 |
| 464 | validation | Let Mother Earth Speak's Native American activist was born w | Leech Lake Indian Reserv | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 465 | train | What county is Keene High School located in? | Cheshire County | 'H' | format_failure | 单 token 函数词/碎片 'H'，无答案内容 |
| 466 | train | Which British first-generation jet-powered medium bomber was | English Electric Canberr | ' Canberra Canberra' | incorrect | gold 未命中 |
| 467 | test | Black Book starred the actress and writer of what heritage? | Dutch | 'Ir' | format_failure | 单 token 函数词/碎片 'Ir'，无答案内容 |
| 468 | train | Kingdom Hearts 358/2 Days was made by the company based in w | Shinjuku | 'Shibuya' | incorrect | 单 token 短答 'Shibuya'（疑似错答，人工留意 |
| 469 | train | When was the novella written whose film adaptation was playe | 1843 | '1843' | correct | gold 命中（含等价/别名） |
| 470 | train | In what year was the British actress who starred in a film a | 9 November 1955 | '1967' | incorrect | 单 token 短答 '1967'（疑似错答，人工留意） |
| 471 | train | Riaz-Ur-Rehman Saghar wrote songs for the Pakistani singer w | The Kennedy Center | 'The Square Garden' | incorrect | gold 未命中 |
| 472 | train | Jayaraj made the 2016 epic historical drama that is an adapt | Macbeth | 'Macbeth' | correct | gold 命中（含等价/别名） |
| 473 | test | Mexican Indignados Movement is a response to a war also know | Mexican War on Drugs | 'Cold War' | incorrect | gold 未命中 |
| 474 | train | Both Hatter and March Hare are characters in which book? | Alice's Adventures in Wo | 'Alice in Wonderland' | incorrect | gold 未命中 |
| 475 | train | The Westchester Knicks are a basketball team in a minor leag | National Basketball Deve | 'AmericanBA' | incorrect | 单 token 短答 'AmericanBA'（疑似错答，人 |
| 476 | test | Lafe Pence was a member of which lower chamber of the United | United States House of R | 'House' | incorrect | 单 token 短答 'House'（疑似错答，人工留意） |
| 477 | test | Jimmy D'Arcy played in Northern Ireland for the team based i | Antrim | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 478 | train | What type of magazine is Eugene Habecker the chairman of? | evangelical Christian pe | 'Business' | incorrect | 单 token 短答 'Business'（疑似错答，人工留 |
| 479 | train | What does Age of Chance and Vector share in common? | was a rock band | 'Video' | incorrect | 单 token 短答 'Video'（疑似错答，人工留意） |
| 480 | train | What religion is the composer for India's first science fict | Hindi | 'H' | format_failure | 单 token 函数词/碎片 'H'，无答案内容 |
| 481 | train | Why did the CEO of the football team based in Denver, Colora | due to the onset and pro | 'Health' | incorrect | 单 token 短答 'Health'（疑似错答，人工留意） |
| 482 | test | Were both Peter Duffell and Fred Niblo actors? | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 483 | train | A private university that beat Georgetown during a basketbal | Marietta | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 484 | train | Have Tionne Watkins and Park So-yeon both been members of a  | yes | 'Yes, Tionne Watkins and Park So-yeon have both bee' | correct | gold 命中（含等价/别名） |
| 485 | train | What is the name of the second largest car rental company, t | Hertz | 'Aertz' | incorrect | 单 token 短答 'Aertz'（疑似错答，人工留意） |
| 486 | test | What Minnesota county is the University of Minnesota in? | Hennepin County | 'H' | format_failure | 单 token 函数词/碎片 'H'，无答案内容 |
| 487 | test | In Ancient Egyptian religion how would a citizen be weighted | against the feather of t | 'a' | format_failure | 单 token 函数词/碎片 'a'，无答案内容 |
| 488 | validation | The Death of Cook depicts the death of James Cook at a bay o | Kona coast | 'New Zealand' | incorrect | gold 未命中 |
| 489 | test | Jamie Harris is best known for his role as The Hook-Handed M | Brad Silberling | 'John Jackson' | incorrect | gold 未命中 |
| 490 | validation | What area once connected Great Britain to continental Europe | Doggerland | 'Doggerland' | correct | gold 命中（含等价/别名） |
| 491 | test | Muslim Mahammad oglu Magomayev is the grandfther of what Sov | Muslim Magometovich Mago | 'Rammad Magomayev' | incorrect | gold 未命中 |
| 492 | train | What is the name of the region that includes the cities Dove | Seacoast Region | 'Southern Region' | incorrect | gold 未命中 |
| 493 | test | What profession does John Landis and Gore Verbinski have in  | director | 'filmors' | incorrect | 单 token 短答 'filmors'（疑似错答，人工留意 |
| 494 | test | Did the Sandy and Beaver Canal remain operational until a la | no | 'No' | correct | gold 命中（含等价/别名） |
| 495 | train | Which feature does the G-shock watch have that is tested by  | water resistance | 'Water resistance' | correct | gold 命中（含等价/别名） |
| 496 | train | National Strategy for Homeland Security was a response to th | Pentagon | 'The Pentagon' | correct | gold 命中（含等价/别名） |
| 497 | train | What city was the capital of the Ostrogothic Kingdom and the | Ravenna (] , also locall | 'Ran' | incorrect | 单 token 短答 'Ran'（疑似错答，人工留意） |
| 498 | train | Shannon Purser played the role of June Acosta in a 2017 horr | John R. Leonetti | 'James Wan' | incorrect | gold 未命中 |
| 499 | train | Jim Atchison was the President of the theme park that had he | Orlando | 'Or' | format_failure | 单 token 函数词/碎片 'Or'，无答案内容 |
| 500 | validation | The 1966 Football League Cup Final was contested with which  | West Bromwich Albion Foo | 'West City' | incorrect | gold 未命中 |
| 501 | test | Channel 8 has broadcast which American sports series that pr | HBO World Championship B | 'Monday Night Football' | incorrect | gold 未命中 |
| 502 | train | What is the height of the player who won the 2015 AFL Rising | 1.95 m | '188 cm' | incorrect | gold 未命中 |
| 503 | train | Driven To Perform has a sponsor that includes the electronic | Canada | 'Japan' | incorrect | 单 token 短答 'Japan'（疑似错答，人工留意） |
| 504 | test | The 1966–67 NHL season ended with a win in the Stanley Cup b | Atlantic | 'Atlantic Division' | correct | gold 命中（含等价/别名） |
| 505 | test | which league is the 121th season of top-tier competitive foo | 2017–18 Swiss Super Leag | 'Super' | incorrect | 单 token 短答 'Super'（疑似错答，人工留意） |
| 506 | test | What is the National Grape Cooperative Association classifie | An agricultural cooperat | 'non' | incorrect | 单 token 短答 'non'（疑似错答，人工留意） |
| 507 | train | What date was the person born that Samuel Flores Borrego was | 1 August 1971 | '17 October 1930' | incorrect | gold 未命中 |
| 508 | train | Are both Alabama Slammer and Yorsh non alcoholic drinks? | no | 'Yes' | incorrect | 单 token 短答 'Yes'（疑似错答，人工留意） |
| 509 | validation | What series did William Hopke play in for the Detroit Tigers | 1909 Cuban-American Majo | 'World Series' | incorrect | gold 未命中 |
| 510 | test | Hey Ya is a song performed on The Ed Sullivan Show on CBS by | is a song written and pr | 'OutKast' | incorrect | 单 token 短答 'OutKast'（疑似错答，人工留意 |
| 511 | test | What is the name of the murder victim that worked in a resta | Ron Goldman | 'John Brown' | incorrect | gold 未命中 |
| 512 | train | Ambrose Mendy has managed and/or advised a British professio | "The Ring" magazine | 'The RingBC' | incorrect | gold 未命中 |
| 513 | train | Immanuel Lutheran School is affiliated with the denomination | 2.1 million | 'one million' | incorrect | gold 未命中 |
| 514 | test | What was the manager for the 1891 Cincinnati Kelly's Killers | $10,000 Kelly | 'Charlie Kelly' | incorrect | gold 未命中 |
| 515 | train | What organization does Rosyth Dockyard and Queen Elizabeth-c | Navy | 'Royal Navy' | correct | gold 命中（含等价/别名） |
| 516 | train | Erving Goffman was cited as higher than a literary critic on | The Times Higher Educati | 'Google' | incorrect | 单 token 短答 'Google'（疑似错答，人工留意） |
| 517 | train | What genre did the writer whose novel was based on "I'll Tak | romance genre | 'com' | incorrect | 单 token 短答 'com'（疑似错答，人工留意） |
| 518 | train | Who was the founder of a chain of supermarkets that is now h | Joseph E. Grosberg | 'John Johnson' | incorrect | gold 未命中 |
| 519 | validation | Fred Mace played for which English football club in 1919? | Stalybridge Celtic Footb | 'Ever United' | incorrect | gold 未命中 |
| 520 | train | Who was the recipient of a prize also given to a player for  | Rivaldo of Milan | 'Davidao' | incorrect | 单 token 短答 'Davidao'（疑似错答，人工留意 |
| 521 | train | Reveille Park is the eighth album by which American rapper b | South Park Mexican | 'Ice-Z' | incorrect | 单 token 短答 'Ice-Z'（疑似错答，人工留意） |
| 522 | test | In which city were the olympic games held in which Willi Meu | Berlin, Germany | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 523 | train | What actor played the male lead in a teen comedy about a hig | Patrick Dempsey | 'John Black' | incorrect | gold 未命中 |
| 524 | train | Is The Devils of Loudun and Maskarade both operas? | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 525 | train | Faces is a mixtape that features guest appearances from an A | Country Thuggin | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 526 | test | In the 2011 census what was the population of suburban area  | 26,788 | '10,000' | incorrect | gold 未命中 |
| 527 | test | What collaboration with DJ Muggs did Gary Grice participate  | Grandmasters | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 528 | validation | Both the Pulandian District and Hailar District are located  | China | 'China' | correct | gold 命中（含等价/别名） |
| 529 | test | The Companions were the first of what type of cavalry? | Shock troops | 'heavy cavalry' | incorrect | gold 未命中 |
| 530 | train | Who was a Christian Evangelist and US prisoner of war surviv | Louis "Louie" Zamperini | 'John Johnson' | incorrect | gold 未命中 |
| 531 | train | Which Oxford University graduate did Midge Mackenzie intervi | Kate Millett | 'Emily Thomas' | incorrect | gold 未命中 |
| 532 | train | How many laps did Harry Prowell run during the 10,000 metres | 25 laps | '2' | format_failure | 单 token 函数词/碎片 '2'，无答案内容 |
| 533 | train | The host of PokerFace is from where? | Newcastle upon Tyne, Eng | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 534 | train | Aleksandras Stulginskis' successor held office between what  | 7 June 1926 to 17 Decemb | '2014-2019' | incorrect | 单 token 短答 '2014-2019'（疑似错答，人工 |
| 535 | validation | What is the nickname of the singer with which Castor McCord  | Satchmo | 'Big' | incorrect | 单 token 短答 'Big'（疑似错答，人工留意） |
| 536 | test | Gül Mosque and Hippodrome of Constantinople are both located | Istanbul, Turkey | 'Turkeystanbul' | incorrect | 单 token 短答 'Turkeystanbul'（疑似错 |
| 537 | train | Are Danie Visser and Oliver Marach both Grand Slam tennis to | no | 'No' | correct | gold 命中（含等价/别名） |
| 538 | train | What year was the bank famously opposed by Brendan Bracken f | 1694 | '1870' | incorrect | 单 token 短答 '1870'（疑似错答，人工留意） |
| 539 | validation | What movie did John Gavin Malkovich play in with Matt Damon  | Rounders | 'Good Will Hunting' | incorrect | gold 未命中 |
| 540 | validation | which Australian politician represented Electoral district o | Jane Goward | 'John Wilson' | incorrect | gold 未命中 |
| 541 | test | Where did the hijacked plane rammed by Heather Penney crash? | Pennsylvania | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 542 | validation | What is in both the Lithocarpus and Duranta species? | trees | 'family' | incorrect | 单 token 短答 'family'（疑似错答，人工留意） |
| 543 | validation | Jordan's Furniture is a furniture retailer with a location i | the junction with Inters | 'North' | incorrect | 单 token 短答 'North'（疑似错答，人工留意） |
| 544 | train | Is it correct to state that Tetrapanax is an evergreen shrub | yes | 'yes' | correct | gold 命中（含等价/别名） |
| 545 | train | Chantal Thomas wrote a book that was turned into a 2012 film | Benoît Jacquot | 'John Thomas' | incorrect | gold 未命中 |
| 546 | train | Which of the actress starred in Zombie Night appeared in the | Jennifer Taylor | 'Tina King' | incorrect | gold 未命中 |
| 547 | train | What is the gross leasable area of the shopping mall served  | 1800000 sqft | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 548 | validation | Are Euptelea and Muehlenbeckia both genuses? | yes | 'Yes' | correct | gold 命中（含等价/别名） |
| 549 | train | Which of Mabel Keyes Babcock's distant relatives wrote "Of P | William Bradford | 'William Bradford' | correct | gold 命中（含等价/别名） |
| 550 | train | What Albanian department is reasonbile for an international  | Ministry of European Int | 'Department of Defence' | incorrect | gold 未命中 |
| 551 | validation | Pajottenland has historically provided beers that include ar | Zenne | 'Theine Valley' | incorrect | gold 未命中 |
| 552 | train | Luke Null is an actor who was on the program that premiered  | September 30, 2017 | 'September 17, 2018' | incorrect | gold 未命中 |
| 553 | train | Alexander S. Wadsworth served during the war that was faught | United States, the Unite | 'England and France' | incorrect | gold 未命中 |
| 554 | train | Baltic Neopaganism was a religious movement that included wh | Vilius Storostas-Vydūnas | 'Johnau' | incorrect | 单 token 短答 'Johnau'（疑似错答，人工留意） |
| 555 | train | Which composer was wrote his music most recently, Michael Ti | Michael Kemp Tippett | 'Michael Tippett' | incorrect | gold 未命中 |
| 556 | train | What did both Karel Bossart and Sergei Korolev design? | rocket | 'spacecraft' | incorrect | 单 token 短答 'spacecraft'（疑似错答，人 |
| 557 | train | The man known as the voice of "Elgar" voices the English cha | Love Hina | 'El' | format_failure | 单 token 函数词/碎片 'El'，无答案内容 |
| 558 | test | Which actor does American Beauty and American Beauty have in | Kevin Spacey | 'Kevin Spacey' | correct | gold 命中（含等价/别名） |
| 559 | test | The Hip Hop Republican was credited with giving blacks empha | 2008 | '2000' | incorrect | 单 token 短答 '2000'（疑似错答，人工留意） |
| 560 | train | Camp Modin moved to the Belgrade Lakes region of Maine from  | Somerset County | 'Clin' | incorrect | 单 token 短答 'Clin'（疑似错答，人工留意） |
| 561 | test | Michael J. Hunter replaced the lawyer who became the adminis | EPA | 'Social Security Administration' | incorrect | gold 未命中 |
| 562 | test | What is the primary role of the position played by Viktor Ra | prevent the opposing tea | 'Viktor Raychev plays as a central-back for Lokomot' | incorrect | gold 未命中 |
| 563 | test | Stephen Joseph Bercik was mayer of a city that had a populat | 129,007 | '124,969' | incorrect | gold 未命中 |
| 564 | train | who is a British physicist and also a British government's c | Frederick Alexander | 'Sir David King' | incorrect | gold 未命中 |
| 565 | test | Who were the stars of the 2008 South Korean movie that was l | Kim Yoon-seok and Ha Jun | 'Mur' | incorrect | 单 token 短答 'Mur'（疑似错答，人工留意） |
| 566 | train | What genre was the movie that Austin Nichols was in with Kir | romantic comedy | 'Actionedy' | incorrect | 单 token 短答 'Actionedy'（疑似错答，人工 |
| 567 | test | One of the actors in the film Dhruva Natchathiram was awarde | 2011 | '2010' | incorrect | 单 token 短答 '2010'（疑似错答，人工留意） |
| 568 | test | where is the American professional basketball team which Jal | Louisiana. | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 569 | test | The M1919 and the M1 was used by what military? | U.S. | 'United States' | incorrect | gold 未命中 |
| 570 | validation | What is the name of the person that named Moltke Nunatak aft | Second German Antarctic  | 'Johnne' | incorrect | 单 token 短答 'Johnne'（疑似错答，人工留意） |
| 571 | test | Which town is the venue, in which the APRA Music Awards of 2 | New South Wales | 'Sydney' | incorrect | 单 token 短答 'Sydney'（疑似错答，人工留意） |
| 572 | train | Gorgoroth is a band based in which Norwegian county? | Hordaland | 'Osder' | incorrect | 单 token 短答 'Osder'（疑似错答，人工留意） |
| 573 | validation | When did the mother of Joseph Ferdinand Leopold of Bavaria d | 1692 | '1840' | incorrect | 单 token 短答 '1840'（疑似错答，人工留意） |
| 574 | validation | Is The Stuff of Legend and Babes in Toyland both entertainme | by | 'Yes' | incorrect | 单 token 短答 'Yes'（疑似错答，人工留意） |
| 575 | train | Carroll County, Ohio is named after the only Catholic signat | Charles Carroll of Carro | 'Charles Carroll' | correct | gold 命中（含等价/别名） |
| 576 | test | Who was a member of "Cheney", who won 'Song of the Year' in  | Christopher John Cheney | 'Chris Cheney' | incorrect | gold 未命中 |
| 577 | train | In what corner of Missouri is radio station WMBH located? | southwestern | 'North' | incorrect | 单 token 短答 'North'（疑似错答，人工留意） |
| 578 | train | Are the Laleli Mosque and Esma Sultan Mansion located in the | no | 'No, the Laleli Mosque and Esma Sultan Mansion are ' | correct | gold 命中（含等价/别名） |
| 579 | validation | The Cleveland Thyagaraja Festival is a type of festival that | Telugu | 'Tugu' | incorrect | 单 token 短答 'Tugu'（疑似错答，人工留意） |
| 580 | train | In which county does the 8th Military Police Brigade of the  | Honolulu | 'K County' | incorrect | gold 未命中 |
| 581 | train | When was one of the teacher of Nikolai Lugansky died who was | 1924November 22, 1993 | '1945' | incorrect | 单 token 短答 '1945'（疑似错答，人工留意） |
| 582 | train | What IBF Light Flyweight Championship winner was related to  | Ricardo “El Finito” Lópe | 'Omar Martinez' | incorrect | gold 未命中 |
| 583 | validation | American Blues included the drummer from which American rock | ZZ Top | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 584 | train | When was one of the science fiction survival horror video ga | 22 September 2015 | '2000' | incorrect | 单 token 短答 '2000'（疑似错答，人工留意） |
| 585 | validation | What nationality is the singer who recorded "Who I Was Born  | Scottish | 'The singer who recorded "Who I Was Born to Be" is ' | incorrect | gold 未命中 |
| 586 | validation | What cartel drug lord with the reputation as "The King of Co | Pablo Escobar | 'Pablo Escobar' | correct | gold 命中（含等价/别名） |
| 587 | test | Are both Cypress and Ajuga genera? | no | 'Yes' | incorrect | 单 token 短答 'Yes'（疑似错答，人工留意） |
| 588 | train | The 2014 All-Pac-12 Conference football team featured player | Mark Helfrich | 'Mike' | incorrect | 单 token 短答 'Mike'（疑似错答，人工留意） |
| 589 | train | Where will the student which pass the exam for which Le Rêve | secondary school study | 'high school' | incorrect | gold 未命中 |
| 590 | train | Fodder on My Wings is an album by a singer/pianist/songwrite | 1933 | '1950' | incorrect | 单 token 短答 '1950'（疑似错答，人工留意） |
| 591 | train | Which organization has been led by the overseer of the Renew | Northern Ireland Assembl | 'HM' | format_failure | 单 token 函数词/碎片 'HM'，无答案内容 |
| 592 | test | Which amusement park at Coney Island, Brooklyn, New York Cit | Steeplechase Park | 'Cland Park' | incorrect | gold 未命中 |
| 593 | train | David Sinclair is a fictional character in "Numb3rs", a crim | CBS Corporation | 'CBS' | incorrect | 单 token 短答 'CBS'（疑似错答，人工留意） |
| 594 | validation | The Actaea genus is native to what continent that the Onocle | Europe | 'North' | incorrect | 单 token 短答 'North'（疑似错答，人工留意） |
| 595 | test | Where in London was the 2012 Olympic event featuring athlete | ExCeL Exhibition Centre | 'West' | incorrect | 单 token 短答 'West'（疑似错答，人工留意） |
| 596 | test | La Yesca Dam was inaugurated by which Mexican politiician an | Felipe de Jesús Calderón | 'Vicente Fox' | incorrect | gold 未命中 |
| 597 | validation | What made the man who abolished the Consell in 1718 resume t | upon his son's death | 'a' | format_failure | 单 token 函数词/碎片 'a'，无答案内容 |
| 598 | train | Socialist conferences were held with what countries that opp | The Allies of World War  | 'Great' | incorrect | 单 token 短答 'Great'（疑似错答，人工留意） |
| 599 | validation | In what city is the mortgage lending company, founded by Dan | Detroit, Michigan | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 600 | train | The Secret of Moonacre was directed by the founder of which  | Klasky Csupo | 'Pixworks' | incorrect | 单 token 短答 'Pixworks'（疑似错答，人工留 |
| 601 | test | What novel imagines the true story of a character based on a | Shohola Falls | 'Huckleberry Finn' | incorrect | gold 未命中 |
| 602 | test | What film directed by David Greene did Merrell Jackson play  | Godspell | 'The Apostles' | incorrect | gold 未命中 |
| 603 | validation | the movie "A Cure for Wellness" was a science fiction? | is a 2016 science fictio | 'No' | format_failure | 单 token 函数词/碎片 'No'，无答案内容 |
| 604 | train | Brindisi, the city where Louis-Jean-Nicolas Lejoille died, i | Italy | 'Italy' | correct | gold 命中（含等价/别名） |
| 605 | train | How did the chairman of the Luthuanian Union of Actors discr | one of Lithuania's most  | 'gen' | incorrect | 单 token 短答 'gen'（疑似错答，人工留意） |
| 606 | train | Cherie Currie and Steve Augeri were both what? | American musician | 'musicians' | incorrect | 单 token 短答 'musicians'（疑似错答，人工 |
| 607 | train | What was the occupation of the man who published an individu | American schoolteacher a | 'Journalist' | incorrect | 单 token 短答 'Journalist'（疑似错答，人 |
| 608 | test | What type of product is the sponsor of the Premiership Rugby | pale lager | 'beer' | incorrect | 单 token 短答 'beer'（疑似错答，人工留意） |
| 609 | train | In what year was the uprising that marred John P. Buchanan's | 1891 | '1857' | incorrect | 单 token 短答 '1857'（疑似错答，人工留意） |
| 610 | validation | Which areas of the United States were still able to deny sam | American Samoa, but not  | 'Texas' | incorrect | 单 token 短答 'Texas'（疑似错答，人工留意） |
| 611 | validation | How old was Virginia Bruce when she starred in Let Freedom R | 29 | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 612 | train | Manchester, New Hampshire is a part of the Northeast megalop | Boston, Providence, Hart | 'Boston' | incorrect | 单 token 短答 'Boston'（疑似错答，人工留意） |
| 613 | train | My Neighbor Totoro was produced by a Japanese animation film | 1985 | '1949' | incorrect | 单 token 短答 '1949'（疑似错答，人工留意） |
| 614 | train | The Kansas City Wizards have had three home venues in Kansas | Arrowhead Stadium | 'Khead Stadium' | incorrect | gold 未命中 |
| 615 | train | Gérald Genta, a Swiss jewelllery designer, worked with what  | International Watch Co. | 'Iopard' | incorrect | 单 token 短答 'Iopard'（疑似错答，人工留意） |
| 616 | validation | WSCV's transmitter is located near this stadium located in w | Miami Gardens, Florida, | 'South' | incorrect | 单 token 短答 'South'（疑似错答，人工留意） |
| 617 | test | What two singers who worked together on the song I Would Lik | Johnny Cash, Waylon Jenn | 'The J South' | incorrect | gold 未命中 |
| 618 | train | what is the english name of Émile Verdets editorial? | Annals of Chemistry and  | 'The English name of Émile Verdets editorial is Ver' | incorrect | gold 未命中 |
| 619 | test | What screenplay was worked on by both Edward Carfagno and Mi | Julius Caesar | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 620 | train | The infantry rifle regiment of the British Army that Talaias | 1881 | '1856' | incorrect | 单 token 短答 '1856'（疑似错答，人工留意） |
| 621 | train | Thirukkalacherry is a village in which Indian town? | Tharangambadi | 'Churai' | incorrect | 单 token 短答 'Churai'（疑似错答，人工留意） |
| 622 | train | Northland Mall was the first directionally-named shopping ce | Westland Mall | 'Southland Mall' | incorrect | gold 未命中 |
| 623 | train | What band did both Delores Holmes and an inductee to the Roc | E Street Band | 'The Rolling' | incorrect | gold 未命中 |
| 624 | train | Muz-TV was launched before the 24-hour music channel that wa | Prof Media | 'MTV' | incorrect | 单 token 短答 'MTV'（疑似错答，人工留意） |
| 625 | validation | Are Water dropwort and Costus both in the family Apiaceae? | no | 'No' | correct | gold 命中（含等价/别名） |
| 626 | test | What genre of music was played by both Tappi Tíkarrass and I | rock | 'rock' | correct | gold 命中（含等价/别名） |
| 627 | train | What apartment complex originally constructed in 1927 is inc | Tudor City | 'The Dakota Hotel' | incorrect | gold 未命中 |
| 628 | validation | Lost in Time includes the theme song for a French/Japanese a | Savin Yeatman-Eiffel | 'Studioax' | incorrect | 单 token 短答 'Studioax'（疑似错答，人工留 |
| 629 | train | Which guitar brand was endorsed by the band centered by Ann  | Kramer Guitars | 'Epender' | incorrect | 单 token 短答 'Epender'（疑似错答，人工留意 |
| 630 | test | How long is the bridge in the Öresund Region that connect Co | 8 km | '7.5 km' | incorrect | gold 未命中 |
| 631 | validation | What company headquartered in Whitley, Coventry, United King | Jaguar Land Rover | 'N' | format_failure | 单 token 函数词/碎片 'N'，无答案内容 |
| 632 | train | When did the University, of which The Dove Marine Laboratory | 1963 | '1962' | incorrect | 单 token 短答 '1962'（疑似错答，人工留意） |
| 633 | train | Mehdi Hashemi was thought to be guilty of opposition to the  | Reagan | 'Re Carter' | incorrect | gold 未命中 |
| 634 | test | RL-83 Blindicide was an improved derivative of a wea[on laun | the United States Army | 'US States' | incorrect | gold 未命中 |
| 635 | train | Who was the fourth son of the lord of the Seventeen Province | Diego Félix of Austria | 'William V' | incorrect | gold 未命中 |
| 636 | validation | Dutch-born American businessman, Harry Koch, fathered a son  | Koch Industries | 'K Oil' | incorrect | gold 未命中 |
| 637 | train | High School Confidential, an eight part documentary followed | #364 | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 638 | test | Where does the founder of The International Grenfell Associa | Newfoundland and Labrado | 'Newland' | incorrect | 单 token 短答 'Newland'（疑似错答，人工留意 |
| 639 | train | What is the birthday of the actress who was the Duchess in " | 23 November 1946 | '10 August 1969' | incorrect | gold 未命中 |
| 640 | test | What is the birthday of the Earl of Merioneth? | 10 June 1921 | '17 October 1948' | incorrect | gold 未命中 |
| 641 | train | Who wrote the novel that the movie directed by Stanley Kubri | Stephen King | 'Stephen King' | correct | gold 命中（含等价/别名） |
| 642 | train | What other two divisions of Argentine forces were involved i | Army, Navy | '3rd Division' | incorrect | gold 未命中 |
| 643 | test | Morgan Paull played Dave Holden in a 1982 film loosely adapt | Philip K. Dick | 'Stephen King' | incorrect | gold 未命中 |
| 644 | train | When was the German actress born who is best known for her r | February 22, 1968 | '1970' | incorrect | 单 token 短答 '1970'（疑似错答，人工留意） |
| 645 | train | What movie did Pitof direct which had an action-adventure ti | Catwoman | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 646 | validation | Jennifer Ventimilia co-wrote the teleplay of the episode tha | sixth season | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 647 | train | When was the rock band to which Pre-Creedence name was chang | 1960s and early 1970s | '1968' | incorrect | 单 token 短答 '1968'（疑似错答，人工留意） |
| 648 | train | Jal Pari, which translated in another language refers to whi | A mermaid | 'water spirits' | incorrect | gold 未命中 |
| 649 | test | Roger O. Egeberg was Assistant Secretary for Health and Scie | 1969 until 1974 | '1981-1989' | incorrect | 单 token 短答 '1981-1989'（疑似错答，人工 |
| 650 | train | Which avant-garde Japanese composer studied with John Cage a | Toshi Ichiyanagi | 'David John Cage' | incorrect | gold 未命中 |
| 651 | train | The American restaurant chain, the Original House of Pies, i | orange juice | 'fruit juice' | incorrect | gold 未命中 |
| 652 | train | Did Qionghai or Suining have a population of 658,798 in 2002 | In 2002, Suining had a p | 'Suining' | incorrect | 单 token 短答 'Suining'（疑似错答，人工留意 |
| 653 | test | What son of Larry Johnson was born on November 19, 1979? | Larry Alphonso Johnson J | 'Larry Johnson' | incorrect | gold 未命中 |
| 654 | test | Rocket Rods was a high-speed thrill attraction opened in 199 | August 21, 1995 | '2000' | incorrect | 单 token 短答 '2000'（疑似错答，人工留意） |
| 655 | test | A Pair of Brown Eyes and Wild Mountain Thyme is based from w | Francis McPeake | 'Bob Cash' | incorrect | gold 未命中 |
| 656 | test | Are Benjamin Britten and Béla Bartók from the same country? | no | 'No, Benjamin Britten and Béla Bartók are not from ' | correct | gold 命中（含等价/别名） |
| 657 | train | Love Thy Neighbor starred an AMerican actor who was best kno | Three's Company | 'Happy Days' | incorrect | gold 未命中 |
| 658 | train | Astro Boy and The Secret of Kells share which genre of film? | Animation | 'animated' | incorrect | 单 token 短答 'animated'（疑似错答，人工留 |
| 659 | train | Both Tim Conlon and Kehinde Wiley have what type of occupati | artist | 'artist' | correct | gold 命中（含等价/别名） |
| 660 | train | Which American singer-songwriter toured with J.P. Doherty in | Debbie Harry | 'John Swift' | incorrect | gold 未命中 |
| 661 | test | Berk Communication and Marketing Group best known for repres | New York Yankees | 'Chicago' | incorrect | 单 token 短答 'Chicago'（疑似错答，人工留意 |
| 662 | train | How many records did Shane Lynch sell as a member of Boyzone | 25 million | 'Shane Lynch sold 8 million records as a member of ' | incorrect | gold 未命中 |
| 663 | train | Who was the lead character designer on "Pepper Ann", and the | Thomas Warburton | 'John Thompson' | incorrect | gold 未命中 |
| 664 | test | What platinum selling track was included on the album "The W | I'm Shipping Up to Bosto | 'The Highwayer' | incorrect | gold 未命中 |
| 665 | train | What production company is owned by the director of "She Hat | 40 Acres and a Mule Film | 'Focus Entertainment' | incorrect | gold 未命中 |
| 666 | train | When is the election held for the position former policy dir | November 6, 2018 | 'November' | incorrect | 单 token 短答 'November'（疑似错答，人工留 |
| 667 | train | When did the UVF Mid-Ulster Brigade conducted the attack The | 31 July 1975 | '1976' | incorrect | 单 token 短答 '1976'（疑似错答，人工留意） |
| 668 | train | In what year was the writer of "The Bet" born? | 1964 | '1871' | incorrect | 单 token 短答 '1871'（疑似错答，人工留意） |
| 669 | train | Which university Founded as a college in 1881 is Janet Beer  | The University of Liverp | 'Leiff University' | incorrect | gold 未命中 |
| 670 | test | What was the other Los Angeles team that the 1999 Clippers t | Los Angeles Lakers | 'Los Angeles Lakers' | correct | gold 命中（含等价/别名） |
| 671 | train | Who did President Franklin Roosevelt appoint that was respon | Robert Digges Wimberly C | 'John Roosevelt' | incorrect | gold 未命中 |
| 672 | test | When did former Yugoslav which Patricia Hy-Boulais eventuall | in 1994 | '1992' | incorrect | 单 token 短答 '1992'（疑似错答，人工留意） |
| 673 | train | Which CEO of FedEx becked Value America | Frederick Wallace "Fred" | 'Fred Smith' | correct | gold 命中（含等价/别名） |
| 674 | test | Which football player that topped the 10,000-yard career rus | Curtis James Martin Jr. | 'David Brady' | incorrect | gold 未命中 |
| 675 | test | What is the population of the town that starts with the lett | 15,023 | 'B' | format_failure | 单 token 函数词/碎片 'B'，无答案内容 |
| 676 | train | Charles Scribner's Sons publishes the books of what author w | Donald Richard "Don" DeL | 'Tom Clancy' | incorrect | gold 未命中 |
| 677 | train | What is the name of the record label owned by one of the thr | Dolly Records | 'CCA Records' | incorrect | gold 未命中 |
| 678 | validation | Are Parents and Madame Figaro published in the same country? | no | 'No' | correct | gold 命中（含等价/别名） |
| 679 | test | When is the national league which the Manchester United is p | 13 May 2018 | 'May' | incorrect | 单 token 短答 'May'（疑似错答，人工留意） |
| 680 | train | Which Canadian heavy metal band is Safe the second EP by | Kittie | 'R' | format_failure | 单 token 函数词/碎片 'R'，无答案内容 |
| 681 | train | What was the 2010 population of the town where Black Crescen | 310 | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 682 | train | in 1992 Spengler Cup all matches were played at the home are | HC Davos | 'Zur Lions' | incorrect | gold 未命中 |
| 683 | validation | When was the American actor, film director which Dana Brunet | July 26, 1959 | '1966' | incorrect | 单 token 短答 '1966'（疑似错答，人工留意） |
| 684 | train | Which former American football player had a part in the movi | Terry Crews | 'Will Johnson' | incorrect | gold 未命中 |
| 685 | train | Charlie McDermott plays Axl Heck on a tv show that premiered | September 30, 2009 | 'October 6, 2016' | incorrect | gold 未命中 |
| 686 | test | Which historical drama filmed in the Winter Palace of the Ru | Russian Ark | 'Winter' | incorrect | 单 token 短答 'Winter'（疑似错答，人工留意） |
| 687 | test | Typically how many pages were in the fiction magazine in whi | 128 pages | '62 pages' | incorrect | gold 未命中 |
| 688 | train | What reward did the founder of Chick-Fil-A receive? | Call to Service Award | 'National' | incorrect | 单 token 短答 'National'（疑似错答，人工留 |
| 689 | train | In which year was this public research university in which B | 1874 | '1865' | incorrect | 单 token 短答 '1865'（疑似错答，人工留意） |
| 690 | test | GamesMaster has a sister publicantion that is published how  | 13 | 'tw' | format_failure | 单 token 函数词/碎片 'tw'，无答案内容 |
| 691 | validation | Are both Frank Lloyd and Olivier Assayas American film direc | no | 'No' | correct | gold 命中（含等价/别名） |
| 692 | train | What English campaigner for the suffragette movement did Ang | Sylvia Pankhurst | 'Angela Down portrayed Emily Dav.' | incorrect | gold 未命中 |
| 693 | train | What month did the an online adult website whose last print  | January | 'October 2007' | incorrect | gold 未命中 |
| 694 | train | What did Phuture begin that spread to the United Kingdom and | acid-house | 'house house' | incorrect | gold 未命中 |
| 695 | test | What city has a football team and had a player from Pago Pag | He is from Pago Pago, Am | 'New' | incorrect | 单 token 短答 'New'（疑似错答，人工留意） |
| 696 | test | Are Peter Balakian and James Der Derian both teachers? | yes | 'No' | format_failure | 单 token 函数词/碎片 'No'，无答案内容 |
| 697 | test | Which author was a dentist, Zane Grey or Bhabananda Deka? | Pearl Zane Grey | 'Bhabananda Deka' | incorrect | gold 未命中 |
| 698 | train | When was the University established where Laura Landweber is | 1754 | '1867' | incorrect | 单 token 短答 '1867'（疑似错答，人工留意） |
| 699 | test | What was the name of the 1996 loose adaptation of William Sh | Tromeo and Juliet | 'Quick' | incorrect | 单 token 短答 'Quick'（疑似错答，人工留意） |
| 700 | validation | When did the the Antonine who was known as the third of the  | 24 January 76 – 10 July  | '2nd century' | incorrect | gold 未命中 |
| 701 | train | Chandamama and Kajal Aggarwal are both associated with which | Telugu and Tamil | 'Bollywood' | incorrect | 单 token 短答 'Bollywood'（疑似错答，人工 |
| 702 | train | Which Russian figure skating coach was a former competitive  | Nikolai Morozov | 'Alexander Ivanov' | incorrect | gold 未命中 |
| 703 | train | The Column of Saint Zanobi is a monumental marble column loc | a minor basilica | 'mon' | incorrect | 单 token 短答 'mon'（疑似错答，人工留意） |
| 704 | test | Thomas Tull produced the comedy movie The Hangover, which wa | Las Vegas | 'Las Vegas' | correct | gold 命中（含等价/别名） |
| 705 | train | The 1991–92 NBA season included an Achilles tendon injury to | Jacques Dominique Wilkin | 'Michael Jordan' | incorrect | gold 未命中 |
| 706 | test | When was the album released for which Lady Gaga used for mat | October 21, 2016 | '2016' | incorrect | 单 token 短答 '2016'（疑似错答，人工留意） |
| 707 | train | Are the genera Gordonia and Osbeckia in the same family? | no | 'Yes' | incorrect | 单 token 短答 'Yes'（疑似错答，人工留意） |
| 708 | train | In between Hymenosporum and Agrostemma which one is closely  | Hymenosporum flavum | 'Hymenosporum' | incorrect | 单 token 短答 'Hymenosporum'（疑似错答 |
| 709 | test | Are Ian Brown and Dee Snider both actors? | no | 'No' | correct | gold 命中（含等价/别名） |
| 710 | test | Who had a perfect game against The Ignitor's team in 1998? | David Wells | 'David Johnson' | incorrect | gold 未命中 |
| 711 | test | The author of Sexual Politics attended which British Univers | Oxford | 'Obridge University' | incorrect | gold 未命中 |
| 712 | train | How many people did the South Korean spree killer which NICS | 32 people | '5' | format_failure | 单 token 函数词/碎片 '5'，无答案内容 |
| 713 | train | How many records has the singer which Robert Gale tour with  | 140 million records | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 714 | train | Who recorded the song written by Johnny Russell | Buck Owens | 'Johnny Cash' | incorrect | gold 未命中 |
| 715 | train | Which former mill town is near Rivington Hall Barn? | Bolton | 'Oldley' | incorrect | 单 token 短答 'Oldley'（疑似错答，人工留意） |
| 716 | train | Which American popular music and country music singer record | Linda Maria Ronstadt | 'John Cash' | incorrect | gold 未命中 |
| 717 | train | Are both Stephen R. Donaldson and Michael Moorcock science f | yes | 'Yes, both Stephen R. Donaldson and Michael Moorcoc' | correct | gold 命中（含等价/别名） |
| 718 | train | What airport serviced by American Airlines Shuttle, is also  | Logan International Airp | ' Logan International Airport' | correct | gold 命中（含等价/别名） |
| 719 | train | Where is the group of islands named after Purdue University' | the northwest tip of Can | 'Newaska' | incorrect | 单 token 短答 'Newaska'（疑似错答，人工留意 |
| 720 | train | What is the name of the film directed by Alex Cox adapted fr | Revengers Tragedy | 'The Dutchess' | incorrect | gold 未命中 |
| 721 | train | "Twenty Two" is an episode of the series "The Twilight Zone. | What's My Line | 'Twenty Game' | incorrect | gold 未命中 |
| 722 | test | Tommy's Honour was a drama film that included the actor who  | War & Peace | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 723 | train | The creek of which Paradise Creek is a tributary is a tribut | Delaware River | 'Caware River' | incorrect | gold 未命中 |
| 724 | train | Who created the show with Wendy Schaal doing the voice of Fr | Seth MacFarlane | 'Adam Smith' | incorrect | gold 未命中 |
| 725 | test | What type of veterinary specialist is the star veterinarian  | neuro-orthopaedic | 'ainary surgeon' | incorrect | gold 未命中 |
| 726 | train | Sporobolus and Zea are in the same what? | family | 'gen' | incorrect | 单 token 短答 'gen'（疑似错答，人工留意） |
| 727 | train | Which of the campaign that brought out the term Vichy Republ | presidential campaign of | 'Trump' | incorrect | 单 token 短答 'Trump'（疑似错答，人工留意） |
| 728 | train | What county was Matt Herr raised in? | Bergen | 'Mar County' | incorrect | gold 未命中 |
| 729 | validation | When is the football club which Stan Spinks played for found | in 1902 | '1887' | incorrect | 单 token 短答 '1887'（疑似错答，人工留意） |
| 730 | train | Who is the Chief Executive Officer of the corporation that o | Fatih Ozmen | 'Tim Musk' | incorrect | gold 未命中 |
| 731 | train | Which Disneyland attraction is Matterhorn Bobsleds roller co | Autopia | 'Big Space Mountain' | incorrect | gold 未命中 |
| 732 | validation | In what basketball position does the brother of Saulius Kuzm | small forward | 'Guard' | incorrect | 单 token 短答 'Guard'（疑似错答，人工留意） |
| 733 | test | What player was the first overall pick in the 2004 NFL draft | Eli Manning | ' Eli Manning' | correct | gold 命中（含等价/别名） |
| 734 | test | Which star of The Human Stain was born in 1937? | Anthony Hopkins | 'John Williams' | incorrect | gold 未命中 |
| 735 | test | Who is the father of the king who attempted to have Eardwulf | Æthelwald Moll | 'Albert' | incorrect | 单 token 短答 'Albert'（疑似错答，人工留意） |
| 736 | train | Michaël Llodra of France, called "the best volleyer on tour" | Argentinian | 'Argentine' | incorrect | 单 token 短答 'Argentine'（疑似错答，人工 |
| 737 | train | The Sentinelese language is the language of people of one of | Andaman Islands | 'Andaman Island' | incorrect | gold 未命中 |
| 738 | train | Name an American actress who starred both in High School Hig | Tia Carrere | 'Amber Rose' | incorrect | gold 未命中 |
| 739 | train | What was Thomas Boutflower Bennet's role at The Collegiate S | schoolmaster at J. L. Yo | 'Headmaster' | incorrect | 单 token 短答 'Headmaster'（疑似错答，人 |
| 740 | validation | What South Australian capital held UFC Fight Night 65 in May | Adelaide | 'Adelaide' | correct | gold 命中（含等价/别名） |
| 741 | train | When was the club formed, for which Adam Johnson played as w | 1919 | '1992' | incorrect | 单 token 短答 '1992'（疑似错答，人工留意） |
| 742 | train | Who manages the Laboratory that ran the Aurora Generator Tes | Battelle Energy Alliance | 'John' | incorrect | 单 token 短答 'John'（疑似错答，人工留意） |
| 743 | test | When was the English rock band formed that's first recording | June 1975 | '1968' | incorrect | 单 token 短答 '1968'（疑似错答，人工留意） |
| 744 | test | What year was the major Roman road built that connects to th | 95 AD | '200 BC' | incorrect | gold 未命中 |
| 745 | validation | When was the company that produced rectangular crackers that | 1853 | '1897' | incorrect | 单 token 短答 '1897'（疑似错答，人工留意） |
| 746 | test | What was the other name for the war between the Cherokee peo | Chickamauga Wars | 'The Creek War' | incorrect | gold 未命中 |
| 747 | validation | What is the population of the city in Colombia where Carlos  | 3.7 million | '400,000' | incorrect | gold 未命中 |
| 748 | train | Which British music producer and engineer is notable for wor | Gareth Jones | 'Alan Clarke' | incorrect | gold 未命中 |
| 749 | train | Which character does this protagonist, who secretly loves an | Tybalt | 'Mercutio' | incorrect | 单 token 短答 'Mercutio'（疑似错答，人工留 |
| 750 | validation | The subject of the biography "Name Dropper" was born in what | 1961 | '1900' | incorrect | 单 token 短答 '1900'（疑似错答，人工留意） |
| 751 | train | Bridgewater Trustees major source of income came from a cana | Francis Egerton | 'John Bridgewater' | incorrect | gold 未命中 |
| 752 | train | What was Sophia Dallas' husbands name who served under the 1 | Vice President George | 'John Dallas' | incorrect | gold 未命中 |
| 753 | train | Carl Barks is best known for his comics about the cartoon ch | 1934 | '1934' | correct | gold 命中（含等价/别名） |
| 754 | train | This aircraft carrier served as a recovery ship for this fli | three | 'tw' | format_failure | 单 token 函数词/碎片 'tw'，无答案内容 |
| 755 | train | Which Eminem album included vocals from a singer who had an  | "The Marshall Mathers LP | 'Reapse' | incorrect | 单 token 短答 'Reapse'（疑似错答，人工留意） |
| 756 | train | The Bart the Fink episode of The Simpsons aired in February  | The Itchy & Scratchy Sho | 'Captain' | incorrect | 单 token 短答 'Captain'（疑似错答，人工留意 |
| 757 | train | The revue Putting It Together was devised by Stephen Sondhei | Julia McKenzie | 'Emily Smith' | incorrect | gold 未命中 |
| 758 | train | YouPorn was surpassed, in 2013, by competitor sites xHamster | XVideos | 'XHub' | incorrect | 单 token 短答 'XHub'（疑似错答，人工留意） |
| 759 | test | An Austrian-British psychoanalyst born in 1882 and innovativ | Morita therapy | 'group therapy' | incorrect | gold 未命中 |
| 760 | test | Kam Heskin plays Paige Morgan in a 2004 film directed by who | Martha Coolidge | 'John Scott' | incorrect | gold 未命中 |
| 761 | train | What was the given name of the singer who is most closely as | William Howard Ashton, | 'John' | incorrect | 单 token 短答 'John'（疑似错答，人工留意） |
| 762 | test | Father Jean-Pierre Aulneau de le Touche was killed before he | North Dakota | 'North Dakota' | correct | gold 命中（含等价/别名） |
| 763 | train | What single was released by a American country singer, songw | Feels Like Love | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 764 | train | The Church of the Guanche People was founded in the city tha | Macaronesia | 'Can' | incorrect | 单 token 短答 'Can'（疑似错答，人工留意） |
| 765 | validation | Who was President of the United States when Jennifer Hunt se | Barack Obama | 'Bill Obama' | incorrect | gold 未命中 |
| 766 | train | When was the track from which a sample was featured in "Take | 16 March 1987 | '1999' | incorrect | 单 token 短答 '1999'（疑似错答，人工留意） |
| 767 | test | Isabella Kelly was born at a ruined castle characterized as  | The Changing Scottish La | 'Isabella Kelly' | incorrect | gold 未命中 |
| 768 | test | What 1876 battle featured the Other Magpie? | Battle of the Rosebud | 'Battle of the River' | incorrect | gold 未命中 |
| 769 | test | What type of music features Geetam, created by a devotee of  | Carnatic | 'indotional music' | incorrect | gold 未命中 |
| 770 | train | What was the highest grossing movie of 2010? | Toy Story 3 | 'In' | format_failure | 单 token 函数词/碎片 'In'，无答案内容 |
| 771 | train | English economist and physician Nicholas Barbon helped to pi | Fire insurance | 'fire insurance' | correct | gold 命中（含等价/别名） |
| 772 | test | Mount Lascar is in which South American country? | Chile | 'Chile' | correct | gold 命中（含等价/别名） |
| 773 | train | Which country suspended its annual Antarctic Whale Hunt in F | Japan | 'Japan' | correct | gold 命中（含等价/别名） |
| 774 | validation | Mistral, chinook, zonda, and willy-willy are types of which  | Winds | 'windinds' | incorrect | 单 token 短答 'windinds'（疑似错答，人工留 |
| 775 | validation | The white pinwheel shaped Tiare is the national flower of wh | French Polynesia | 'Tah' | incorrect | 单 token 短答 'Tah'（疑似错答，人工留意） |
| 776 | test | In humans, alopecia is the loss of what? | Hair | 'hair' | correct | gold 命中（含等价/别名） |
| 777 | validation | A popular 1960s TV cowboy series, what is a cutaneous coveri | Rawhide | 'rawhide' | correct | gold 命中（含等价/别名） |
| 778 | train | A Gay Girl in Damascus is the title of a hoax blog by fictio | Syria | 'Syria' | correct | gold 命中（含等价/别名） |
| 779 | train | French for an additive, and a Venezuelan liberator of Ecuado | Sucre | 'socre' | incorrect | 单 token 短答 'socre'（疑似错答，人工留意） |
| 780 | validation | Sukhoi and Tupolev are aircraft manufacturers of what nation | Russia | 'Russia' | correct | gold 命中（含等价/别名） |
| 781 | test | What is the international telephone dialling code for German | 49 | '49' | correct | gold 命中（含等价/别名） |
| 782 | validation | A Tale of Two Cities? | Charles Dickens | 'Charles Dickens' | correct | gold 命中（含等价/别名） |
| 783 | test | Whose father wrote and sang the popular 'Secret Lemonade Dri | Elvis Costello | 'David White' | incorrect | gold 未命中 |
| 784 | train | As at 2012 Goulburn Correctional Centre is considered the hi | Australia | 'Australia' | correct | gold 命中（含等价/别名） |
| 785 | train | What is the main metallic element in the core of the moon? | Iron | 'Iron' | correct | gold 命中（含等价/别名） |
| 786 | train | The medical term bariatric refers (increasingly politically  | Obesity | 'obesity' | correct | gold 命中（含等价/别名） |
| 787 | train | A period of Northern Hemisphere climatic extremes occurring  | Ice Age | 'ice Age' | correct | gold 命中（含等价/别名） |
| 788 | train | A harquebus/arquebus is an early form of? | Gun | 'fireket' | incorrect | 单 token 短答 'fireket'（疑似错答，人工留意 |
| 789 | train | Lysergic Acid Diethylamide is better known by what abbreviat | LSD | 'LSD' | correct | gold 命中（含等价/别名） |
| 790 | test | What cartoon character featured on a $100,000 auctioned post | Mickey Mouse | 'Superman' | incorrect | 单 token 短答 'Superman'（疑似错答，人工留 |
| 791 | train | What is confit meat cooked and preserved in? | Fat | 'fat' | correct | gold 命中（含等价/别名） |
| 792 | train | A ewer is a large? | Jug | 'vessel' | incorrect | 单 token 短答 'vessel'（疑似错答，人工留意） |
| 793 | test | What Olympic event entails disqualification if both feet of  | Racewalking | 'High jump' | incorrect | gold 未命中 |
| 794 | train | The rights to which famous character were sold by creators J | Superman | 'Superman' | correct | gold 命中（含等价/别名） |
| 795 | validation | The UK political Labour Party's famously controversial 1995  | Nationalization | 'socialism' | incorrect | 单 token 短答 'socialism'（疑似错答，人工 |
| 796 | test | "The Duke of Wellington's suggestion of ""Sparrowhawks"" to  | Crystal Palace | 'West Palace' | incorrect | gold 未命中 |
| 797 | validation | What red fruit-juice-based drink whose name alludes to energ | Vimto | 'Redade' | incorrect | 单 token 短答 'Redade'（疑似错答，人工留意） |
| 798 | train | What characteristic of Borneo ranks it among the largest fiv | Island | 'landland' | incorrect | 单 token 短答 'landland'（疑似错答，人工留 |
| 799 | validation | In physics, what is a substance that continually deforms/flo | Fluid | 'fluid' | correct | gold 命中（含等价/别名） |
| 800 | validation | In what year was Band-Aid's Do They Know It's Christmas the  | 1984 | '1984' | correct | gold 命中（含等价/别名） |
| 801 | test | Suya, Puff Puff, and Moin Moin (or Moyi-Moyi) are well-known | Foods | 'foodishes' | incorrect | 单 token 短答 'foodishes'（疑似错答，人工 |
| 802 | validation | In team ball games such as football, a pass to a team-mate w | Hospital | 'd' | format_failure | 单 token 函数词/碎片 'd'，无答案内容 |
| 803 | validation | Matthias Sammer, Ronaldo, Zinedine Zidane, Rivaldo, and Luis | European Footballer of t | 'World Cup' | incorrect | gold 未命中 |
| 804 | train | What in the human body is the calcaneum? | Heel bone | 'ank bone' | incorrect | gold 未命中 |
| 805 | train | What mountain's peak is the farthest point from Earth's cent | Chimborazo | 'Mount Everest' | incorrect | gold 未命中 |
| 806 | test | Name the four terrestrial planets of the Solar System? | Mercury, Venus, Earth, M | 'Mercury, Venus, Earth, Mars' | correct | gold 命中（含等价/别名） |
| 807 | train | The Erythraean Sea, lying between Africa and Asia is more co | Red Sea | 'Red' | incorrect | 单 token 短答 'Red'（疑似错答，人工留意） |
| 808 | train | US veterinary pathologist Daniel Salmon (1850-1914) oversaw  | Salmonella | 'Salmonella' | correct | gold 命中（含等价/别名） |
| 809 | train | American businessman and philanthropist Solomon Guggenheim ( | Museums | 'art museums' | correct | gold 命中（含等价/别名） |
| 810 | train | To what does the portmanteau word Grexit refer? | Greece Exit | 'Gxit' | incorrect | 单 token 短答 'Gxit'（疑似错答，人工留意） |
| 811 | train | JP Morgan, Barclays, RBS, Citigroup, Bank of America, and UB | Foreign Exchange | 'FX market' | incorrect | gold 未命中 |
| 812 | validation | Name the pioneering Game Theory US mathematician featured in | John Nash | 'John Nash' | correct | gold 命中（含等价/别名） |
| 813 | validation | What famous road began in Chicago, Illinois, ending at Santa | Route 66 | 'Route 66' | correct | gold 命中（含等价/别名） |
| 814 | train | Dermalogica, Olay, Clearasil, and Nutrogena are brands of? | Skincare | 'cos care' | incorrect | gold 未命中 |
| 815 | train | The fictitious South American city/country El Dorado was abu | Gold | 'Gold' | correct | gold 命中（含等价/别名） |
| 816 | train | Traditional Latin pluralization of Latin-originating words e | i | '-' | format_failure | 单 token 函数词/碎片 '-'，无答案内容 |
| 817 | train | Five ninths of three fifths is a? | Third | 'fraction' | incorrect | 单 token 短答 'fraction'（疑似错答，人工留 |
| 818 | validation | Which Gilbert and Sullivan operetta is sub-titled The Slave  | The Pirates of Penzance | 'The Sorcerer' | incorrect | gold 未命中 |
| 819 | test | Feugo, Yangin, Brand, and Pozar are Spanish, Turkish, Dutch  | Fire | 'fire' | correct | gold 命中（含等价/别名） |
| 820 | train | What gas, symbol F, is the most reactive of all chemical ele | Fluorine | 'fluorine' | correct | gold 命中（含等价/别名） |
| 821 | train | In 2015 Japan lowered its voting age from what to what? | 20 to 18 | '20 to 18' | correct | gold 命中（含等价/别名） |
| 822 | test | What African nation is known in parts of Asia by the local n | Morocco | 'Morocco' | correct | gold 命中（含等价/别名） |
| 823 | test | Which country occupying 47% of South America has states incl | Brazil | 'Brazil' | correct | gold 命中（含等价/别名） |
| 824 | validation | Leicester City FC's owners are (at 2016) what nationality? | Thailand | 'Americanish' | incorrect | 单 token 短答 'Americanish'（疑似错答， |
| 825 | train | A warm sunny period in Autumn (Fall) in the northern hemisph | Indian Summer | 'Indianwave' | incorrect | 单 token 短答 'Indianwave'（疑似错答，人 |
| 826 | train | Born Henry John Deutschendorf Junior, which American singer  | John Denver | 'John Denver' | correct | gold 命中（含等价/别名） |
| 827 | test | Name the ballet dancer who requested asylum in France while  | Rudolph Nureyev | 'Banchine' | incorrect | 单 token 短答 'Banchine'（疑似错答，人工留 |
| 828 | train | The cult TV series Lost which began in 2004 features 'Oceani | 815 | '815' | correct | gold 命中（含等价/别名） |
| 829 | train | Which country won the 2007 FIFA Women's World Cup? | Germany | 'Germany' | correct | gold 命中（含等价/别名） |
| 830 | train | Who became the new French president in 2007? | Nicolas Sarkozy | 'Nicolas Sarkozy' | correct | gold 命中（含等价/别名） |
| 831 | train | Who wrote and had a hit with the instrumental Classical Gas? | Mason Williams | 'Ray Jones' | incorrect | gold 未命中 |
| 832 | train | In which year did Captain Scott reach the South Pole? | 1912 | '1911' | incorrect | 单 token 短答 '1911'（疑似错答，人工留意） |
| 833 | train | The NASA spacecraft Messenger reached what planet destinatio | Mercury | 'Mercury' | correct | gold 命中（含等价/别名） |
| 834 | train | What colour is the inner ring of an Olympic archery target? | Gold | 'Gold' | correct | gold 命中（含等价/别名） |
| 835 | test | In the human body what is the Axilla commonly known as? | The armpit | 'The Axilla is commonly known as the ar.' | correct | gold 别名命中 |
| 836 | train | Jimmy Wales and Larry Sanger founded which website in 2001? | Wikipedia | 'Wikipedia' | correct | gold 命中（含等价/别名） |
| 837 | validation | Which US lead singer's real name is William Baily? | Axl Rose | 'Billono' | incorrect | 单 token 短答 'Billono'（疑似错答，人工留意 |
| 838 | train | In which English county is the Dickens World Theme Park? | Kent | 'Essex' | incorrect | 单 token 短答 'Essex'（疑似错答，人工留意） |
| 839 | train | Which fashion designer introduced the Polo label in 1967? | Ralph Lauren | 'Palph Lauren' | incorrect | gold 未命中 |
| 840 | train | According to legend who killed the lion represented by the c | Hercules | 'Hercules' | correct | gold 命中（含等价/别名） |
| 841 | test | What merchant bank collapsed in 1995 due to unauthorised deb | Barings | 'Barings Bank' | correct | gold 命中（含等价/别名） |
| 842 | train | What is the Japanese martial art, similar to judo, which use | Aikido | 'Aikido' | correct | gold 命中（含等价/别名） |
| 843 | validation | Which French prime minister was executed for treason in 1945 | Pierre Laval | 'Paul Laval' | incorrect | gold 未命中 |
| 844 | train | Herman Van Rompuy became first Permanent President of what? | The European Council | 'European Union' | correct | gold 别名命中 |
| 845 | train | The Bell Rock Lighthouse, said to be the oldest surviving of | Scotland | 'Scotland' | correct | gold 命中（含等价/别名） |
| 846 | train | The Collegiate Church of St Peter in London is more popularl | Westminster Abbey | 'Westminster Abbey' | correct | gold 命中（含等价/别名） |
| 847 | train | The fortified wine drink Sherry is named after what town? | Jerez | 'Jerez' | correct | gold 命中（含等价/别名） |
| 848 | train | In 1725 Catherine the First succeeded which Russian emperor, | Peter the First | 'Peter the Great' | incorrect | gold 未命中 |
| 849 | validation | How many triangles are on a backgammon board? | Twenty-four | '24' | correct | gold 别名命中 |
| 850 | test | Ireland is known as The 'what' Isle? | Emerald | 'Green' | incorrect | 单 token 短答 'Green'（疑似错答，人工留意） |
| 851 | train | Originating in early central American culture, where on the  | Foot | 'feet' | correct | gold 别名命中 |
| 852 | train | Name the head of the 'whistleblowing' website Wikileaks, in  | Julian Assange | 'Julian Assange' | correct | gold 命中（含等价/别名） |
| 853 | train | Which English public school shares it's name with a farm imp | Harrow | 'Eton' | incorrect | 单 token 短答 'Eton'（疑似错答，人工留意） |
| 854 | train | Who played Clayton Farlowe in Dallas | Howard Keel | 'David Smith' | incorrect | gold 未命中 |
| 855 | test | Which millionaire's daughter married Imran Khan in 1995 | Sir James Goldsmith | 'Imran Khan' | incorrect | gold 未命中 |
| 856 | train | Which musical instrument was Jelly Roll Morton associated wi | Piano | 'Piano' | correct | gold 命中（含等价/别名） |
| 857 | train | What is the largest natural lake in Wales | Lake Bala | 'Llyn Ogwen' | incorrect | gold 未命中 |
| 858 | validation | What was the name of Catherine Zeta Jones character in The D | Mariette | 'L' | format_failure | 单 token 函数词/碎片 'L'，无答案内容 |
| 859 | train | In which country was Queen Elizabeth 11 when she heard of he | Kenya | 'Canada' | incorrect | 单 token 短答 'Canada'（疑似错答，人工留意） |
| 860 | train | What was bandleader Joe Loss's signature tune | In The Mood | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 861 | test | What nationality is singer Vanessa Paradis | French | 'Singer Vanessa Paradis is French.' | correct | gold 命中（含等价/别名） |
| 862 | train | Which cup competition was founded by Charles William Alcock  | The FA Cup | 'Al FA Cup' | correct | gold 别名命中 |
| 863 | train | Who played the title role in the TV western series Bronco | Ty Hardin | 'John York' | incorrect | gold 未命中 |
| 864 | train | How was Monday October 19, 1987 known in the world of financ | Black Monday | 'Black Monday' | correct | gold 命中（含等价/别名） |
| 865 | test | On which river is the city of Ely | The Ouse | 'Riverames' | incorrect | 单 token 短答 'Riverames'（疑似错答，人工 |
| 866 | train | Which Oscar winning song came from the film Pocahontas | Colours of the Wind | 'Colors of the Wind' | correct | gold 别名命中 |
| 867 | test | What is the title of Max Bygraves autobiography | I Wanna Tell You a Story | 'Max' | incorrect | 单 token 短答 'Max'（疑似错答，人工留意） |
| 868 | train | What country singer's duets with Loretta Lynn ended when he  | Conway Twitty | 'John Nelson' | incorrect | gold 未命中 |
| 869 | test | What flower was named after the Duke of Cumberland | Sweet William | 'Carnia' | incorrect | 单 token 短答 'Carnia'（疑似错答，人工留意） |
| 870 | train | Whose autobiography was titled 1966 And All That | Geoff Hurst | 'George Best' | incorrect | gold 未命中 |
| 871 | train | Which English town's Anglo Saxon name was Gipeswic pronounce | Ipswich | 'Gwich' | incorrect | 单 token 短答 'Gwich'（疑似错答，人工留意） |
| 872 | train | Made in Scotland what type of beverage is Rock Rose | Gin | 'whiskey' | incorrect | 单 token 短答 'whiskey'（疑似错答，人工留意 |
| 873 | test | What is vellum parchment made from | Calfskin | 'animal skin' | incorrect | gold 未命中 |
| 874 | train | Who wrote the poems If, Gunga Din, Mandalay, and The Female  | Rudyard Kipling | 'Ryard Kipling' | correct | gold 别名命中 |
| 875 | train | Which British submarine sank the General Belgrano in the Fal | HMS Conqueror | ' HMSon' | incorrect | 单 token 短答 ' HMSon'（疑似错答，人工留意） |
| 876 | validation | What was the name of the building destroyed in the Oklahoma  | Alfred Murrah Federal Bu | ' Murrah Federal Building' | correct | gold 命中（含等价/别名） |
| 877 | test | During a penalty shoot out in soccer where should the non pa | In the centre circle | 'outside the penalty box' | incorrect | gold 未命中 |
| 878 | train | What was the former name of The Home Guard | Local Defence Volunteers | 'Home Guard' | correct | gold 别名命中 |
| 879 | train | What was the name of the character played by Bonnie Langford | Violet Elizabeth Bott | 'William' | incorrect | 单 token 短答 'William'（疑似错答，人工留意 |
| 880 | validation | What used to be bought at Spitalfields market apart from fru | Flowers | 'clo' | incorrect | 单 token 短答 'clo'（疑似错答，人工留意） |
| 881 | test | Which Australian prime minister was said to have tweaked the | Paul Keating | 'John Howard' | incorrect | gold 未命中 |
| 882 | validation | "Which famous children's novel begins with the words ""The m | The Wind in the Willows | 'The Willy Mole' | incorrect | gold 未命中 |
| 883 | test | Who were the first League Cup winners | Aston Villa | 'Manchester United' | incorrect | gold 未命中 |
| 884 | test | What nationality was Aristotle Onassis originally | Turkish | 'Greek' | incorrect | 单 token 短答 'Greek'（疑似错答，人工留意） |
| 885 | train | Which female singer had a top ten hit in 1998 with My Favour | Sheryl Crow | 'L' | format_failure | 单 token 函数词/碎片 'L'，无答案内容 |
| 886 | train | Who in verse sailed to the land where the bong tree grows | The owl and the pussycat | 'John Columbus' | incorrect | gold 未命中 |
| 887 | train | On which game show was Bobby Charlton once a contestant and  | Double Your Money | 'Mastermind' | incorrect | 单 token 短答 'Mastermind'（疑似错答，人 |
| 888 | train | Which wild life quiz show was hosted by Henry Kelly | Monkey Business | 'Wild Kingdom' | incorrect | gold 未命中 |
| 889 | train | What award is given for a wound in the American forces | Purple Heart | ' Purple Star' | incorrect | gold 未命中 |
| 890 | train | Which boxer broke Muhammed Ali's jaw | Ken Norton | 'Joe Patterson' | incorrect | gold 未命中 |
| 891 | train | What nationality was Che Guevara | Argentinean | 'Argentine' | incorrect | 单 token 短答 'Argentine'（疑似错答，人工 |
| 892 | train | Born in 1970, which female has been a presenter on the TV sh | Zoë Ball | 'Mel Bruce' | incorrect | gold 未命中 |
| 893 | test | Which torture chamber was invented by George Orwell? | Room 101 | 'The Thought' | incorrect | gold 未命中 |
| 894 | train | Which 1949 film was set on the Scottish island of Todday? | Whisky Galore | 'High' | incorrect | 单 token 短答 'High'（疑似错答，人工留意） |
| 895 | train | Red Grant was a villain in which James Bond movie? | From Russia With Love | 'Moonraker' | incorrect | 单 token 短答 'Moonraker'（疑似错答，人工 |
| 896 | train | The Conservation of Energy is the first ……..what? | Law of Thermodynamics | 'law' | incorrect | 单 token 短答 'law'（疑似错答，人工留意） |
| 897 | train | Whose “left hand” rule can predict the direction of motion o | John Ambrose Fleming | 'left Fleming' | incorrect | gold 未命中 |
| 898 | validation | What is the name of the O’Haras’ plantation in ‘Gone with th | TARA | ' Tara Tara' | correct | gold 命中（含等价/别名） |
| 899 | train | Clyde Tombaugh discovered which celestial object in our sola | PLUTO | 'Pluto' | correct | gold 命中（含等价/别名） |
| 900 | train | In a 1763 swap, what expanse of land did Britain gain from S | FLORIDA | 'Florida Florida' | correct | gold 命中（含等价/别名） |
| 901 | test | What is the official march of the Royal Navy? | Heart of Oak | 'The Navy Navy' | incorrect | gold 未命中 |
| 902 | train | Which crop is attacked by the Colorado Beetle? | Potato | 'potato' | correct | gold 命中（含等价/别名） |
| 903 | train | Who had a hit in 1966 with When a Man Loves a Woman? | Percy Sledge | 'The Jones' | incorrect | gold 未命中 |
| 904 | test | From what illness did Mary II die in 1694? | Smallpox | 'cption' | incorrect | 单 token 短答 'cption'（疑似错答，人工留意） |
| 905 | train | Which football team are nicknamed the Blaugrana? | Barcelona | 'FCcelona' | incorrect | 单 token 短答 'FCcelona'（疑似错答，人工留 |
| 906 | validation | Which is the highest position in the Metropolitan Police? | Commissioner | 'Commission Commissioner' | correct | gold 命中（含等价/别名） |
| 907 | test | What bird did Good Queen Bess decree should be eaten at Chri | GOOSE | 'tur' | incorrect | 单 token 短答 'tur'（疑似错答，人工留意） |
| 908 | train | Which Michael Frayn play features a ‘play within a play’ ent | Noises Off | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 909 | train | What is measured by a Bourdon Gauge? | Pressure | 'Pressure pressure' | correct | gold 命中（含等价/别名） |
| 910 | train | At which battle of 2 December 1805 did Napoleon defeat a com | Battle of Austerlitz | 'Battle of Austerlitz' | correct | gold 命中（含等价/别名） |
| 911 | validation | What is the symbol for the chemical element protactinium, at | Pa | 'Pa' | correct | gold 命中（含等价/别名） |
| 912 | validation | 'Nobody puts Baby in a corner.' is a line from which 1987 fi | Dirty Dancing | 'Flash Dancing' | incorrect | gold 未命中 |
| 913 | train | Mrs Darrell Waters books were translated into 120 languages. | Enid Blyton | 'Mary Brown' | incorrect | gold 未命中 |
| 914 | train | Sidney Poitier, Eartha Kitt, Val Doonican and Ferenc Puskas  | 1927 | '1927' | correct | gold 命中（含等价/别名） |
| 915 | train | Who is widely credited with introducing his former wife Whit | BOBBY BROWN | 'Bob Brown' | incorrect | gold 未命中 |
| 916 | train | Captain of the Flying Dustman, what was the name of Captain  | Cut-throat Jake | 'Black' | incorrect | 单 token 短答 'Black'（疑似错答，人工留意） |
| 917 | train | Weighing-in at up 48 stone, who wrestled under the ring-name | Martin Ruane | 'John' | incorrect | 单 token 短答 'John'（疑似错答，人工留意） |
| 918 | train | Which woman was voted BBC Sports Personality of the Year in  | PRINCESS ANNE | 'Mary White' | incorrect | gold 未命中 |
| 919 | test | What do 4 roods equal? | An Acre | '1 acre' | correct | gold 别名命中 |
| 920 | train | The bumblebee or hog-nosed is the smallest mammal in the wor | Bat | 'bumumblebee bat' | correct | gold 命中（含等价/别名） |
| 921 | train | What do we call the selfless and virtuous practice of concer | ALTRUISM | 'char' | incorrect | 单 token 短答 'char'（疑似错答，人工留意） |
| 922 | test | The SI unit the ohm is often represented by the upper-case f | OMEGA | 'Omega' | correct | gold 命中（含等价/别名） |
| 923 | test | As well as municipalities, which country is made up of 26 st | BRAZIL | 'Brazil' | correct | gold 命中（含等价/别名） |
| 924 | train | In which city did the gangland St Valentine’s Day Massacre t | CHICAGO | 'Chicago' | correct | gold 命中（含等价/别名） |
| 925 | test | Which bird is the international symbol for happiness? | Bluebird | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 926 | train | Who wrote the BBC tv serial drama ‘The Singing Detective’ (1 | DENNIS POTTER | 'Stephen Thomas' | incorrect | gold 未命中 |
| 927 | train | What is Britain’s bestselling breakfast cereal? | Weetabix | ' corn Flakes' | incorrect | gold 未命中 |
| 928 | train | The bestselling children’s book “Grandpa’s great escape” is  | David Walliams | 'David Brown' | incorrect | gold 未命中 |
| 929 | train | Tintern Abbey, made famous by Wordsworth’s poetry, stands on | Wye | 'Wye' | correct | gold 命中（含等价/别名） |
| 930 | test | What was Her Majesty's Prison Manchester called until 1990? | Strangeways | 'Manchester Prison' | correct | gold 别名命中 |
| 931 | test | What was Margot’s surname in “The Good Life” TV series? | Leadbetter | 'Margot\'s surname in "The Good Life" TV series was ' | incorrect | gold 未命中 |
| 932 | validation | In humans ribs are divided into three types. True, False and | Floating | 'Floating' | correct | gold 命中（含等价/别名） |
| 933 | test | Which is the most southerly of the Shipping Forecast areas? | Trafalgar | 'Area' | incorrect | 单 token 短答 'Area'（疑似错答，人工留意） |
| 934 | test | The disease blossom end rot is most frequently found in whic | Tomatoes | 'tomatoes' | correct | gold 命中（含等价/别名） |
| 935 | train | According to several early Old Testament books, who led the  | JOSHUA | 'Joshua' | correct | gold 命中（含等价/别名） |
| 936 | test | ‘When Will You Marry?’ became the world’s most expensive wor | Paul GAUGUIN | 'True' | incorrect | 单 token 短答 'True'（疑似错答，人工留意） |
| 937 | train | The prominent headland known as the Great Orme is close to w | LLANDUDNO | 'Wiff' | incorrect | 单 token 短答 'Wiff'（疑似错答，人工留意） |
| 938 | train | What dark brown food paste is the Australian version of Marm | VEGEMITE | 'Bemite' | incorrect | 单 token 短答 'Bemite'（疑似错答，人工留意） |
| 939 | test | Which planet did Gustav Holst describe as the ‘Winged Messen | Mercury | 'Mercury' | correct | gold 命中（含等价/别名） |
| 940 | train | Which early sixties singer was backed by The Bruvvers? | Joe Brown | 'The Richard' | incorrect | gold 未命中 |
| 941 | test | Merton Pride and Williams are varieties of which fruit? | Pear | 'apple' | incorrect | 单 token 短答 'apple'（疑似错答，人工留意） |
| 942 | train | Which city in the USA suffered a huge fire in 1871 allegedly | Chicago | 'Chicago' | correct | gold 命中（含等价/别名） |
| 943 | train | “Dreams from my father, a story of race and heritance” is ab | Barack Obama | 'Barack Obama' | correct | gold 命中（含等价/别名） |
| 944 | train | Created in 1662, In which city is Phoenix Park? | Dublin | 'Dublin' | correct | gold 命中（含等价/别名） |
| 945 | train | Which character was played by John Inman in “Are you being s | Mr. Humphries | 'Mr' | format_failure | 单 token 函数词/碎片 'Mr'，无答案内容 |
| 946 | test | Which two countries took part in the short Kargil War in 199 | India and Pakistan | 'India and Pakistan' | correct | gold 命中（含等价/别名） |
| 947 | test | From the Greek for ‘artificial’, what was the first synthesi | Technetium | 'uran' | incorrect | 单 token 短答 'uran'（疑似错答，人工留意） |
| 948 | train | Who presented the 1980 blockbuster documentary series, Cosmo | Carl Sagan | 'Carl Sagan' | correct | gold 命中（含等价/别名） |
| 949 | train | The Analects are the writings of which Eastern philosopher? | Confucius | 'Confucius' | correct | gold 命中（含等价/别名） |
| 950 | test | Which 1987 US film was based on the 1985 French film ‘Trois  | THREE MEN AND A BABY | 'Three' | incorrect | 单 token 短答 'Three'（疑似错答，人工留意） |
| 951 | train | What are the last six words of Rudyard Kipling’s ‘If’? | YOU’LL BE A MAN, MY SON | '' | refusal_empty | 空输出 |
| 952 | train | Which motor scooter had a name meaning ‘wasp’? | Vespa | 'Apa Vespa' | correct | gold 命中（含等价/别名） |
| 953 | train | The Wasp Factory was the debut novel of which author who die | Iain Banks | 'Alex Welsh' | incorrect | gold 未命中 |
| 954 | train | The Most Noble Order of the Garter was established during th | Edward III | 'King Edward III' | correct | gold 命中（含等价/别名） |
| 955 | validation | Which duo created the “Dagenham dialogues”? | Peter Cook and Dudley Mo | 'Benn and Smith' | incorrect | gold 未命中 |
| 956 | validation | Swinley Bottom forms part of the track on which famous racec | Ascot | 'Newwood' | incorrect | 单 token 短答 'Newwood'（疑似错答，人工留意 |
| 957 | train | If you were performing an orison what would you be doing? | Praying | 'praying' | correct | gold 命中（含等价/别名） |
| 958 | train | What type of food or drink is a macchiato? | COFFEE | 'coffee' | correct | gold 命中（含等价/别名） |
| 959 | train | Amanuensis is an archaic word for what profession? | Secretary | 'secretary' | correct | gold 命中（含等价/别名） |
| 960 | train | Who did Claus von Stauffenberg plot to kill? | Adolf Hitler | 'Adolf Hitler' | correct | gold 命中（含等价/别名） |
| 961 | validation | What does the French word noir mean in English? | Black | 'black' | correct | gold 命中（含等价/别名） |
| 962 | train | "What country's ""Kingdom Tower"" is planned to be more than | Saudi Arabia | 'Saudi Arabia' | correct | gold 命中（含等价/别名） |
| 963 | test | What country does Waterford crystal come from? | Ireland | 'I' | format_failure | 单 token 函数词/碎片 'I'，无答案内容 |
| 964 | train | What country is the largest oil producer in Africa? | Nigeria | 'Nigeria' | correct | gold 命中（含等价/别名） |
| 965 | train | What company is the world's largest auction house? | Christie's | "Christie's" | correct | gold 命中（含等价/别名） |
| 966 | train | What movie starred Michael Jordan? | Space Jam | 'Air Jam' | incorrect | gold 未命中 |
| 967 | test | Hafidh are people who have memorized what? | The Quran | 'Quran' | correct | gold 别名命中 |
| 968 | validation | If I sail on the Neva river past the Hermitage Museum, what  | St. Petersburg | 'St.' | format_failure | 单 token 函数词/碎片 'St.'，无答案内容 |
| 969 | test | Where would a Viking warrior hope to go if he died in battle | Valhalla | 'Valhalla' | correct | gold 命中（含等价/别名） |
| 970 | train | What is the most common phobia in the United States, accordi | Fear of Public Speaking | 'height' | incorrect | 单 token 短答 'height'（疑似错答，人工留意） |
| 971 | test | What city will host the 2016 Olympics? | Rio de Janeiro | 'Rio de Janeiro' | correct | gold 命中（含等价/别名） |
| 972 | validation | Followers of what cult leader committed mass suicide by drin | Jim Jones | 'Jim Jones' | correct | gold 命中（含等价/别名） |
| 973 | train | What is Brazil's most widely-spoken language? | Portuguese | 'Portuguese' | correct | gold 命中（含等价/别名） |
| 974 | test | In alphabetical order, what is the last U.S. state? | Wyoming | 'Wy' | format_failure | 单 token 函数词/碎片 'Wy'，无答案内容 |
| 975 | train | What is the number 17 in binary? | 10001 | 'The number 17 in binary is 10001.' | correct | gold 命中（含等价/别名） |
| 976 | validation | "In the ""Peanuts"" comic strip, who is Lucy's brother?" | Linus | 'Charlieus' | incorrect | 单 token 短答 'Charlieus'（疑似错答，人工 |
| 977 | train | What Olympics-like event is for athletes with physical disab | Paralympics | 'Parampics' | incorrect | 单 token 短答 'Parampics'（疑似错答，人工 |
| 978 | train | What movie takes place at Shermer High School's detention? | The Breakfast Club | 'The Breakfast Club' | correct | gold 命中（含等价/别名） |
| 979 | train | What musician formed a singing duo with Art Garfunkel in 196 | Paul Simon | 'Paul Simon' | correct | gold 命中（含等价/别名） |
| 980 | train | What religious text was recently adapted into a hit Broadway | The Book of Mormon | 'The Book of Mormon' | correct | gold 命中（含等价/别名） |
| 981 | test | What Carl Sagan television series was resurrected in 2014 wi | Cosmos | 'Cosmos: A Spacetime Odyssey' | correct | gold 命中（含等价/别名） |
| 982 | test | What is Paris's largest airport? | Charles de Gaulle | 'Orly International Airport' | incorrect | gold 未命中 |
| 983 | train | What notorious leader had a similar style mustache to Charli | Adolf Hitler | 'Adolf Hitler' | correct | gold 命中（含等价/别名） |
| 984 | train | What Pakistani river valley was home to one of the world's m | Indus Valley | 'Indus River' | correct | gold 别名命中 |
| 985 | train | "The song ""Sunday Bloody Sunday"" was about a massacre on w | Ireland | 'I' | format_failure | 单 token 函数词/碎片 'I'，无答案内容 |
| 986 | train | What is the name of the vast hall where the Norse gods live? | Valhalla | 'Valhalla' | correct | gold 命中（含等价/别名） |
| 987 | test | On what body of water did Jesus supposedly walk? | Sea of Galilee | 'Sea' | incorrect | 单 token 短答 'Sea'（疑似错答，人工留意） |
| 988 | test | What was abolished by the Supreme Court in 1972, but reinsta | Death Penalty | 'the death penalty' | correct | gold 命中（含等价/别名） |
| 989 | train | What bridge connects the two peninsulas of Michigan? | Mackinac Bridge | 'Thein Bridge' | incorrect | gold 未命中 |
| 990 | train | Grozny is the capital of what war-torn Russian republic? | Chechnya | 'Chechnya' | correct | gold 命中（含等价/别名） |
| 991 | train | What are the two major European cities that start with the l | Belfast | 'Belgrade and Belgium' | incorrect | gold 未命中 |
| 992 | test | What is the tallest kind of tree? | Coast Redwood | 'redwood' | incorrect | 单 token 短答 'redwood'（疑似错答，人工留意 |
| 993 | train | What was the last name of brothers Chico, Harpo, Groucho, Ze | Marx | 'Marx' | correct | gold 命中（含等价/别名） |
| 994 | test | "What play is about ""star-crossed lovers""?" | Romeo and Juliet | 'Romeo and Juliet' | correct | gold 命中（含等价/别名） |
| 995 | train | What comes next in the sequence kilo, mega, giga? | Tera | 'tera' | correct | gold 命中（含等价/别名） |
| 996 | test | David Jason starred as Inspector Frost, but who played his b | BRUCE ALEXANDER | 'David Williams' | incorrect | gold 未命中 |
| 997 | train | The Habit of Art is a play by Alan Bennett about a fictional | W H AUDEN | 'Thomas Thomas' | incorrect | gold 未命中 |
| 998 | train | Which river runs through York? | OUSE | 'Riveruse' | incorrect | 单 token 短答 'Riveruse'（疑似错答，人工留 |
| 999 | train | Who played 'Captain Corelli' in the film 'Captain Corelli's  | NICOLAS CAGE | 'Anthony Hopkins' | incorrect | gold 未命中 |
| 1000 | train | The 2013 G8 Summit was held at Lough Erne Resort in Northern | FERMANAGH | 'Done' | incorrect | 单 token 短答 'Done'（疑似错答，人工留意） |
| 1001 | train | In which British city is the Mitchell Library | Glasgow | 'Beds' | incorrect | 单 token 短答 'Beds'（疑似错答，人工留意） |
| 1002 | train | The Wolfe Noel Cup is awarded to the winners of the woman's  | Squash | 'golf' | incorrect | 单 token 短答 'golf'（疑似错答，人工留意） |
| 1003 | train | Which artist was famed for his paintings of the water lilies | CLAUDE MONET | 'Monet' | correct | gold 别名命中 |
| 1004 | train | Octavian, who became Augustus, and Marcus Aemilius Lepidus w | MARK ANTONY | 'Mark Antony' | correct | gold 命中（含等价/别名） |
| 1005 | train | In which Italian city is the newspaper 'La Stampa' published | TURIN | 'Turan' | incorrect | 单 token 短答 'Turan'（疑似错答，人工留意） |
| 1006 | train | Which is the largest city on the Caspian Sea? | BAKU | 'Baku' | correct | gold 命中（含等价/别名） |
| 1007 | train | Which island was home to Odysseus? | ITHACA | 'Ithaca' | correct | gold 命中（含等价/别名） |
| 1008 | test | Which boxer fought Mohammed Ali in the fight known as 'The T | JOE FRAZIER | 'Floydman' | incorrect | 单 token 短答 'Floydman'（疑似错答，人工留 |
| 1009 | train | 'Original Pirate Material' was the 2002 debut album of which | 'THE STREETS' | 'Thehead' | incorrect | 单 token 短答 'Thehead'（疑似错答，人工留意 |
| 1010 | train | Who was the head of the German Ministry of Public Enlightenm | JOSEPH GOEBBELS | 'Joseph Goebbels' | correct | gold 命中（含等价/别名） |
| 1011 | test | Who won a Best Actress Oscar for the 1940 film 'Kitty Foyle' | Ginger Rogers | 'Jane Arthur' | incorrect | gold 未命中 |
| 1012 | train | Which precious gem is the birthstone for May? | Emerald | 'The birthstone for May is theapphire.' | incorrect | gold 未命中 |
| 1013 | train | 'Whom we invite to see us crowned at Scone' is a line from w | MacBeth | 'Macbeth' | correct | gold 命中（含等价/别名） |
| 1014 | train | In which novel does Flora Poste move to live with her relati | Cold Comfort Farm | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1015 | train | In 2006 Orhan Pamuk became the first Nobel Laureate from whi | Turkey | 'Turkey' | correct | gold 命中（含等价/别名） |
| 1016 | validation | Which European city is served by Domodedovo Airport? | Moscow | 'Moscow' | correct | gold 命中（含等价/别名） |
| 1017 | train | Albacore, bigeye and longtail are species of what type of fi | TUNA | 'Tuna' | correct | gold 命中（含等价/别名） |
| 1018 | test | "Complete the name of the group for whom Young Girl was a Nu | PUCKETT | 'Gl' | format_failure | 单 token 函数词/碎片 'Gl'，无答案内容 |
| 1019 | validation | Luzon and Mindanao are the two largest islands in which coun | PHILIPPINES | 'Philippines' | correct | gold 命中（含等价/别名） |
| 1020 | train | Interflug used the AN-2 and AN-24 aircraft - manufactured by | ANTONOV | ' Antonov' | correct | gold 命中（含等价/别名） |
| 1021 | test | Han of Iceland, Oedipus in Athens & The Ballet of Unhatched  | (Modest) Mussorgsky | 'John Glass' | incorrect | gold 未命中 |
| 1022 | test | OJ presenter Stephen Fry stepped down earlier this year, who | (Sandi) Toksvig | 'Jo Jones' | incorrect | gold 未命中 |
| 1023 | train | For which 1960 film did Billy Wilder become the first person | The Apartment | 'The Apartment' | correct | gold 命中（含等价/别名） |
| 1024 | train | Which fashion designer wrote the book, 'Men Without Ties'? | GIANNI VERSACE | 'Tom Ford' | incorrect | gold 未命中 |
| 1025 | validation | Dame Judi Dench and which other actress played the Widdingto | Maggie Smith | 'Emma Smith' | incorrect | gold 未命中 |
| 1026 | validation | What is the most famous work of the architect James Hoban? | The Whitehouse | 'White House' | correct | gold 别名命中 |
| 1027 | validation | The childhood disease 'Rickets' is caused by a lack of which | VITAMIN D | 'Vitamin D' | correct | gold 命中（含等价/别名） |
| 1028 | train | Cassiterite is the main ore of which metal? | Tin | 'tin' | correct | gold 命中（含等价/别名） |
| 1029 | train | Complete the title of the novel that won the 2001 Booker Pri | Kelly | 'G' | format_failure | 单 token 函数词/碎片 'G'，无答案内容 |
| 1030 | train | Who was the last British athlete to compete in the Olympic 1 | DWAYNE CHAMBERS | 'David Johnson' | incorrect | gold 未命中 |
| 1031 | validation | Which company produces the 'Magentis' car model? | KIA | 'N' | format_failure | 单 token 函数词/碎片 'N'，无答案内容 |
| 1032 | test | What mission was the fifth human space flight of 'Project Ap | APOLLO 11 | 'Apollo 11' | correct | gold 命中（含等价/别名） |
| 1033 | train | Who was the British monarch when Theodore Roosevelt was the  | EDWARD VII | 'King Edward VII' | correct | gold 命中（含等价/别名） |
| 1034 | train | 'London Is The Place For Me' which was sung by Lord Kitchene | CALYPSO | 'folk song' | incorrect | gold 未命中 |
| 1035 | test | Which philosopher, 1872 - 1970, co-wrote 'Principia Mathemat | BERTRAND RUSSELL | 'Bertrand Russell' | correct | gold 命中（含等价/别名） |
| 1036 | train | Which hymn, based on Psalm 90, by Isaac Watts to a tune by W | 'OH GOD OUR HELP IN AGES | 'How Great is Our God' | incorrect | gold 未命中 |
| 1037 | train | Which capital city is served by Arlanda Airport | Stockholm | 'Stockholm' | correct | gold 命中（含等价/别名） |
| 1038 | train | Who wrote 'The Legend Of Sleepy Hollow'? | WASHINGTON IRVING | 'Washington Washington Irving' | correct | gold 命中（含等价/别名） |
| 1039 | test | Which daily newspaper was merged with the daily Mail in 1971 | DAILY SKETCH | 'The Daily Express' | incorrect | gold 未命中 |
| 1040 | validation | Which group had UK top ten hits in 1987 with 'Sweet Little M | 'WET WET WET' | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1041 | train | Which island of just over 30 square miles lies between North | Benbecula | 'Mra' | incorrect | 单 token 短答 'Mra'（疑似错答，人工留意） |
| 1042 | train | 'Whole Lotta Love', 'Yellow Pearl', 'The Wizard', and 'Get O | 'TOP OF THE POPS' | 'Top Gear' | incorrect | gold 未命中 |
| 1043 | train | What nationality is singer Rhianna? | BARBADIAN | 'Tradian' | incorrect | 单 token 短答 'Tradian'（疑似错答，人工留意 |
| 1044 | train | What word can mean loose broken rocks or someone who is vulg | Brash | 'brash' | correct | gold 命中（含等价/别名） |
| 1045 | validation | The largest region in New Zealand is Canterbury. Which city  | CHRISTCHURCH | 'Wellington' | incorrect | 单 token 短答 'Wellington'（疑似错答，人 |
| 1046 | train | Which band, formed in Salford in 1976, contained Ian Curtis, | 'JOY DIVISION' | 'Joy Division' | correct | gold 命中（含等价/别名） |
| 1047 | train | According to figures released by the ONS what was the most p | HARRY | 'Ol' | format_failure | 单 token 函数词/碎片 'Ol'，无答案内容 |
| 1048 | train | Who is the current World Snooker Champion? | Stuart Bingham | 'Mark Trump' | incorrect | gold 未命中 |
| 1049 | train | On which Italian track was the Formula One San Marino Grand  | Imola | 'Imola' | correct | gold 命中（含等价/别名） |
| 1050 | train | In which 1996 film were there characters known as Rent Boy,  | Trainspotting | 'Trainspot' | incorrect | 单 token 短答 'Trainspot'（疑似错答，人工 |
| 1051 | train | In music how many quavers make a minim? | Four (4) | '2' | format_failure | 单 token 函数词/碎片 '2'，无答案内容 |
| 1052 | train | Which US state is called 'Old Dominion'? | VIRGINIA | 'Virginia' | correct | gold 命中（含等价/别名） |
| 1053 | train | Which Liverpool player scored two goals in both the semi-fin | IAN RUSH | 'John Rush' | incorrect | gold 未命中 |
| 1054 | test | Which word is missing from this music hall song ‘When father | PARLOUR | 'walls' | incorrect | 单 token 短答 'walls'（疑似错答，人工留意） |
| 1055 | validation | Which car manufacturer made models called 'Ensign' and 'Vang | STANDARD | 'V' | format_failure | 单 token 函数词/碎片 'V'，无答案内容 |
| 1056 | validation | By what first name was the actor brother of Vanessa and Lynn | CORIN | 'Michael' | incorrect | 单 token 短答 'Michael'（疑似错答，人工留意 |
| 1057 | train | Which writer created the detective Charlie Chan? | EARL DERR BIGGERS | 'John Buchan' | incorrect | gold 未命中 |
| 1058 | train | Which of the 'Classic' horse races, run at Epsom for three y | 'THE OAKS' | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1059 | train | Which country defeated the Ivory Coast to win football's Afr | ZAMBIA | 'N' | format_failure | 单 token 函数词/碎片 'N'，无答案内容 |
| 1060 | train | In which sport did the future King Olav V of Norway in 1928  | SAILING | 'f' | format_failure | 单 token 函数词/碎片 'f'，无答案内容 |
| 1061 | test | With which common fish is Gooseberry sauce most often served | MACKEREL | 'Salmon' | incorrect | 单 token 短答 'Salmon'（疑似错答，人工留意） |
| 1062 | train | From which country does 'Manchego' cheese come? | SPAIN | 'Spain' | correct | gold 命中（含等价/别名） |
| 1063 | validation | The 'Vuvuzela' is traditionally made from the horn of which  | KUDU | 'Kudu' | correct | gold 命中（含等价/别名） |
| 1064 | train | Which Hollywood actor was married to Uma Thurman 1998 - 2004 | ETHAN HAWKE | 'David Pitt' | incorrect | gold 未命中 |
| 1065 | train | What name is shared by the capital city of Newfoundland and  | St Johns | 'Ant John' | incorrect | gold 未命中 |
| 1066 | train | Livorno, Pisa and Siena are three of the largest cities in w | TUSCANY | 'Tuscany' | correct | gold 命中（含等价/别名） |
| 1067 | train | The 1999 film, 'The Green Mile' was directed by whom? | FRANK DARABONT | 'Frank Spielberg' | incorrect | gold 未命中 |
| 1068 | validation | In the late 60's, Owen Finlay Maclaren pioneered what aid to | BABY BUGGY | 'carchair' | incorrect | 单 token 短答 'carchair'（疑似错答，人工留 |
| 1069 | train | "What is the literal meaning of the French expression ""Son  | """SOUND AND LIGHT""" | 'Sound and light' | correct | gold 命中（含等价/别名） |
| 1070 | train | Tommy Bolin, who died of a heroin overdose in 1976, was the  | DEEP PURPLE | 'Deep' | incorrect | 单 token 短答 'Deep'（疑似错答，人工留意） |
| 1071 | train | Donald Neilson was a notorious figure in the 1970's, but how | 'THE BLACK PANTHER' | 'Red Manson' | incorrect | gold 未命中 |
| 1072 | validation | What is the meteorological name of the clouds commonly known | CIRRUS | 'Cirrus' | correct | gold 命中（含等价/别名） |
| 1073 | train | Who wrote the Buddy Holly hit 'It Doesn't Matter Anymore'? | PAUL ANKA | 'Buddy Holly' | incorrect | gold 未命中 |
| 1074 | test | Which Shakespeare play centres around a novice nun called 'I | 'MEASURE FOR MEASURE' | 'The Merchant of Venice' | incorrect | gold 未命中 |
| 1075 | validation | The trade union Unison was formed by a merger of NALGO, NUPE | COHSE | 'NU' | format_failure | 单 token 函数词/碎片 'NU'，无答案内容 |
| 1076 | train | The second act, set in the Land of Sweets, of which ballet b | THE NUTCRACKER SUITE | 'The Nutcracker' | correct | gold 命中（含等价/别名） |
| 1077 | train | In the human body, what is the common name for the 'Talus bo | ANKLE | 'The ankle bone' | correct | gold 命中（含等价/别名） |
| 1078 | validation | Which director won the 'Oscar' for best Director for the pic | RON HOWARD | 'Ron Howard' | correct | gold 命中（含等价/别名） |
| 1079 | train | In which town or city would you find the 'Caledonian Brewery | EDINBURGH | 'Ed' | format_failure | 单 token 函数词/碎片 'Ed'，无答案内容 |
| 1080 | train | Who was the youngest ever Pope? | BENEDICT IX | 'Pope Benedict VI' | incorrect | gold 未命中 |
| 1081 | validation | What name is given to a substance that accelerates a chemica | CATALYST | 'Catalyst' | correct | gold 命中（含等价/别名） |
| 1082 | train | In 1932 which British physicist discovered the part of the n | (James) CHADWICK | 'Sir James Chadwick' | correct | gold 命中（含等价/别名） |
| 1083 | train | Which Puccini opera begins with 'Rodolfo' finishing writing  | 'LA BOHEME' | 'La boheme' | correct | gold 命中（含等价/别名） |
| 1084 | train | The painting 'Faithful Unto Death' can be found in Liverpool | SIR EDWARD JOHN POYNTER | 'John Blake' | incorrect | gold 未命中 |
| 1085 | validation | Which motor company owns the truck maker, Scania? | SAAB | 'Vol' | incorrect | 单 token 短答 'Vol'（疑似错答，人工留意） |
| 1086 | test | What type of animal, according to its alternative name, is t | TASMANIAN WOLF | 'wolf' | incorrect | 单 token 短答 'wolf'（疑似错答，人工留意） |
| 1087 | train | "Who famously said after the 'Dunblane Massacre', ""If a cri | DUKE OF EDINBURGH | 'Tony Blair' | incorrect | gold 未命中 |
| 1088 | validation | Which artist, a member of the Order of Merit, was born in Br | DAVID HOCKNEY | 'David Blake' | incorrect | gold 未命中 |
| 1089 | train | Which type of roof is pitched at two different angles, the l | Mansard | 'grel roof' | incorrect | gold 未命中 |
| 1090 | train | Whose picture is on the US 20 dollar note? | Andrew Jackson | 'Andrew Jackson' | correct | gold 命中（含等价/别名） |
| 1091 | train | What name is given to a line on a map joining places of equa | ISOHYET | 'isoh' | incorrect | 单 token 短答 'isoh'（疑似错答，人工留意） |
| 1092 | test | Who played the part of 'herman' in the 1960's TV series 'The | FRED GWYNNE | 'Al Johnson' | incorrect | gold 未命中 |
| 1093 | validation | Which is the sixth book of the New Testament, following Acts | EPISTLE TO THE ROMANS | 'Romans' | incorrect | 单 token 短答 'Romans'（疑似错答，人工留意） |
| 1094 | test | rtve is the state broadcaster in which country? | SPAIN | 'Spain' | correct | gold 命中（含等价/别名） |
| 1095 | train | Who is the only Rugby League player to win two consecutive L | Paul Wellens | 'Matthew Clinton' | incorrect | gold 未命中 |
| 1096 | train | The Cerval is one of the more uncommon members of which fami | CAT | 'cat' | correct | gold 命中（含等价/别名） |
| 1097 | validation | Terry Scott starred as middle-aged, suburban husband, Terry  | 'HAPPY EVER AFTER' | 'The Family' | incorrect | gold 未命中 |
| 1098 | validation | What is the general term for the seed-bearing part of a flow | PISTIL | 'carpel' | correct | gold 别名命中 |
| 1099 | test | "In British history, who was nicknamed ""The Sailor King""?" | WILLIAM IV | 'George III' | incorrect | gold 未命中 |
| 1100 | test | In Shakespeare's 'Hamlet', what was the name of 'Hamlet's' m | 'GERTRUDE' | 'Gertrude' | correct | gold 命中（含等价/别名） |
| 1101 | validation | Which country is the world's largest producer of copper? | CHILE | 'Ch' | format_failure | 单 token 函数词/碎片 'Ch'，无答案内容 |
| 1102 | test | What may be described as a 'red earthworm with rings of a br | BRANDLING | 'redworm' | incorrect | 单 token 短答 'redworm'（疑似错答，人工留意 |
| 1103 | train | For which film did Tatum O'Neal receive the Best Supporting  | 'PAPER MOON' | "Tatum O'Neal received the Best Supporting Actress " | incorrect | gold 未命中 |
| 1104 | train | The Leverhulme Stand and 1539 Restaurant and Bar are facilit | Chester | 'Newwood' | incorrect | 单 token 短答 'Newwood'（疑似错答，人工留意 |
| 1105 | train | In Greek mythology, Heracles' Twelfth Labour (final) was to  | 'CERBERUS' | 'The Minotaur' | incorrect | gold 未命中 |
| 1106 | train | Which film starring Will Smith, Bill Pullman and Jeff Goldbl | 'INDEPENDENCE DAY' | 'Independence Day' | correct | gold 命中（含等价/别名） |
| 1107 | train | In which country is the most northerly point on mainland Afr | TUNISIA | 'Libali' | incorrect | 单 token 短答 'Libali'（疑似错答，人工留意） |
| 1108 | train | The ancient Egyptian goddess Serket took the form of which c | SCORPION | 'a' | format_failure | 单 token 函数词/碎片 'a'，无答案内容 |
| 1109 | train | The adjective “buccal” refers to which part of the body? | Cheek | 'The adjective "buccal" refers to the cheek or chee' | correct | gold 命中（含等价/别名） |
| 1110 | train | Belonging to Indonesia, Irian Jaya is the western portion of | New Guinea | 'New Guinea' | correct | gold 命中（含等价/别名） |
| 1111 | train | How many wheels are there on a sulky? | 2 | 'Two' | correct | gold 别名命中 |
| 1112 | train | At the beginning of 'Two Towers', the second book in 'The Lo | 'GANDALF' | 'Legolas' | incorrect | 单 token 短答 'Legolas'（疑似错答，人工留意 |
| 1113 | train | Octavian, who became Augustus, and Lepidus were two of the ' | MARK ANTONY | 'Mark Antony' | correct | gold 命中（含等价/别名） |
| 1114 | test | What was the name of the British nurse who was shot by a Ger | EDITH CAVELL | 'Edith Cavell' | correct | gold 命中（含等价/别名） |
| 1115 | train | Who coached New Zealand when they won the 2011 Rugby Union W | GRAHAM HENRY | 'John Jones' | incorrect | gold 未命中 |
| 1116 | validation | What name is given to the temperature of -273.15 degrees Cel | ABSOLUTE ZERO | 'Absolute zero' | correct | gold 命中（含等价/别名） |
| 1117 | validation | By what name are the Essex one-day cricket team known? | 'EAGLES' | 'The Essex' | incorrect | gold 未命中 |
| 1118 | test | What first name is shared by Turner Prize winning artists Wa | MARK | 'Mark' | correct | gold 命中（含等价/别名） |
| 1119 | validation | Complete the name of the MLB (Baseball) team based in Arling | '..RANGERS' | 'Rangers' | correct | gold 命中（含等价/别名） |
| 1120 | train | Which now defunct newspaper was originally owned by Eddy Sha | Today | 'The Sunday' | incorrect | gold 未命中 |
| 1121 | train | Until the introduction of the Euro, what is the unit of curr | Schilling | 'Theilling' | incorrect | 单 token 短答 'Theilling'（疑似错答，人工 |
| 1122 | test | Pipistrellus is a genus of which mammal? | BAT | 'bat' | correct | gold 命中（含等价/别名） |
| 1123 | train | How many sides did the pre-decimal British threepence have a | TWELVE | '1' | format_failure | 单 token 函数词/碎片 '1'，无答案内容 |
| 1124 | train | What in Sikhism, is a Kanga? | COMB | 'Com comb' | correct | gold 命中（含等价/别名） |
| 1125 | test | With what area of manufacturing are the names 'Audemars Pigu | WATCHMAKING | 'watchmaking' | correct | gold 命中（含等价/别名） |
| 1126 | test | Complete the sequence: Johnson, Nixon, Ford....? | JIMMY CARTER | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 1127 | test | In which game could you be faced with a 'Simple or Double Sq | BRIDGE | 'Bridge' | correct | gold 命中（含等价/别名） |
| 1128 | train | Which prominent Irish Nationalist was hung for treason in 19 | Roger Casement | 'Michael Collins' | incorrect | gold 未命中 |
| 1129 | train | Which American University is situated in Ithaca, New York? | CORNELL | 'Cornell University' | correct | gold 命中（含等价/别名） |
| 1130 | validation | Who according to the title of a 1992 novel was 'Count Lazzio | 'THE ENGLISH PATIENT' | 'Count' | incorrect | 单 token 短答 'Count'（疑似错答，人工留意） |
| 1131 | train | Who wrote the children's books 'Pigeon Post' and 'Coot Club' | ARTHUR RANSOME | 'David Brown' | incorrect | gold 未命中 |
| 1132 | train | The traditional gift for a ninth anniversary should be made  | POTTERY | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 1133 | train | How many 'Oscars' did the film 'Slumdog Millionaire' win? | 8 | '8' | correct | gold 命中（含等价/别名） |
| 1134 | train | In 1986, whilst facing England which West Indian batsman sco | VIV RICHARDS | 'Vie Richards' | incorrect | gold 未命中 |
| 1135 | validation | Which former US boxer is referred to as the ‘Poet laureate o | Floyd Mayweather Sr | 'Mike Ali' | incorrect | gold 未命中 |
| 1136 | test | The UK television drama series ‘Boys From the Black Stuff’ w | Liverpool | 'B' | format_failure | 单 token 函数词/碎片 'B'，无答案内容 |
| 1137 | train | Who became the host of the UK television game show Blankety  | Les Dawson | 'David Vine' | incorrect | gold 未命中 |
| 1138 | train | Acmeism relates to poetry from the early 20th Century in whi | Russia | 'Russia' | correct | gold 命中（含等价/别名） |
| 1139 | train | Who does the commentary in the UK tv programme ‘Come Dine Wi | Dave Lamb | 'David Brand' | incorrect | gold 未命中 |
| 1140 | test | Which country was invaded by Iraq in 1990? | Kuwait | 'Kuwait' | correct | gold 命中（含等价/别名） |
| 1141 | train | In Greek mythology, Amphitrite, queen of the sea, was the wi | Poseidon | 'Poseidon' | correct | gold 命中（含等价/别名） |
| 1142 | train | Maria Fitzherbert was ‘married’ to which British monarch? | George IV | 'King George IV' | correct | gold 命中（含等价/别名） |
| 1143 | validation | Henry Blake, Charles Winchester and Father Mulcahy are all c | M*A*S*H | 'M*A*S*H' | correct | gold 命中（含等价/别名） |
| 1144 | test | ‘Obey your thirst’ is the advertising slogan for which soft  | Sprite | 'Coke' | incorrect | 单 token 短答 'Coke'（疑似错答，人工留意） |
| 1145 | train | What did fictional detective Sherlock Holmes keep in the toe | Tobacco | 'a pipe' | incorrect | gold 未命中 |
| 1146 | train | Which creatures are used as croquet balls in the novel ‘Alic | Hedgehogs | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 1147 | train | Which Spanish artist painted the series known as ‘Fantasy an | Francisco Goya | ' Francisco Goya' | correct | gold 命中（含等价/别名） |
| 1148 | train | In the 2005 Julian Barnes novel ‘Arthur and George’, who is  | Arthur Conan Doyle | 'Arthur George George' | incorrect | gold 未命中 |
| 1149 | test | The UEFA (Union of European Football Associations) was found | Switzerland | 'Switzerland' | correct | gold 命中（含等价/别名） |
| 1150 | test | The ‘La Scala Opera House’ is in which European city? | Milan | 'The ‘La Scala Opera House’ is in Milan, Italy.' | correct | gold 命中（含等价/别名） |
| 1151 | test | In medicine, algology is the study of what? | Pain | 'P' | format_failure | 单 token 函数词/碎片 'P'，无答案内容 |
| 1152 | validation | The meibomian gland is found in which part of the human body | Eyelid | 'eye' | incorrect | 单 token 短答 'eye'（疑似错答，人工留意） |
| 1153 | train | Which British swimmer won Olympic Gold Medals in 2008 in the | Rebecca Adlington | 'Mark Pe' | incorrect | gold 未命中 |
| 1154 | train | The Cuatro Torres Business Area is in which European city? | Madrid | 'Madrid' | correct | gold 命中（含等价/别名） |
| 1155 | test | In the poem ‘Monday’s Child’, what is Wednesday’s child full | Woe | "Wednesday's child is full of grace" | incorrect | gold 未命中 |
| 1156 | test | Which clothing chain was founded by brothers Clemens and Aug | C&A | 'H&M' | incorrect | 单 token 短答 'H&M'（疑似错答，人工留意） |
| 1157 | validation | Which fictional character is the subject of George Frampton’ | Peter Pan | 'Peter Pan' | correct | gold 命中（含等价/别名） |
| 1158 | train | In which London street does fictional character Sweeney Todd | Fleet Street | 'B Fleet Street' | correct | gold 命中（含等价/别名） |
| 1159 | train | The Nullarbor Plain is in which country? | Australia | 'Australia' | correct | gold 命中（含等价/别名） |
| 1160 | train | Who was the first Hanover King of England? | George I | 'George I' | correct | gold 命中（含等价/别名） |
| 1161 | validation | The 1981 film ‘Chariots of Fire’ was based on the stories of | Harold Abrahams and Eric | 'David Foster and Eric Light.' | incorrect | gold 未命中 |
| 1162 | test | What is the US state capital of Kansas? | Topeka | 'Kansas' | incorrect | 单 token 短答 'Kansas'（疑似错答，人工留意） |
| 1163 | train | Who wrote the novel ‘Seven Pillars of Wisdom’? | T E Lawrence | 'Thomas Lawrence' | incorrect | gold 未命中 |
| 1164 | validation | Which British-American actress died on 23rd March 2011, aged | Elizabeth Taylor | 'Elizabeth Taylor' | correct | gold 命中（含等价/别名） |
| 1165 | train | Who became US President John Kennedy’s Vice President in 196 | Lyndon B Johnson | 'Richard Johnson' | incorrect | gold 未命中 |
| 1166 | train | Blinky, Mr Teeny and Jub-Jub are all animals in which US ani | The Simpsons | 'The Park' | incorrect | gold 未命中 |
| 1167 | test | What is the name of the steam locomotive which set the world | Mallard | ' Mallard' | correct | gold 命中（含等价/别名） |
| 1168 | train | What type of creature is a bananaquit? | Bird | 'A bananaquit is a type of bird.' | correct | gold 命中（含等价/别名） |
| 1169 | train | What is the art of hand-making cricket bats called? | Podshaving | ' Batting' | incorrect | 单 token 短答 ' Batting'（疑似错答，人工留 |
| 1170 | test | In the Charles Dickens novel ‘Oliver Twist’ what is the name | Bulls Eye | 'T' | format_failure | 单 token 函数词/碎片 'T'，无答案内容 |
| 1171 | validation | Elliot Carver is the villain in which James Bond film? | Tomorrow Never Dies | 'Moonraker' | incorrect | 单 token 短答 'Moonraker'（疑似错答，人工 |
| 1172 | train | What is the system of raised dots called which blind people  | Braille | 'Braille' | correct | gold 命中（含等价/别名） |
| 1173 | validation | In the nursery rhyme ‘Oranges and Lemons’, the bells of whic | St Martins | 'Paul Paul Church' | incorrect | gold 未命中 |
| 1174 | train | In the US, which state lies to the west of New Hampshire? | Vermont | 'Maine' | incorrect | 单 token 短答 'Maine'（疑似错答，人工留意） |
| 1175 | train | Which Radio 2 DJ christened ‘Dallas’ character Lucy Ewing ‘T | Terry Wogan | 'Chris Bruce' | incorrect | gold 未命中 |
| 1176 | test | What was the name of the band, featuring members of Thin Liz | The Greedies (originally | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1177 | train | What is the nickname of the great bell of the clock at the n | Big Ben | 'Big Ben' | correct | gold 命中（含等价/别名） |
| 1178 | test | In June 1978, who became the first cricketer to score a cent | Ian Botham | 'Don Bradman' | incorrect | gold 未命中 |
| 1179 | train | On a standard dartboard, which number lies between 12 and 20 | 5 | '15' | format_failure | 单 token 函数词/碎片 '15'，无答案内容 |
| 1180 | train | In Ian Fleming’s novel ‘Moonraker’, Sir Hugo Drax is suspect | Bridge | 'Poker' | incorrect | 单 token 短答 'Poker'（疑似错答，人工留意） |
| 1181 | train | What was the name of the Cunard ocean liner which was launch | Mauretania | 'Oceanic' | incorrect | 单 token 短答 'Oceanic'（疑似错答，人工留意 |
| 1182 | train | In which James Bond film does actress Jane Seymour play Soli | Live and Let Die | 'Goldeneye' | incorrect | 单 token 短答 'Goldeneye'（疑似错答，人工 |
| 1183 | train | To ‘Defenestrate’ is to throw something or someone out of wh | A window | 'a window' | correct | gold 命中（含等价/别名） |
| 1184 | train | During which year was Washington DC declared the capital of  | 1790 | '1790' | correct | gold 命中（含等价/别名） |
| 1185 | test | Who played boxer Jim Braddock in the 2005 film ‘Cinderella m | Russell Crowe | 'Tom Hanks' | incorrect | gold 未命中 |
| 1186 | train | In the UK, the LTA is the governing body of which sport? | Tennis | 'Tnis' | incorrect | 单 token 短答 'Tnis'（疑似错答，人工留意） |
| 1187 | validation | Who played Brad Pitt’s wife Theresa Mills in the film ‘Seven | Gwyneth Paltrow | 'Morgan Fox' | incorrect | gold 未命中 |
| 1188 | test | St Joseph’s Day is celebrated during which month of the year | March -19th | 'March' | incorrect | 单 token 短答 'March'（疑似错答，人工留意） |
| 1189 | train | Which is the largest state in the US? | Alaska | 'Alaska' | correct | gold 命中（含等价/别名） |
| 1190 | train | Which English Rugby Union team play their home games at Adam | London Wasps | 'Bps' | incorrect | 单 token 短答 'Bps'（疑似错答，人工留意） |
| 1191 | test | Apart from white, what colour are the other two ‘triangles’  | Blue | 'Blue' | correct | gold 命中（含等价/别名） |
| 1192 | validation | How many US Presidents have been impeached? | Two | 'Two' | correct | gold 命中（含等价/别名） |
| 1193 | test | Arturo Frondizi became president of which South American cou | Argentina | 'Argentina' | correct | gold 命中（含等价/别名） |
| 1194 | train | On 7th July 2011 which UK tabloid was closed down because jo | News of the World | 'The Sun' | incorrect | gold 未命中 |
| 1195 | train | Which island group became known as The Friendly Islands? | Tonga | 'The Cook Islands' | incorrect | gold 未命中 |
| 1196 | train | ‘Probably the best lager in the world’ is the advertising sl | Carlsberg | 'Cor' | incorrect | 单 token 短答 'Cor'（疑似错答，人工留意） |
| 1197 | test | Who won the 1989 Ladies Singles Wimbledon Championship? | Steffi Graf | 'Chris Evert' | incorrect | gold 未命中 |
| 1198 | validation | Which American car manufacturer has a logo which features th | Buick | 'Chevrolet' | incorrect | 单 token 短答 'Chevrolet'（疑似错答，人工 |
| 1199 | train | The Museum of Bags and Purses is in which European city? | Amsterdam | 'London' | incorrect | 单 token 短答 'London'（疑似错答，人工留意） |
| 1200 | test | How many times did Actress Zsa Zsa Gabor marry? | Nine | '8' | format_failure | 单 token 函数词/碎片 '8'，无答案内容 |
| 1201 | train | American singer Al, late British television host Hughie and  | Green | 'G' | format_failure | 单 token 函数词/碎片 'G'，无答案内容 |
| 1202 | train | Who wrote the 1975 novel ‘The History Man’? | Malcolm Bradbury | 'John Barnes' | incorrect | gold 未命中 |
| 1203 | validation | In the 1965 film ‘Those Magnificent Men in Their Flying Mach | 10,000 | '£1,000' | incorrect | gold 未命中 |
| 1204 | validation | Who directed the 1969 film ‘Women in Love’, starring Oliver  | Ken Russell | 'David Lean' | incorrect | gold 未命中 |
| 1205 | train | Which country invaded the Falkland Islands in April 1982? | Argentina | 'Argentina invaded the Falkland Islands in April 19' | correct | gold 命中（含等价/别名） |
| 1206 | test | A group of which fish is called a Lap? | Cod | 'Trfish' | incorrect | 单 token 短答 'Trfish'（疑似错答，人工留意） |
| 1207 | test | What is the title of the 18th Century novel by Lawrence Ster | (The Life and Opinions o | 'Tristram Shandy' | correct | gold 命中（含等价/别名） |
| 1208 | test | The Aviva Sports Stadium is in which European country? | Ireland | 'Ireland' | correct | gold 命中（含等价/别名） |
| 1209 | train | Who played Gomez Addams in the 1993 film ‘Addams Family Valu | Raul Julia | 'Tim Curry' | incorrect | gold 未命中 |
| 1210 | validation | In which UK city is Headingley railway station? | Leeds | 'Headingley railway station is located in Leeds, En' | correct | gold 命中（含等价/别名） |
| 1211 | train | Which, then fictional, award is mentioned in the opening sce | The Sarah Siddons Award | 'Theie Award' | incorrect | gold 未命中 |
| 1212 | test | What disease was Robert the Bruce, King of Scotland, said to | Leprosy | 'plague' | incorrect | 单 token 短答 'plague'（疑似错答，人工留意） |
| 1213 | train | In humans, the medical condition Hyposmia affects which of t | Smell | 'Smell' | correct | gold 命中（含等价/别名） |
| 1214 | validation | Which London football club won the last FA cup final held at | Chelsea FC | 'Arsenal' | incorrect | 单 token 短答 'Arsenal'（疑似错答，人工留意 |
| 1215 | train | Which is the only US state to begin with the letter ‘U’? | Utah | 'Utah' | correct | gold 命中（含等价/别名） |
| 1216 | train | Who played Thelma in the UK television series ‘The Likely La | Brigit Forsyth | 'Jane Lee' | incorrect | gold 未命中 |
| 1217 | train | In Greek mythology, how many heads does Cerberus, the dog wh | Three | 'three' | correct | gold 命中（含等价/别名） |
| 1218 | train | Breve, Mocha and Americano are all types of which drink? | Coffee | 'coffee' | correct | gold 命中（含等价/别名） |
| 1219 | test | Sound engineer Peter Lodge first announced which phrase on t | Mind the gap | 'Mind' | incorrect | 单 token 短答 'Mind'（疑似错答，人工留意） |
| 1220 | test | Who did Germany defeat to win the 1990 FIFA World Cup? | Argentina | 'Italy' | incorrect | 单 token 短答 'Italy'（疑似错答，人工留意） |
| 1221 | test | What is the name of the life-size plastic dummies in the tel | Autons | 'Cymen' | incorrect | 单 token 短答 'Cymen'（疑似错答，人工留意） |
| 1222 | train | Who designed the red telephone box, which first appeared in  | Sir Giles Gilbert Scott | 'Charles Gill' | incorrect | gold 未命中 |
| 1223 | train | Strangles is a bacterial infection of the respiratory tract  | Horse | 'horses' | correct | gold 别名命中 |
| 1224 | train | Saint Fidelis Church, otherwise known as The Cathedral of th | Kansas | 'New Mexico' | incorrect | gold 未命中 |
| 1225 | train | In March 1951, which comic strip character first appeared in | Dennis the Menace | 'Garfield' | incorrect | 单 token 短答 'Garfield'（疑似错答，人工留 |
| 1226 | test | The Formula One Sepang International Circuit is in which cou | Malaysia | 'Malaysia' | correct | gold 命中（含等价/别名） |
| 1227 | train | The Paragons originally recorded which 1980 hit single by Bl | The Tide is High | 'Raptureanne' | incorrect | 单 token 短答 'Raptureanne'（疑似错答， |
| 1228 | train | Arkansas Black is a variety of which fruit? | Apple | 'apple' | correct | gold 命中（含等价/别名） |
| 1229 | train | What was is the name of Penelope Pitstop’s car in the childr | Compact Pussycat | 'Penelope' | incorrect | 单 token 短答 'Penelope'（疑似错答，人工留 |
| 1230 | train | The discovery of what in Australia in February 1851 is tradi | Gold | 'gold' | correct | gold 命中（含等价/别名） |
| 1231 | test | How is the year 1994 depicted in Roman Numerals? | MCMXCIV | 'The year 1994 in Roman Numerals is MCXCIV' | correct | gold 别名命中 |
| 1232 | train | The 1995 autobiography ‘Dreams From My Father’ is by which U | Barack Obama | ' Barack Obama' | correct | gold 命中（含等价/别名） |
| 1233 | train | 8Â Fort Ville-Marie was the original name of which Canadian  | Montreal | 'Montreal' | correct | gold 命中（含等价/别名） |
| 1234 | train | Which was Disney's second animated film? | Pinocchio | 'Pinocchio' | correct | gold 命中（含等价/别名） |
| 1235 | train | What would a Scotsman do with a spurtle? | Eat porridge | 'st' | format_failure | 单 token 函数词/碎片 'st'，无答案内容 |
| 1236 | train | When running around the athletics track, what does the sound | The last lap | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1237 | validation | Who played 'Chief Inspector Dreyfus' in the 'Pink Panther' f | Herbert Lom | 'Peter Sellers' | incorrect | gold 未命中 |
| 1238 | train | Who played Dr Richard Kimble in the 1993 film The Fugitive? | Harrison Ford | ' Harrison Ford' | correct | gold 命中（含等价/别名） |
| 1239 | test | In 1967, who was the first DJ on Radio 1? | Tony Blackburn | 'John Peel' | incorrect | gold 未命中 |
| 1240 | test | Patusnaya and mallasol are types of what? | Caviar | 'soil' | incorrect | 单 token 短答 'soil'（疑似错答，人工留意） |
| 1241 | train | In a petrol engine what component mixes fuel and air? | The carburettor | ' Carburetor' | correct | gold 别名命中 |
| 1242 | train | Ascorbic acid is usually known as what? | Vitamin C | 'vitamin C' | correct | gold 命中（含等价/别名） |
| 1243 | train | Until 1796, there was a state in the United States called Fr | Tennessee! | 'Tennessee' | correct | gold 命中（含等价/别名） |
| 1244 | train | The Southern Alps can be found in which country? | New Zealand | 'New Zealand' | correct | gold 命中（含等价/别名） |
| 1245 | train | Beaufort who created The Wind Scale had which profession ? | Sailor | 'nav Navy' | incorrect | gold 未命中 |
| 1246 | train | Who played the role of George Carter in The Sweeney? | Dennis Waterman | 'David Lee' | incorrect | gold 未命中 |
| 1247 | train | 'Diva' released in 1992 was the first solo album for who? | Annie Lennox | 'Celine Dion' | incorrect | gold 未命中 |
| 1248 | validation | 'Roquefort Cheese' is made from what sort of milk? | Ewe's Milk | "she's milk" | incorrect | gold 未命中 |
| 1249 | train | Which King reigned for only 325 days? | Edward 8th | 'King Richard II' | incorrect | gold 未命中 |
| 1250 | train | In British Wrestling who was Shirley Crabtree? | Big Daddy | 'Shirley Crabtree' | incorrect | gold 未命中 |
| 1251 | train | What was Britain called - before it was Britain? | Albion | 'Great' | incorrect | 单 token 短答 'Great'（疑似错答，人工留意） |
| 1252 | train | What is Africa's most populated country? | Nigeria | 'Nigeria' | correct | gold 命中（含等价/别名） |
| 1253 | test | Which comedy duo were born Bartholomew and Wiseman? | Morecambe and Wise | 'Bob and Hardy' | incorrect | gold 未命中 |
| 1254 | validation | Who founded the Jaguar motor company? | William Lyons | 'Henry Lyons' | incorrect | gold 未命中 |
| 1255 | validation | What was Billy Connolly's only No. 1 hit? | D-I-V-O-R-C-E | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1256 | train | Which fashion craze was made popular by the film 'Flashdance | Legwarmers | 'Leg pants' | incorrect | gold 未命中 |
| 1257 | train | The rivers Trent and Ouse flow into which estuary? | Humber | 'Humber' | correct | gold 命中（含等价/别名） |
| 1258 | train | Aviemore, in Scotland is at the heart of which National Park | The Cairngorms National  | 'High Ness National Park' | incorrect | gold 未命中 |
| 1259 | train | Which is the largest cat in the world? | Siberian Tiger | 'Tiger' | incorrect | 单 token 短答 'Tiger'（疑似错答，人工留意） |
| 1260 | validation | Who had an August 1969 No.1 with 'In The Year 2525 (Exordium | Zager & Evans | 'T' | format_failure | 单 token 函数词/碎片 'T'，无答案内容 |
| 1261 | validation | Founded in 1775, George Washington was the Commander-in-Chie | Continental Army | 'Contin Continental Army' | correct | gold 命中（含等价/别名） |
| 1262 | test | What boxer was stripped of his heavyweight boxing titles whe | Muhammed Ali | 'Mu Ali' | incorrect | gold 未命中 |
| 1263 | train | According to Arthurian legend, Arthur's wife Guinevere, had  | Lancelot | 'Lancelot' | correct | gold 命中（含等价/别名） |
| 1264 | test | In which city would you find the International Court of Just | The Hague, Netherlands | 'The Hague' | correct | gold 命中（含等价/别名） |
| 1265 | train | What noted film director and producer, born on May 14, 1944, | George Lucas | 'George Lucas' | correct | gold 命中（含等价/别名） |
| 1266 | train | May 15, 1940 saw what fast food chain get started in San Ber | McDonald's | 'Burger King' | incorrect | gold 未命中 |
| 1267 | validation | Also known as the Roland Garros, what is the Grand Slam Tenn | French Open | 'French Open' | correct | gold 命中（含等价/别名） |
| 1268 | train | In 2001: A Space Odyssey, what was the name of the computer  | HAL 9000 | 'HAL' | incorrect | 单 token 短答 'HAL'（疑似错答，人工留意） |
| 1269 | validation | Portrayed by James Doohan, what was the actual name of the e | Montgomery Scott | ' Montgomery Scott' | correct | gold 命中（含等价/别名） |
| 1270 | test | Who flew a kite in a storm on June 15, 1750, proving that li | Benjamin Franklin | 'Benjamin Franklin' | correct | gold 命中（含等价/别名） |
| 1271 | train | The first civilians executed for espionage in the United Sta | Julius and Ethel Rosenbe | 'Julius and Ethel Rosenberg' | correct | gold 命中（含等价/别名） |
| 1272 | train | June 17, 1994 saw a low speed chase up Interstate 405 as OJ  | White Ford Bronco | 'Fordco' | incorrect | 单 token 短答 'Fordco'（疑似错答，人工留意） |
| 1273 | train | Used as an alloy in making high-speed cutting tools, mo is t | Molybdenum | 'molybdenum' | correct | gold 命中（含等价/别名） |
| 1274 | validation | What do you practice in a dojo? | Martial Arts | 'martial arts' | correct | gold 命中（含等价/别名） |
| 1275 | train | The 1999 Spike Lee film Summer of Sam focuses on the crimes  | David Berkowitz | 'David Berkowitz' | correct | gold 命中（含等价/别名） |
| 1276 | train | Named after an abduction at the Japanese Embassy in a South  | Lima Syndrome | 'La syndrome' | incorrect | gold 未命中 |
| 1277 | train | By what name are Rontgen rays more commonly known? | X-Rays | 'Rontgen rays are more commonly known as X-rays.' | correct | gold 命中（含等价/别名） |
| 1278 | test | Which Apollo mission, which was launched on July 16, 1969, w | 11 | 'Apollo 11' | correct | gold 命中（含等价/别名） |
| 1279 | train | In the Tour de France who wears the polka dot jersey? | The king of the mountain | 'The mountains leader' | incorrect | gold 未命中 |
| 1280 | train | On July 21, 1969, who became the first man to set foot on th | Neil Armstrong | 'Neil Armstrong' | correct | gold 命中（含等价/别名） |
| 1281 | train | Anchored by the star Polaris, the constellation ursa minor r | bear | 'small bear' | correct | gold 命中（含等价/别名） |
| 1282 | train | What Latin phrase, which translates as Out of many, one, is  | E Pluribus Unum | 'E Pluribus Un' | incorrect | gold 未命中 |
| 1283 | test | The Sharks face off against what gang in Leonard Bernsteins  | The Jets | 'The Jets' | correct | gold 命中（含等价/别名） |
| 1284 | train | What ice cream company produces flavors such as Everything B | Ben & Jerry's | "By's" | incorrect | gold 未命中 |
| 1285 | train | The gravesite of what American writer, buried in Baltimore,  | Edgar Allen Poe | ' Edgar Allan Poe' | correct | gold 别名命中 |
| 1286 | validation | What type of rain did Prince sing about in 1984? | Purple Rain | 'Purple rain' | correct | gold 命中（含等价/别名） |
| 1287 | validation | The Dukes of Hazzard, the CBS TV series that debuted on Jan  | Bo and Luke Duke | 'Bo and Bo' | incorrect | gold 未命中 |
| 1288 | test | What synthetic opioid is used to help treat heroin addiction | Methadone | 'methadone' | correct | gold 命中（含等价/别名） |
| 1289 | train | Who broke Lou Gehrig's record by playing in his 2131st conse | Cal Ripken, Jr | 'Alex Rose' | incorrect | gold 未命中 |
| 1290 | train | What magician-turned-actor portrayed a recurring role as a t | Harry Anderson | 'David Williams' | incorrect | gold 未命中 |
| 1291 | train | On Sept 18, 1947, which branch of the US Military became an  | US Air Force | 'US Air Force' | correct | gold 命中（含等价/别名） |
| 1292 | train | The journal of which Amsterdam schoolgirl was first publishe | Anne Frank | 'Anie Frank' | incorrect | gold 未命中 |
| 1293 | train | Name the 1998 movie from the IMDB plot summary: "A former ne | American History X | 'Americanhead' | incorrect | 单 token 短答 'Americanhead'（疑似错答 |
| 1294 | train | Commonly known as nipplegate, whose wardrobe malfunction dur | Janet Jackson | 'Janet Jackson' | correct | gold 命中（含等价/别名） |
| 1295 | train | What is the 3rd largest car rental company in the United Sta | Alamo | 'Hertz' | incorrect | 单 token 短答 'Hertz'（疑似错答，人工留意） |
| 1296 | validation | What Arizona national park was formed over millions of years | The Grand Canyon | 'Grand Canyon' | correct | gold 命中（含等价/别名） |
| 1297 | train | On Oct 28, 1886, the rotund one himself, Grover Cleveland, o | The Statue of Liberty | 'Statue of Liberty' | correct | gold 命中（含等价/别名） |
| 1298 | validation | Used primarily to talk to the dead (and the scare the snot o | Ouija Board | 'Ouija board' | correct | gold 命中（含等价/别名） |
| 1299 | train | What company advertised itself with the slogan “We’ll leave  | Motel 6 | 'AT' | format_failure | 单 token 函数词/碎片 'AT'，无答案内容 |
| 1300 | train | First put on sale last week, Decision Points, currently rank | George W. Bush | 'George Obama' | incorrect | gold 未命中 |
| 1301 | train | What planets orbit takes it the furthest away from the sun? | Neptune | 'Pluto' | incorrect | 单 token 短答 'Pluto'（疑似错答，人工留意） |
| 1302 | train | Although it ended up being very ineffective, what was the na | Maginot Line | 'Maginot Line' | correct | gold 命中（含等价/别名） |
| 1303 | train | What is the name for the flexible, connective tissue found i | Cartilage | 'cartilage' | correct | gold 命中（含等价/别名） |
| 1304 | validation | What radio station do you find at 90.3 on your FM dial? | KEXP | 'W' | format_failure | 单 token 函数词/碎片 'W'，无答案内容 |
| 1305 | train | The sinking of what battleship in Havana harbor on Feb 15, 1 | USS Maine | 'USS Maine' | correct | gold 命中（含等价/别名） |
| 1306 | train | In what card game do you need the queen of spades to shoot t | Hearts | 'Eades' | incorrect | 单 token 短答 'Eades'（疑似错答，人工留意） |
| 1307 | train | Who's missing: Bashful, Doc, Dopey, Grumpy, Happy, Sleepy | Sneezy | 'S' | format_failure | 单 token 函数词/碎片 'S'，无答案内容 |
| 1308 | train | What was the name of two tyrants who ruled Syracuse in the 2 | Dionysius | 'H' | format_failure | 单 token 函数词/碎片 'H'，无答案内容 |
| 1309 | test | Which ocean is closest to the capital of the USA? | Atlantic | 'The Atlantic Ocean' | correct | gold 命中（含等价/别名） |
| 1310 | train | Which river flows through Cologne? | Rhine | 'Rhine' | correct | gold 命中（含等价/别名） |
| 1311 | train | "Who has hosted the US series ""Power of 10"", ""Whose Line  | Drew Carey | 'Ryan Carey' | incorrect | gold 未命中 |
| 1312 | train | What name has been used on Irish postage stamps since 1922,  | ire | 'Eire' | incorrect | 单 token 短答 'Eire'（疑似错答，人工留意） |
| 1313 | train | Where, in 2011 and since, is a major gathering place in Egyp | Tahrir Square | 'Tahrir Square' | correct | gold 命中（含等价/别名） |
| 1314 | train | What is the surname of sisters and singers Dannii and Kylie? | Minogue | 'Minogue' | correct | gold 命中（含等价/别名） |
| 1315 | train | What is the name of Tony and Cherie Blair's daughter? | Kathryn | 'Ch' | format_failure | 单 token 函数词/碎片 'Ch'，无答案内容 |
| 1316 | train | What term is used for the actress that has the main part in  | Leading lady | 'Lead' | incorrect | 单 token 短答 'Lead'（疑似错答，人工留意） |
| 1317 | validation | Dishes prepared with spinach can be referred to as what? | la Florentine | 'spinach dishes' | incorrect | gold 未命中 |
| 1318 | train | "John Wayne appeared as a centurion in the film ""The Greate | Truly this man was the s | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1319 | test | Whose alter ego is Sasha Fierce? | Beyonc | 'Beyonce' | incorrect | 单 token 短答 'Beyonce'（疑似错答，人工留意 |
| 1320 | train | What is a mosquito-borne virus, also known as breakbone feve | Dengue fever | 'due virus' | incorrect | gold 未命中 |
| 1321 | validation | Christmas Island is administered by which country? | Australia | 'Australia' | correct | gold 命中（含等价/别名） |
| 1322 | train | Who is the next in this series: John L. Sullivan, James J. C | Tommy Burns | 'Jackie' | incorrect | 单 token 短答 'Jackie'（疑似错答，人工留意） |
| 1323 | validation | What was the name of the operation whereby 1,373 U.S. citize | Operation Frequent Wind | 'Operation Eagle' | incorrect | gold 未命中 |
| 1324 | train | "Literally, what old French word translates approximately as | Blancmange | 'bl' | format_failure | 单 token 函数词/碎片 'bl'，无答案内容 |
| 1325 | train | Who was the only Prime Minister of Great Britain born outsid | Andrew Bonar Law | 'John Wilson' | incorrect | gold 未命中 |
| 1326 | validation | What is a legislative or executive act by which a state rest | Amnesty | 'amnesty' | correct | gold 命中（含等价/别名） |
| 1327 | train | Quadrille, a popular card game in the 18th century, is for f | 40 | '52' | format_failure | 单 token 函数词/碎片 '52'，无答案内容 |
| 1328 | test | On the buttons of a VCR or DVD player, what does the sign in | Fast forward | 'Fast' | incorrect | 单 token 短答 'Fast'（疑似错答，人工留意） |
| 1329 | train | The composer Frdric Chopin had a decade-long affair with whi | George Sand | 'Ge George Sand' | correct | gold 命中（含等价/别名） |
| 1330 | train | The Australian Tennis Open is played in what city? | Melbourne | 'Melbourne' | correct | gold 命中（含等价/别名） |
| 1331 | validation | He was the fourth of 6 children and the oldest surviving, wa | Adolf Hitler | 'Martin Luther' | incorrect | gold 未命中 |
| 1332 | train | What is a name for the abstract study of topics such as quan | Mathematics | 'Mathematics' | correct | gold 命中（含等价/别名） |
| 1333 | test | "Which German was deprived of his nationality in 1938 mainly | Erich Maria Remarque | 'Paul Mann' | incorrect | gold 未命中 |
| 1334 | train | "What is the first line of ""Walk on the Wild Side"" by Lou  | Holly came from Miami F  | 'Hey' | incorrect | 单 token 短答 'Hey'（疑似错答，人工留意） |
| 1335 | train | What is the name of the scientific discipline that deals wit | Geodesy | 'Geodesy' | correct | gold 命中（含等价/别名） |
| 1336 | train | In the books by A A Milne, what was Eeyore? | Donkey | 'a donkey' | correct | gold 命中（含等价/别名） |
| 1337 | test | Which pigment is named after an Italian city? | Sienna | 'Venna' | incorrect | 单 token 短答 'Venna'（疑似错答，人工留意） |
| 1338 | train | What is someone allergic to if they have coeliac disease? | Gluten | 'gluten' | correct | gold 命中（含等价/别名） |
| 1339 | train | Yelena Isinbayeva broke her first World record in 2003 and c | Women's Pole Vault | 'high jump' | incorrect | gold 未命中 |
| 1340 | validation | The ship Andrea Gail features in which 1997 book and 2000 fi | The Perfect Storm | 'In The Perfect Storm' | correct | gold 命中（含等价/别名） |
| 1341 | test | Which 19th century American poet wrote over 1,000 poems whic | Emily Dickinson | 'Emily Dickinson' | correct | gold 命中（含等价/别名） |
| 1342 | train | Who was crowned MotoGP World Champion after he finished thir | Jorge Lorenzo | 'Case Lorenzo' | incorrect | gold 未命中 |
| 1343 | validation | What was the name of the 1976 film that told the story of Wo | Bound for Glory | 'Woody Guthrie' | incorrect | gold 未命中 |
| 1344 | validation | The main international cricket competitions are Test matches | Twenty20 Internationals | 'T20' | incorrect | 单 token 短答 'T20'（疑似错答，人工留意） |
| 1345 | test | Marat, Robespierre, Danton are names associated with what ev | The French Revolution | 'French Revolution' | correct | gold 命中（含等价/别名） |
| 1346 | validation | Cayenne, after which the spicy condiment is named, is a city | French Guiana | 'French' | incorrect | 单 token 短答 'French'（疑似错答，人工留意） |
| 1347 | train | Where is the homeland of Queen Boudica (also Boudicca or Boa | East Anglia | 'England' | incorrect | 单 token 短答 'England'（疑似错答，人工留意 |
| 1348 | train | In a film script, what do the letters ECU mean? | Extreme Close Up | 'Extreme shot' | incorrect | gold 未命中 |
| 1349 | train | Since the Association of Tennis Professionals (ATP) World To | Rafael Nadal | 'Roger Federer' | incorrect | gold 未命中 |
| 1350 | train | What is the name given to a bone fracture when one part of i | Impacted | 'Impacted fracture' | correct | gold 命中（含等价/别名） |
| 1351 | test | What year did the cable television network ESPN made its deb | 1979 | '1979' | correct | gold 命中（含等价/别名） |
| 1352 | train | "Which British composer wrote ""The Dam Busters March""?" | Eric Coates | 'John Williams' | incorrect | gold 未命中 |
| 1353 | validation | Which of Queen Elizabeth's children is the lowest in success | Anne | 'Andrew Andrew' | incorrect | gold 未命中 |
| 1354 | train | A synonym for french kissing would be what? | Cataglottis | 'k' | format_failure | 单 token 函数词/碎片 'k'，无答案内容 |
| 1355 | train | "The book ""Dirty Sexy Politics"", released in 2010, was abo | John McCain | 'Hillary Clinton' | incorrect | gold 未命中 |
| 1356 | test | Macao Special Administrative Region of the People's Republic | Textile and garment manu | 'ret' | incorrect | 单 token 短答 'ret'（疑似错答，人工留意） |
| 1357 | validation | In which country was Saddam Hussein President 1979-2003, bei | Iraq | 'Iraq' | correct | gold 命中（含等价/别名） |
| 1358 | train | Calvados apple brandy is traditionally produced in which cou | France | 'France' | correct | gold 命中（含等价/别名） |
| 1359 | train | In which country did Queen Isabella secure the throne when h | Spain | 'Spain' | correct | gold 命中（含等价/别名） |
| 1360 | train | What game, created in 1904 by a quaker, Elizabeth (Lizzie) P | Monopoly | 'Monopoly' | correct | gold 命中（含等价/别名） |
| 1361 | test | The first Paralympic Games to officially tie in with the Sum | Rome | 'The first Paralympic Games to officially tie in wi' | correct | gold 命中（含等价/别名） |
| 1362 | train | What is the name for a large circular stained glass window f | Rose window | 'ros rose window' | correct | gold 命中（含等价/别名） |
| 1363 | train | What is the name of the son of Pete Wentz and Ashlee Simpson | Bronx Mowgli | 'Max' | incorrect | 单 token 短答 'Max'（疑似错答，人工留意） |
| 1364 | train | "Which 19th century English writer wrote ""Swallows and Amaz | Arthur Ransome | 'Kenugh' | incorrect | 单 token 短答 'Kenugh'（疑似错答，人工留意） |
| 1365 | train | In which country did Juan Domingo Peron seize power in 1943, | Argentina | 'Argentina' | correct | gold 命中（含等价/别名） |
| 1366 | train | The U.S. Masters, one of the four major championships in pro | Augusta National Golf Cl | 'August National Golf Club' | incorrect | gold 未命中 |
| 1367 | train | On 12 September 1995, the Belarusian air force shot down a g | Gordon Bennett Cup | 'Red Trophy' | incorrect | gold 未命中 |
| 1368 | validation | The highest mountain in North America is part of which mount | Alaska Range | 'Rock' | incorrect | 单 token 短答 'Rock'（疑似错答，人工留意） |
| 1369 | train | Which conflict began in England in 1455 after King Henry VI, | The Wars of the Roses | 'Wars of the Roses' | correct | gold 命中（含等价/别名） |
| 1370 | test | "Which 16th century Venetian, born Jacopo Robusti, studied u | Tintoretto | 'Titian' | incorrect | 单 token 短答 'Titian'（疑似错答，人工留意） |
| 1371 | test | Which group of around 200 Greek islands in the Aegean Sea in | Cyclades | 'Cyclades' | correct | gold 命中（含等价/别名） |
| 1372 | train | "Which German social economist of Jewish descent, expelled f | Karl Marx | 'Karl Marx' | correct | gold 命中（含等价/别名） |
| 1373 | test | The English cities of Gloucester and Worcester are on which  | River Severn | ' River Severn' | correct | gold 命中（含等价/别名） |
| 1374 | train | Which British comedy-drama series (1979 to 1994) starred Geo | Minder | '"The Heat of the Game" is the British comedy-drama' | incorrect | gold 未命中 |
| 1375 | train | Prince Philip, Duke of Edinburgh, was born on which island? | Corfu | 'Gte' | incorrect | 单 token 短答 'Gte'（疑似错答，人工留意） |
| 1376 | train | Who was the leader of the Peasant's Revolt in 1381 who, afte | Wat Tyler | 'W Wat Tyler' | correct | gold 命中（含等价/别名） |
| 1377 | test | Australian Shane Warne is associated with which sport? | Cricket | 'Cricket' | correct | gold 命中（含等价/别名） |
| 1378 | train | What was the name of the computer in Stanley Kubricks 2001:  | HAL | 'HAL' | correct | gold 命中（含等价/别名） |
| 1379 | train | What is a popular name for the North American bison? | Buffalo | 'Balo' | incorrect | 单 token 短答 'Balo'（疑似错答，人工留意） |
| 1380 | test | Badminton debuted at the 1992 Summer Olympics. How many diff | 5 | '5' | correct | gold 命中（含等价/别名） |
| 1381 | validation | What name was given to a series of thirty evening radio spee | Fireside chats | 'Fireside chats' | correct | gold 命中（含等价/别名） |
| 1382 | train | The final carrier of the Olympic flame in the Olympic Torch  | A sports celebrity of th | 'a celebrity athlete' | incorrect | gold 未命中 |
| 1383 | validation | What was the first name of de Gaulle, the first President of | Charles | 'Charles' | correct | gold 命中（含等价/别名） |
| 1384 | train | Measuring from the closest point of each of these countries  | Canada | 'Ch' | format_failure | 单 token 函数词/碎片 'Ch'，无答案内容 |
| 1385 | validation | "What is the setting for the Alfred Hitchcock film ""The Bir | Bodega Bay, California | 'San' | incorrect | 单 token 短答 'San'（疑似错答，人工留意） |
| 1386 | test | After sporadic visits by European explorers and merchants fr | Australia | 'Australia' | correct | gold 命中（含等价/别名） |
| 1387 | train | Lee Kuan Yew and Goh Chok Tong were the first two Prime Mini | The Republic of Singapor | 'Singapore' | correct | gold 别名命中 |
| 1388 | train | Farthings were in use in England as coinage from the 13th ce | 960 | '46' | format_failure | 单 token 函数词/碎片 '46'，无答案内容 |
| 1389 | train | What was the Mississippi State Penitentiary formerly called? | Parchman Farm | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1390 | train | What name is given to the syndrome which involves a delusion | Clinical lycanthropy | 'Lycanth syndrome' | incorrect | gold 未命中 |
| 1391 | test | "Where would one find ""Bachmann's bundle""?" | The human heart | 'human' | incorrect | 单 token 短答 'human'（疑似错答，人工留意） |
| 1392 | train | In 1848, Mexico ratified the Treaty of Guadalupe Hidalgo, of | Land | 'California' | incorrect | 单 token 短答 'California'（疑似错答，人 |
| 1393 | train | The Great Sphinx of Giza in Egypt is a statue of a reclining | Human | 'human' | correct | gold 命中（含等价/别名） |
| 1394 | validation | What is the disease that Stephen Hawking has? | Motor neuron disease | 'amyotrophic lateral sclerosis' | incorrect | gold 未命中 |
| 1395 | train | Formula 1 driver Ayrton Senna died while leading the 1994 Sa | Imola | 'Imola' | correct | gold 命中（含等价/别名） |
| 1396 | test | In which novel does Michael Henchard sell his wife and child | The Mayor of Casterbridg | 'The Moon Man' | incorrect | gold 未命中 |
| 1397 | train | The capital of Brazil was moved from Rio de Janeiro to the p | 1960 | '1960' | correct | gold 命中（含等价/别名） |
| 1398 | test | Who won the gold medal for the 100m at the 1992 Olympics at  | Linford Christie | 'Ben Johnson' | incorrect | gold 未命中 |
| 1399 | train | Cricketer W G Grace, who played first-class cricket from 186 | Lawn bowls | 'Cricket' | incorrect | 单 token 短答 'Cricket'（疑似错答，人工留意 |
| 1400 | train | Who invaded Europe from Mongolia and Turkey over 300 years,  | Tartars | 'Mongols' | incorrect | 单 token 短答 'Mongols'（疑似错答，人工留意 |
| 1401 | test | What is the name of Madonna's proposed chain of fitness club | Hard Candy Fitness | 'Mad' | incorrect | 单 token 短答 'Mad'（疑似错答，人工留意） |
| 1402 | validation | What is a group of jellyfish called? | Smack | 'A group of jellyfish is called a bloom.' | incorrect | gold 未命中 |
| 1403 | validation | Which shipping passage was closed from 1967 to 1975? | Suez Canal | 'Suez Canal' | correct | gold 命中（含等价/别名） |
| 1404 | test | "In Victorian England, what was a ""reticule""?" | Bag | 'a small bag' | correct | gold 命中（含等价/别名） |
| 1405 | validation | The Limpopo River separates Zimbabwe and Botswana from what  | South Africa | 'South Africa' | correct | gold 命中（含等价/别名） |
| 1406 | validation | "In the 19th century, the term ""penny dreadful"" applied to | Book | 'booksels' | incorrect | 单 token 短答 'booksels'（疑似错答，人工留 |
| 1407 | train | "The ""Three Laws of Motion"" are named after which scientis | Isaac Newton | 'Sir Isaac Newton' | correct | gold 命中（含等价/别名） |
| 1408 | train | Who was the first US president to succeed to the Presidency  | Andrew Johnson | 'Andrew Andrew Johnson' | correct | gold 命中（含等价/别名） |
| 1409 | train | "Which American vocalist (described by the British newspaper | Eva Cassidy | 'Billie Holiday' | incorrect | gold 未命中 |
| 1410 | test | What name is given to describes the phenomenon of the gradua | Diffusion | 'diffusion' | correct | gold 命中（含等价/别名） |
| 1411 | train | Maine Coon, Munchkin, Oriental Shorthair, Persian, Ragamuffi | Cat | 'cats' | correct | gold 别名命中 |
| 1412 | train | In which year was the first robbery for which it is known th | 1869 | '1871' | incorrect | 单 token 短答 '1871'（疑似错答，人工留意） |
| 1413 | train | "In what sport are the ""stones"" aimed at the ""house""?" | Curling | 'curling' | correct | gold 命中（含等价/别名） |
| 1414 | validation | Who married Heidi Klum in May 2005? | Seal | 'David Seal' | correct | gold 命中（含等价/别名） |
| 1415 | test | How many US states border Lake Superior? | 3 | '3' | correct | gold 命中（含等价/别名） |
| 1416 | test | Where was the world's tallest road bridge opened in December | France | 'Chinawan' | incorrect | 单 token 短答 'Chinawan'（疑似错答，人工留 |
| 1417 | test | What was the UK #1 single released by the band Stereophonics | Dakota | 'Sh' | format_failure | 单 token 函数词/碎片 'Sh'，无答案内容 |
| 1418 | train | Which member of the British royal family was born on 8/8/88? | Princess Beatrice of Yor | 'Prince Harry' | incorrect | gold 未命中 |
| 1419 | train | What is traditionally written in a ledger? | Accounts | 'financial transactions' | incorrect | gold 未命中 |
| 1420 | train | Which 20th century American composer wrote the American Fest | William Schuman | 'Aaron Aaron Copland' | incorrect | gold 未命中 |
| 1421 | test | What is the maximum number of points that can be scored from | 3 | '3' | correct | gold 命中（含等价/别名） |
| 1422 | train | "Who wrote the poem ""Daffodils""?" | William Wordsworth | 'William Words' | incorrect | gold 未命中 |
| 1423 | test | Where was the first permanent European settlement establishe | Florida | ' Jame' | incorrect | 单 token 短答 ' Jame'（疑似错答，人工留意） |
| 1424 | validation | Which famous painter's surname was Harmenzoon van Rijn which | Rembrandt | 'Rem' | incorrect | 单 token 短答 'Rem'（疑似错答，人工留意） |
| 1425 | train | From which animal does Haggis come? | Sheep | 'Sheep' | correct | gold 命中（含等价/别名） |
| 1426 | test | Which King did Guy Fawkes attempt to kill with his gunpowder | James I | 'King James I' | correct | gold 命中（含等价/别名） |
| 1427 | test | Which animal has the longest gestation period at around 22 m | The elephant | 'Elephant' | incorrect | 单 token 短答 'Elephant'（疑似错答，人工留 |
| 1428 | train | Which famous book features the character of Bob Cratchit? | A Christmas Carol | 'A Christmas Carol' | correct | gold 命中（含等价/别名） |
| 1429 | train | Which actress married Dennis Quaid on Valentine's Day in 199 | Meg Ryan | 'Jennifer Ryan' | incorrect | gold 未命中 |
| 1430 | train | How many pieces are there in a standard set of dominoes? | 28 | '28' | correct | gold 命中（含等价/别名） |
| 1431 | test | What is the acronym for the agency which provides co-operati | Interpol | 'Interpol' | correct | gold 命中（含等价/别名） |
| 1432 | validation | The Ducati is manufactured in which city and what country? | Bologna, Italy | 'Bola, Italy' | incorrect | gold 未命中 |
| 1433 | train | Who presented Family Fortunes in the two years between Bob M | Max Bygraves | 'Les Dennis' | incorrect | gold 未命中 |
| 1434 | train | Which planet has moons named after Shakespearean characters? | Uranus | 'Uranus' | correct | gold 命中（含等价/别名） |
| 1435 | train | Which movie starred Michael Caine as a murderous transvestit | Dressed To Kill | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1436 | train | Meryl Streep's character, Miranda, in the 2006 film The Devi | Vogue | 'Vanity Fair' | incorrect | gold 未命中 |
| 1437 | train | Who won the 2010 Giro D'Italia? | Ivan Basso | 'adel Martin' | incorrect | gold 未命中 |
| 1438 | train | In the Commonwealth games in Delhi, which British athlete wo | Leon Baptiste | 'Chris Thompson' | incorrect | gold 未命中 |
| 1439 | train | Who sang the theme song for the TV show 'Rawhide'? | Frankie Laine | 'Gene Williams' | incorrect | gold 未命中 |
| 1440 | validation | Which constellation contains many bright shining stars, such | Leo. | 'Leo' | correct | gold 命中（含等价/别名） |
| 1441 | train | For what novel did J. K. Rowling win the 1999 Whitbread Chil | Harry Potter and the Pri | "Harry Potter and the Philosopher's Stone" | incorrect | gold 未命中 |
| 1442 | test | Which company were responsible for the production of the Spi | Supermarine | 'Supermarine' | correct | gold 命中（含等价/别名） |
| 1443 | train | 1986 film starring Goldie Hawn as a High School football coa | Wildcats | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1444 | test | Which Italian explorer had ships named Nina, Pinta and Santa | Christopher COLUMBUS | 'Christopher Columbus' | correct | gold 命中（含等价/别名） |
| 1445 | test | Which famous resident resides at Highgrove House? | The Prince of Wales | 'Prince Charles' | correct | gold 别名命中 |
| 1446 | validation | Rarely is the question asked: Is our children learning? | George W Bush | 'Yes' | incorrect | 单 token 短答 'Yes'（疑似错答，人工留意） |
| 1447 | train | Mel Gibson (1990) and Kenneth Branagh (1996) have both playe | Hamlet | 'Shlet' | incorrect | 单 token 短答 'Shlet'（疑似错答，人工留意） |
| 1448 | validation | Which Holiday movie favourite featured a character called Ke | Home Alone | 'Home Alone' | correct | gold 命中（含等价/别名） |
| 1449 | train | What year did E.T. Hit the cinema screen? | 1982 | '1982' | correct | gold 命中（含等价/别名） |
| 1450 | test | Which singer played the Goblin King Jareth in the film Laby | David Bowie | 'David Bowie' | correct | gold 命中（含等价/别名） |
| 1451 | train | Who created the Miss World pageant? | Eric Morley. | 'Michael Smith' | incorrect | gold 未命中 |
| 1452 | train | What dish, especially popular in parts of Wales and the Engl | Faggots | 'Haggis' | incorrect | 单 token 短答 'Haggis'（疑似错答，人工留意） |
| 1453 | train | What was the name of Shari Lewis' sassy sock puppet? | Lamb Chop. | 'Sally' | incorrect | 单 token 短答 'Sally'（疑似错答，人工留意） |
| 1454 | train | What is the southernmost city in USA | Honolulu | 'Key' | incorrect | 单 token 短答 'Key'（疑似错答，人工留意） |
| 1455 | test | In Vladimir Nabokov's book "Lolita", what is Lolita's real n | Dolores HAZE | "Lolita's real name is Dol" | correct | gold 别名命中 |
| 1456 | test | What animal did Reggie Perrin think of every time his Mother | A Hippopotamus. | 'a' | format_failure | 单 token 函数词/碎片 'a'，无答案内容 |
| 1457 | validation | More commonly known as the thigh bone, what is the medical n | The Femur | 'femur' | correct | gold 别名命中 |
| 1458 | train | What is being built in the Olympic Park, that will be the wo | A slide | 'Waterway' | incorrect | 单 token 短答 'Waterway'（疑似错答，人工留 |
| 1459 | train | What was the name of the Liverpool nightclub where the Beatl | The Cavern | 'Cavern Club' | correct | gold 别名命中 |
| 1460 | test | How many US states are prefixed by the word New? | 4 | '3' | format_failure | 单 token 函数词/碎片 '3'，无答案内容 |
| 1461 | train | Which ITV magazine style show ran from 1968 to 1980 and feat | Magpie | 'This' | format_failure | 单 token 函数词/碎片 'This'，无答案内容 |
| 1462 | train | In which New York borough would you find Hell’s Kitchen? | Manhattan | 'Manhattan' | correct | gold 命中（含等价/别名） |
| 1463 | train | The melody for which famous song was written by sisters and  | Happy Birthday | 'America the Beautiful' | incorrect | gold 未命中 |
| 1464 | test | What do we call the vegetable called the rutabaga in America | Swede | 'turnede' | incorrect | 单 token 短答 'turnede'（疑似错答，人工留意 |
| 1465 | train | In which city in the UK is the National Railways Museum? | York | 'Le' | format_failure | 单 token 函数词/碎片 'Le'，无答案内容 |
| 1466 | test | Which boxer was the first to defeat Mike Tyson in a professi | "James (""Buster"") Doug | 'Mike Holmes' | incorrect | gold 未命中 |
| 1467 | train | Who has been Archbishop of York since 2005? | John Sentamu | 'John Williams' | incorrect | gold 未命中 |
| 1468 | train | In the Muslim religion what name is given to an invisible sp | DJINN | 'Jinn' | correct | gold 别名命中 |
| 1469 | test | As a figure of speech, what is a statement made in exaggerat | HYPERBOLE | 'hyperbole' | correct | gold 命中（含等价/别名） |
| 1470 | test | Which 'literary' nickname has been given to the extinct spec | Hobbits | 'Hobbit' | correct | gold 别名命中 |
| 1471 | train | Which character from a comic strip had the real name Marmadu | Lord Snooty | 'Marmaduke, Earl of Bunkerton' | format_failure | 输出为问句回显，无答案内容 |
| 1472 | validation | Who, according to legend, cut the Gordian Knot? | Alexander the Great | 'Alexander the Great' | correct | gold 命中（含等价/别名） |
| 1473 | train | In Greek mythology which king of Corinth was compelled to et | Sisyphus | 'Sisyph' | incorrect | 单 token 短答 'Sisyph'（疑似错答，人工留意） |
| 1474 | train | What is the name of Long John Silver's parrot in Treasure Is | Captain Flint | 'Ben' | incorrect | 单 token 短答 'Ben'（疑似错答，人工留意） |
| 1475 | validation | What consumer electronics product shares its name with the c | BLACKBERRY | 'iberry' | incorrect | 单 token 短答 'iberry'（疑似错答，人工留意） |
| 1476 | train | The Corryvreckan whirlpool lies to the north of which Scotti | JURA | 'Man' | incorrect | 单 token 短答 'Man'（疑似错答，人工留意） |
| 1477 | train | Which Hollywood film star advertises 'Qantas' airlines and i | JOHN TRAVOLTA | 'Tom Cruise' | incorrect | gold 未命中 |
| 1478 | test | 'The Castle of Otranto' often called the first gothic novel, | HORACE WALPOLE | 'Horpole' | incorrect | 单 token 短答 'Horpole'（疑似错答，人工留意 |
| 1479 | train | Which group became the first to reach Number One with their  | THE SPICE GIRLS | 'The Beatles' | incorrect | gold 未命中 |
| 1480 | train | The flag of which European country is a blue-white-red horiz | Serbia | 'Belgium' | incorrect | 单 token 短答 'Belgium'（疑似错答，人工留意 |
| 1481 | train | Who, in May 2006 when aged 17 years and 75 days, became the  | Theo Walcott | 'David Cole' | incorrect | gold 未命中 |
| 1482 | train | Blinky, Pinky, Inky, and Clyde are four ghosts in which arca | Pac-Man | 'P-Man' | incorrect | 单 token 短答 'P-Man'（疑似错答，人工留意） |
| 1483 | test | 2012 is the Chinese year of which creature? | DRAGON | 'Dragon' | correct | gold 命中（含等价/别名） |
| 1484 | validation | What was the code name for the British retreat from Dunkirk  | Dynamo | 'Operation Dynamo' | correct | gold 命中（含等价/别名） |
| 1485 | train | In Greek Mythology who was the princess rescued from the Sea | ANDROMEDA | 'Persephone' | incorrect | 单 token 短答 'Persephone'（疑似错答，人 |
| 1486 | train | The term 'the fourth wall' would be used for an imaginary wa | Theatre | 'theater' | correct | gold 别名命中 |
| 1487 | test | According to ancient Greek philosophers the universe was mad | Ether | 'ether' | correct | gold 命中（含等价/别名） |
| 1488 | validation | Which tree has the Lath name Taxus? | YEW | 'yew' | correct | gold 命中（含等价/别名） |
| 1489 | test | Who hit six sixes in one over at 2007 Cricket World Cup in t | (Herschelle) GIBBS | 'Chris Gayle' | incorrect | gold 未命中 |
| 1490 | train | "Who played Luke Skywalker in the 1977 original ""Star Wars" | (Mark) HAMILL | 'Mark Ford' | incorrect | gold 未命中 |
| 1491 | train | Which car company manufacturers the Corolla model? | Toyota | 'Toyota' | correct | gold 命中（含等价/别名） |
| 1492 | test | What name is given to the nine square mile area of West York | THE RHUBARB TRIANGLE | 'Theip Valley' | incorrect | gold 未命中 |
| 1493 | train | Pearl is composed of minute crystals of which compound? | Calcium Carbonate | 'calcium carbonate' | correct | gold 命中（含等价/别名） |
| 1494 | train | Who was the last British male to reach the final of a Grand  | Greg Rusedski | 'Andy Murray' | incorrect | gold 未命中 |
| 1495 | test | The folk song Johnny Todd is the signature tune for which 60 | Z Cars | 'Dr' | format_failure | 单 token 函数词/碎片 'Dr'，无答案内容 |
| 1496 | train | Britain's first jet fighter, The Meteor was made by which co | GLOSTER | 'Superster' | incorrect | 单 token 短答 'Superster'（疑似错答，人工 |
| 1497 | test | What is the name of the strong fibrous tissue that joins one | Ligament | 'ligament' | correct | gold 命中（含等价/别名） |
| 1498 | test | Who was housekeeper to Sherlock Holmes? | Mrs Hudson | 'Mary' | incorrect | 单 token 短答 'Mary'（疑似错答，人工留意） |
| 1499 | train | Which European country's flag is a blue cross on a white bac | Finland | 'Swmark' | incorrect | 单 token 短答 'Swmark'（疑似错答，人工留意） |
| 1500 | train | Who is the oldest person to have a number one hit in Britain | LOUIS ARMSTRONG | 'Paul Jones' | incorrect | gold 未命中 |
| 1501 | validation | What is the name of the whirlpool in the Hebrides between Sc | Corryvreckan | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1502 | validation | If you were to fly due east out of Rio de Janeiro, which cou | Namibia | 'Brazil' | incorrect | 单 token 短答 'Brazil'（疑似错答，人工留意） |
| 1503 | train | Which country joined the G7 government forum which then beca | Russia | 'Russia' | correct | gold 命中（含等价/别名） |
| 1504 | train | In which activity are banderillas used? | BULLFIGHTING | 'bullfighting' | correct | gold 命中（含等价/别名） |
| 1505 | test | In radio technology, what does the 'A' represent in 'DAB'? | AUDIO | "The 'A' in 'DAB' stands for Audio." | correct | gold 命中（含等价/别名） |
| 1506 | train | Made in Cornwall, Yarg cheese is wrapped in what? | NETTLES | 'al' | format_failure | 单 token 函数词/碎片 'al'，无答案内容 |
| 1507 | train | Which Norwegian firm supposedly produced the first fleece fa | Helly Hansen | 'Nlo' | incorrect | 单 token 短答 'Nlo'（疑似错答，人工留意） |
| 1508 | train | In the cartoon series, what kind of dog is Scooby Doo? | Great Dane | 'Scooby Doo is a Great Dane.' | correct | gold 命中（含等价/别名） |
| 1509 | test | What was the name of Gary Puckett's backing group? | The Union Gap | 'The D' | incorrect | gold 未命中 |
| 1510 | validation | "Which English comedian had a minor hit in 1958 with his cov | CHARLIE DRAKE | 'Peter Sellers' | incorrect | gold 未命中 |
| 1511 | train | In which Indian city is Eden Gardens, the second largest tes | KOLKATA | 'Kolkata' | correct | gold 命中（含等价/别名） |
| 1512 | test | Which opera star was born Claire Mary Teresa Rawstron in 194 | KIRI TE KANAWA | 'K Baker' | incorrect | gold 未命中 |
| 1513 | validation | The Melrose Cup is awarded in which ball sport? | RUGBY SEVENS | 'rugicket' | incorrect | 单 token 短答 'rugicket'（疑似错答，人工留 |
| 1514 | validation | "Which make of car is advertised under the slogan ""Vorsprun | Audi | 'Audi' | correct | gold 命中（含等价/别名） |
| 1515 | train | In Pride and Prejudice what was the first name of Mr Darcy? | Fitzwilliam | 'Fitzick' | incorrect | 单 token 短答 'Fitzick'（疑似错答，人工留意 |
| 1516 | validation | Name the French artist (1839-1906) whose painting 'The Card  | Paul Cézanne | 'Picasso' | incorrect | 单 token 短答 'Picasso'（疑似错答，人工留意 |
| 1517 | train | Which famous conductor conducted the very first performance  | Sir Adrian Boult | 'Edward Elgar' | incorrect | gold 未命中 |
| 1518 | test | Which man won a record 26 Academy Award 'Oscars'? | Walt Disney | 'Walt Disney' | correct | gold 命中（含等价/别名） |
| 1519 | train | Who played the part of 'Fitz' in the TV series 'Cracker'? | Robbie Coltrane | 'David Jackson' | incorrect | gold 未命中 |
| 1520 | train | The flag of the Great Socialist People's Libyan Arab Jamahir | Green | 'green' | correct | gold 命中（含等价/别名） |
| 1521 | train | Who was born at Villa Mon Repos, Corfu, in 1921? | Prince Philip | 'John' | incorrect | 单 token 短答 'John'（疑似错答，人工留意） |
| 1522 | train | In which children's TV series does Shaggy appear? | SCOOBY DOO | 'Shaggy appears in the children\'s TV series "Scooby' | correct | gold 别名命中 |
| 1523 | train | Which of England's 1966 World Cup winning footballers played | George Cohen | 'John Taylor' | incorrect | gold 未命中 |
| 1524 | validation | At what age does an individual first become entitled to a fr | 75 | '75' | correct | gold 命中（含等价/别名） |
| 1525 | train | In which sport is the Vince Lombardi awarded? | American Football | 'American' | incorrect | 单 token 短答 'American'（疑似错答，人工留 |
| 1526 | train | Which island nation lost a day in Dec. 2011 by moving the In | Samoa | 'Kiribati' | incorrect | 单 token 短答 'Kiribati'（疑似错答，人工留 |
| 1527 | train | Which Roman Emperor succeeded his father Vespasian in 79? | Titus | 'Tititian' | incorrect | 单 token 短答 'Tititian'（疑似错答，人工留 |
| 1528 | train | The bones of King Richard III have been discovered under a c | LEICESTER | 'Leicester' | correct | gold 命中（含等价/别名） |
| 1529 | test | Which Briton won the Nobel Prize for Literature in the 1980s | WILLIAM GOLDING | 'John Morrison' | incorrect | gold 未命中 |
| 1530 | train | Which Scotsman became the first European to reach the River  | Mungo Park | 'John Park' | incorrect | gold 未命中 |
| 1531 | train | On which West Indian island did the Calypso originate? | TRINIDAD | 'Trinidad' | correct | gold 命中（含等价/别名） |
| 1532 | train | Which American motor manufacturer's logo is the head of a ra | Dodge | 'Ch' | format_failure | 单 token 函数词/碎片 'Ch'，无答案内容 |
| 1533 | train | Who was the first President to be an American citizen from b | Martin Van Buren | 'John Jackson' | incorrect | gold 未命中 |
| 1534 | test | Which Pacific nation consists of over 800 islands and islets | FIJI | 'Fiji' | correct | gold 命中（含等价/别名） |
| 1535 | train | Which April fool's joke did Richard Dimbleby report on in 19 | THE SPAGHETTI TREE | 'the moon moon' | incorrect | gold 未命中 |
| 1536 | train | Which English county is Bletchley Park, the WW II code-break | BUCKINGHAMSHIRE | 'Berkshire' | incorrect | 单 token 短答 'Berkshire'（疑似错答，人工 |
| 1537 | train | According to the late Dr Robert Atkins, what kind of nutrien | Carbohydrates | 'carbs' | correct | gold 别名命中 |
| 1538 | train | "What does the Latin phrase ""primus inter pares "" mean?" | First Amongst Equals | 'first among equals' | correct | gold 别名命中 |
| 1539 | train | Sir William Herschel discovered which planet, calling it 'Ge | Uranus | 'Uranus' | correct | gold 命中（含等价/别名） |
| 1540 | train | What is added to white wine to make a Kir? | Cassis | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 1541 | train | In Imperial measurement, how many pounds are there in a hund | 112 | '112 pounds' | correct | gold 命中（含等价/别名） |
| 1542 | train | The most southerly part of mainland Australia is in which st | VICTORIA | 'T Australia' | incorrect | gold 未命中 |
| 1543 | train | Which female country and Western singer died in a plane cras | PATSY CLINE | 'June Cash' | incorrect | gold 未命中 |
| 1544 | validation | In the 1920s by what name did Angelo Siciliano become better | CHARLES ATLAS | 'Joe' | incorrect | 单 token 短答 'Joe'（疑似错答，人工留意） |
| 1545 | test | Which 1980s TV sitcom starred Keith Barron and Gwen Taylor a | Duty Free | 'Sun Holiday' | incorrect | gold 未命中 |
| 1546 | test | The painting A Dance to the Music of Time 1634 - 1635 displa | Nicholas Poussin | 'Rubmeer' | incorrect | 单 token 短答 'Rubmeer'（疑似错答，人工留意 |
| 1547 | train | Which adjective is used when pertaining to the fox? | VULPINE | 's' | format_failure | 单 token 函数词/碎片 's'，无答案内容 |
| 1548 | validation | Euclid of Alexandria established the foundations of which br | Geometry | 'Geometry' | correct | gold 命中（含等价/别名） |
| 1549 | train | Alfred Munnings was famous for his paintings of what? | HORSES | 'horses' | correct | gold 命中（含等价/别名） |
| 1550 | train | Who is the most famous cartoon creation of Al Capp? | Li'l Abner | 'L Brown' | incorrect | gold 未命中 |
| 1551 | train | Juba is the capital of which country? | South Sudan | 'South Sudan' | correct | gold 命中（含等价/别名） |
| 1552 | validation | What is the French name for the English channel? | La Manche | 'Manche' | incorrect | 单 token 短答 'Manche'（疑似错答，人工留意） |
| 1553 | validation | Which European country has Switzerland to the west Austria t | Lichtenstein | 'Italyitzerland' | incorrect | 单 token 短答 'Italyitzerland'（疑似 |
| 1554 | train | Who composed the 'War Requiem'? | Benjamin Britten | 'Benjamin Britten' | correct | gold 命中（含等价/别名） |
| 1555 | train | Who founded the Body Shop, in the UK, in 1976? | Anita Roddick | ' Anita Watson' | incorrect | gold 未命中 |
| 1556 | test | Which literary location did John Jarndyce own? | Bleak House | 'New House' | incorrect | gold 未命中 |
| 1557 | train | Under what pseudonym did JK Rowling publish the book 'The Cu | Robert Galbraith | 'Robert Galbraith' | correct | gold 命中（含等价/别名） |
| 1558 | train | Who won the first ever boxing gold for women? She shares her | Nicola Adams | 'Hillary Robinson' | incorrect | gold 未命中 |
| 1559 | train | What was the Christian name of the wife of composer Robert S | CLARA | 'Clara' | correct | gold 命中（含等价/别名） |
| 1560 | test | Which comic strip character was created in the early fifties | DAN DARE | 'Sandy' | incorrect | 单 token 短答 'Sandy'（疑似错答，人工留意） |
| 1561 | validation | In which TV 'quiz' show was the consolation prize a dustbin? | 3-2-1 | 'Topmind' | incorrect | 单 token 短答 'Topmind'（疑似错答，人工留意 |
| 1562 | train | The books 'The Edge of Reason' and 'Mad About The Boy' are s | Bridget Jones' Diary | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1563 | train | St John's is the capital of which Canadian Province? | NEWFOUNDLAND | 'Newfoundland and Labrador' | correct | gold 命中（含等价/别名） |
| 1564 | train | 'We Will Stand Together' is a song to music from which class | Nimrod | 'A' | format_failure | 单 token 函数词/碎片 'A'，无答案内容 |
| 1565 | train | 'Eureka', the National Children's Museum is in which town? | Halifax | 'Indianapolis' | incorrect | 单 token 短答 'Indianapolis'（疑似错答 |
| 1566 | train | The first session of the United Nations General Assembly was | London | 'New York City' | incorrect | gold 未命中 |
| 1567 | test | Broxtowe District Council is in which English county? | Nottinghamshire | 'Nottinghamshire' | correct | gold 命中（含等价/别名） |
| 1568 | train | Where does Rupert Bear live? | NUTWOOD | 'Rupert Bear lives in the forest.' | incorrect | gold 未命中 |
| 1569 | test | Which Shakespeare comedy is set in Messina, Italy? | MUCH ADO ABOUT NOTHING | 'The Comedy of Errors' | incorrect | gold 未命中 |
| 1570 | train | Which organisation was founded in Ontario, Canada in 1897 by | WOMEN'S INSTITUTE | 'Red Cross' | incorrect | gold 未命中 |
| 1571 | test | Forbes Magazine named which author as the top earner between | E L JAMES | 'Stephen King' | incorrect | gold 未命中 |
| 1572 | validation | Which is the largest island in Canada? | Baffin Island | 'Vville Island' | incorrect | gold 未命中 |
| 1573 | train | Which company produced the Hastings and Herald aircraft? | Handley-Page | 'BritishAC' | incorrect | 单 token 短答 'BritishAC'（疑似错答，人工 |
| 1574 | test | The Carnegie family fortune was built around Andrew Carnegie | Steel | 'steel' | correct | gold 命中（含等价/别名） |
| 1575 | test | In 1986 the prime minister of which European country was ass | Sweden | 'I' | format_failure | 单 token 函数词/碎片 'I'，无答案内容 |
| 1576 | test | Which member of the cabinet is MP for Maidenhead? | THERESA MAY | 'David Johnson' | incorrect | gold 未命中 |
| 1577 | train | Who wrote the opera A Masked Ball? | Giuseppe Verdi | 'Richard Strauss' | incorrect | gold 未命中 |
| 1578 | train | Who, c1819, wrote the poem Ode to the West Wind? | PERCY BYSSHE SHELLY | 'By Shelley' | incorrect | gold 未命中 |
| 1579 | train | Which island is named after the world's largest bear? | Kodiak | 'Grizzly Island' | incorrect | gold 未命中 |
| 1580 | train | Mount Elbrus, arguably Europe's highest peak, is in which mo | Caucasus | 'Caucus Mountains' | incorrect | gold 未命中 |
| 1581 | train | Which popular dessert was invented at the Hungry Monk in Alf | SUSSEX POND | 'iceifle' | incorrect | 单 token 短答 'iceifle'（疑似错答，人工留意 |
| 1582 | test | The disease pertussis is more commonly known by what name? | Whooping Cough | 'whooping cough' | correct | gold 命中（含等价/别名） |
| 1583 | test | In anatomy, what is a ganglion? | Nerve Cell Cluster | 'cluster of neurons' | incorrect | gold 未命中 |
| 1584 | train | Which indoor sport includes a side wall, front wall, and a t | Squash | 'Rquetball' | incorrect | 单 token 短答 'Rquetball'（疑似错答，人工 |
| 1585 | train | HRH Princess Anne?s Gloucestershire country home is called w | Gatcombe Park | 'Highfield' | incorrect | 单 token 短答 'Highfield'（疑似错答，人工 |
| 1586 | train | What is the derived SI unit of pressure? | Pascal | 'pascal' | correct | gold 命中（含等价/别名） |
| 1587 | test | Who captained the England rugby union team 59 times between  | Will Carling | 'Martin Johnson' | incorrect | gold 未命中 |
| 1588 | test | Which standard orchestral instrument has a name which derive | Oboe | 'Oboe' | correct | gold 命中（含等价/别名） |
| 1589 | train | Which Mexican dish is a steamed corn husk filled with meat o | Tamale | 'Tamales' | correct | gold 别名命中 |
| 1590 | test | Which mountain range stretches for 1500 miles and has Mount  | Appalachians | 'App Appalachian Mountains' | correct | gold 别名命中 |
| 1591 | test | In which 1816 novel do we meet the characters Anne Elliot an | Persuasion | 'Persuasion' | correct | gold 命中（含等价/别名） |
| 1592 | train | Which chemical element is named after a university in Oaklan | Berkelium | 'berifornium' | incorrect | 单 token 短答 'berifornium'（疑似错答， |
| 1593 | train | Under what name did Dr Brooke Magnanti write her blog about  | Belle du Jour | 'Dr' | format_failure | 单 token 函数词/碎片 'Dr'，无答案内容 |
| 1594 | train | Who won the .1995 Best Actress Oscar for her role as Sister  | SUSAN SARANDON | 'Sandra Bullock' | incorrect | gold 未命中 |
| 1595 | train | Jose Mourinho was appointed manager of which football club S | BENFICA | 'Porto' | incorrect | 单 token 短答 'Porto'（疑似错答，人工留意） |
| 1596 | train | "Who according to the Book of Genesis was described as ""A m | NIMROD | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 1597 | train | What does the Greek word Mesopotamia mean? | Between two rivers | 'land between the rivers' | incorrect | gold 未命中 |
| 1598 | test | in which century was St Bartholomew's Hospital located in We | 12th century | '16th century' | incorrect | gold 未命中 |
| 1599 | train | Who was King of England in the year 1300? | Edward I | 'Edward I' | correct | gold 命中（含等价/别名） |
| 1600 | train | Which musical instrument is Albert Schweitzer known to have  | Organ | 'Piano' | incorrect | 单 token 短答 'Piano'（疑似错答，人工留意） |
| 1601 | test | In the acronym DEFRA, for what does the A stand? | Affairs | 'A' | format_failure | 单 token 函数词/碎片 'A'，无答案内容 |
| 1602 | test | In an electrical circuit what is measured by a Wheatstone Br | Resistance | 'res resistance' | correct | gold 命中（含等价/别名） |
| 1603 | train | In which country are the wine producing regions Huasco Valle | Chile | 'Chile' | correct | gold 命中（含等价/别名） |
| 1604 | train | According to the rhyme, what is Wednesday’s child? | Full of woe | "Wednesday's child is full of grace" | incorrect | gold 未命中 |
| 1605 | test | What sport do you associate with Francesco Molinari? | Golf | 'Golf' | correct | gold 命中（含等价/别名） |
| 1606 | train | jhe BBC2 production of Wolf Hal! was based on the novels by  | Bring Up the Bodies | 'The Hall' | incorrect | gold 未命中 |
| 1607 | train | Who wrote the opera Faust in 1859? | Charles Gounod | 'G Wagner' | incorrect | gold 未命中 |
| 1608 | test | Who penned his own epitaph ‘Here lies one whose name was wri | John Keats | 'William Shakespeare' | incorrect | gold 未命中 |
| 1609 | test | Which flower is also known as the Lent Lily? | Daffodil | 'E Lent Lily' | incorrect | gold 未命中 |
| 1610 | validation | What is the name of me political party, led by Alexis Tsipra | SYRIZA | 'S' | format_failure | 单 token 函数词/碎片 'S'，无答案内容 |
| 1611 | train | Who was known as 'The Great One' in North American ice hocke | WAYNE GRETZKY | 'Wayne Gretzky' | correct | gold 命中（含等价/别名） |
| 1612 | test | Oswald Cobblepot is a devious crime-boss who is seldom seen  | PENGUIN | 'The Penguin' | correct | gold 命中（含等价/别名） |
| 1613 | train | Raphanus Sativus is the Latin name of what vegetable, which  | Radish | 'radish' | correct | gold 命中（含等价/别名） |
| 1614 | train | What nationality is former Liverpool FC footballer Jan Molby | Danish | 'Danish' | correct | gold 命中（含等价/别名） |
| 1615 | train | Who wrote the 20th century verse play Murder in the Cathedra | T S ELIOT | 'Thomas Thomas' | incorrect | gold 未命中 |
| 1616 | train | When hallmarking articles made of platinum, what pictorial m | AN ORB | 'A crown' | incorrect | gold 未命中 |
| 1617 | train | As SNCF is the French railway system, what are the initials  | DB | 'DB' | correct | gold 命中（含等价/别名） |
| 1618 | validation | Which British 2012 Olympic Gold medallist won two events at  | MO FARAH | 'Mo Williams' | incorrect | gold 未命中 |
| 1619 | test | What was the name of the flying island in Gulliver’s Travels | LAPUTA | 'Lilliput' | incorrect | 单 token 短答 'Lilliput'（疑似错答，人工留 |
| 1620 | test | Which US city began as a trading post on the Chisholm Trail  | WICHITA | 'Kansas' | incorrect | 单 token 短答 'Kansas'（疑似错答，人工留意） |
| 1621 | validation | In which war did the battles of Crecy and Poitiers take plac | HUNDRED YEARS WAR | " Hundred Years' War" | correct | gold 命中（含等价/别名） |
| 1622 | test | Koh-I-Noor, as in the diamond, means what in English? | MOUNTAIN of LIGHT | 'mount Mountain of Light' | correct | gold 命中（含等价/别名） |
| 1623 | validation | Of what does the usual base of a Florentine biscuit consist? | CHOCOLATE | 'al' | format_failure | 单 token 函数词/碎片 'al'，无答案内容 |
| 1624 | train | Actor John Hewer died early in 2008 aged 86; under what name | Captain Birdseye | 'Mrman' | incorrect | 单 token 短答 'Mrman'（疑似错答，人工留意） |
| 1625 | train | “Tis Herself’ published in 2005 was the autobiography of whi | MAUREEN O’HARA | 'Jennifer Ryan' | incorrect | gold 未命中 |
| 1626 | train | Which King of England is buried in Gloucester Cathedral? | EDWARD II | 'Henry III' | incorrect | gold 未命中 |
| 1627 | train | The storyline of which 1994 Disney animated film is based on | THE LION KING | 'The Lion King' | correct | gold 命中（含等价/别名） |
| 1628 | validation | In which country is the Sierra Madre mountain range, with it | Mexico | 'Mexico' | correct | gold 命中（含等价/别名） |
| 1629 | validation | Canaletto is famous for his landscapes of Venice and which o | London | 'Rome' | incorrect | 单 token 短答 'Rome'（疑似错答，人工留意） |
| 1630 | validation | In which European city is Kurtfurstendamm the main shopping  | BERLIN | 'Kurtfurstendamm is the main shopping street in Ber' | correct | gold 命中（含等价/别名） |
| 1631 | train | Harvard University is situated in which American State? | MASSACHUSETTS | 'Mass' | correct | gold 别名命中 |
| 1632 | train | Which popular garden flower is the national flower of Mexico | THE DAHLIA | 'Caisy' | incorrect | 单 token 短答 'Caisy'（疑似错答，人工留意） |
| 1633 | train | Which illness caused Edward VII's coronation to be delayed b | APPENDICITIS | 'm fever' | incorrect | gold 未命中 |
| 1634 | validation | Which piece of laboratory equipment consists of a vertical c | A BURETTE. | 'Aipette' | incorrect | 单 token 短答 'Aipette'（疑似错答，人工留意 |
| 1635 | validation | "Who produces the perfumes ""Opium"" and ""Rive Gauche""?" | Yves Saint Laurent | 'Chanel' | incorrect | 单 token 短答 'Chanel'（疑似错答，人工留意） |
| 1636 | test | Botswana was known by what name until 1966? | Bechuanaland | 'Bechuanaland' | correct | gold 命中（含等价/别名） |
| 1637 | train | What do the Americans call what we call a 'sofa'? | DAVENPORT | 'couch' | incorrect | 单 token 短答 'couch'（疑似错答，人工留意） |
| 1638 | train | In which English city is the HQ of the Ordnance Survey? | Southampton | 'Ed' | format_failure | 单 token 函数词/碎片 'Ed'，无答案内容 |
| 1639 | train | Which singer had a number 1 hit album in 2008 entitled 'Hard | Madonna | 'Lady Swift' | incorrect | gold 未命中 |
| 1640 | test | Which Irish politician was known as 'The Liberator'? | Daniel O'Connell | "Daniel O'Connell" | correct | gold 命中（含等价/别名） |
| 1641 | validation | Which device, now a plaything, has a lift end, a dingle end  | Boomerang | 'a clothes' | incorrect | gold 未命中 |
| 1642 | validation | Which is the only property on a traditional UK Monopoly boar | OLD KENT ROAD | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1643 | validation | In the context of UK government, for what does the C stand i | Cabinet | 'Commitabinet' | incorrect | 单 token 短答 'Commitabinet'（疑似错答 |
| 1644 | train | Which island in the Grenadines of St. Vincent was bought by  | MUSTIQUE | 'Gique' | incorrect | 单 token 短答 'Gique'（疑似错答，人工留意） |
| 1645 | test | The Aran Islands are located at the mouth of which bay? | Galway Bay | 'Bish Bay' | incorrect | gold 未命中 |
| 1646 | test | The former Queen Mother, Elizabeth Bowes-Lyon, married the D | Durham | 'North' | incorrect | 单 token 短答 'North'（疑似错答，人工留意） |
| 1647 | train | Who wrote much of King George V's first Christmas broadcast, | Rudyard Kipling | 'George Churchill' | incorrect | gold 未命中 |
| 1648 | train | In terms of tonnage of cargo handled, which is the world's l | Rotterdam | 'Sh Kong' | incorrect | gold 未命中 |
| 1649 | train | By what name was Peggy Hookham DBE better known? | Margot Fonteyn | 'Peggy Hookham DBE was better known as Peggy Lee.' | correct | gold 别名命中 |
| 1650 | train | General James Wolfe was killed at which battle in 1759? | Quebec | 'Battle of Quebec' | correct | gold 命中（含等价/别名） |
| 1651 | train | What is the perfect score in ten pin bowling? | 300 | '300' | correct | gold 命中（含等价/别名） |
| 1652 | train | Which Alpine peak is known in Italy as Monte Cervino? | The Matterhorn | 'Monte Rosa' | incorrect | gold 未命中 |
| 1653 | test | What is the largest state in Brazil? | AMAZONAS | 'Amazoná' | incorrect | 单 token 短答 'Amazoná'（疑似错答，人工留意 |
| 1654 | test | Which official residence is No.12 Downing Street? | GOVERNMENT CHIEF WHIP | 'The Prime Minister' | incorrect | gold 未命中 |
| 1655 | train | In the Lake District which is the only body of water to actu | Bassenthwaite Lake | 'Windermere' | incorrect | 单 token 短答 'Windermere'（疑似错答，人 |
| 1656 | train | What is the imperial distance of a marathon race? | 26 miles, 385 yards | '26.2 miles' | incorrect | gold 未命中 |
| 1657 | validation | What kind of aircraft gave the space shuttle a piggy-back pr | BOEING 747 | 'B-52' | incorrect | 单 token 短答 'B-52'（疑似错答，人工留意） |
| 1658 | test | As at November 2007, who is the Shadow Home Secretary? | David Davis | 'David Johnson' | incorrect | gold 未命中 |
| 1659 | test | Aglaia, Thalia and. Euphrosyne were known as what? | THREE GRACES | 'Musesai' | incorrect | 单 token 短答 'Musesai'（疑似错答，人工留意 |
| 1660 | train | What is the name for a female bear? | A sow | 'S' | format_failure | 单 token 函数词/碎片 'S'，无答案内容 |
| 1661 | train | On which island in the North Sea did both St Aidan and St Cu | LINDISFARNE | 'T Island' | incorrect | gold 未命中 |
| 1662 | test | Who played the part of companion Martha Jones in the 2007 se | FREEMA AGYEMAN | 'Karen Gillan' | incorrect | gold 未命中 |
| 1663 | train | Which large American bird (Gymnogyps) has been reintroduced  | (California) Condor | 'California condor' | correct | gold 命中（含等价/别名） |
| 1664 | train | Whose portrait (apart from the Queen) appeared on the now de | ISAAC NEWTON | 'George Newton' | incorrect | gold 未命中 |
| 1665 | train | By what name is the garden flowering plant hypericum commonl | ST JOHN'S WORT | 'Goldenells' | incorrect | 单 token 短答 'Goldenells'（疑似错答，人 |
| 1666 | train | Which well known 1987 film, featured a character named Priva | FULL METAL JACKET | 'Full Metal Jacket' | correct | gold 命中（含等价/别名） |
| 1667 | train | The 2010 Winter Olympics will be held where? | Vancouver | 'Vancouver,' | correct | gold 命中（含等价/别名） |
| 1668 | train | The name of which Chinese dish translates as 'bits and piece | Chop Suey | 'Chow mein' | incorrect | gold 未命中 |
| 1669 | train | In GB Shaw's Major Barbara in which army was Barbara a major | SALVATION ARMY | 'British Army' | incorrect | gold 未命中 |
| 1670 | train | "The novel, ""Birdsong"", by Sebastian Faulks, is mainly set | WORLD WAR I | 'World War I' | correct | gold 命中（含等价/别名） |
| 1671 | test | "What was the sequel to 'Tom Brown's Schooldays""?" | Tom Brown at Oxford | "Tom Brown's College" | incorrect | gold 未命中 |
| 1672 | validation | Which British Prime Ministers death is commemorated on 19th  | Benjamin Disraeli | 'William Gladstone' | incorrect | gold 未命中 |
| 1673 | test | "Which English comedian/actor said ""Girls are like pianos.  | Benny Hill | 'Peter Sellers' | incorrect | gold 未命中 |
| 1674 | train | Who in 1476 brought his painting press from Bruges to London | WILLIAM CAXTON | 'John Gutenberg' | incorrect | gold 未命中 |
| 1675 | test | Which American city has districts called Financial, Mission, | San Francisco | 'San Francisco' | correct | gold 命中（含等价/别名） |
| 1676 | train | Which river flows from northern Moscow to the Caspian Sea? | Volga | 'Oga River' | incorrect | gold 未命中 |
| 1677 | train | Which actor was the fifth Doctor Who from 1982-1984, and in  | PETER DAVISON | 'Tom Baker' | incorrect | gold 未命中 |
| 1678 | test | Which post in England and Wales is held by Anne Owers? | (CHIEF) INSPECTOR OF PRI | 'Attitor General' | incorrect | gold 未命中 |
| 1679 | train | In what year was the Battle of Stamford Bridge? | 1066 | '1066' | correct | gold 命中（含等价/别名） |
| 1680 | train | Born in 1947, James Jewel Osterberg is a rock/punk pop singe | Iggy Pop | 'David Reed' | incorrect | gold 未命中 |
| 1681 | validation | How many faces has an icosahedron? | 20 | '20' | correct | gold 命中（含等价/别名） |
| 1682 | train | Which boxer was portrayed b Robert De Niro in the film 'Ragi | Jake La Motta | 'Robert De Niro portrayed Jake LaMotta in the film ' | correct | gold 别名命中 |
| 1683 | train | Which 20th Century U.S. President was a Peanut Farmer? | JIMMY CARTER | 'Jimmy Carter' | correct | gold 命中（含等价/别名） |
| 1684 | train | In Greek mythology what was the name of the goatlike man wit | A SATYR | ' Satyrrs' | incorrect | 单 token 短答 ' Satyrrs'（疑似错答，人工留 |
| 1685 | train | The axilla is the anatomical name for which part of the body | Armpit | 'underarm' | correct | gold 别名命中 |
| 1686 | train | Give any year in the life of the painter Raphael. | 1483-1520 | '1510' | incorrect | 单 token 短答 '1510'（疑似错答，人工留意） |
| 1687 | test | In 2002, Chechen terrorists took more than 700 people as hos | Theatre | 'theater' | correct | gold 别名命中 |
| 1688 | train | What is the surname of the father and son who rode Grand Nat | Carberry | 'H' | format_failure | 单 token 函数词/碎片 'H'，无答案内容 |
| 1689 | train | At which school was Billy Bunter a pupil | GREYFRIARS | 'The High School' | incorrect | gold 未命中 |
| 1690 | train | The two wives of King John of England shared which forename? | Isabella | 'E' | format_failure | 单 token 函数词/碎片 'E'，无答案内容 |
| 1691 | train | "Give the name of the character played by James Stewart in t | George Bailey | 'George Bailey' | correct | gold 命中（含等价/别名） |
| 1692 | train | In January 2010, who became the first mother to win the Aust | Kim Clijsters | 'Serena Williams' | incorrect | gold 未命中 |
| 1693 | validation | "Who created the fictional character ""Tilly Trotter'?" | Catherine Cookson | 'John King' | incorrect | gold 未命中 |
| 1694 | train | Which UK international airport has the code PIK? | Prestwick | 'Peterwick Airport' | incorrect | gold 未命中 |
| 1695 | test | Who judged Aphrodite more beautiful than Hera or Athena? | Paris | 'Eris' | incorrect | 单 token 短答 'Eris'（疑似错答，人工留意） |
| 1696 | test | What was the name of the second wife of Johnny Cash, who he  | June Carter | 'Carie Cash' | incorrect | gold 未命中 |
| 1697 | train | KHI is the international code for which Asian airport? | Karachi | 'Khi' | incorrect | 单 token 短答 'Khi'（疑似错答，人工留意） |
| 1698 | train | In 1842, what was ceded to Britain by the Treaty of Nanking? | HONG KONG | 'Hong Kong' | correct | gold 命中（含等价/别名） |
| 1699 | test | Hawley Harvey were the first names of which criminal? | Dr. Crippen | 'Bon James' | incorrect | gold 未命中 |
| 1700 | train | If the Staten Island Ferry is to New York, the Star Ferry th | Hong Kong | 'Hong Kong' | correct | gold 命中（含等价/别名） |
| 1701 | train | Which city in Egypt has been characterised as the 'world's g | Luxor | 'Theor' | incorrect | 单 token 短答 'Theor'（疑似错答，人工留意） |
| 1702 | train | The Battle of Kadesh in 1274 BC that took place between the  | Chariots | 'chariots' | correct | gold 命中（含等价/别名） |
| 1703 | train | A fictional species of great apes called 'Mangani' are respo | Tarzan | 'Tarzan' | correct | gold 命中（含等价/别名） |
| 1704 | train | The Miller-Urey experiment conducted in 1953 that simulated  | Chemical origins of life | 'the origins of life' | incorrect | gold 未命中 |
| 1705 | train | "The name of what tennis star was used by a commentator for  | Anna Kournikova | 'Roger Federer' | incorrect | gold 未命中 |
| 1706 | train | What American city has suffered two (separate) outcomes of w | Cleveland | 'C' | format_failure | 单 token 函数词/碎片 'C'，无答案内容 |
| 1707 | validation | What type of 'helpful' businesses operate on the basis of th | Co-operatives | 'Cooperativeatives' | incorrect | 单 token 短答 'Cooperativeatives' |
| 1708 | train | A tourist attraction near Alliance, Nebraska created by Jim  | Stonehenge | 'Mount Rushmore' | incorrect | gold 未命中 |
| 1709 | train | What 2009 hit that rewarded a woman director opens with the  | The Hurt Locker | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1710 | validation | Mammy Two Shoes, a recurring character in MGM's Tom and Jerr | Hattie McDaniel | 'Bessie Smith' | incorrect | gold 未命中 |
| 1711 | train | What is the second-largest day for U.S. food consumption, af | Super Bowl Sunday | 'Christmas Day' | incorrect | gold 未命中 |
| 1712 | train | Which crop that was of great nutritional importance in pre-C | Quinoa | 'Quinoa' | correct | gold 命中（含等价/别名） |
| 1713 | train | Used to describe US citizens who attempted to foment insurre | Filibuster | 'merer' | incorrect | 单 token 短答 'merer'（疑似错答，人工留意） |
| 1714 | train | In 1914 a paleontologist suggested that what legend might ha | Cyclops | 'Cyclops' | correct | gold 命中（含等价/别名） |
| 1715 | validation | After USA, what is the largest country in the world named af | Saudi Arabia | 'Canada' | incorrect | 单 token 短答 'Canada'（疑似错答，人工留意） |
| 1716 | train | Beloved in 1999 was whose first movie since The Color Purple | Oprah Winfrey | 'Steve Lee' | incorrect | gold 未命中 |
| 1717 | train | Which sitcom star appeared on the big screening The Object o | Jennifer Aniston | 'John Crystal' | incorrect | gold 未命中 |
| 1718 | train | Nigel Hawthorne was Oscar nominated for The Madness of which | George | 'George II' | correct | gold 命中（含等价/别名） |
| 1719 | train | Which Oscar-nominated film had You Sexy Thing as its theme s | The Full Monty | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1720 | train | Who was the male star of the movie The Man of La Mancha? | Peter O'Toole | 'Tony Martin' | incorrect | gold 未命中 |
| 1721 | test | Which sports event was first held at Worcester, Massachusett | Ryder Cup | 'The Open' | incorrect | gold 未命中 |
| 1722 | train | In which European city is the Belvederen Gallery? | Vienna | 'Vienna' | correct | gold 命中（含等价/别名） |
| 1723 | train | Who's home runs record did Mark McGwire break in the 1998 se | Roger Maris | 'Roger Maris' | correct | gold 命中（含等价/别名） |
| 1724 | train | Which future Hollywood star got her break as Wonder Girl, Wo | Debra Winger | 'Gal Gadot' | incorrect | gold 未命中 |
| 1725 | train | In Hanna and Barbera's TV cartoons base on The Addams Family | John Astin | 'Don Melville' | incorrect | gold 未命中 |
| 1726 | train | Which grand slam did Pete Sampras not win in the 20th centur | French | 'The French Open' | correct | gold 命中（含等价/别名） |
| 1727 | train | Which European town gave its name to a Treaty which symboliz | Maastricht | 'Luxussels' | incorrect | 单 token 短答 'Luxussels'（疑似错答，人工 |
| 1728 | train | Which home of champagne in France was also where the German  | Reims | 'Reims' | correct | gold 命中（含等价/别名） |
| 1729 | train | What color golf balls are used on the golf course in Antarct | Orange | 'White' | incorrect | 单 token 短答 'White'（疑似错答，人工留意） |
| 1730 | train | "Who said, To err is human but it feels divine?""" | Mae West | 'William Pope' | incorrect | gold 未命中 |
| 1731 | train | In WWII, who was the head of the Nazi party's security servi | Reinhard Heidrich | 'H Himmler' | incorrect | gold 未命中 |
| 1732 | train | In what year was the first in-flight movie shown on an inter | 1929 | '1982' | incorrect | 单 token 短答 '1982'（疑似错答，人工留意） |
| 1733 | train | In which city was John Lennon murdered? | New York | 'New York City' | correct | gold 命中（含等价/别名） |
| 1734 | train | How was President Kennedy assassinated? | Shot | 'shotooting' | incorrect | 单 token 短答 'shotooting'（疑似错答，人 |
| 1735 | train | Of which African country is Niamey the capital? | Niger | 'Niger' | correct | gold 命中（含等价/别名） |
| 1736 | train | Which Syrian city is said to be the oldest continually inhab | Damascus | 'Aleppo' | incorrect | 单 token 短答 'Aleppo'（疑似错答，人工留意） |
| 1737 | train | Which wife of Henry VIII had already married twice before sh | Catherine Parr | 'Catherine Howard' | incorrect | gold 未命中 |
| 1738 | test | Which builder of steam engines formed a successful partnersh | James Watt | 'James Watt' | correct | gold 命中（含等价/别名） |
| 1739 | validation | What is the name of the strong material found in plant cell  | Cellulose | 'cellulose' | correct | gold 命中（含等价/别名） |
| 1740 | train | What is the most abundant substance in the plant kingdom, wh | Cellulose | 'cellulose' | correct | gold 命中（含等价/别名） |
| 1741 | train | What has a central vein called a midrib? | Leaf | 'leaf' | correct | gold 命中（含等价/别名） |
| 1742 | train | Which 90s sci fi series with James Belushi was based on Bruc | Wild Palms | 'Spaceiders' | incorrect | 单 token 短答 'Spaceiders'（疑似错答，人 |
| 1743 | train | What is the Milky Way? | The local galaxy | 'The Milky Way is a galaxy.' | correct | gold 别名命中 |
| 1744 | test | If I Were A Rich Man Was a big hit from which stage show? | Fiddler on the Roof | 'Fiddler on the Roof' | correct | gold 命中（含等价/别名） |
| 1745 | train | Kagoshima international airport is in which country? | Japan | 'Japan' | correct | gold 命中（含等价/别名） |
| 1746 | train | Kim Carnes' nine weeks at No 1 with Bette Davis Eyes was int | Stars on 45 medley | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1747 | train | Which musician founded the Red Hot Peppers? | Jelly Roll Morton | ' Flea' | incorrect | 单 token 短答 ' Flea'（疑似错答，人工留意） |
| 1748 | train | Who was the first US-born winner of golf's British Open? | Walter Hagen | 'Ben Jones' | incorrect | gold 未命中 |
| 1749 | train | Who was the youngest brother in the Beach Boys? | Carl Wilson | 'Die Wilson' | incorrect | gold 未命中 |
| 1750 | train | Who first hosted Family Feud? | Richard Dawson | 'Richard Dawson' | correct | gold 命中（含等价/别名） |
| 1751 | train | What did the Lone Ranger's title Kemo Sabe mean in Apache? | White Shirt | 'friend brother' | incorrect | gold 未命中 |
| 1752 | test | The Nazi regime was Germany's Third Reich; which was the fir | HOLY ROMAN EMPIRE | 'Holy Empire' | correct | gold 别名命中 |
| 1753 | train | Which county won the County Cricket Championship in 1959, af | YORKSHIRE | 'Yorksex' | incorrect | 单 token 短答 'Yorksex'（疑似错答，人工留意 |
| 1754 | test | The magic lantern was an early form of what item of photogra | SLIDE PROJECTOR | 'l slide projector' | correct | gold 命中（含等价/别名） |
| 1755 | train | What was the name of the USAAF B-17 Flying Fortress whose ai | MEMPHIS BELLE | 'B' | format_failure | 单 token 函数词/碎片 'B'，无答案内容 |
| 1756 | test | Although not the state capital, which is the largest city in | OMAHA | 'Omaha' | correct | gold 命中（含等价/别名） |
| 1757 | train | In which Lake District town would you find the Cumberland Pe | KESWICK | 'Workal' | incorrect | 单 token 短答 'Workal'（疑似错答，人工留意） |
| 1758 | train | Created in 1952, which is Britain's only coastal National Pa | PEMBROKESHIRE COAST NATI | 'North District National Park' | incorrect | gold 未命中 |
| 1759 | train | Who directed the Noughties films One Day in September, The L | KEVIN MACDONALD | 'Danny Boyle' | incorrect | gold 未命中 |
| 1760 | train | """Because I'm worth it"" was the advertising slogan for whi | L'OREAL | 'GE' | format_failure | 单 token 函数词/碎片 'GE'，无答案内容 |
| 1761 | test | Traditionally served in a tall glass, what name is given to  | KNICKERBOCKER GLORY | 'frifle' | incorrect | 单 token 短答 'frifle'（疑似错答，人工留意） |
| 1762 | train | "What was the name of the Jester in Shakespeare's ""As You L | TOUCHSTONE | 'The Jester in Shakespeare\'s "As You Like It" is To' | correct | gold 命中（含等价/别名） |
| 1763 | train | "Which famous western movie ends with the line :- ""Oh good, | BUTCH CASSIDY AND THE SU | 'High Noon' | incorrect | gold 未命中 |
| 1764 | validation | Near which village in North Wales were the rowing events hel | LLANBERIS | 'Bor' | incorrect | 单 token 短答 'Bor'（疑似错答，人工留意） |
| 1765 | train | "In Italy, if you were served ""Mortadella"", what foodstuff | SAUSAGE | 'Mortadella' | incorrect | 单 token 短答 'Mortadella'（疑似错答，人 |
| 1766 | train | A Lemur is a small primate found only on which island? | MADAGASCAR | 'Madagascar' | correct | gold 命中（含等价/别名） |
| 1767 | train | Formula 1 - On which racetrack was the World Champion Ayrton | IMOLA | 'Spola' | incorrect | 单 token 短答 'Spola'（疑似错答，人工留意） |
| 1768 | test | Which famous sporting figure was the subject of attention by | STEVEN GERARD | 'Michael Woods' | incorrect | gold 未命中 |
| 1769 | validation | Which British band reached number one in the UK pop charts i | POLICE | 'The Police' | correct | gold 命中（含等价/别名） |
| 1770 | test | Ridden by jockey Brian Fletcher, which horse won the 1968 Gr | RED ALLIGATOR | 'Red Rum' | incorrect | gold 未命中 |
| 1771 | train | Alternatively known as Austrpphlebia Costalis, what type of  | DRAGONFLY | 'Dragonfly' | correct | gold 命中（含等价/别名） |
| 1772 | train | Which political party, founded in 1967, has its headquarters | NATIONAL FRONT | 'The Green Party' | incorrect | gold 未命中 |
| 1773 | test | Darwin is the capital of which Australian state ? | NORTHERN TERRITORY | 'Northern Territory' | correct | gold 命中（含等价/别名） |
| 1774 | train | What is the largest island in the Mediterrainean Sea? | SICILY | 'Sicily' | correct | gold 命中（含等价/别名） |
| 1775 | validation | Which film of 1988 sees the lead male character, named Dan G | FATAL ATTRACTION | 'The' | format_failure | 单 token 函数词/碎片 'The'，无答案内容 |
| 1776 | train | Which tennis player played in three consecutive men's single | FRED STOLLE | 'Arthur Ashe' | incorrect | gold 未命中 |
| 1777 | train | Ailurophobia is the abnormal fear of what? | CATS | 'cats' | correct | gold 命中（含等价/别名） |
| 1778 | validation | Which German word meaning 'armour' was applied to certain ar | PANZER | ' Panzer' | correct | gold 命中（含等价/别名） |
| 1779 | test | Name the town in the vicinity of Versailles famous for its h | SEVRES | 'Sèaux' | incorrect | 单 token 短答 'Sèaux'（疑似错答，人工留意） |
| 1780 | train | In which part of the human body can you find the Malleus or  | THE EAR | 'ear' | incorrect | 单 token 短答 'ear'（疑似错答，人工留意） |
| 1781 | train | In Indian cookery, dishes known as 'tandoori' are so named b | AN OVEN | 'cl clay oven' | correct | gold 别名命中 |
| 1782 | train | What is the name of the island that separates the two larges | GOAT ISLAND | 'Goid Island' | incorrect | gold 未命中 |
| 1783 | train | Some Americans claim to have seen a Sasquatch; by what name  | BIGFOOT | 'Bigfoot' | correct | gold 命中（含等价/别名） |
| 1784 | train | What was the surname of the 19th president of the USA who ha | HAYES | 'B' | format_failure | 单 token 函数词/碎片 'B'，无答案内容 |
| 1785 | train | Which two word named plant, also known as Dionaea Muscipala  | VENUS FLYTRAP | ' Venus fly trap' | correct | gold 别名命中 |
| 1786 | train | Which is the most southerly Irish city ? | CORK | 'Cork' | correct | gold 命中（含等价/别名） |
| 1787 | train | In which year was the ten shilling note withdrawn in the UK  | 1970 | '1983' | incorrect | 单 token 短答 '1983'（疑似错答，人工留意） |
| 1788 | validation | What nationality was the pointillist artist MONDRIAN? | DUTCH | 'Dutch' | correct | gold 命中（含等价/别名） |
| 1789 | test | Who was the first Republican President of the United States  | ABRAHAM LINCOLN | 'raham Lincoln' | incorrect | gold 未命中 |
| 1790 | test | Which national anthem was originally called the 'War Song fo | MARSELLAISE | 'Germany' | incorrect | 单 token 短答 'Germany'（疑似错答，人工留意 |
| 1791 | train | "The opera ""Duke Bluebeard's Castle"" and the ballet ""The  | BARTOK | 'B Strauss' | incorrect | gold 未命中 |
| 1792 | validation | Which superhero film, produced by Marvel Studios and written | THE AVENGERS | 'The Avengers' | correct | gold 命中（含等价/别名） |
| 1793 | validation | Which Italian liqueur is a key ingredient of the well known  | GALLIANO | 'amaretto' | incorrect | 单 token 短答 'amaretto'（疑似错答，人工留 |
| 1794 | test | Which rider won the ladies European Three Day event Champion | PRINCESS ANNE | 'Mary King' | incorrect | gold 未命中 |
| 1795 | validation | "Which product was promoted with the slogan ""Full of Easter | FRY'S TURKISH DELIGHT | 'Te' | format_failure | 单 token 函数词/碎片 'Te'，无答案内容 |
| 1796 | train | Which opera by Borodin features the Polovtsian Dances? | PRINCE IGOR | 'Prince Igor' | correct | gold 命中（含等价/别名） |
| 1797 | validation | What was the name of the British teacher jailed in Sudan in  | GILLIAN GIBBONS | 'David Thomas' | incorrect | gold 未命中 |
| 1798 | train | Which city in Saxony was known as Karl-Marx-Stadt from 1953  | CHEMNITZ | 'Dresdenau' | incorrect | 单 token 短答 'Dresdenau'（疑似错答，人工 |
| 1799 | train | David Tyler is the current chairman of which leading superma | SAINSBURY'S | 'Tesco' | incorrect | 单 token 短答 'Tesco'（疑似错答，人工留意） |
| 1800 | train | "Which snooker player had the nickname ""The Thunder from Do | NEIL ROBERTSON | 'John White' | incorrect | gold 未命中 |
