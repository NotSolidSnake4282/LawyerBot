# LawyerBot
Discord bot for Open Legend RPG


## Rulebook
You need to have a yaml containing boons, banes, and feats for the bot to read. Set this on settings.py. The easiest way would be to just copy the entire Open Legend RPG git project, and have the bot read the files from there. See this project : https://github.com/openlegend/core-rules

## Running the bot
Simply obtain your bot token and owner ID from discord developer console, add it to settings.py and run main.py. It's recommended to run this from Supervisor as the bot sometimes exits by itself due to connection problem.