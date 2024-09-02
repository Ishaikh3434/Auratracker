Swagbot is a simple-to-use Discord bot written with the discord.py library. 

The main function of the bot is to track "Swag". By default, the "🔥" reaction will give points, and the "🤓" reaction will remove points from a user. Giving points also gives the reacter 10 points, and removing points will cost the reacter 10 points.
The bot also features a quicktime-style minigame; periodically the bot will add a "🔮" emoji to the most recent message; if the poster of that message clicks the reaction in time, they'll get a bonus of 100 points.

Basic commands:
- /ping - Displays the bot's latency in ms
- /pointsname - Change the alias of the points tracked by the bot. Default is "swag".
- /mypoints - Display a user's total points.
- /changereaction - Change the emojis the bot will award and deduct points for. Default are 🔥 and 🤓, respectively.
- /leaderboard - Display the current serverwide rankings.
