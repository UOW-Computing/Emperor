# [Emperor v0.1.41](https://github.com/UOW-Computing/Emperor)

*Bot is limited in functionality as its currently in development.*

Discord bot used for School of Computing discord server.
The bot is highly customisable and coded by the server members themselves.

## Updates
Setup.py now can genereate an .env file on it's own!
LJ Logger now handles logs into a logs folder.  
When logging anything, just simply use self.lj.respective_log_name, LJ will handle writing to file on its own.  

## Setting up the project
### Before you begin
When setting up the project for the first time, the following command has to be executed on your enviroment terminal:  
`pip install -r requirements. txt`. 
Currently Emperor is not a working package, therefore it cannot automatically install dependencies. Install them manually using the command above.  

### Instructions
To localy run Emperor, you need a `.env` file. Which can be considered as your credentials to be parsed into the bot.
Follow this order when setting up the project for the first time:
<ol>
 <li>Before running the modules, make sure to have a bot ready with its token copied.</li>
 You can create one here: [Discord Application](https://discord.com/developers/applications/). This will generate your bot token.  
 <li>Run setup.py follow it's instructions.</li>
 When attempting to run main.py without running setup.py first you will get errors.
 <li>Run main.py - main.py runs the server for the bot.</li>
</ol>  


## Commands

### Moderation

- `ticket create`: Creates a channel exclusive to the ticket creater and staff members
- `ticket close`: Closes a ticket channel

### General

- `hello`: Says hello back to you
 - `info server`: Gives info of the server in which it was executed in
 - `info member`: Gives information about the member mentioned

### API

- `reddit`: Responds with a post in the subreddit given

## TODO

- [x] Add Lj logging into Ticket command
- [ ] Rewrite `clear` as `purge` command for discord.py
- [ ] Handle attachmens on `on_message` event
- [ ] Turn createrole into sub commands of their own respective command, `create role` for `createrole`
- [ ] Introduce `CHANGELOG.md`
- [ ] Better error handling than just Lj
- [ ] Add database into Lj for logging and server backups

## Notes for editors.
Need to add instructions on how to fork/git init the project enviroment.  
Need to add explanations on how to get log_channel_id, guild_id, token ?  
ReadME has to be updated, TODO's, etc...  
