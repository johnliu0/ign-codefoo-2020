# Introduction

## Who Am I?
I'm a computer engineering student at the University of Waterloo. I have a passion for coding and I used to play a lot of big e-sports titles.

I peaked at Gold I in LOL (about 2-3 years ago) and MG2 in CSGO (last year). I also used to play a lot of TF2.

Working at IGN would be amazing because I haven't had time recently to enjoy what I like doing. I'm super busy with my studies and I didn't bring my gaming computer from my home in Toronto (there's a GTX 1060 just sitting at home collecting dust).

I'd love to use this summer to engineer software alongside some great (and I bet super chill) people at IGN and have a lot of fun with video games and developing and learning awesome things.

I'm not a super gamer that has played every single COD or GTA game and has tons of merchandise; but I do enjoy them, and I think I would love to be a part of IGN where everyone has one common interest: video games.

If you're a hiring manager/engineer and reading this; please do give me a chance! I promise I will try my best to succeed :)

## Repository Structure

### Backend Option
I selected the backend option. Code is available under the folder backend. Part 1 is implemented in csv_reader.py and loads the csv into the database. Part 2 is implemented in api.py. The only dependency I require is Flask for the server and mysql-connector for the MySQL database connection. Explanation for all my decisions is in api.py.

To run:
First ensure that a MySQL database called igncodefoo is created and ready for use.
Then run `python3 csv_reader.py` to extract the csv file.
Finally run `env FLASK_APP=server FLASK_ENV=development flask run --port=5000` on UNIX to start the server.

Note that I chose Python/Flask/MySQL because I've been working in Python *a lot* the past few months. I'm actually a better engineer with Node.js/JavaScript/MongoDB since I've worked with these tools and technologies more in the past.

I like trying new things; and Flask seems to be really awesome at being lightweight and easy to use. (Of course I'd be more than willing to pick up more things for the job :D).

### Optimize Link's Quest Rewards
Code to optimize Link's quest finding is available under the quest folder. The data for available quests is in quest.csv (I trimmed down the data you guys provided.). When you run it with python (`python3 graph.py`), it will give you this:

```
Quest Reward Optimizer: IGN Code Foo Summer 2020
Author: John Liu

The maximum amount of rupees that Link can earn in 31 days is 5970.
To achieve this, Link should do the following quests in order: 
Quest                          Start   End     Reward
The Weapon Connoisseur             1     5        920
Sunken Treasure                    5     6        200
Riddles of Hyrule                  7     9       1200
Rushroom Rush!                     9    10        460
Frog Catching                     10    14        900
Medicinal Molduga                 14    18        600
A Gift for the Great Fairy        20    27       1100
A Rare Find                       28    31        590
```

The correct answer should hopefully be 5970 rupees. This was achieved using dynamic programming. Further explanation is in quest.py.

My language of choice is Python. Besides Flask, all code uses vanilla Python3. I am also proficient in JavaScript, and actively learning C++.