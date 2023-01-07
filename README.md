# [Emperor v0.1.41](https://github.com/UOW-Computing/Emperor)

*Bot is limited in functionality as its currently in development.*

Discord bot used for School of Computing discord server.
The bot is highly customisable and coded by the server members themselves.

## Instructions

To localy run Emperor, you need a `.env` file.
You can look at `.env.example`, it outlines how the file should look like.

Before creating the file make sure to have a bot ready with its token copied.

You can create one here: [Discord Application](https://discord.com/developers/applications/).

Afterwards, either create a `.env` file yourself or use the `setup.py` to create one for yourself.

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
