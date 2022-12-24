# [Emperor v0.0.62](https://github.com/UOW-Computing/Emperor)
*Bot is limited in functionality as its currently in development.*


Discord bot used for School of Computing discord server.
The bot is highly customisable and coded by the server members themselves.

## Instructions

To localy run Emperor, you need a `.env` file.
You can look at `.env.example`, it outlines how the file should look like.

Before creating the file make sure to have a bot ready with its token copied.

You can create one here: [Discord Application](https://discord.com/developers/applications/).

Afterwards, either create a `.env` file yourself or use the `setup.py` to create one for yourself.

###### Currently `setup.py` is not ready, will be released in `v0.0.7` or `v0.0.8`.

## Commands

### Moderation

- `announce`: Makes a post using embeds
- `kick`: Kicks a member from a server
- `clear`: Removes messages in the executed channel
- `createrole`: Creates a role with default permissions

### Fun
- `hello`: Says hello back to you
- `server`: Gives info of the server in which it was executed in
- `reddit`: Responds with a post in the subreddit given

## TODO

- [ ] Add database into Lj for logging and server backups
- [ ] Turn createrole and server into sub commands of their own respective command, `create role` for `createrole` and `info server` for `server`
- [ ] Introduce `CHANGELOG.md`
- [ ] Push `setup.py` into repo
- [ ] Better error handling than just Lj
- [X] Remove use of `eval`
- [ ] Add timeout in `reddit` command, when asking for subreddit
