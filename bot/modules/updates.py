# Implement By https://github.com/jusidama18
# Based on this https://github.com/DevsExpo/FridayUserbot/blob/master/plugins/updater.py

import sys
import subprocess
import heroku3

from datetime import datetime
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from pyrogram import filters

from bot import app, OWNER_ID, UPSTREAM_REPO, UPSTREAM_BRANCH, bot
from bot.helper import get_text, HEROKU_URL
from bot.helper.telegram_helper.bot_commands import BotCommands

REPO_ = UPSTREAM_REPO
BRANCH_ = UPSTREAM_BRANCH

def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return ''.join(
        f'• [{c.committed_datetime.strftime(d_form)}]: {c.summary} **{c.author}**\n'
        for c in repo.iter_commits(diff)
    )

# Update Command

@app.on_message(filters.command([BotCommands.UpdateCommand, f'{BotCommands.UpdateCommand}@{bot.username}']) & filters.user(OWNER_ID))
async def update_it(client, message):
    msg_ = await message.reply_text("`Updating Bot with Latest Changes, Please Wait!!`")
    text = get_text(message)
    try:
        repo = Repo()
    except GitCommandError:
        return await msg_.edit(
            "**Invalid Git Command. Please Rimport logging

from os import path as ospath, environ
from subprocess import run as srun
from requests import get as rget
from dotenv import load_dotenv

if ospath.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL', None)
try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
                f.close()
        else:
            logging.error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        logging.error(f"CONFIG_FILE_URL: {e}")
except TypeError:
    pass

load_dotenv('config.env', override=True)

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', None)
try:
    if len(UPSTREAM_REPO) == 0:
       raise TypeError
except TypeError:
    UPSTREAM_REPO = None

if UPSTREAM_REPO is not None:
    if ospath.exists('.git'):
        srun(["rm", "-rf", ".git"])

    srun([f"git init -q \
                      && git config --global user.email e.anastayyar@gmail.com \
                      && git config --global user.name mltb \
                      && git add . \
                      && git commit -sm update -q \
                      && git remote add origin {UPSTREAM_REPO} \
                      && git fetch origin -q \
                      && git reset --hard origin/master -q"], shell=True)
eport This Bug To [Github](https://github.com/venomsnake/vhascometo/issues/new)**"
        )
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "upstream" in repo.remotes:
            origin = repo.remote("upstream")
        else:
            origin = repo.create_remote("upstream", REPO_)
        origin.fetch()
        repo.create_head(UPSTREAM_BRANCH, origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    if repo.active_branch.name != UPSTREAM_BRANCH:
        return await msg_.edit(
            f"`Seems Like You Are Using Custom Branch - {repo.active_branch.name}! Please Switch To {UPSTREAM_BRANCH} To Make This Updater Function!`"
        )
    try:
        repo.create_remote("upstream", REPO_)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(UPSTREAM_BRANCH)
    clogs = gen_chlog(repo, f'HEAD..upstream/{UPSTREAM_BRANCH}')

    if not clogs:
        await msg_.edit(f"Bot up-to-date with **{UPSTREAM_BRANCH}**", parse_mode="Markdown")
        return

    if text == "now":
        await msg_.edit(f"`Bot Updating with` **{UPSTREAM_BRANCH}** `Branch Please Wait...`", parse_mode="Markdown")
        if not HEROKU_URL:
            try:
                ups_rem.pull(UPSTREAM_BRANCH)
            except GitCommandError:
                repo.git.reset("--hard", "FETCH_HEAD")
            await msg_.edit("`Updated Successfully! It Will Take Some Time To Restart!`")
            with open("./aria.sh", 'rb') as file:
                script = file.read()
            subprocess.call("./aria.sh", shell=True)
            args = [sys.executable, "-m", "bot"]
            execle(sys.executable, *args, environ)
        else:
            await msg_.edit("`Heroku Detected! Pushing, Please wait!`")
            ups_rem.fetch(UPSTREAM_BRANCH)
            repo.git.reset("--hard", "FETCH_HEAD")
            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(HEROKU_URL)
            else:
                remote = repo.create_remote("heroku", HEROKU_URL)
            try:
                remote.push(refspec="HEAD:refs/heads/master", force=True)
            except BaseException as error:
                await msg_.edit(f"**Updater Error** \nTraceBack : `{error}`")
                return repo.__del__()
            await msg_.edit(f"`Updated Successfully! \n\nCheck your config with` `/{BotCommands.ConfigMenuCommand}`")
    else:
        await msg_.edit(f"**New Update Available**\n\nFrom [REPO]({REPO_})\nCHANGELOG:\n\n{clogs}\n\nDo `/update now` to Update BOT.", parse_mode="Markdown",disable_web_page_preview=True)
        return