# Daily Chess Pro
### A HackTheNorth 2020++ Submission
#### By Russell Islam and Kara Dietz

### DevPost Link
https://devpost.com/software/daily-chess-pro

### Video Demo
https://www.youtube.com/watch?v=vAucpL8m-W4


## What is it?
Most people who play chess or are beginning to get into chess want to become better players. We all want to be like Hikaru Nakamura or Magnus Carlsen. One thing that GMs and Super GMs do in order to become better chess players are chess puzzles. This is something that many beginners do not tend to do. Furthermore, it is something that beginners do not do consistently (I am speaking from personal experience).

We decided to build a Facebook Messenger Bot which will send registered users a daily random chess puzzle. This provides a daily reminder which will allow people to consistently solve chess puzzles to become a better player.

## How it works
You can go on the Messenger bot and start speaking to it. The following are a list of commands that you can say to the Messenger bot:

:point_right: **Help:** Provides a brief description and a list of commands that you can execute

:point_right: **Commands:** List all possible commands

:point_right: **Status:** Tells you whether you are currently registered to receive daily chess puzzles

:point_right: **Subscribe:** Subscribe to receive daily chess puzzles.

:point_right: **Unsubscribe:** Unsubscribe from receiving daily chess puzzles

:point_right: **Send Puzzle:** Sends you a link to a random chess puzzle

### Technology Used
- Facebook Messenger API
- Google Cloud Platform: App Engine, Cloud SQL MySQL Database
- Flask backend for Webhooks
- Google App Engine Cron jobs

**Disclaimer: The bot is not public yet due to Facebook's limitations.**
