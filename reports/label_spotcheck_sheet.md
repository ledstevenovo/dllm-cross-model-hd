# 标签人工抽查表（第二 judge 对照，主项目 + DynHD）

- 两套被判分条目共 200（dynhd 100, main 100），其中不一致 7 条；`review_priority` 标记：不一致全部 + 一致中抽 43 条 = 50 条建议人工复核（不少于 50 条）。
- `source` 列：`main` = 主项目 reviewed 标签（迁移矩阵/稳定性所用）；`dynhd` = DynHD 复现规则标签。
- 每行给出：规则标签（主表所用）vs 第二 judge 标签、判定理由。请只看题面与参考答案，独立判断后填 CSV 的 `your_verdict`（agree | rule_ok_judge_wrong | judge_ok_rule_wrong | unsure）与 `your_notes`。
- 本表不改主标签，只作为标签质量证据留存。

## 1. [disagreement] dynhd/dream · triviaqa__qw_4069 · ⚠️ 不一致

- **问题**：Who succeeded Prince Rainier of Monaco?
- **参考答案**：Prince Albert；Prince Consort Albert；Albert of Saxe-Coburg-Gotha；Albert of Saxe Coburg-Gotha；Prince Albert of Saxe-Coburg-Saalfield；Francis Albert Augustus Charles Emmanuel；Francis Charles Augustus Albert；Prince Albert Of Saxe-Coburg-Gotha；Albert Charles Augustus Emmanuel；Albert, Prince Consort of the United Kingdom；Prince Consort of Great Britain and Ireland Albert；Prince Albert of the United Kingdom；Prince Albert, Prince Consort；Albert of Saxe-Coburg-Saalfield；Albert of Saxe-Coburg and Gotha；The Prince Consort；Prince Albert of Saze-Coburg-Gotha；Prince Albert of Saxe Coburg-Gotha；Albert Saxe-Gotha；Albert of Saxe-Coburg；Prince Albert of Saxe-Coburg and Gotha；Albert, prince consort of Victoria of Great Britain；Prince Albert of Saxe-Coburg；Albert of the United Kingdom；Prince Albert；Albert, Prince Consort；Prince Albert of Saxe-Coburg-Gotha；Prince Albert Saxe-Coburg and Gotha
- **模型回答**：Prince Albert II
- **规则标签**：correct(0) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Prince Albert II' does not match any of the supplied reference answers. All reference answers refer to Prince Albert, the 19th-century Prince Consort of the United Kingdom (of Saxe-Coburg-Gotha), not Albert II of Monaco who succeeded Rainier III. Since the answer is not semantically equivalent to any valid reference answer, it is incorrect.

## 2. [disagreement] dynhd/llada · hotpotqa__5a8b78775542997f31a41d3d · ⚠️ 不一致

- **问题**：Chimaja Appawas the younger brother of a general of the Maratha Empire in India, who served as what to the fifth Maratha Chhatrapati Shahu from 1720 until his death?
- **参考答案**："Peshwa" (Prime Minister)
- **模型回答**：Chimaja Appawas was the younger brother of Chimaji Appa, a general of the Maratha Empire in India. Chimaja Appawas served as the Peshwa (prime minister) to the fifth Maratha Chhatrapati Shahu from 1720 until his death.
- **规则标签**：correct(0) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The answer correctly names 'Peshwa (prime minister)' but misattributes the role to Chimaja Appa. Historically, the Peshwa to Chhatrapati Shahu from 1720 until his death (1740) was Bajirao I (Chimaji Appa's brother), not Chimaja Appa. This is a material factual error, so the answer is incorrect despite containing the right title.

## 3. [disagreement] dynhd/llada · hotpotqa__5adc0d2955429947ff1738e6 · ⚠️ 不一致

- **问题**：Are Roger Waters and Tom Johnston both musicians?
- **参考答案**：yes
- **模型回答**：Yes, both Roger Waters and Tom Johnston are musicians. Roger Waters is a drummer, and Tom Johnston is a guitarist.
- **规则标签**：correct(0) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：While it correctly answers yes to the question, it adds a material factual error: Roger Waters is a bassist/vocalist, not a drummer.

## 4. [disagreement] main/dream · hotpotqa__5a876f785542993e715abf42__seed20261020 · ⚠️ 不一致

- **问题**：Which person, William Blake Herron or John Carpenter, held more diverse roles in the movie industry?
- **参考答案**：musician, editor and composer.
- **模型回答**：John Carpenter
- **规则标签**：incorrect(1) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'John Carpenter' correctly identifies the person who held more diverse roles in the movie industry. The reference answer lists roles (musician, editor, composer) that describe Carpenter's multifaceted career as director, composer, editor, and producer, confirming he is the correct choice over William Blake Herron, who is primarily known as a screenwriter/director.

## 5. [disagreement] main/dream · triviaqa__qw_4069__seed20261020 · ⚠️ 不一致

- **问题**：Who succeeded Prince Rainier of Monaco?
- **参考答案**：Prince Albert；Prince Consort Albert；Albert of Saxe-Coburg-Gotha；Albert of Saxe Coburg-Gotha；Prince Albert of Saxe-Coburg-Saalfield；Francis Albert Augustus Charles Emmanuel；Francis Charles Augustus Albert；Prince Albert Of Saxe-Coburg-Gotha；Albert Charles Augustus Emmanuel；Albert, Prince Consort of the United Kingdom；Prince Consort of Great Britain and Ireland Albert；Prince Albert of the United Kingdom；Prince Albert, Prince Consort；Albert of Saxe-Coburg-Saalfield；Albert of Saxe-Coburg and Gotha；The Prince Consort；Prince Albert of Saze-Coburg-Gotha；Prince Albert of Saxe Coburg-Gotha；Albert Saxe-Gotha；Albert of Saxe-Coburg；Prince Albert of Saxe-Coburg and Gotha；Albert, prince consort of Victoria of Great Britain；Prince Albert of Saxe-Coburg；Albert of the United Kingdom；Prince Albert；Albert, Prince Consort；Prince Albert of Saxe-Coburg-Gotha；Prince Albert Saxe-Coburg and Gotha
- **模型回答**：Prince Albert II
- **规则标签**：correct(0) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Prince Albert II' refers to Albert II of Monaco who succeeded Rainier III. However, all reference answers refer to Prince Albert, Prince Consort of Queen Victoria (of Saxe-Coburg and Gotha), a completely different historical figure from the 19th century. The proposed answer does not semantically match any of the reference answers.

## 6. [disagreement] main/llada · hotpotqa__5adc2f53554299438c868d6d__seed20261020 · ⚠️ 不一致

- **问题**：Were Triumph of the Will and The End of America both made in the same year?
- **参考答案**：no
- **模型回答**：No, Triumph of the Will and The End of America were not made in the same year. Triumph of the Will was released in 1955, while The End of America was released in 1956.
- **规则标签**：correct(0) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer states Triumph of the Will was released in 1955, but it was actually released in 1935. This is a material factual error.

## 7. [disagreement] main/llada · triviaqa__qw_15432__seed20261020 · ⚠️ 不一致

- **问题**：The actor John Wayne was known by what nickname?
- **参考答案**：The Duke；The Duke；Duke (disambiguation)；Duke (dog)；The Duke (1999 film)；Dukes (disambiguation)
- **模型回答**：Duke.
- **规则标签**：incorrect(1) ｜ **judge 标签**：correct(0)
- **judge 理由**：John Wayne's nickname was 'The Duke'; 'Duke' is a semantically equivalent short form matching the reference answer.

## 8. [sample] dynhd/dream · hotpotqa__5a72f74a55429901807daf59 · 一致

- **问题**：Which American comedian born on March 21, 1962, appeared in the movie "Sleepless in Seattle?"
- **参考答案**：Rosie O'Donnell
- **模型回答**：Billy Crystal
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer is Billy Crystal, but the correct answer is Rosie O'Donnell, who was born on March 21, 1962. Billy Crystal was born on March 14, 1948, so he does not match the birth date criterion.

## 9. [sample] dynhd/dream · hotpotqa__5a7b3b4f5542992d025e67ac · 一致

- **问题**：Who is the older brother of the king that was overthrown in the Henriad?
- **参考答案**：Edward of Angoulême
- **模型回答**：Henry
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Henry' does not match the reference answer 'Edward of Angoulême'. The king overthrown in the Henriad is Richard II, and his older brother was Edward of Angoulême, not Henry.

## 10. [sample] dynhd/dream · hotpotqa__5a7ccb3655429909bec7680b · 一致

- **问题**：Who bestowed Kaganoi Shigemochi with a blade made by the person that founded the Muramasa school?
- **参考答案**：Hideyoshi
- **模型回答**：Muramasa
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names the blade's maker, not the person who bestowed the blade; the valid answer is Hideyoshi.

## 11. [sample] dynhd/dream · hotpotqa__5a8242c155429940e5e1a81d · 一致

- **问题**：Where was the author of Thoughts of Machiavelli born?
- **参考答案**：Germany
- **模型回答**：Florence
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Florence' contradicts the reference answer 'Germany'.

## 12. [sample] dynhd/dream · hotpotqa__5a84d2775542994c784dda5f · 一致

- **问题**：What disease is the Wolf Prize winner and Vadim Bereinskii-inspired Nobel laureate suffering from?
- **参考答案**：dementia
- **模型回答**：cancer
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer "cancer" contradicts the reference answer "dementia".

## 13. [sample] dynhd/dream · hotpotqa__5a8b78775542997f31a41d3d · 一致

- **问题**：Chimaja Appawas the younger brother of a general of the Maratha Empire in India, who served as what to the fifth Maratha Chhatrapati Shahu from 1720 until his death?
- **参考答案**："Peshwa" (Prime Minister)
- **模型回答**：prime Minister
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'prime Minister' is semantically equivalent to the reference answer 'Peshwa (Prime Minister)', correctly identifying the role Bajirao I served under Chhatrapati Shahu.

## 14. [sample] dynhd/dream · hotpotqa__5a906f9f5542995b442420b3 · 一致

- **问题**：What theatre in St. Martin's Lane often hosts the English National Ballet?
- **参考答案**：London Coliseum
- **模型回答**：The Opera Theatre
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer contradicts the reference answer 'London Coliseum' and names a different, incorrect venue.

## 15. [sample] dynhd/dream · hotpotqa__5ab43179554299233955004d · 一致

- **问题**：What is the female star of Klepto best known for performing in?
- **参考答案**：The Secret World of Alex Mack
- **模型回答**：com
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The answer "com" does not name a performance or show and is not semantically equivalent to the reference answer "The Secret World of Alex Mack".

## 16. [sample] dynhd/dream · hotpotqa__5ab9668c55429970cfb8eaba · 一致

- **问题**：What major city is John Bice Memorial Oval located within?
- **参考答案**：City of Onkaparinga
- **模型回答**：Mel
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names a different major city and does not match the valid reference answer, City of Onkaparinga.

## 17. [sample] dynhd/dream · hotpotqa__5abdba405542993f32c2a023 · 一致

- **问题**：Orlando Brown is best known for his role as 3J Winslow in an American sitcom that was a spin-off of what?
- **参考答案**：Perfect Strangers
- **模型回答**：Family House
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer "Family House" contradicts the reference answer "Perfect Strangers".

## 18. [sample] dynhd/dream · hotpotqa__5ac372195542995ef918c194 · 一致

- **问题**：Which major regional shopping centre in the western suburb of Indooroopilly in the City of Brisbane, Queensland, Australia is served by TransLink bus routes?
- **参考答案**：Indooroopilly Shopping Centre
- **模型回答**：Indooroopilly Shopping Centre
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches the reference answer exactly and correctly identifies the shopping centre.

## 19. [sample] dynhd/dream · hotpotqa__5adbf81a554299438c868cfd · 一致

- **问题**：Are Vintage Life and InStyle both US-based magazines?
- **参考答案**：no
- **模型回答**：Yes
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer contradicts the reference answer, which states "no".

## 20. [sample] dynhd/dream · hotpotqa__5adc0d2955429947ff1738e6 · 一致

- **问题**：Are Roger Waters and Tom Johnston both musicians?
- **参考答案**：yes
- **模型回答**：Yes, Roger Waters and Tom Johnston are both musicians.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer affirms that both Roger Waters and Tom Johnston are musicians, which matches the reference answer.

## 21. [sample] dynhd/dream · hotpotqa__5adc2f53554299438c868d6d · 一致

- **问题**：Were Triumph of the Will and The End of America both made in the same year?
- **参考答案**：no
- **模型回答**：No
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'No' is semantically equivalent to the reference answer 'no'.

## 22. [sample] dynhd/dream · hotpotqa__5adcf3e35542994ed6169c3a · 一致

- **问题**：Dean Mills Reservoir is on the slopes of the hill located in what town?
- **参考答案**：Rivington Moor
- **模型回答**：Dean Mills
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Dean Mills' is just part of the reservoir's name and does not identify the town. It does not match the reference answer 'Rivington Moor'.

## 23. [sample] dynhd/dream · hotpotqa__5ae088525542993d6555eba1 · 一致

- **问题**：Are Stan Lee and Mark Helprin both comic book writers?
- **参考答案**：no
- **模型回答**：Yes
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Mark Helprin is a novelist, not a comic book writer, so the correct answer is 'no', not 'Yes'.

## 24. [sample] dynhd/dream · triviaqa__bb_4464 · 一致

- **问题**：Turkey's internet country TLD (Top Level Domain) code is?
- **参考答案**：.tr；.tr；.nc.tr；.TR；.gen.tr
- **模型回答**：.tr
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：.tr is Turkey's country code top-level domain and matches the reference answers.

## 25. [sample] dynhd/dream · triviaqa__bb_5094 · 一致

- **问题**：What London medicinal water site, later a music hall, was the birthplace of the Royal Ballet and English National Opera?
- **参考答案**：Sadler's Wells；Sadler's Wells；New Sadler's Wells Opera；Sadler’s Wells；Sadler's-Wells；Lilian Baylis Theatre；New Sadler's Wells Opera Company；Sadlers Wells；Sadler’s Wells Theatre；Sadler's Wells Theatre
- **模型回答**：The Garden
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'The Garden' does not match any valid reference answer. The correct answer is Sadler's Wells (or a recognized variant thereof).

## 26. [sample] dynhd/dream · triviaqa__bt_1 · 一致

- **问题**：Who was the lead singer with Stylistics
- **参考答案**：Russell Thompkins；Airrion Love；The Stylistics；Russell Thompkins
- **模型回答**：David James
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'David James' does not match any valid reference answer (Russell Thompkins, Airrion Love, or The Stylistics).

## 27. [sample] dynhd/dream · triviaqa__bt_3007 · 一致

- **问题**：Who wrote the epic 1869 novel War and Peace
- **参考答案**：Leo Tolstoy；Lyof Nikolaivitch Tolstoi；Tolstoy；Leo Nikolaievich Tolstoy；Lev Nikolaïevitch Tolstoï；Lev Nikolajevič Tolstoj；Count Lev Tolstoy；Lev Nikolajevic Tolstoj；Lev Nikolaevich Tolstoy；Leo tolstoi；Tolstoi；LN Tolstoi；Leo N. Tolstoy；Buried Alive (play)；Lev N. Tolstoi；Lev Tolstoi；Voice of Thunder (Lincoln)；Lev Tolstoï；Leo N. Tolstoi；Tolstoy, Lev Nikolayevich；Lev N. Tolstoï；LN Tolstoy；Count Lev Nikolaevich Tolstoi；Lev Nikolaevic Tolstoj；Leo N. Tolstoï；Толстой；Lev N. Tolstoy；Lev Tolstoy；Leo Tolstoï；Count Lev N. Tolstoy；Leo Tolstoy's religious beliefs；Leo tolstoy；Count Leo Tolstoy；León Tolstói；Lev Nikolayevich Tolstoy；Лев Никола́евич Толсто́й；Leo Tolstoy；Leo Nikolayevich Tolstoy；Leo Nikoleyevich Tolstoy；Count Leo Tolstoï；Count Leo N. Tolstoy；Leon Tolstoi；Leo Nikolayevitch Tolstoy；Count Leo Tolstoi；Lyof Tolstoy；Count Leo N. Tolstoi；Count Leo N. Tolstoï；Lev Tolstói；Lev Nikolaevič Tolstoj；Leo Tolstoi；Léon Tolstoï；Лев Николаевич Толстой；Leon Tolstoy；Lev Tolstoj；Leo, Count Tolstoy；Tolstoy, Leo Nikolayevich；Lev Nikolaievitch Tolstoi
- **模型回答**：Le Leo Tolstoy
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer names Leo Tolstoy (with a French article 'Le' prefix), which matches multiple valid reference answers and correctly identifies the author of War and Peace.

## 28. [sample] dynhd/dream · triviaqa__bt_3768 · 一致

- **问题**：Which is the only sign of the Zodiac to start and finish with the same letter
- **参考答案**：Sagittarius；Sagittarius Dwarf；Saggattarius；Saggattarrius；Sagittarius；Sagittarius (disambiguation)；Sagittarius Galaxy；Saggittarius；Sagittarius dwarf galaxy；Saggittarrius；Sagitarius；Sagitarrius；Sagittarius Dwarf Galaxy；Saggatarrius；Saggitarius；Sagittarius (dwarf galaxy)；Sagittarius dwarf；Saggitarrius；Sagittarius galaxy；Saggatarius
- **模型回答**：Aries
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The only zodiac sign starting and ending with the same letter is Sagittarius (starts and ends with 'S'). Aries starts with 'A' and ends with 'S', so it does not match any valid reference answer.

## 29. [sample] dynhd/dream · triviaqa__dpql_5449 · 一致

- **问题**：What is the secret identity of Penrod ‘Penry’ Pooch?
- **参考答案**：Hong Kong Phooey；Hong Kong Phooie；Hong Kong Phooey (film)；Hong Kong Fuey；Hong Kong Phuey；Hong Kong Phooey；Hong Kong Fooey
- **模型回答**：Pen
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The secret identity of Penrod Pooch is Hong Kong Phooey, not 'Pen'.

## 30. [sample] main/dream · hotpotqa__5a70f1685542994082a3e40f__seed20261020 · 一致

- **问题**：Which piece did Ludwig van Beethoven publish in 1801 that was dedicated to Count Moritz von Fries?
- **参考答案**：Symphony No. 7
- **模型回答**：Moonlight Sonata
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Moonlight Sonata' does not match the reference answer 'Symphony No. 7' and contradicts it.

## 31. [sample] main/dream · hotpotqa__5a77dadd5542997042120b59__seed20261020 · 一致

- **问题**：Hall of Fame Racing was created by Troy Aikman, Bill Saunders, and which Dallas Cowboys quarterback known as "Captain Comback"?
- **参考答案**：Roger Thomas Staubach (born February 5, 1942)
- **模型回答**：Jerry Carter
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Jerry Carter' does not match the reference answer Roger Staubach, who is the Dallas Cowboys quarterback known as 'Captain Comeback' and co-founder of Hall of Fame Racing.

## 32. [sample] main/dream · hotpotqa__5a796c805542990784727805__seed20261020 · 一致

- **问题**：The brother of Ferdinand Alfred Friedrich Jodl served as what position in World War II?
- **参考答案**：Chief of the Operations Staff of the Armed Forces High Command
- **模型回答**：Fielder
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Fielder' does not match the reference answer 'Chief of the Operations Staff of the Armed Forces High Command' and does not address the question.

## 33. [sample] main/dream · hotpotqa__5a7b493855429931da12ca58__seed20261020 · 一致

- **问题**：The Good Dinosaur features the voice of what Canadian-born New Zealand actress?
- **参考答案**：Anna Helene Paquin
- **模型回答**：Elisabeth Moss
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Elisabeth Moss is an American actress, not Canadian-born New Zealand; the correct answer is Anna Paquin.

## 34. [sample] main/dream · hotpotqa__5a81b43d5542995ce29dcc39__seed20261020 · 一致

- **问题**：John Stoltenberg is the managing editor of the magazine that focuses on what?
- **参考答案**：aging issues
- **模型回答**：pol
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**："pol" is not semantically equivalent to "aging issues" and does not answer the question about the magazine's focus.

## 35. [sample] main/dream · hotpotqa__5a88d7875542993b751ca876__seed20261020 · 一致

- **问题**：Who won the 1981 CART PPG Indy Car World Series in Avondale Arizona?
- **参考答案**：Rick Ravon Mears
- **模型回答**：John Jones
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'John Jones' contradicts the valid reference answer 'Rick Ravon Mears' (Rick Mears won the 1981 CART championship).

## 36. [sample] main/dream · hotpotqa__5a8b3c0055429949d91db4f8__seed20261020 · 一致

- **问题**：IS Paul Sloane noted for directing more musicals than Jacques Demy
- **参考答案**：no
- **模型回答**：No
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches the reference answer semantically and factually.

## 37. [sample] main/dream · hotpotqa__5a8b78775542997f31a41d3d__seed20261020 · 一致

- **问题**：Chimaja Appawas the younger brother of a general of the Maratha Empire in India, who served as what to the fifth Maratha Chhatrapati Shahu from 1720 until his death?
- **参考答案**："Peshwa" (Prime Minister)
- **模型回答**：prime Minister
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'prime Minister' is a casing variant of the reference answer 'Peshwa (Prime Minister)', which is semantically equivalent and correctly answers the question.

## 38. [sample] main/dream · hotpotqa__5a8ec55f5542995a26add50c__seed20261020 · 一致

- **问题**：At what height does State Route 160 start?
- **参考答案**：4145 ft
- **模型回答**：sea level
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'sea level' contradicts the reference answer of 4145 ft.

## 39. [sample] main/dream · hotpotqa__5ab8397155429919ba4e2272__seed20261020 · 一致

- **问题**：What was the event where Jacob Minah had his personal best also known as?
- **参考答案**：XXIV Summer Universiade
- **模型回答**：High jump
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'High jump' refers to an athletic discipline, not the name of the competition. The reference answer is 'XXIV Summer Universiade', which is the event where Jacob Minah achieved his personal best.

## 40. [sample] main/dream · hotpotqa__5ac3044f5542990b17b154dc__seed20261020 · 一致

- **问题**：Danny Jones and Aleksi Sihvonen are both what?
- **参考答案**：vocalist
- **模型回答**：musingers
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**："musingers" is not a recognized term and does not match the reference answer "vocalist"; it does not correctly answer the question.

## 41. [sample] main/dream · hotpotqa__5adbf81a554299438c868cfd__seed20261020 · 一致

- **问题**：Are Vintage Life and InStyle both US-based magazines?
- **参考答案**：no
- **模型回答**：Yes
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The reference answer is 'no' (Vintage Life is UK-based, not US-based). The proposed answer 'Yes' contradicts the reference and is factually wrong.

## 42. [sample] main/dream · hotpotqa__5ae27f22554299495565da8d__seed20261020 · 一致

- **问题**：In what year was the mathematician husband of Anneli Cahn Lax born?
- **参考答案**：1926
- **模型回答**：1910
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer (1910) contradicts the valid reference answer (1926).

## 43. [sample] main/dream · hotpotqa__5ae326e95542990afbd1e0b6__seed20261020 · 一致

- **问题**：Where is the American Hockey League, that Dan Frawley played in, located?
- **参考答案**：United States and Canada
- **模型回答**：Canadaario
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer "Canadaario" is not a valid location and does not match the reference answer "United States and Canada."

## 44. [sample] main/dream · hotpotqa__5ae675245542991bbc9760dc__seed20261020 · 一致

- **问题**：What is the name of the father of Childericus?
- **参考答案**：Merovech
- **模型回答**：Childvis
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Childvis' does not match the reference answer 'Merovech' and does not provide a valid alternative name for the father of Childericus.

## 45. [sample] main/dream · hotpotqa__5ae7a9765542994a481bbdbc__seed20261020 · 一致

- **问题**：What is the long name of the Government of Ireland Act 1920 that relates to Islam in Northern Ireland?
- **参考答案**：An Act to provide for the better government of Ireland
- **模型回答**：Northern
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer "Northern" does not provide the long name of the Government of Ireland Act 1920 and is not semantically equivalent to the reference answer "An Act to provide for the better government of Ireland".

## 46. [sample] main/dream · triviaqa__bb_436__seed20261020 · 一致

- **问题**：What standard test characteristic has been produced in genetically modified laboratory animals so that researchers can see easily that genetic modification has occurred?
- **参考答案**：Glow in the dark；Glow-in-the-dark；Glow in the Dark；Glow-in-the-dark (disambiguation)；Glow in the dark
- **模型回答**：green eyes
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'green eyes' does not match any reference answer. The correct characteristic is 'glow in the dark' (referring to GFP fluorescence), not green eyes.

## 47. [sample] main/dream · triviaqa__bb_5094__seed20261020 · 一致

- **问题**：What London medicinal water site, later a music hall, was the birthplace of the Royal Ballet and English National Opera?
- **参考答案**：Sadler's Wells；Sadler's Wells；New Sadler's Wells Opera；Sadler’s Wells；Sadler's-Wells；Lilian Baylis Theatre；New Sadler's Wells Opera Company；Sadlers Wells；Sadler’s Wells Theatre；Sadler's Wells Theatre
- **模型回答**：The Garden
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The answer names the wrong site; the references identify Sadler's Wells, not The Garden.

## 48. [sample] main/dream · triviaqa__bb_7225__seed20261020 · 一致

- **问题**：A salpingectomy is the surgical removal of which part of the body?
- **参考答案**：Fallopian tubes；Tubal patency；Fallopian tube diseases；Fallopian；Fallopian tube；Fallopian Tube；Salpinx tube；Tuba uterina；Oviducts；Uterine tube；Fallopian tube pathology；Uterine tubes；Oviducal；Fallopian Tubes；Fallopian tubes
- **模型回答**：ovaries
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：A salpingectomy is the surgical removal of the Fallopian tube(s) (salpinx), not the ovaries. Removal of the ovaries is an oophorectomy.

## 49. [sample] main/dream · triviaqa__bt_1__seed20261020 · 一致

- **问题**：Who was the lead singer with Stylistics
- **参考答案**：Russell Thompkins；Airrion Love；The Stylistics；Russell Thompkins
- **模型回答**：David James
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names the wrong person; valid answers include Russell Thompkins or Airrion Love.

## 50. [sample] main/dream · triviaqa__dpql_5449__seed20261020 · 一致

- **问题**：What is the secret identity of Penrod ‘Penry’ Pooch?
- **参考答案**：Hong Kong Phooey；Hong Kong Phooie；Hong Kong Phooey (film)；Hong Kong Fuey；Hong Kong Phuey；Hong Kong Phooey；Hong Kong Fooey
- **模型回答**：Pen
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**："Pen" is only a truncation of the character's given name and does not provide the secret identity; the correct answer is Hong Kong Phooey.

## 51. [-] dynhd/dream · triviaqa__jp_3637 · 一致

- **问题**：What is either a bay in the Indian ocean or a subspecies of tiger?
- **参考答案**：Bengal；Bengal (India)；Kingdom of Bengal；Bengal, India；Bôngo；Bôngodesh；বঙ্গদেশ；Bongodesh；Greater Bengal；Etymology of Bengal；Bengal；বঙ্গ
- **模型回答**：Bayay
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Bayay' does not match any valid reference answer and is not a known bay in the Indian Ocean or a tiger subspecies.

## 52. [-] dynhd/dream · triviaqa__odql_12408 · 一致

- **问题**：Who is the current occupant of Dorneywood in Buckinghamshire?
- **参考答案**：George Osborne；Gideon Osborne；Chancellor George Osborne；George Osbourne；George osborne；George Gideon Oliver Osborne；George Osborne MP；Gideon George Oliver Osborne；George Osborne
- **模型回答**：David
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'David' contradicts all reference answers, which identify the occupant as George Osborne.

## 53. [-] dynhd/dream · triviaqa__odql_2542 · 一致

- **问题**：Of which country is Yingluck Shinawatra the Prime Minister?
- **参考答案**：THAILAND；Muang Thai；Taihland；ISO 3166-1:TH；Thai Empire；Prathet Thai；Muang-Thai；Kingdom of Thailand；Skateboarding in Thailand；THAILAND；Siam；Sport in Thailand；Etymology of Thailand；Thayland；Name of Thailand；The Kingdom Of Thailand；เมืองไทย；Thailand；ราชอาณาจักรไทย；Sayam；Thailande；Siam (Thailand)；ประเทศไทย；Kingdom Of Thailand；Tailand；Thai Kingdom；Ratcha Anachak Thai；Kingdom of the Thai
- **模型回答**：Thailand
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Thailand' directly matches multiple reference answers and correctly identifies the country where Yingluck Shinawatra served as Prime Minister.

## 54. [-] dynhd/dream · triviaqa__odql_3310 · 一致

- **问题**：What is the name of the tropical shrub from which the reddish dye is extracted to colourhair?
- **参考答案**：HENNA；Mylaanchi；HENNA；Hina (body art)；Henna；Camphire；Mailanchi；Lawsonia alba；Mylanji；Jamaica mignonette；Lawsonia (plant genus)；Lawsonia inermis；Black henna；Mignonette tree；Lawsonia (plant)；Mylanchi
- **模型回答**：Madder
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Madder' refers to a different plant (Rubia tinctorum) and contradicts the reference answers, which all identify henna (Lawsonia inermis) as the tropical shrub used to produce the reddish dye for coloring hair.

## 55. [-] dynhd/dream · triviaqa__odql_6828 · 一致

- **问题**：Aboard which ship did Japan sign the surrender at the end of World War II?
- **参考答案**：U.S.S. MISSOURI；U.S.S. Missouri；U.S.S. MISSOURI；Battleship Missouri；Uss Missouri；USS Missouri；Uss missouri
- **模型回答**：USS Missouri
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches one of the reference answers exactly.

## 56. [-] dynhd/dream · triviaqa__odql_8118 · 一致

- **问题**：In World War I, the British soldiers were nicknamed 'Tommies', what name was given to French soldiers?
- **参考答案**：'POILU'；Poilu；'POILU'；Poilus
- **模型回答**：Gies
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The answer 'Gies' does not match any valid reference answer ('POILU' or 'Poilus'), which is the correct nickname for French WWI soldiers.

## 57. [-] dynhd/dream · triviaqa__qb_3878 · 一致

- **问题**：Who wrote the political treatise ‘The Prince’, published in 1532?
- **参考答案**：Niccolo Machiavelli；Niccolò Macchiavelli；Nicole Machiavelli；Machavelli；Nioccolo Machiavelli；Machavellian；Macchiavelian；Nicolo Machiavelli；Machiavilli；Nicoli Machiavelli；Fawce；Marietta Corsini；Machiaveli；Niccolo Macchiavelli；Niccolo di Bernardo dei Machiavelli；Niccolò Machiavelli；Macchiavelianism；Niccol Machiavelli；Machiavellian test；Macavelli；Machiavellia；Niccolo' Macchiavelli；Machiavelians；Niccol%5CxC3%5CxB2 Machiavelli；Nicollo Machiavelli；Machievel；Machiavelian；Machevelli；Machiavelli；Niccolò di Bernardo dei Machiavelli；Nicholas Machiavelli；Macchiavelli；Macchiaveli；Makiavelo；Machiavelli's；Nicholas Machiavell；Machiavelli, Niccolò；Machaevelli；Niccolo Machiavelli；Machiavelliism；Machievelli；Nicolò Machiavelli；Niccoló Macchiavelli；Nicoló Machiavelli；Macavhelli；Machiavelli, Niccolo
- **模型回答**：Machiavelli
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：Machiavelli is listed as a valid reference answer and correctly identifies the author of The Prince.

## 58. [-] dynhd/dream · triviaqa__qb_606 · 一致

- **问题**：The Hotel Matignon is the official residence of the Prime Minister of which European country?
- **参考答案**：France；La Republique francaise；Franciaország；La Republique française；Belle France；FRANCE；Republique française；France；Ranska；Franciaorszag；French Republic；République francaise；République française；ISO 3166-1:FR；Frankreich；France (country)；Etymology of France；FrancE；La République française；People of France；Republic of France；Fracne；Le France；The French Republic；Republique francaise；The Republic of France；La République francaise；La France；Rain in France；Republic of france；FRance；Frakkland；Climate of France；Franse
- **模型回答**：France
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches the reference answers; Hôtel Matignon is the official residence of the French Prime Minister.

## 59. [-] dynhd/dream · triviaqa__qb_777 · 一致

- **问题**：In 1951, which European country saw the abdication of King Leopold lll in favour of his son Baudouin?
- **参考答案**：Belgium；Belguim；Koenigreich Belgien；Belgium/Belgie；Kingdom of Belgium；Belgian；Beljum；Königreich Belgien；Belgique；Belgium；Beligum；Kingdom of the Belgians；Beljam；Kingdom Of Belgium；Belgum；ISO 3166-1:BE；Belgie；Cockpit of Europe；Koninkrijk België；Beldjike；Blegium；Belgio；The Quebec of Europe；België；Begium；Royaume de Belgique；Konigreich Belgien；Koninkrijk Belgie；People of Belgium；Belgien；Belgium/facts；Administrative divisions of Belgium；Belgium facts
- **模型回答**：Belgium
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Belgium' matches the reference answer exactly and is factually correct—Leopold III abdicated in favor of Baudouin in Belgium in 1951.

## 60. [-] dynhd/dream · triviaqa__qf_854 · 一致

- **问题**：Who was the French wife of Charles1st?
- **参考答案**：Henrietta Maria；Queen Henrietta Maria；Queen Henrietta Maria of England；Henrietta Maria De Bourbon；Henrietta Maria of France；Henrietta Maria de Bourbon；Queen Henriette Maria；Henriette Marie de France；Henrietta-Maria de Bourbon；Henrietta Maria；Henrietta Maria of England；Charles James Stuart, Duke of Cornwall
- **模型回答**：Elizabeth of France
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Elizabeth of France' does not match any valid reference answer; the correct answer is Henrietta Maria (of France).

## 61. [-] dynhd/dream · triviaqa__qf_957 · 一致

- **问题**：In what year did Torville and Dean (Jane and Christopher) win their first Olympic gold, scoring 12 perfect sixes in their free-dance routine?
- **参考答案**：1984；1984；one thousand, nine hundred and eighty-four
- **模型回答**：1984
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer '1984' matches the reference answers exactly and correctly answers the question about Torville and Dean's first Olympic gold.

## 62. [-] dynhd/dream · triviaqa__qw_10077 · 一致

- **问题**：Between 1783 and 1865, Englishmen William Wilberforce, Sir Cecil Wray and Dr Beilby Porteus, Africans Olaudah Equiano and Ignatius Sancho and, in the USA, William Lloyd Garrison, John Greenleaf Whittier, Harriet Beecher Stowe, Frederick Douglass, Charles Henry Langston and John Mercer Langston were leading figures in which movement?
- **参考答案**：Abolition of the slave trade；Abolitionism.；Critic of the slave trade；Emancipation of Slaves；White abolitionists；Abolition of slavery；Anti slavery movement；Antislavery movement；Emancipation of slaves；Abolutionism；Abolitionistic；Abolition (slavery)；Abolitionism in France；Anti-abolitionism；Abolition of Slavery；Abolitionism (slavery)；Movement to abolish slavery；Abolitionst；Abolishing slavery；White Abolitionists；Abolitionists；Opponent of slavery；Abolitionist movement；Slavery abolition；Anti-slavery；Emancipation Of Slaves；Abolition Of Slavery；Abolitionism；Slave emancipation；Opposition to slavery；Antislavery；Abolitionist (slavery)；Abolitionist；Abolitionist Movement；Emancipationist；Abolition of the slave trade；Anti-slavery movement
- **模型回答**：abolitionist movement
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches a valid reference answer and correctly identifies the movement these figures led.

## 63. [-] dynhd/dream · triviaqa__qw_12980 · 一致

- **问题**：What object was unveiled outside John Lennon Airport, Liverpool, in 2005?
- **参考答案**：Yellow submarine；Yellow Submarine；Yellow submarine；The Yellow Submarine；Yellow Submarine (disambiguation)；Yello Sub
- **模型回答**：John Lennon statue
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'John Lennon statue' contradicts the reference answers, which all indicate the Yellow Submarine was unveiled.

## 64. [-] dynhd/dream · triviaqa__qw_13271 · 一致

- **问题**：When were the first Winter Paralympics held?
- **参考答案**：1976；1976；one thousand, nine hundred and seventy-six
- **模型回答**：1960
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The answer 1960 contradicts the reference answers, which state 1976.

## 65. [-] dynhd/dream · triviaqa__qw_3850 · 一致

- **问题**：Where was the final of the 1999 Rugby World Cup held?
- **参考答案**：Wales；Welsh nation；Climate of Wales；Autonomous Province of Wales；Cymru / wales；Cyrmu；Wales；WALES；Rain in Wales；Welsh Nation；Welsh Peninsula；Wales, UK；Etymology of Wales；Cymru；Wales, United Kingdom；Pays de Galles；Communications in Wales；The Principality of Wales；West of the Rhymney；Wales, U.K.；Cymru am byth；Gymru；Cymru / Wales；Welsh mountains；CYMRU
- **模型回答**：New
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'New' does not match any reference answer and fails to identify Wales as the location of the 1999 Rugby World Cup final.

## 66. [-] dynhd/dream · triviaqa__qz_4047 · 一致

- **问题**：When Mr Benn was looking for an adventure, what type of shop did he visit?
- **参考答案**：A fancy dress shop；A fancy dress shop
- **模型回答**：Book shop
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Book shop' contradicts the reference answers, which state 'A fancy dress shop'.

## 67. [-] dynhd/dream · triviaqa__qz_4151 · 一致

- **问题**：What was the name of the ferry that capsized after leaving Zeebrugge in 1987
- **参考答案**：The Herald of free Enterprise；M/S Herald of Free Enterprise；Zeebrugge ferry disaster；MS Herald of Free Enterprise；Herald of free enterprise；IMO 7820485；Flushing Range；The Herald of Free Enterprise；Herald of Free Enterprise；The Herald of free Enterprise；Zeebrugge Disaster
- **模型回答**：The ferry that capsized after leaving Zeebrugge in 1987 was the Heraldia.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Heraldia' does not match any valid reference answer; the correct name is 'Herald of Free Enterprise'.

## 68. [-] dynhd/dream · triviaqa__qz_866 · 一致

- **问题**：What seven letter word, beginning with the letters 'Ra' is a palindrome?
- **参考答案**：Racecar；Racing cars；Automobile Racing；Automotive racing；Car racing；Race driver；Racecars；Automobile racer；Autorace；Car race；Autosports；Racecar；Race cars；Automobile race；🏎；Racing driver；AutoRacing；Racing Car；Auto racing；Auto Racing；Auto race；Race-car；Race Cars；Auto Race；Race car；Racing car；Race car driver；Automobile racing；Racecar driver
- **模型回答**：radcar
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**："radcar" is not a palindrome (it reads "racdar" backwards), failing the question's core requirement. The correct reference answer is "Racecar".

## 69. [-] dynhd/dream · triviaqa__sfq_10625 · 一致

- **问题**：'If you have a problem, if no-one else can help, and if you can find them'; then maybe you could hire who, on TV in the 1980s?
- **参考答案**：THE A-TEAM；A-Team；A - team；The A-Team cultural effects；The A-team；THE A-TEAM；Ateam；B.a. barracas；A team；B.A. Barracas；Ba barracas；Half pincer movement；Brigada A；A-Team, The；A Team, The；The A-Team；The A Team；The ateam；The a-team；Cultural effects of The A-Team；A Team；A-team
- **模型回答**：Theman
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The question's famous tagline clearly refers to The A-Team, as confirmed by all reference answers. The proposed answer 'Theman' does not match any valid reference answer and is factually wrong.

## 70. [-] dynhd/dream · triviaqa__sfq_11095 · 一致

- **问题**：Which pop singer shot himself to death in 1990 whilst suffering from depression?
- **参考答案**：DEL SHANNON；DEL SHANNON；Berlee Records；Berlee records；Del Shannon；Del shannon
- **模型回答**：Davidain
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Davidain' does not match any valid reference answer (Del Shannon or Berlee Records) and is not a known alias for the pop singer who died by suicide in 1990.

## 71. [-] dynhd/dream · triviaqa__sfq_1110 · 一致

- **问题**：Which English clergyman/chemist discovered oxygen?
- **参考答案**：Joseph Priestley；Priestley, Joseph；Joseph priestley；Joseph Priestly；Joseph Priestly (1733 - 1804)；J. Priestley；J Priestley；A Lover of the Gospel；Joseph Priestley；Joseph Preistley；A Lover of Peace and Truth
- **模型回答**：Joseph Priestley
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Joseph Priestley' exactly matches multiple reference answers and correctly identifies the English clergyman/chemist credited with discovering oxygen.

## 72. [-] dynhd/dream · triviaqa__sfq_13031 · 一致

- **问题**：Who was British Prime Minister at the end of the Second World War?
- **参考答案**：Clement Attlee；Premiership of Clement Attlee；1st Earl Attlee；Clement Richard Attlee, 1st Earl Attlee；Attlee；Clement Attlee；Clement Richard Attlee；C.R. Attlee；Clement Richard Atlee；Clement Richard Attlee, 1st Earl Attlee of Walthamstow, Viscount Prestwood；C. R. Attlee；Clem Atlee；Clem Attlee；Clement Attlee, 1st Earl Attlee；Clement Atlee；Sir Clement Richard Attlee 1st Earl Attlee；Clement R. Attlee
- **模型回答**：Winston Churchill
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Winston Churchill was not Prime Minister at the end of WWII; Clement Attlee became PM after the July 1945 election, which the references confirm.

## 73. [-] dynhd/dream · triviaqa__sfq_23994 · 一致

- **问题**：Who wrote the 1911 opera ‘Der Rosenkavalier’?
- **参考答案**：Richard Strauss；Strauss, Richard；Richard Strauss；Richard Georg Strauss；Ricardo Strauss
- **模型回答**：Richard Strauss
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Richard Strauss' directly matches multiple reference answers and correctly identifies the composer of Der Rosenkavalier.

## 74. [-] dynhd/dream · triviaqa__sfq_5218 · 一致

- **问题**：What is the US equivalent of the British Army's SAS?
- **参考答案**：Delta Force；Funny Platoon；1st Special Forces Operational Detachment-Delta (1st SFOD-D)；United States Army 1st Special Forces Operational Detachment Delta；Delta Forces；Combat Application Group；Combat Applications Group；1st SFOD；Delta force；SFOD-D；1st SFOD-D；Army Compartmented Elements；Delta Force；1st Special Forces Operational Detachment；1st Special Forces Operational Detachment - Delta；1st Special Forces Operational Detachment-Delta
- **模型回答**：Delta Force
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：Delta Force is explicitly listed as a valid reference answer and is the well-known US equivalent of the British SAS.

## 75. [-] dynhd/dream · triviaqa__wh_3277 · 一致

- **问题**：What invention by a Mr Schick in 1931 might be said to have changed the face of man ?
- **参考答案**：ELECTRIC RAZOR；Electric shaver；Disposable blades；ELECTRIC RAZOR；Razor；Disposable razor；Electric razor；Electric dry shaver；Razor cut；Razor blades；Electric razors；Beard shaver；Razor blade；Razors；Razor Cut
- **模型回答**：electric shaver
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'electric shaver' matches the reference answer 'Electric shaver' (differing only in capitalization) and correctly identifies Jacob Schick's 1931 invention.

## 76. [-] dynhd/dream · triviaqa__wh_4199 · 一致

- **问题**：What is Marge Simpson's maiden name ?
- **参考答案**：BOUVIER；Augustus Jules Bouvier；AUGUSTUS JULES BOUVIER (1837-81)；A. Bouvier；BOUVIER
- **模型回答**：Sson
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Marge Simpson's maiden name is Bouvier, not Sson.

## 77. [-] dynhd/dream · triviaqa__wh_679 · 一致

- **问题**：Sharing his surname with a biblical character, which footballer scored the deciding goal in the 1967 FA Cup Final?
- **参考答案**：FRANK SAUL；Frank Saul (disambiguation)；Frank Saul；FRANK SAUL
- **模型回答**：David Best
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'David Best' does not match any of the reference answers ('Frank Saul') and is not a valid answer to the question.

## 78. [-] dynhd/llada · hotpotqa__5a72f74a55429901807daf59 · 一致

- **问题**：Which American comedian born on March 21, 1962, appeared in the movie "Sleepless in Seattle?"
- **参考答案**：Rosie O'Donnell
- **模型回答**：Jim Carrey
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Jim Carrey was not born on March 21, 1962, and did not appear in 'Sleepless in Seattle.' The correct answer is Rosie O'Donnell.

## 79. [-] dynhd/llada · hotpotqa__5a796bfd55429970f5fffeac · 一致

- **问题**：What adorns the archaeological artefact excavated by Thomas Bateman on 3 May 1848?
- **参考答案**：A simple iron boar crest
- **模型回答**：The archaeological artefact excavated by Thomas Bateman on 3 May 1848 is the Sutton Hoo Burial. The Sutton Hoo Burial is adorned with a variety of artifacts, including the famous Sutton Hoo helmet, gold torcs, and other valuable items from the Anglo-Saxon period.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer incorrectly identifies the artefact as the Sutton Hoo Burial and lists unrelated items. Thomas Bateman excavated the Benty Grange burial on 3 May 1848, and the reference answer states the artefact is adorned with a simple iron boar crest. The proposed answer contradicts the reference and contains material factual errors.

## 80. [-] dynhd/llada · hotpotqa__5a7b493855429931da12ca58 · 一致

- **问题**：The Good Dinosaur features the voice of what Canadian-born New Zealand actress?
- **参考答案**：Anna Helene Paquin
- **模型回答**：Anna Bell.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The correct answer is Anna Helene Paquin, who voiced in The Good Dinosaur. 'Anna Bell' is a different name and does not match any valid reference answer.

## 81. [-] dynhd/llada · hotpotqa__5a7c646e55429907fabeef7c · 一致

- **问题**：Aerodynamik is a Kraftwerk song on an album recorded for what anniversity of the Tour de France bicycle race?
- **参考答案**：100th
- **模型回答**：Aerodynamik is a Kraftwerk song on an album recorded for the 50th anniversary of the Tour de France bicycle race.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer states the 50th anniversary, but the reference answer is the 100th anniversary.

## 82. [-] dynhd/llada · hotpotqa__5a881ea055429938390d3ef3 · 一致

- **问题**：Arabella Chapman graduated from which school that was opened as the Albany Free Academy?
- **参考答案**：Albany High School
- **模型回答**：Arabella Chapman graduated from the Albany Free Academy.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names the school by its original name (Albany Free Academy) rather than the valid reference answer, Albany High School.

## 83. [-] dynhd/llada · hotpotqa__5a8835245542994846c1ce27 · 一致

- **问题**：Do Tropical Fish Hobbyist and Curve cover the same topic?
- **参考答案**：no
- **模型回答**：No, Tropical Fish Hobbyist and Curve do not cover the same topic. Tropical Fish Hobbyist is a magazine about tropical fish, while Curve is a fashion magazine.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer states 'No' which matches the reference answer, and the supporting details about each magazine's topic are factually accurate and support the conclusion.

## 84. [-] dynhd/llada · hotpotqa__5a90b4fe55429916514e7525 · 一致

- **问题**：How many films did the star of Tum Milo Toh Sahi appear in?
- **参考答案**：110
- **模型回答**：The star of Tum Milo Toh Sahi appeared in 10 films.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Proposed answer (10) contradicts the reference answer (110).

## 85. [-] dynhd/llada · hotpotqa__5ab8397155429919ba4e2272 · 一致

- **问题**：What was the event where Jacob Minah had his personal best also known as?
- **参考答案**：XXIV Summer Universiade
- **模型回答**：The event where Jacob Minah had his personal best is also known as the Boston Marathon.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer contradicts the reference answers; it names the Boston Marathon instead of the XXIV Summer Universiade.

## 86. [-] dynhd/llada · hotpotqa__5ab9631a55429970cfb8eaad · 一致

- **问题**：Who made a hip-hop album with guest appearances from Justice, Lotek and Necro and also wrote semi-autobiographical crime books?
- **参考答案**：Mark "Chopper" Read
- **模型回答**：Ice-T.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The correct answer is Mark "Chopper" Read, an Australian criminal and author who released the hip-hop album 'Interview with a Madman' featuring those guests and wrote semi-autobiographical crime books. Ice-T does not match these details.

## 87. [-] dynhd/llada · hotpotqa__5ab9668c55429970cfb8eaba · 一致

- **问题**：What major city is John Bice Memorial Oval located within?
- **参考答案**：City of Onkaparinga
- **模型回答**：John Bice Memorial Oval is located in Melbourne, Australia.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer states Melbourne, which contradicts the reference answer City of Onkaparinga.

## 88. [-] dynhd/llada · hotpotqa__5aba9e235542994dbf019984 · 一致

- **问题**：Are both Weberocereus and Conospermum part of the same genus?
- **参考答案**：no
- **模型回答**：Yes, both Weberocereus and Conospermum are part of the genus Cactaceae.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer says 'Yes', which contradicts the reference answer 'no'. Weberocereus and Conospermum are different genera (in different families), and Cactaceae is a family, not a genus.

## 89. [-] dynhd/llada · hotpotqa__5ac372195542995ef918c194 · 一致

- **问题**：Which major regional shopping centre in the western suburb of Indooroopilly in the City of Brisbane, Queensland, Australia is served by TransLink bus routes?
- **参考答案**：Indooroopilly Shopping Centre
- **模型回答**：Indooroopilly Shopping Centre
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer exactly matches the reference answer.

## 90. [-] dynhd/llada · hotpotqa__5adcf3e35542994ed6169c3a · 一致

- **问题**：Dean Mills Reservoir is on the slopes of the hill located in what town?
- **参考答案**：Rivington Moor
- **模型回答**：Dean Mills Reservoir is on the slopes of the hill located in the town of Dean Mills.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer says the town is Dean Mills, which contradicts the valid reference answer Rivington Moor.

## 91. [-] dynhd/llada · hotpotqa__5ade0a275542997545bbbe2d · 一致

- **问题**：Where is the American hip hop group, that released the song "RedEye to Paris", from?
- **参考答案**：Flatbush section of Brooklyn, New York City
- **模型回答**：Chicago, Illinois
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer contradicts the reference answer; the group is from the Flatbush section of Brooklyn, New York City, not Chicago, Illinois.

## 92. [-] dynhd/llada · hotpotqa__5ade8bd955429975fa854f04 · 一致

- **问题**：What is the name of the genocidal mass slaughter of Tutsi Rwanda, in which Cyprian and Daphrose Rugamba were assassinated?
- **参考答案**：Rwandan genocide
- **模型回答**：The genocidal mass slaughter of Tutsi Rwanda in which Cyprian and Daphrose Rugamba were assassinated is known as the Rwandan Genocide.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer names the event as the Rwandan Genocide, which matches the reference answer semantically.

## 93. [-] dynhd/llada · hotpotqa__5ae088525542993d6555eba1 · 一致

- **问题**：Are Stan Lee and Mark Helprin both comic book writers?
- **参考答案**：no
- **模型回答**：Yes, both Stan Lee and Mark Helprin are comic book writers. Stan Lee is a renowned comic book writer, editor, and publisher, while Mark Helprin is a comic book writer, artist, and editor, primarily working for Marvel Comics. Both have made significant contributions to the comic book industry.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer claims both are comic book writers and specifically states Mark Helprin worked for Marvel Comics as a comic book writer, artist, and editor. This contradicts the reference answer 'no.' Mark Helprin is a novelist and screenwriter, not a comic book writer, so the answer contains a material factual error.

## 94. [-] dynhd/llada · hotpotqa__5ae600325542992663a4f237 · 一致

- **问题**：What type of diary did one of the founders of the John Bishop Memorial Hospital in Srinagar write?
- **参考答案**：a travel diary
- **模型回答**：One of the founders of the John Bishop Memorial Hospital in Srinagar, John Bishop, wrote a personal diary.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer states the founder wrote a 'personal diary', but the reference answer specifies 'a travel diary'. These are different types of diaries and are not semantically equivalent.

## 95. [-] dynhd/llada · triviaqa__bb_1161 · 一致

- **问题**：Who is the the voice of cartoon character Jack Kahuna Laguna in a special episode of Spongebob Squarepants?
- **参考答案**：Johnny Depp；Johnny deep；Johnny Dep；Caliber (film)；The Affected Provincial's Companion；Lori Anne Allison；Caliber (2014 film)；Affected Provincial's Companion (film)；List of Johnny Depp awards；Fierce Invalids Home from Hot Climates (film)；The Vault (2015 film)；John Depp；Depp, Johnny；The Vault (film)；Johnny Depp:List of awards & nominations；Lily-Rose Melody Depp；Johny Depp；Johhny Depp；Mortimer Wintergreen；List of Johnny Depp awards and nominations；Depp；Johnny Depp；John Christopher %22Johnny%22 Depp II；Inamorata (film)；Johnny Deep；Jonny Depp；Mortimer Wintergreen (2015 film)；John Christopher Depp II；Affected Provincial's Companion；Oprah Noodlemantra；John Christopher Depp；Johnny depp；Mortimer Wintergreen (film)；List of Johnny Depp's awards and nominations
- **模型回答**：Tom Kenny.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The reference answers identify the voice as Johnny Depp; Tom Kenny voices Spongebob, not Jack Kahuna Laguna.

## 96. [-] dynhd/llada · triviaqa__bb_2727 · 一致

- **问题**：American Jim Yong Kim was appointed head of which international organization in April 2012?
- **参考答案**：World Bank；World Bank Publications；Criticism of the World Bank；Clean Air Initiative；World Bank；World Bank Carbon Finance Unit；World bank
- **模型回答**：World Bank
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'World Bank' directly answers the question and matches multiple valid reference answers.

## 97. [-] dynhd/llada · triviaqa__bb_5364 · 一致

- **问题**：What 'seasonal-mood' name was given to the western social phenomenon of mid-1967, sparked by the vast gathering of young people in Haight-Ashbury, San Francisco?
- **参考答案**：The Summer of Love；Summer of love；The summer of love；Summer Of Love；Summer of Love；The Summer of Love
- **模型回答**：The 'seasonal-mood' name given to the western social phenomenon of mid-1967, sparked by the vast gathering of young people in Haight-Ashbury, San Francisco, is "Summer of Love."
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer "Summer of Love" is semantically equivalent to the reference answers and correctly answers the question.

## 98. [-] dynhd/llada · triviaqa__bt_3007 · 一致

- **问题**：Who wrote the epic 1869 novel War and Peace
- **参考答案**：Leo Tolstoy；Lyof Nikolaivitch Tolstoi；Tolstoy；Leo Nikolaievich Tolstoy；Lev Nikolaïevitch Tolstoï；Lev Nikolajevič Tolstoj；Count Lev Tolstoy；Lev Nikolajevic Tolstoj；Lev Nikolaevich Tolstoy；Leo tolstoi；Tolstoi；LN Tolstoi；Leo N. Tolstoy；Buried Alive (play)；Lev N. Tolstoi；Lev Tolstoi；Voice of Thunder (Lincoln)；Lev Tolstoï；Leo N. Tolstoi；Tolstoy, Lev Nikolayevich；Lev N. Tolstoï；LN Tolstoy；Count Lev Nikolaevich Tolstoi；Lev Nikolaevic Tolstoj；Leo N. Tolstoï；Толстой；Lev N. Tolstoy；Lev Tolstoy；Leo Tolstoï；Count Lev N. Tolstoy；Leo Tolstoy's religious beliefs；Leo tolstoy；Count Leo Tolstoy；León Tolstói；Lev Nikolayevich Tolstoy；Лев Никола́евич Толсто́й；Leo Tolstoy；Leo Nikolayevich Tolstoy；Leo Nikoleyevich Tolstoy；Count Leo Tolstoï；Count Leo N. Tolstoy；Leon Tolstoi；Leo Nikolayevitch Tolstoy；Count Leo Tolstoi；Lyof Tolstoy；Count Leo N. Tolstoi；Count Leo N. Tolstoï；Lev Tolstói；Lev Nikolaevič Tolstoj；Leo Tolstoi；Léon Tolstoï；Лев Николаевич Толстой；Leon Tolstoy；Lev Tolstoj；Leo, Count Tolstoy；Tolstoy, Leo Nikolayevich；Lev Nikolaievitch Tolstoi
- **模型回答**：Leo Tolstoy
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Leo Tolstoy' matches the primary reference answer exactly and is semantically equivalent to the other valid reference answers.

## 99. [-] dynhd/llada · triviaqa__bt_4324 · 一致

- **问题**：What is the state capital of Alabama
- **参考答案**：Montgomery；Montgomerie；Montgomery (disambiguation)；Montgomery
- **模型回答**：The state capital of Alabama is Montgomery.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer states Montgomery, which matches the reference answers and correctly answers the question.

## 100. [-] dynhd/llada · triviaqa__dpql_2073 · 一致

- **问题**：Which constellation has, uniquely, in Rigel and Betelgeuse, two of the ten brightest stars?
- **参考答案**：Orion；Orion (music)；Orion (song)；Orion Class Spaceship；Orions (disambiguation)；Orion-class spaceship；Orion (system)；ORION；Orions；Orion；Orion (disambiguation)
- **模型回答**：The constellation is Orion.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer identifies Orion, which matches the reference answers and is factually correct since Rigel and Betelgeuse are both in Orion.

## 101. [-] dynhd/llada · triviaqa__dpql_4841 · 一致

- **问题**：Which northern Duchies were questionable until the 1860s?
- **参考答案**：Schleswig-Holstein；Lütt-Witt Moor；Sleswick-Holsatia；Slesvig-Holsten；Schleswig-Holstein；Sleswick-Holstein；Schleswig–Holstein；Slesvig-Holstein；Schleswig-Holstein (Germany)；Schleswig-Holstein, Germany；Sleswig-Holsteen；Schleswig Holstein
- **模型回答**：The northern Duchies that were questionable until the 1860s include the Duchy of Luxembourg, the Duchy of Luxembourg, and the Duchy of Luxembourg. These duchies were subject to various political and territorial disputes, leading to their status being uncertain for extended periods.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names Luxembourg, which contradicts all reference answers (variants of Schleswig-Holstein) and is factually wrong for the northern Duchies in question.

## 102. [-] dynhd/llada · triviaqa__jp_3637 · 一致

- **问题**：What is either a bay in the Indian ocean or a subspecies of tiger?
- **参考答案**：Bengal；Bengal (India)；Kingdom of Bengal；Bengal, India；Bôngo；Bôngodesh；বঙ্গদেশ；Bongodesh；Greater Bengal；Etymology of Bengal；Bengal；বঙ্গ
- **模型回答**：tiger Bay
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'tiger Bay' does not match any reference answer. The correct answer is 'Bengal', which satisfies both conditions: Bay of Bengal (a bay in the Indian Ocean) and Bengal tiger (a subspecies of tiger). 'Tiger Bay' is neither a bay in the Indian Ocean nor a tiger subspecies.

## 103. [-] dynhd/llada · triviaqa__odql_10031 · 一致

- **问题**：What was the first name of Mr. Ferrari, the founder of the car manufacturing company?
- **参考答案**：ENZO；Enzo；ENZO；Enzo (disambiguation)
- **模型回答**：Enzo
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Enzo' matches the reference answers 'ENZO' and 'Enzo', which are semantically equivalent and correctly answer the question.

## 104. [-] dynhd/llada · triviaqa__odql_12408 · 一致

- **问题**：Who is the current occupant of Dorneywood in Buckinghamshire?
- **参考答案**：George Osborne；Gideon Osborne；Chancellor George Osborne；George Osbourne；George osborne；George Gideon Oliver Osborne；George Osborne MP；Gideon George Oliver Osborne；George Osborne
- **模型回答**：The current occupant of Dorneywood in Buckinghamshire is Prince Charles III.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names Prince Charles III, which contradicts the reference answers identifying George Osborne.

## 105. [-] dynhd/llada · triviaqa__odql_3310 · 一致

- **问题**：What is the name of the tropical shrub from which the reddish dye is extracted to colourhair?
- **参考答案**：HENNA；Mylaanchi；HENNA；Hina (body art)；Henna；Camphire；Mailanchi；Lawsonia alba；Mylanji；Jamaica mignonette；Lawsonia (plant genus)；Lawsonia inermis；Black henna；Mignonette tree；Lawsonia (plant)；Mylanchi
- **模型回答**：The madder root.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names madder root, which contradicts the reference answers that identify the tropical shrub as henna (Lawsonia inermis) and its aliases.

## 106. [-] dynhd/llada · triviaqa__odql_351 · 一致

- **问题**：Which spy was sentenced to 42 years in prison in 1961, but escaped from Wormwood Scrubs in 1966?
- **参考答案**：GEORGE BLAKE；GEORGE BLAKE；George Blake；Max de Vries
- **模型回答**：David Chapman.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'David Chapman' does not match any valid reference answer (George Blake or Max de Vries).

## 107. [-] dynhd/llada · triviaqa__odql_8118 · 一致

- **问题**：In World War I, the British soldiers were nicknamed 'Tommies', what name was given to French soldiers?
- **参考答案**：'POILU'；Poilu；'POILU'；Poilus
- **模型回答**：Frenchies.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Frenchies' does not match the correct nickname 'Poilu' (or 'Poilus') for French soldiers in WWI.

## 108. [-] dynhd/llada · triviaqa__qb_2148 · 一致

- **问题**：Louis Reard created which two-piece item of clothing in 1946?
- **参考答案**：Bikini；Bikinis；Bikini-tanned；Men's bikini；Unikini；Bikini (underwear)；Bikini-tanning；Bikini tops；Bikini tanned；Bikini-tan；Bikinitanning；Bikinitan；Pale breast；Bikini；Pale breasts；Bikini top；👙；Bikini tanning；Vkini；Bikini-tans；Two-piece swimsuit；Bikinitans；Bikini bottom；Bikinitanned；Bikini tans
- **模型回答**：Le Smoking Suit
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Le Smoking Suit' does not match any reference answer. Louis Reard created the bikini in 1946, not a smoking suit.

## 109. [-] dynhd/llada · triviaqa__qb_3878 · 一致

- **问题**：Who wrote the political treatise ‘The Prince’, published in 1532?
- **参考答案**：Niccolo Machiavelli；Niccolò Macchiavelli；Nicole Machiavelli；Machavelli；Nioccolo Machiavelli；Machavellian；Macchiavelian；Nicolo Machiavelli；Machiavilli；Nicoli Machiavelli；Fawce；Marietta Corsini；Machiaveli；Niccolo Macchiavelli；Niccolo di Bernardo dei Machiavelli；Niccolò Machiavelli；Macchiavelianism；Niccol Machiavelli；Machiavellian test；Macavelli；Machiavellia；Niccolo' Macchiavelli；Machiavelians；Niccol%5CxC3%5CxB2 Machiavelli；Nicollo Machiavelli；Machievel；Machiavelian；Machevelli；Machiavelli；Niccolò di Bernardo dei Machiavelli；Nicholas Machiavelli；Macchiavelli；Macchiaveli；Makiavelo；Machiavelli's；Nicholas Machiavell；Machiavelli, Niccolò；Machaevelli；Niccolo Machiavelli；Machiavelliism；Machievelli；Nicolò Machiavelli；Niccoló Macchiavelli；Nicoló Machiavelli；Macavhelli；Machiavelli, Niccolo
- **模型回答**：Niccolò Machiavelli
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer exactly matches a valid reference answer and correctly identifies the author of 'The Prince'.

## 110. [-] dynhd/llada · triviaqa__qg_2404 · 一致

- **问题**：Name the book and the author: 'The Time Traveler (for so it will be convenient to speak of him) was expounding a recondite matter to us.'
- **参考答案**：The Time Machine, by H.G. Wells；The Time Machine, by H.G. Wells
- **模型回答**：The Time Machine by H.G. Wells.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer correctly identifies the book as 'The Time Machine' and the author as H.G. Wells, which matches the reference answers.

## 111. [-] dynhd/llada · triviaqa__qg_548 · 一致

- **问题**：According to Samuel Beckett, who are Vladimir and Estragon waiting for?
- **参考答案**：Godot；Godot；Godot (disambiguation)
- **模型回答**：Vladimir and Estragon are waiting for Godot.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer states that Vladimir and Estragon are waiting for Godot, which directly matches the reference answers.

## 112. [-] dynhd/llada · triviaqa__qw_10077 · 一致

- **问题**：Between 1783 and 1865, Englishmen William Wilberforce, Sir Cecil Wray and Dr Beilby Porteus, Africans Olaudah Equiano and Ignatius Sancho and, in the USA, William Lloyd Garrison, John Greenleaf Whittier, Harriet Beecher Stowe, Frederick Douglass, Charles Henry Langston and John Mercer Langston were leading figures in which movement?
- **参考答案**：Abolition of the slave trade；Abolitionism.；Critic of the slave trade；Emancipation of Slaves；White abolitionists；Abolition of slavery；Anti slavery movement；Antislavery movement；Emancipation of slaves；Abolutionism；Abolitionistic；Abolition (slavery)；Abolitionism in France；Anti-abolitionism；Abolition of Slavery；Abolitionism (slavery)；Movement to abolish slavery；Abolitionst；Abolishing slavery；White Abolitionists；Abolitionists；Opponent of slavery；Abolitionist movement；Slavery abolition；Anti-slavery；Emancipation Of Slaves；Abolition Of Slavery；Abolitionism；Slave emancipation；Opposition to slavery；Antislavery；Abolitionist (slavery)；Abolitionist；Abolitionist Movement；Emancipationist；Abolition of the slave trade；Anti-slavery movement
- **模型回答**：Abolitionism
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：Abolitionism is explicitly listed as a valid reference answer and directly answers the question.

## 113. [-] dynhd/llada · triviaqa__qw_352 · 一致

- **问题**：The pericardium is part of which organ?
- **参考答案**：Heart；Four chambered heart；Atria of the heart；Cardiac chambers；Left heart；Sternocostal surface of heart；Heart；Cardiogenic；Cardiac chamber；❤️；Heart chambers；Heart (anatomy)；Sternocostal surface；Base of heart；Anterior surface of the heart；Base of the heart；Facies cordis；Heart in literature；The heart；Systemic heart；Heart Symbolism and Metaphor；Heart (symbolism)；Cardiac；Facies diaphragmatica cordis；The human heart；Basis cordis；Chambers of the heart；Heart chamber；Heart (Symbolism and Metaphor)；Left side of the heart；Right heart；Heart (biology)；Diaphragmatic surface of heart；Dorsal tube；Apex cordis；Heart (metaphor)；Facies anterior cordis；Human heart；Heart (food)；Anterior wall of heart；Apex of heart；Right side of the heart；Heart (organ)；Atlas of Human Cardiac Anatomy；Facies sternocostalis cordis
- **模型回答**：The pericardium is part of the heart.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer directly states the pericardium is part of the heart, which matches the primary reference answer and is factually accurate.

## 114. [-] dynhd/llada · triviaqa__qw_3850 · 一致

- **问题**：Where was the final of the 1999 Rugby World Cup held?
- **参考答案**：Wales；Welsh nation；Climate of Wales；Autonomous Province of Wales；Cymru / wales；Cyrmu；Wales；WALES；Rain in Wales；Welsh Nation；Welsh Peninsula；Wales, UK；Etymology of Wales；Cymru；Wales, United Kingdom；Pays de Galles；Communications in Wales；The Principality of Wales；West of the Rhymney；Wales, U.K.；Cymru am byth；Gymru；Cymru / Wales；Welsh mountains；CYMRU
- **模型回答**：The final of the 1999 Rugby World Cup was held in Paris, France.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The answer contradicts all reference answers, which consistently identify Wales as the location; Paris, France is factually wrong.

## 115. [-] dynhd/llada · triviaqa__qz_4151 · 一致

- **问题**：What was the name of the ferry that capsized after leaving Zeebrugge in 1987
- **参考答案**：The Herald of free Enterprise；M/S Herald of Free Enterprise；Zeebrugge ferry disaster；MS Herald of Free Enterprise；Herald of free enterprise；IMO 7820485；Flushing Range；The Herald of Free Enterprise；Herald of Free Enterprise；The Herald of free Enterprise；Zeebrugge Disaster
- **模型回答**：SS Northern Star
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names a different vessel and contradicts the reference answers, which identify the ferry as the Herald of Free Enterprise.

## 116. [-] dynhd/llada · triviaqa__sfq_11477 · 一致

- **问题**：Who is the only Scotsman to have been European Footballer of the Year (now called the Ballon d'Or)?
- **参考答案**：Denis Law；Denis Law
- **模型回答**：Alex Ferguson.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Denis Law is the only Scotsman to win the European Footballer of the Year/Ballon d'Or (1964); Alex Ferguson never won this award as a player.

## 117. [-] dynhd/llada · triviaqa__sfq_14798 · 一致

- **问题**：For what does the G stand in the navigational aid, usually known as a `GPS'?
- **参考答案**：Global；Earthwide；Global (album)；Global；Globals；Global (disambiguation)
- **模型回答**：Global Positioning System
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The G in GPS stands for 'Global,' which matches the reference answers. The proposed answer 'Global Positioning System' correctly expands the acronym and identifies the G as Global.

## 118. [-] dynhd/llada · triviaqa__sfq_17048 · 一致

- **问题**：Who was the only British medal winner at the 2010 Winter Olympics?
- **参考答案**：AMY WILLIAMS；AMY WILLIAMS；Amy Williams
- **模型回答**：Jenny Jones.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Jenny Jones' contradicts all reference answers, which identify Amy Williams as the only British medal winner at the 2010 Winter Olympics.

## 119. [-] dynhd/llada · triviaqa__sfq_18437 · 一致

- **问题**：Who has presented BBC TV programmes called his 'Toy Stories' and `Man Lab'?
- **参考答案**：James May；Captain Slow；James May；James Daniel May；James may；Captain slow
- **模型回答**：Richard Hammond
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The reference answers identify James May (also known as Captain Slow); Richard Hammond is a different presenter and does not match any valid reference.

## 120. [-] dynhd/llada · triviaqa__sfq_18543 · 一致

- **问题**：Who was the first football nation to win the World Cup outside their own continent?
- **参考答案**：BRAZIL；Brazil；BRAZIL；Etymology of Brazil；Federal Republic of Brazil；Brasil；Barzil；Federative Republic of Brazil；Brazil (country)；Brassil；Republic of Brazil；Brésil；Brzil；Brazilian Federative Republic；Republica Federativa do Brasil；Bresil；Brazilian Republic；ISO 3166-1:BR；República Federativa do Brasil；Brazilo
- **模型回答**：Argentina
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Argentina' contradicts the reference answers, which all indicate Brazil.

## 121. [-] dynhd/llada · triviaqa__sfq_3248 · 一致

- **问题**：Which cartoon character created by Al Capp lives in Dog Patch?
- **参考答案**：L'ABNER；L'ABNER
- **模型回答**：Popeye
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer Popeye was created by E.C. Segar, not Al Capp, and does not live in Dogpatch. The correct answer is Li'l Abner.

## 122. [-] dynhd/llada · triviaqa__sfq_3503 · 一致

- **问题**：Which star in the constellation of Ophiuchus, is just under six light years away and the fifth closest star to Earth?
- **参考答案**：BARNARD'S STAR；Gliese 699；Munich 15040；Velox Barnardi；Barnard's Runaway Star；Proxima Ophiuchi；V2500 Ophiuchi；Barnards Star；Barnard Star；Barnard's star；BARNARD'S STAR；Barnard's Star
- **模型回答**：Proxima Centauri
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Proxima Centauri is the closest star to Earth, located in Centaurus, not Ophiuchus, and is about 4.2 light years away. The correct answer is Barnard's Star.

## 123. [-] dynhd/llada · triviaqa__sfq_5218 · 一致

- **问题**：What is the US equivalent of the British Army's SAS?
- **参考答案**：Delta Force；Funny Platoon；1st Special Forces Operational Detachment-Delta (1st SFOD-D)；United States Army 1st Special Forces Operational Detachment Delta；Delta Forces；Combat Application Group；Combat Applications Group；1st SFOD；Delta force；SFOD-D；1st SFOD-D；Army Compartmented Elements；Delta Force；1st Special Forces Operational Detachment；1st Special Forces Operational Detachment - Delta；1st Special Forces Operational Detachment-Delta
- **模型回答**：The US equivalent of the British Army's SAS is the Navy SEALs.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer states Navy SEALs, which contradicts the reference answers. The US equivalent of the British SAS is Delta Force (1st SFOD-D), not the Navy SEALs.

## 124. [-] dynhd/llada · triviaqa__sfq_7104 · 一致

- **问题**：Silkworms feed on the leaves of which tree?
- **参考答案**：Mulberry；Mulberry tea；Mulberry trees；Mulberries；Mullberry；Mulbery；Moriculture；Mulberry；Morus (plant)；Mulberry tree；Mulberry Tree
- **模型回答**：Silkworms feed on the leaves of silk trees.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer states 'silk trees,' which is not a valid alias or paraphrase for mulberry trees and contradicts the reference answers.

## 125. [-] dynhd/llada · triviaqa__tc_691 · 一致

- **问题**：Who is the most successful UK solo artist in the USA?
- **参考答案**：Elton John；Sir Elton；Rockaday Johnny；Elthon John；Eltonjohn；List of Elton John awards；John, Elton；Reggie Dwight；Lord Choc Ice；Redget Buntovan；Elton John's discography；Elton john discography；Reginald K. Dwight；Elton John；Mrs. Elton John；Lady Choc Ice；Reg Kenneth Dwight；Renate Blauel；Reginald Kenneth Dwight；Ann Orson；Reg Dwight；Elton John Band；Reginald Dwight；Sir John Elton；Elton john；Elton John Discography；Reginald Kenneth；Elton Hercules John；Sir Elton Hercules John CBE；Elton H. John；Nancy Treadlight；Reginald kenneth dwight；Reginald dwight；Sir Elton John；Kenneth Dwight
- **模型回答**：Taylor Swift
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names Taylor Swift, an American artist, whereas all reference answers identify Elton John (or aliases thereof) as the most successful UK solo artist in the USA.

## 126. [-] main/dream · triviaqa__jp_2054__seed20261020 · 一致

- **问题**：Which newspaper did Peter Parker work for?
- **参考答案**：The Daily Bugle；DB (comics)；Daily Bugle；The DB；Daily Bugle: Civil War Edition；Front Line (comics)；The Daily Bugle；Daily Bugle Communications；Dexter Bennett
- **模型回答**：The Daily Bug
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer "The Daily Bug" is a truncation of "The Daily Bugle" (cut off mid-word), not a valid abbreviation or paraphrase. It does not match any of the acceptable reference answers semantically.

## 127. [-] main/dream · triviaqa__jp_927__seed20261020 · 一致

- **问题**：The Mossad is the intelligence agency of what country?
- **参考答案**：Israel；İsrail；ISRAEL；Israeli Republic；Isræl；Medinat Yisrael；מְדִינַת יִשְׂרָאֵל；Istrael；Israeli (nation)；ISO 3166-1:IL；Medinat Israel；Dawlat Isra'il；State of israel；Yisraél；Isra'il；Republic of Israel；دولة إسرائيل；Israel；Israël；Israelim；Medinat Yisra'el；ישראל；State of Israel；יִשְרָאֵל；מדינת ישראל；Dawlat Isrā'īl；Yisra'el；Yisrael；Israeli state；The state of Israel；Jewish Republic；Israil；Jewish Palestine；Etymology of Israel；Isreal；Yisroel；Israyl；Israel (nation)；Modern Israel；Israelian；Hebrew state；M'dinat Yisrael；Israe;；Izrael (state)；Isreael；Isreali；יִשְׂרָאֵל；Medīnat Yisrā'el；Yisroeil；Israel (country)
- **模型回答**：Israel
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Israel' is factually correct and matches multiple reference answers exactly.

## 128. [-] main/dream · triviaqa__odql_10031__seed20261020 · 一致

- **问题**：What was the first name of Mr. Ferrari, the founder of the car manufacturing company?
- **参考答案**：ENZO；Enzo；ENZO；Enzo (disambiguation)
- **模型回答**：Enzo
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Enzo' matches the valid reference answers and correctly answers the question.

## 129. [-] main/dream · triviaqa__odql_351__seed20261020 · 一致

- **问题**：Which spy was sentenced to 42 years in prison in 1961, but escaped from Wormwood Scrubs in 1966?
- **参考答案**：GEORGE BLAKE；GEORGE BLAKE；George Blake；Max de Vries
- **模型回答**：Kim Philby
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Kim Philby was not sentenced to 42 years in 1961 or imprisoned in Wormwood Scrubs; he defected to the USSR in 1963. The correct answer is George Blake.

## 130. [-] main/dream · triviaqa__odql_6828__seed20261020 · 一致

- **问题**：Aboard which ship did Japan sign the surrender at the end of World War II?
- **参考答案**：U.S.S. MISSOURI；U.S.S. Missouri；U.S.S. MISSOURI；Battleship Missouri；Uss Missouri；USS Missouri；Uss missouri
- **模型回答**：USS Missouri
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer "USS Missouri" matches one of the accepted reference answers and correctly identifies the ship where Japan signed the surrender.

## 131. [-] main/dream · triviaqa__qb_2148__seed20261020 · 一致

- **问题**：Louis Reard created which two-piece item of clothing in 1946?
- **参考答案**：Bikini；Bikinis；Bikini-tanned；Men's bikini；Unikini；Bikini (underwear)；Bikini-tanning；Bikini tops；Bikini tanned；Bikini-tan；Bikinitanning；Bikinitan；Pale breast；Bikini；Pale breasts；Bikini top；👙；Bikini tanning；Vkini；Bikini-tans；Two-piece swimsuit；Bikinitans；Bikini bottom；Bikinitanned；Bikini tans
- **模型回答**：Theini
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**："Theini" does not match any valid reference answer and is not a recognized name for the two-piece swimsuit created by Louis Reard.

## 132. [-] main/dream · triviaqa__qb_5532__seed20261020 · 一致

- **问题**：What is the Japanese art of paper-folding called?
- **参考答案**：Origami；Oragami；Paper folding art；Paper Folding；Paper-folding；Paperfolding；List of origami societies；Origami-bonsai；Origaming；折紙；Origami；Origamy；Paper folding；折り紙
- **模型回答**：Origami
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Origami' matches the first reference answer exactly and is the correct term for the Japanese art of paper-folding.

## 133. [-] main/dream · triviaqa__qb_5808__seed20261020 · 一致

- **问题**：Vendredi is French for which day of the week?
- **参考答案**：Friday；Parasceve；Prosábbaton；Frigg's Day；TGIFF；Friday；Thank Goodness It's Friday；Frigg's day；Prosabbaton；Friday the 12th；Fryeeday
- **模型回答**：Friday
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：Vendredi is French for Friday, which matches the reference answer.

## 134. [-] main/dream · triviaqa__qf_1632__seed20261020 · 一致

- **问题**：The Guinness Book of Records was first published in what year?
- **参考答案**：1955；1955；one thousand, nine hundred and fifty-five
- **模型回答**：1955
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches the reference answer 1955.

## 135. [-] main/dream · triviaqa__qg_3452__seed20261020 · 一致

- **问题**：Named for its chairman, The Warren Commission published its final report on Sept 27, 1965. What event was it seated to investigate?
- **参考答案**：JFK Assassination；Shooting of John F. Kennedy；Dealey Plaza shootings；President Kennedy's assassination；J.F.K assassination；JFK assassination；Assassination of JFK；Assassination of President Kennedy；Assassination of John F. Kennedy；Kennedy assassination；Death of JFK；November 22, 1963；Faye Chism；Kennedy assasination；Assassination of John Kennedy；Shooting of JFK；Kennedy's assassination；The Kennedy assassination；JFK Assassination；Assassination of Kennedy；Assassination of United States President John F. Kennedy；John F kennedy assassination；John F. Kennedy assassination；John F. Kennedy's assassination；Assassination of john f. kennedy；John Fitzgerald Kennedy's assassination；Killing of JFK；John F. Kennedy Assassination；Assassanation of John F. Kennedy；Kennedy Assassination；JFK shooting；Kennedy assassination theories；The Assassination of JFK；Back and to the left；Jfk assassination；John F.Kennedy assassination；Murder of JFK；Assassination of John Fitzgerald Kennedy；John F Kennedy assassination；Assassination Information Bureau；Murder of John F. Kennedy；John f. kennedy assassination；JFK blown away；Death of John F. Kennedy；JFK's Assassination；Kennedy Assasination；Assassination of john f kennedy；J.F.K. Assassination；JFK murder；John F. Kennedy assassination/Archive 4；Emmett Hudson；Assassination of jfk；JFK assasination；Assassination of John F Kennedy；John f kennedy assassination；Clark Panel；Assassination of President John F. Kennedy
- **模型回答**：theedy assassination
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The answer 'theedy assassination' does not match any reference answer or identify the JFK assassination; it appears to be an unrelated or erroneous term.

## 136. [-] main/dream · triviaqa__qw_10077__seed20261020 · 一致

- **问题**：Between 1783 and 1865, Englishmen William Wilberforce, Sir Cecil Wray and Dr Beilby Porteus, Africans Olaudah Equiano and Ignatius Sancho and, in the USA, William Lloyd Garrison, John Greenleaf Whittier, Harriet Beecher Stowe, Frederick Douglass, Charles Henry Langston and John Mercer Langston were leading figures in which movement?
- **参考答案**：Abolition of the slave trade；Abolitionism.；Critic of the slave trade；Emancipation of Slaves；White abolitionists；Abolition of slavery；Anti slavery movement；Antislavery movement；Emancipation of slaves；Abolutionism；Abolitionistic；Abolition (slavery)；Abolitionism in France；Anti-abolitionism；Abolition of Slavery；Abolitionism (slavery)；Movement to abolish slavery；Abolitionst；Abolishing slavery；White Abolitionists；Abolitionists；Opponent of slavery；Abolitionist movement；Slavery abolition；Anti-slavery；Emancipation Of Slaves；Abolition Of Slavery；Abolitionism；Slave emancipation；Opposition to slavery；Antislavery；Abolitionist (slavery)；Abolitionist；Abolitionist Movement；Emancipationist；Abolition of the slave trade；Anti-slavery movement
- **模型回答**：abolitionist movement
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'abolitionist movement' matches one of the reference answers exactly and correctly identifies the movement these historical figures were part of.

## 137. [-] main/dream · triviaqa__qw_11386__seed20261020 · 一致

- **问题**：What is the opposite side from starboard on a ship?
- **参考答案**：Port；Sea port；Seaport；Fishing port；Shipping port；Deep water port；Ice-free port；Ice free port；Deepwater port；Ports (disambiguation)；Sea ports；Port of discharge；Ferry port；Deepwater pier；Fishing Port；Fluvial port；Deep-water port；Warm-water port；Ice-free harbor；Sea-port；Warm water port；Ice free harbour；Port city；Ports；Seaports of Japan；Seaports；Ice-free harbour；Port town；Commercial port；Port
- **模型回答**：port
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'port' correctly identifies the left side of a ship, which is the opposite of starboard, and matches the primary reference answer.

## 138. [-] main/dream · triviaqa__qw_14469__seed20261020 · 一致

- **问题**："Complete the title of this James Bond film: ""From Russia With ... """
- **参考答案**：Love；Idealized love；Loveliest；Love；Loves；Prem (Hinduism)；Sacrificial love；True Love (The feeling)；Chemistry of love；Lovable；💑；Idealised love；Love interest；Loving relationship；Latin words for love；Lovingly；愛；Loveworthy；Lovelier
- **模型回答**：Love
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Love' matches the reference answer and correctly completes the James Bond film title 'From Russia With Love'.

## 139. [-] main/dream · triviaqa__qw_3850__seed20261020 · 一致

- **问题**：Where was the final of the 1999 Rugby World Cup held?
- **参考答案**：Wales；Welsh nation；Climate of Wales；Autonomous Province of Wales；Cymru / wales；Cyrmu；Wales；WALES；Rain in Wales；Welsh Nation；Welsh Peninsula；Wales, UK；Etymology of Wales；Cymru；Wales, United Kingdom；Pays de Galles；Communications in Wales；The Principality of Wales；West of the Rhymney；Wales, U.K.；Cymru am byth；Gymru；Cymru / Wales；Welsh mountains；CYMRU
- **模型回答**：New
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer "New" does not answer the question and contradicts all reference answers, which indicate Wales.

## 140. [-] main/dream · triviaqa__qw_3910__seed20261020 · 一致

- **问题**："""84 Charing Cross Road"" is a book based on 20 years of correspondence between which New York writer and Frank Doel, an antiquarian bookseller in London?"
- **参考答案**：Helene Hanff；Helene Hanff；Herman Knight
- **模型回答**：John James
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'John James' does not match any valid reference answer and is factually wrong; the writer was Helene Hanff.

## 141. [-] main/dream · triviaqa__qw_829__seed20261020 · 一致

- **问题**：Which German-born chemist split the uranium atom in 1939 and won the Nobel prize in 1944?
- **参考答案**：Otto Hahn；Otto Hahn；Hahn, Otto
- **模型回答**：Otto Hahn
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches the reference answers and correctly identifies Otto Hahn as the German-born chemist who won the 1944 Nobel Prize for his role in the discovery of nuclear fission.

## 142. [-] main/dream · triviaqa__qw_9664__seed20261020 · 一致

- **问题**：Under the Treaty of Breda (31 July 1667), negotiated to end the Second Anglo-Dutch War, the Dutch kept the colony of Suriname conquered from the English, and left the English with what area of land?
- **参考答案**：New Amsterdam；Fort Amsterdam (New Amsterdam)；Nieuv Amsterdam；New Orange；New Amsterdam
- **模型回答**：Bermuda
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Bermuda' contradicts the reference answers, which all identify New Amsterdam as the area left to the English.

## 143. [-] main/dream · triviaqa__qz_1111__seed20261020 · 一致

- **问题**：Which brand of beer does Homer Simpson drink regularly?
- **参考答案**：Duff；Duff；Duff (disambiguation)
- **模型回答**：Dud
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Dud' does not match any valid reference answer. The correct brand is 'Duff', not 'Dud'.

## 144. [-] main/dream · triviaqa__sfq_11095__seed20261020 · 一致

- **问题**：Which pop singer shot himself to death in 1990 whilst suffering from depression?
- **参考答案**：DEL SHANNON；DEL SHANNON；Berlee Records；Berlee records；Del Shannon；Del shannon
- **模型回答**：Davidain
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Davidain' does not match any valid reference answer (Del Shannon) and is factually incorrect.

## 145. [-] main/dream · triviaqa__sfq_11360__seed20261020 · 一致

- **问题**：What is the capital of the French region of Burgundy?
- **参考答案**：DIJON；Dijon；Dijonnaise；DIJON；Dijon, France
- **模型回答**：Lons
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The capital of Burgundy is Dijon; Lons is not the correct answer.

## 146. [-] main/dream · triviaqa__sfq_14547__seed20261020 · 一致

- **问题**：Which TV programme's 'experts' include Francis Prior and Phil Harding?
- **参考答案**：Time Team；Timeteam；The Time Team Big Dig；Time Team
- **模型回答**：TheI
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'TheI' is garbled, incomplete, and does not match any valid reference answer such as 'Time Team'.

## 147. [-] main/dream · triviaqa__sfq_14798__seed20261020 · 一致

- **问题**：For what does the G stand in the navigational aid, usually known as a `GPS'?
- **参考答案**：Global；Earthwide；Global (album)；Global；Globals；Global (disambiguation)
- **模型回答**：Global
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The G in GPS stands for 'Global' (Global Positioning System), which matches the reference answers.

## 148. [-] main/dream · triviaqa__sfq_15254__seed20261020 · 一致

- **问题**：Who was the star of the film comedies 'The Navigator' (1924) and 'The General' (1927)?
- **参考答案**：BUSTER KEATON；Buster Keeton；BUSTER KEATON；Eleanor Keaton；Buster keaton；Buster Keaton；Keatonesque；Buster Keaton's；Joseph Francis %22Buster%22 Keaton；Joseph Frank Keaton VI；Joseph Francis Keaton
- **模型回答**：Buster Keaton
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Buster Keaton' matches multiple reference answers exactly and correctly identifies the star of both films.

## 149. [-] main/dream · triviaqa__sfq_18543__seed20261020 · 一致

- **问题**：Who was the first football nation to win the World Cup outside their own continent?
- **参考答案**：BRAZIL；Brazil；BRAZIL；Etymology of Brazil；Federal Republic of Brazil；Brasil；Barzil；Federative Republic of Brazil；Brazil (country)；Brassil；Republic of Brazil；Brésil；Brzil；Brazilian Federative Republic；Republica Federativa do Brasil；Bresil；Brazilian Republic；ISO 3166-1:BR；República Federativa do Brasil；Brazilo
- **模型回答**：Brazil
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：Brazil won the 1958 World Cup in Sweden, becoming the first nation to win outside their home continent. The answer matches the reference answers.

## 150. [-] main/dream · triviaqa__tc_691__seed20261020 · 一致

- **问题**：Who is the most successful UK solo artist in the USA?
- **参考答案**：Elton John；Sir Elton；Rockaday Johnny；Elthon John；Eltonjohn；List of Elton John awards；John, Elton；Reggie Dwight；Lord Choc Ice；Redget Buntovan；Elton John's discography；Elton john discography；Reginald K. Dwight；Elton John；Mrs. Elton John；Lady Choc Ice；Reg Kenneth Dwight；Renate Blauel；Reginald Kenneth Dwight；Ann Orson；Reg Dwight；Elton John Band；Reginald Dwight；Sir John Elton；Elton john；Elton John Discography；Reginald Kenneth；Elton Hercules John；Sir Elton Hercules John CBE；Elton H. John；Nancy Treadlight；Reginald kenneth dwight；Reginald dwight；Sir Elton John；Kenneth Dwight
- **模型回答**：Adele
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Adele' contradicts the reference answers, which all identify Elton John as the most successful UK solo artist in the USA.

## 151. [-] main/dream · triviaqa__tc_886__seed20261020 · 一致

- **问题**：Which drink did The Spice Girls promote?
- **参考答案**：Pepsi；Pep.si；Pepsey；Pepsi Convoy；Pepsi Lime；Pepsi: summer Mix；Pepsi Si；Brad's drink；Cherry Pepsi；Pepsi Sí；Pepsi edge；Joy of Cola；Pepsi Summer mix；Pepsi tarik；Pepsi cino；Pepsi Holiday Spice；Pepsi Perfect；PepsiCola；Pepsi: Summer mix；Pepsi: summer mix；Pepsi Gold；Pepsi Samba；Pepsi Vanilla；Pepsi Avantage；Vanilla Pepsi；Pepsi cola；Pepsi Tarik；Pepsi (Summer Mix)；Pepsi；Mandarin Orange Slice；Pepsi advantage；Pepsi (summer mix)；Wildcherrypepsi；Cokesi；Pepsi-Cola；Pepsi Fire；Pepsi EDGE；Pepsi Cola；Pepsiman；Pepsi avantage；Pepsi AM；Pepsi: Summer Mix；Diet Wild Cherry Pepsi；Pepsi Man；Pepsi-cola；Pepsi Cappuccino；Pepsi summer Mix；Pepsi Ice；Pepsi lime；Peppsey；Diet Cherry Pepsi；Pepsi Edge；Pepsi summer mix；Brad's Drink；Pepsi B；Pepsi Summer Mix；Pepsi Limited Edition Summer Mix；Pepsi X；PEPSI；Brads drink；Homemade Pepsi；Diet Pepsi Vanilla；Pepsi (Summer mix)
- **模型回答**：Redoke
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Redoke' does not match any valid reference answer (Pepsi and its variants).

## 152. [-] main/dream · triviaqa__wh_2223__seed20261020 · 一致

- **问题**：Which business organisation took over the Somerfield chain of stores ?
- **参考答案**：THE CO-OPERATIVE；International (supermarket)；Scottish Co-operative Wholesale Society；Co-op Group；Co-operative Group members；Co-operative Group；The co-op group；Manx Co-operative Society；The Co-Operative Group；Plymouth & South West；Plymco Co-op；CWS UK；Cooperative Group；Members of the Co-Operative Group；Co-operative Group Members；Co-Operative Group；THE CO-OPERATIVE；Societies of The Co-operative Group；Coop Group；The Co-Operative；The co-operative group's new head office；Co-Op UK；The Co-operative Group；Members of The Co-Operative Group；The Co-operative；The co-op；Members of the Co-operative Group；Plymouth and South West Co-operative Society；Scottish co-op；Co-operative group；Members of The Co-operative Group；Cooperative Wholesale Society；Linfood Holdings；Co-operative Group Ltd.；Plymco
- **模型回答**：Tesco
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Tesco' contradicts all reference answers, which consistently identify The Co-operative Group (or its variants) as the organization that took over Somerfield.

## 153. [-] main/llada · hotpotqa__5a7109e95542994082a3e4fa__seed20261020 · 一致

- **问题**：What town did Sean Robert Francis play in as part of the most successful club in the Republic of Ireland?
- **参考答案**：Tallaght, South Dublin
- **模型回答**：Dublin
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The reference answer specifies 'Tallaght, South Dublin' as the town. While Tallaght is within the greater Dublin area, 'Dublin' is a broader city/region and is not semantically equivalent to the specific town of Tallaght.

## 154. [-] main/llada · hotpotqa__5a796bfd55429970f5fffeac__seed20261020 · 一致

- **问题**：What adorns the archaeological artefact excavated by Thomas Bateman on 3 May 1848?
- **参考答案**：A simple iron boar crest
- **模型回答**：The archaeological artefact excavated by Thomas Bateman on 3 May 1848 is the Rosetta Stone.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names the Rosetta Stone, which was discovered in 1799 and is unrelated to Thomas Bateman; it contradicts the reference answer that the artefact (the Benty Grange helmet) is adorned by a simple iron boar crest.

## 155. [-] main/llada · hotpotqa__5a81141855429938b61422ad__seed20261020 · 一致

- **问题**：What team does the third place winner from the 2006 San Marino Grand Prix currently compete with?
- **参考答案**：Team Penske
- **模型回答**：Red Bull Racing
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Red Bull Racing' does not match the reference answer 'Team Penske'.

## 156. [-] main/llada · hotpotqa__5a8242c155429940e5e1a81d__seed20261020 · 一致

- **问题**：Where was the author of Thoughts of Machiavelli born?
- **参考答案**：Germany
- **模型回答**：London
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer London contradicts the reference answer Germany.

## 157. [-] main/llada · hotpotqa__5ab43179554299233955004d__seed20261020 · 一致

- **问题**：What is the female star of Klepto best known for performing in?
- **参考答案**：The Secret World of Alex Mack
- **模型回答**：The female star of Klepto is best known for performing in musical theater.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer contradicts the reference answer. The reference states the female star is best known for 'The Secret World of Alex Mack', not musical theater.

## 158. [-] main/llada · hotpotqa__5abdba405542993f32c2a023__seed20261020 · 一致

- **问题**：Orlando Brown is best known for his role as 3J Winslow in an American sitcom that was a spin-off of what?
- **参考答案**：Perfect Strangers
- **模型回答**：Orlando Brown is best known for his role as 3J Winslow in the American sitcom "3J," which was a spin-off of "Full House."
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer states the sitcom was a spin-off of "Full House" and refers to the show as "3J", but the correct spin-off is "Perfect Strangers" (the show was Family Matters).

## 159. [-] main/llada · hotpotqa__5abe86365542993f32c2a14d__seed20261020 · 一致

- **问题**：Joel H. Cohen is the younger brother of one-time Simpsons writer who has also written for which show?
- **参考答案**："The Wonder Years"
- **模型回答**：Joel H. Cohen is the younger brother of Gary Cohen, who has also written for The Simpsons.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer identifies Gary Cohen as Joel H. Cohen's brother and states he wrote for The Simpsons, but the question asks which show the brother has *also* written for. The answer does not mention 'The Wonder Years' or any other additional show, so it fails to answer the question.

## 160. [-] main/llada · hotpotqa__5ac12275554299012d1db6a3__seed20261020 · 一致

- **问题**：Charlie Rowe plays Billy Costa in a film based on what novel?
- **参考答案**："Northern Lights"
- **模型回答**：Charlie Rowe plays Billy Costa in the film based on the novel "The Big Sleep."
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names the wrong novel; the correct novel is "Northern Lights."

## 161. [-] main/llada · hotpotqa__5adcbb815542994ed6169bde__seed20261020 · 一致

- **问题**：Beer Wars covers the differences between large corporate breweries, and small breweries, such as what brewery that is headquartered in Escondido, california?
- **参考答案**：Stone Brewing
- **模型回答**：San Diego Brewery
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'San Diego Brewery' does not match the reference answer 'Stone Brewing'. Stone Brewing is the brewery headquartered in Escondido, California, featured in Beer Wars.

## 162. [-] main/llada · hotpotqa__5ae202f2554299234fd0438d__seed20261020 · 一致

- **问题**：Hndrxx features a guest appearance by what Canadian singer?
- **参考答案**：The Weeknd
- **模型回答**：Hndrxx features a guest appearance by Canadian singer Justin Bieber.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names Justin Bieber, which contradicts the reference answer The Weeknd.

## 163. [-] main/llada · hotpotqa__5ae27f22554299495565da8d__seed20261020 · 一致

- **问题**：In what year was the mathematician husband of Anneli Cahn Lax born?
- **参考答案**：1926
- **模型回答**：The mathematician husband of Anneli Cahn Lax, Peter Lax, was born in 1919.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer states Peter Lax was born in 1919, which contradicts the valid reference answer of 1926.

## 164. [-] main/llada · hotpotqa__5ae326e95542990afbd1e0b6__seed20261020 · 一致

- **问题**：Where is the American Hockey League, that Dan Frawley played in, located?
- **参考答案**：United States and Canada
- **模型回答**：The American Hockey League (AHL) is located in the United States.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The AHL is located in both the United States and Canada; the proposed answer omits Canada, making it incomplete and factually insufficient compared to the reference.

## 165. [-] main/llada · hotpotqa__5ae37e6e5542992f92d822e0__seed20261020 · 一致

- **问题**：Which countries forces fought in The Battle of Hürtgen Forest which was covered in the shooter video game Darkest Hour: Europe '44-'45?
- **参考答案**：American and German
- **模型回答**：The Battle of Hürtgen Forest was fought between American and German forces.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer states American and German forces, matching the reference answer.

## 166. [-] main/llada · triviaqa__bb_1161__seed20261020 · 一致

- **问题**：Who is the the voice of cartoon character Jack Kahuna Laguna in a special episode of Spongebob Squarepants?
- **参考答案**：Johnny Depp；Johnny deep；Johnny Dep；Caliber (film)；The Affected Provincial's Companion；Lori Anne Allison；Caliber (2014 film)；Affected Provincial's Companion (film)；List of Johnny Depp awards；Fierce Invalids Home from Hot Climates (film)；The Vault (2015 film)；John Depp；Depp, Johnny；The Vault (film)；Johnny Depp:List of awards & nominations；Lily-Rose Melody Depp；Johny Depp；Johhny Depp；Mortimer Wintergreen；List of Johnny Depp awards and nominations；Depp；Johnny Depp；John Christopher %22Johnny%22 Depp II；Inamorata (film)；Johnny Deep；Jonny Depp；Mortimer Wintergreen (2015 film)；John Christopher Depp II；Affected Provincial's Companion；Oprah Noodlemantra；John Christopher Depp；Johnny depp；Mortimer Wintergreen (film)；List of Johnny Depp's awards and nominations
- **模型回答**：Tom Kenny.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：Tom Kenny is not listed among the valid answers; reference answers identify Johnny Depp as the voice actor.

## 167. [-] main/llada · triviaqa__bb_5094__seed20261020 · 一致

- **问题**：What London medicinal water site, later a music hall, was the birthplace of the Royal Ballet and English National Opera?
- **参考答案**：Sadler's Wells；Sadler's Wells；New Sadler's Wells Opera；Sadler’s Wells；Sadler's-Wells；Lilian Baylis Theatre；New Sadler's Wells Opera Company；Sadlers Wells；Sadler’s Wells Theatre；Sadler's Wells Theatre
- **模型回答**：Covent Garden
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names Covent Garden, but the references identify the site as Sadler's Wells, so it does not match any valid answer.

## 168. [-] main/llada · triviaqa__bb_5364__seed20261020 · 一致

- **问题**：What 'seasonal-mood' name was given to the western social phenomenon of mid-1967, sparked by the vast gathering of young people in Haight-Ashbury, San Francisco?
- **参考答案**：The Summer of Love；Summer of love；The summer of love；Summer Of Love；Summer of Love；The Summer of Love
- **模型回答**：The 'seasonal-mood' name given to the western social phenomenon of mid-1967, sparked by the vast gathering of young people in Haight-Ashbury, San Francisco, is "Summer of Love."
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer "Summer of Love" is semantically equivalent to the reference answers and correctly answers the question.

## 169. [-] main/llada · triviaqa__bt_3007__seed20261020 · 一致

- **问题**：Who wrote the epic 1869 novel War and Peace
- **参考答案**：Leo Tolstoy；Lyof Nikolaivitch Tolstoi；Tolstoy；Leo Nikolaievich Tolstoy；Lev Nikolaïevitch Tolstoï；Lev Nikolajevič Tolstoj；Count Lev Tolstoy；Lev Nikolajevic Tolstoj；Lev Nikolaevich Tolstoy；Leo tolstoi；Tolstoi；LN Tolstoi；Leo N. Tolstoy；Buried Alive (play)；Lev N. Tolstoi；Lev Tolstoi；Voice of Thunder (Lincoln)；Lev Tolstoï；Leo N. Tolstoi；Tolstoy, Lev Nikolayevich；Lev N. Tolstoï；LN Tolstoy；Count Lev Nikolaevich Tolstoi；Lev Nikolaevic Tolstoj；Leo N. Tolstoï；Толстой；Lev N. Tolstoy；Lev Tolstoy；Leo Tolstoï；Count Lev N. Tolstoy；Leo Tolstoy's religious beliefs；Leo tolstoy；Count Leo Tolstoy；León Tolstói；Lev Nikolayevich Tolstoy；Лев Никола́евич Толсто́й；Leo Tolstoy；Leo Nikolayevich Tolstoy；Leo Nikoleyevich Tolstoy；Count Leo Tolstoï；Count Leo N. Tolstoy；Leon Tolstoi；Leo Nikolayevitch Tolstoy；Count Leo Tolstoi；Lyof Tolstoy；Count Leo N. Tolstoi；Count Leo N. Tolstoï；Lev Tolstói；Lev Nikolaevič Tolstoj；Leo Tolstoi；Léon Tolstoï；Лев Николаевич Толстой；Leon Tolstoy；Lev Tolstoj；Leo, Count Tolstoy；Tolstoy, Leo Nikolayevich；Lev Nikolaievitch Tolstoi
- **模型回答**：Leo Tolstoy
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Leo Tolstoy' exactly matches multiple reference answers and is factually correct.

## 170. [-] main/llada · triviaqa__bt_4324__seed20261020 · 一致

- **问题**：What is the state capital of Alabama
- **参考答案**：Montgomery；Montgomerie；Montgomery (disambiguation)；Montgomery
- **模型回答**：The state capital of Alabama is Montgomery.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer states Montgomery, which matches the reference answers.

## 171. [-] main/llada · triviaqa__dpql_4567__seed20261020 · 一致

- **问题**：N’Djamena is the capital city of which landlocked country in central Africa?
- **参考答案**：Chad；تشاد；Republique du Tchad；Tšād；Republic of Chad；République du Tchad；Chade；Chad；Tshād；ISO 3166-1:TD；Chad (country)；The Chad；جمهورية تشاد；Tsjad；Chadian Republic；Tschad；Gumhuriyyat Tšad；Culture of Chad；Tchad；Ǧumhūriyyat Tšād；Jumhūriyyat Tshād
- **模型回答**：N’Djamena is the capital city of Chad, a landlocked country in central Africa.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer correctly identifies Chad as the landlocked country in central Africa whose capital is N'Djamena, matching the reference answers.

## 172. [-] main/llada · triviaqa__jp_3637__seed20261020 · 一致

- **问题**：What is either a bay in the Indian ocean or a subspecies of tiger?
- **参考答案**：Bengal；Bengal (India)；Kingdom of Bengal；Bengal, India；Bôngo；Bôngodesh；বঙ্গদেশ；Bongodesh；Greater Bengal；Etymology of Bengal；Bengal；বঙ্গ
- **模型回答**：tiger Bay
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'tiger Bay' does not match any valid reference answer. The correct answer is 'Bengal' (referring to both the Bay of Bengal and the Bengal tiger). 'Tiger Bay' is a different entity and does not satisfy the question's criteria of being either a bay in the Indian Ocean or a subspecies of tiger.

## 173. [-] main/llada · triviaqa__odql_10031__seed20261020 · 一致

- **问题**：What was the first name of Mr. Ferrari, the founder of the car manufacturing company?
- **参考答案**：ENZO；Enzo；ENZO；Enzo (disambiguation)
- **模型回答**：Enzo
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Enzo' matches the reference answer 'Enzo', which is the first name of Enzo Ferrari, founder of the Ferrari car company.

## 174. [-] main/llada · triviaqa__odql_14154__seed20261020 · 一致

- **问题**：What is the name given to the vertical groove that runs between the top lip and the nose?
- **参考答案**：FILTRUM；Sniffleridge；Filtrum；Nasal divot；Philthrum；Infranasal depressions；Philtra；Philtrium；Infranasal depression；FILTRUM；Philtrum；Philtron；Philtrums
- **模型回答**：Lip crease.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Lip crease' does not match any valid reference answer or name the vertical groove between the top lip and the nose.

## 175. [-] main/llada · triviaqa__odql_3292__seed20261020 · 一致

- **问题**：Which Cricket broadcaster is famous for his observations of passing traffic?
- **参考答案**：HENRY BLOFELD；Henry Blofeld；HENRY BLOFELD
- **模型回答**：Lord Harris
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Lord Harris' does not match any of the valid reference answers, which identify HENRY BLOFELD as the cricket broadcaster famous for observing passing traffic.

## 176. [-] main/llada · triviaqa__odql_351__seed20261020 · 一致

- **问题**：Which spy was sentenced to 42 years in prison in 1961, but escaped from Wormwood Scrubs in 1966?
- **参考答案**：GEORGE BLAKE；GEORGE BLAKE；George Blake；Max de Vries
- **模型回答**：David Chapman.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'David Chapman' does not match any of the valid reference answers (George Blake or Max de Vries) and is factually incorrect.

## 177. [-] main/llada · triviaqa__qb_2743__seed20261020 · 一致

- **问题**：Who is recognised as Britain’s first Prime Minister?
- **参考答案**：Robert Walpole；Sir Blustering；Robert Walpole；Walpole Government；Screen-Master General；The Rt. Hon. Sir Robert Walpole, KT GCB 1st Earl of Orford；Sir Robert Walpole；Bob of Lym；Orford, Robert Walpole, 1st earl of；Robert Walpole, 1st Earl of Orford；Bob Booty
- **模型回答**：William Pitt
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names William Pitt, which contradicts the reference answers identifying Robert Walpole as Britain's first Prime Minister.

## 178. [-] main/llada · triviaqa__qb_5532__seed20261020 · 一致

- **问题**：What is the Japanese art of paper-folding called?
- **参考答案**：Origami；Oragami；Paper folding art；Paper Folding；Paper-folding；Paperfolding；List of origami societies；Origami-bonsai；Origaming；折紙；Origami；Origamy；Paper folding；折り紙
- **模型回答**：Origami.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer 'Origami' is semantically equivalent to multiple valid reference answers and directly answers the question.

## 179. [-] main/llada · triviaqa__qb_5712__seed20261020 · 一致

- **问题**：Which drink is known as ‘The Wine of Islam’?
- **参考答案**：Coffee；Kawha；Ginseng coffee；Cafe de Columbia；Coffee (drink)；Coffee brews；Caffé；Coffee Bags；Health effect of coffee；Brazilian coffee；Gourmet coffee；Kaffee；Coffe；Joe (coffee)；Medical effects of coffee；Gavaccino；Cup of Joe；Specialty coffees；Coffee；Effects of coffee；Health and pharmacology of coffee；Regular coffee；Ginseng Coffee；Specialty Coffees；Coffee brewing method；Health effects of coffee；Coffee and health；Roasted coffee
- **模型回答**：Alcohol.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Alcohol' contradicts all reference answers, which are variants of 'Coffee.' Coffee is historically known as 'The Wine of Islam,' not alcohol, which is prohibited in Islam.

## 180. [-] main/llada · triviaqa__qg_2404__seed20261020 · 一致

- **问题**：Name the book and the author: 'The Time Traveler (for so it will be convenient to speak of him) was expounding a recondite matter to us.'
- **参考答案**：The Time Machine, by H.G. Wells；The Time Machine, by H.G. Wells
- **模型回答**：The Time Machine by H.G. Wells.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer identifies the book as 'The Time Machine' and the author as 'H.G. Wells', which matches the reference answers.

## 181. [-] main/llada · triviaqa__qg_2992__seed20261020 · 一致

- **问题**：According to Sammy Haggar, what can't he drive?
- **参考答案**：55；55；fifty-five
- **模型回答**：Sammy Haggar can't drive a car.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The reference answers indicate Sammy Haggar can't drive 55 (mph), not that he can't drive a car. The proposed answer contradicts the references by claiming he can't drive a car.

## 182. [-] main/llada · triviaqa__qg_3452__seed20261020 · 一致

- **问题**：Named for its chairman, The Warren Commission published its final report on Sept 27, 1965. What event was it seated to investigate?
- **参考答案**：JFK Assassination；Shooting of John F. Kennedy；Dealey Plaza shootings；President Kennedy's assassination；J.F.K assassination；JFK assassination；Assassination of JFK；Assassination of President Kennedy；Assassination of John F. Kennedy；Kennedy assassination；Death of JFK；November 22, 1963；Faye Chism；Kennedy assasination；Assassination of John Kennedy；Shooting of JFK；Kennedy's assassination；The Kennedy assassination；JFK Assassination；Assassination of Kennedy；Assassination of United States President John F. Kennedy；John F kennedy assassination；John F. Kennedy assassination；John F. Kennedy's assassination；Assassination of john f. kennedy；John Fitzgerald Kennedy's assassination；Killing of JFK；John F. Kennedy Assassination；Assassanation of John F. Kennedy；Kennedy Assassination；JFK shooting；Kennedy assassination theories；The Assassination of JFK；Back and to the left；Jfk assassination；John F.Kennedy assassination；Murder of JFK；Assassination of John Fitzgerald Kennedy；John F Kennedy assassination；Assassination Information Bureau；Murder of John F. Kennedy；John f. kennedy assassination；JFK blown away；Death of John F. Kennedy；JFK's Assassination；Kennedy Assasination；Assassination of john f kennedy；J.F.K. Assassination；JFK murder；John F. Kennedy assassination/Archive 4；Emmett Hudson；Assassination of jfk；JFK assasination；Assassination of John F Kennedy；John f kennedy assassination；Clark Panel；Assassination of President John F. Kennedy
- **模型回答**：The Warren Commission was seated to investigate the assassination of President John F. Kennedy.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer states the Warren Commission investigated the assassination of President John F. Kennedy, which matches multiple reference answers (e.g., 'Assassination of President John F. Kennedy', 'Assassination of President Kennedy') and correctly answers the question.

## 183. [-] main/llada · triviaqa__qw_10077__seed20261020 · 一致

- **问题**：Between 1783 and 1865, Englishmen William Wilberforce, Sir Cecil Wray and Dr Beilby Porteus, Africans Olaudah Equiano and Ignatius Sancho and, in the USA, William Lloyd Garrison, John Greenleaf Whittier, Harriet Beecher Stowe, Frederick Douglass, Charles Henry Langston and John Mercer Langston were leading figures in which movement?
- **参考答案**：Abolition of the slave trade；Abolitionism.；Critic of the slave trade；Emancipation of Slaves；White abolitionists；Abolition of slavery；Anti slavery movement；Antislavery movement；Emancipation of slaves；Abolutionism；Abolitionistic；Abolition (slavery)；Abolitionism in France；Anti-abolitionism；Abolition of Slavery；Abolitionism (slavery)；Movement to abolish slavery；Abolitionst；Abolishing slavery；White Abolitionists；Abolitionists；Opponent of slavery；Abolitionist movement；Slavery abolition；Anti-slavery；Emancipation Of Slaves；Abolition Of Slavery；Abolitionism；Slave emancipation；Opposition to slavery；Antislavery；Abolitionist (slavery)；Abolitionist；Abolitionist Movement；Emancipationist；Abolition of the slave trade；Anti-slavery movement
- **模型回答**：Abolitionism
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The answer is directly listed among the valid reference answers. The listed figures from England and the USA are historically recognized as leading abolitionists, making abolitionism the correct identification of the movement.

## 184. [-] main/llada · triviaqa__qw_11386__seed20261020 · 一致

- **问题**：What is the opposite side from starboard on a ship?
- **参考答案**：Port；Sea port；Seaport；Fishing port；Shipping port；Deep water port；Ice-free port；Ice free port；Deepwater port；Ports (disambiguation)；Sea ports；Port of discharge；Ferry port；Deepwater pier；Fishing Port；Fluvial port；Deep-water port；Warm-water port；Ice-free harbor；Sea-port；Warm water port；Ice free harbour；Port city；Ports；Seaports of Japan；Seaports；Ice-free harbour；Port town；Commercial port；Port
- **模型回答**：The opposite side from starboard on a ship is port.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer states 'port', which matches the primary reference answer and is factually correct.

## 185. [-] main/llada · triviaqa__qw_12980__seed20261020 · 一致

- **问题**：What object was unveiled outside John Lennon Airport, Liverpool, in 2005?
- **参考答案**：Yellow submarine；Yellow Submarine；Yellow submarine；The Yellow Submarine；Yellow Submarine (disambiguation)；Yello Sub
- **模型回答**：The Beatles sculpture.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'The Beatles sculpture' does not match any valid reference answer, which all indicate a Yellow Submarine.

## 186. [-] main/llada · triviaqa__qw_13977__seed20261020 · 一致

- **问题**：What is kept in the sump of a motor car engine?
- **参考答案**：Oil；Oily；Oil；ATCvet code QA06AG06；🝆；Oil (liquid)；Heat transfer oil；Fixed oils；Petro；Oils；ATC code A06AG06；Thermal oil；Diathermal oil；Heat-transfer oil
- **模型回答**：Engine oil.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：Engine oil is the oil kept in the sump of a motor car engine, which is semantically equivalent to the reference answers 'Oil' and 'Oils'.

## 187. [-] main/llada · triviaqa__qw_14469__seed20261020 · 一致

- **问题**："Complete the title of this James Bond film: ""From Russia With ... """
- **参考答案**：Love；Idealized love；Loveliest；Love；Loves；Prem (Hinduism)；Sacrificial love；True Love (The feeling)；Chemistry of love；Lovable；💑；Idealised love；Love interest；Loving relationship；Latin words for love；Lovingly；愛；Loveworthy；Lovelier
- **模型回答**：Love
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches the reference answer and correctly completes the James Bond film title.

## 188. [-] main/llada · triviaqa__qw_16018__seed20261020 · 一致

- **问题**：Who was the youngest person to become president of the USA?
- **参考答案**：Teddy Roosevelt；T Ros；Feddy Roosevelt；26th President of the United States；Trust Buster；The Cowboy President；Teddy roosevelt；Theodore Roosavelt；President Theodore Roosevelt；Theodor roosevelt；Teddy Rose；Teddy Roosevelt；Theodore roosevelt；T. Roosevelt；Teodoro Roosevelt；T. Roosevelt Administration；Teddy Roosvelt；Teddy Rosevelt；Roosevelt, Theodore；Teddy Roosevelt foreign policy；T Roosevelt；Cowboy of the Dakotas；Teddy Roose；Theodore Roosevelt
- **模型回答**：William Henry Harrison
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The reference answers indicate Theodore Roosevelt was the youngest person to become president; William Henry Harrison was the oldest at inauguration, not the youngest.

## 189. [-] main/llada · triviaqa__sfq_10625__seed20261020 · 一致

- **问题**：'If you have a problem, if no-one else can help, and if you can find them'; then maybe you could hire who, on TV in the 1980s?
- **参考答案**：THE A-TEAM；A-Team；A - team；The A-Team cultural effects；The A-team；THE A-TEAM；Ateam；B.a. barracas；A team；B.A. Barracas；Ba barracas；Half pincer movement；Brigada A；A-Team, The；A Team, The；The A-Team；The A Team；The ateam；The a-team；Cultural effects of The A-Team；A Team；A-team
- **模型回答**：A psychic.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'A psychic' does not match the reference answers; the correct answer is 'The A-Team', based on the show's famous tagline.

## 190. [-] main/llada · triviaqa__sfq_11095__seed20261020 · 一致

- **问题**：Which pop singer shot himself to death in 1990 whilst suffering from depression?
- **参考答案**：DEL SHANNON；DEL SHANNON；Berlee Records；Berlee records；Del Shannon；Del shannon
- **模型回答**：David Bowie.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：David Bowie died in 2016 of liver cancer; he did not die by suicide in 1990. The correct answer is Del Shannon.

## 191. [-] main/llada · triviaqa__sfq_1233__seed20261020 · 一致

- **问题**：Who wrote the book 'Elmer Gantry'?
- **参考答案**：Sinclair Lewis；(Harry) Sinclair Lewis；Harry Sinclair Lewis；Lewis, (Harry) Sinclair；Grace Hegger；Sinclair Lewis
- **模型回答**：The book 'Elmer Gantry' was written by Ernest Hemingway.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer names Ernest Hemingway, which contradicts all reference answers identifying Sinclair Lewis as the author.

## 192. [-] main/llada · triviaqa__sfq_15254__seed20261020 · 一致

- **问题**：Who was the star of the film comedies 'The Navigator' (1924) and 'The General' (1927)?
- **参考答案**：BUSTER KEATON；Buster Keeton；BUSTER KEATON；Eleanor Keaton；Buster keaton；Buster Keaton；Keatonesque；Buster Keaton's；Joseph Francis %22Buster%22 Keaton；Joseph Frank Keaton VI；Joseph Francis Keaton
- **模型回答**：Charlie Chaplin
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Charlie Chaplin' contradicts the reference answers, which all identify Buster Keaton as the star of both films.

## 193. [-] main/llada · triviaqa__sfq_19462__seed20261020 · 一致

- **问题**：In 480 BC, Leonidas led his 300 Spartans against the Persian army, led by Xerxes, in which land battle?
- **参考答案**：Thermopylae；Thermopalee；Θερμοπύλες；Thermopoli；Thermapolyae；Thermoplyae；Thermopalae；Thermopale；Thermapoalye；Θερμοπύλαι；Thermopoly；Thermpoali；Thermopyle；Thermopylee；Thermopolae；Thermopolyae；Thermopylae
- **模型回答**：Battle of Thermopylae
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer matches the reference answers.

## 194. [-] main/llada · triviaqa__sfq_20557__seed20261020 · 一致

- **问题**：Who was the conservative candidate beaten by Ken Livingstone in the first two elections for Mayor of London?
- **参考答案**：Steven Norris；Steve Norris；Steven John Norris；Stephen Norris；Steven Norris
- **模型回答**：John Prescott.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'John Prescott' does not match any valid reference answer. The conservative candidate beaten by Ken Livingstone was Steven Norris.

## 195. [-] main/llada · triviaqa__sfq_23994__seed20261020 · 一致

- **问题**：Who wrote the 1911 opera ‘Der Rosenkavalier’?
- **参考答案**：Richard Strauss；Strauss, Richard；Richard Strauss；Richard Georg Strauss；Ricardo Strauss
- **模型回答**：Wolfgang Strauss II
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The correct composer is Richard Strauss; 'Wolfgang Strauss II' is not a valid name and contradicts all reference answers.

## 196. [-] main/llada · triviaqa__sfq_279__seed20261020 · 一致

- **问题**：In which religion is the temple, or place of worship, known as the gurdwara?
- **参考答案**：SIKHISM；Sikh faith；Sikhi；Sikhsim；Sikh Brahmins；SIKHISM；Sikhism Other Observations；Sikh religion；Sikhism；The Sikh Religion；The Ten Gurus；Sikism；Baptized Sikh；Sikkhi；Ten gurus；Sikha Dharma
- **模型回答**：The gurdwara is a place of worship in the Sikh religion.
- **规则标签**：correct(0) ｜ **judge 标签**：correct(0)
- **judge 理由**：The proposed answer correctly identifies the Sikh religion, which matches the reference answers (Sikhism, Sikh religion, etc.).

## 197. [-] main/llada · triviaqa__sfq_3248__seed20261020 · 一致

- **问题**：Which cartoon character created by Al Capp lives in Dog Patch?
- **参考答案**：L'ABNER；L'ABNER
- **模型回答**：Popeye
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The correct answer is Li'l Abner (L'ABNER), created by Al Capp, who lives in Dogpatch. Popeye was created by E.C. Segar and does not live in Dogpatch.

## 198. [-] main/llada · triviaqa__sfq_6889__seed20261020 · 一致

- **问题**：Which actress and singer is known as Li Lo?
- **参考答案**：LINDSAY LOHAN；Lindsay Lohen；Lindsey Lohan；La Lohan；Lindsay Dee Joanne Lohan；Linsey Lohan；Linsay Lohan；Lindsey Lowhan；Spirit in the Dark (Lindsay Lohan album)；Playground (Lindsay Lohan & Pharrell song)；Playground (Lindsay Lohan single)；Lindsay Dee Lohan；Spirit In the dark；Lndsay Lohan；Lindsay Lohan；Lindsay Morgan Lohan；Lezlo；Linsday Lohan；LiLo (actress)；Lyndsay Lohan；Lindsay Loahn；Playground (Lindsay Lohan)；Lindsi Lohan；LINDSAY LOHAN；Lezzlo；Lindsay Lohan's Forthcoming Studio Album；Lindsy Lohan；Lindsay Lohan Remixes；Lindsay lohan
- **模型回答**：Li Li.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer 'Li Li' does not match any reference answer; the correct answer is Lindsay Lohan.

## 199. [-] main/llada · triviaqa__sfq_7104__seed20261020 · 一致

- **问题**：Silkworms feed on the leaves of which tree?
- **参考答案**：Mulberry；Mulberry tea；Mulberry trees；Mulberries；Mullberry；Mulbery；Moriculture；Mulberry；Morus (plant)；Mulberry tree；Mulberry Tree
- **模型回答**：Silkworms feed on the leaves of silk trees.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The proposed answer says 'silk trees' but silkworms feed on mulberry leaves, not silk trees.

## 200. [-] main/llada · triviaqa__wh_2686__seed20261020 · 一致

- **问题**：In which TV establishment were Miss Gatsby and Miss Tibbs residents ?
- **参考答案**：FAWLTY TOWERS；FAWLTY TOWERS；Polly Shearman；Polly Sherman (Fawlty Towers)；Fawlty Towers Episode 13；Fawlty Towers；Fawlty towers；Flowery Twats；List of Fawlty Towers episodes；Fawlty Towers (hotel)；Fawlty；Dr. Abbott；Woodburn Grange Country Club；Polly Sherman；Fawlty Towers episode guide；Audrey (Fawlty Towers)；Fawlty towers episodes；Terry the Chef；Faulty Towers；Wooburn Grange Country Club
- **模型回答**：Miss Gatsby and Miss Tibbs were residents of the Grand Budapest Hotel.
- **规则标签**：incorrect(1) ｜ **judge 标签**：incorrect(1)
- **judge 理由**：The answer names 'Grand Budapest Hotel', which contradicts the reference answers identifying Fawlty Towers (and its characters/episodes).

