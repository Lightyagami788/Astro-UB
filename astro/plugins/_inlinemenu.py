import asyncio
import html
import os
import re
from math import ceil

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest

from astro import CMD_HELP, CMD_LIST, CUSTOM_PMPERMIT, bot
from astro.config import Config

NAME = Config.NAME
PM_PIC = Config.PM_PIC
PM_TEXT = Config.PM_TEXT

ASTROPIC = (
    PM_PIC
    if PM_PIC
    else "https://telegra.ph/file/1dc4cf071ecd2be57e30a.jpg"
)

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
myid = bot.uid
mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
    
GROUP = Config.PRIVATE_GROUP_ID
MESAG = (
    str(CUSTOM_PMPERMIT)
    if CUSTOM_PMPERMIT
    else "Hii This is Security Provided by \n~ƛsτʀ๏ υsєяъ๏т~"
)

MYUSER = str(NAME) if NAME else "Astro✨User"

USER_BOT_WARN_ZERO = "**🤦I told you lot Not To spam But you didn't stopped..!\nYour Mistake 🙂\nNow Don't Disturb to my master and Fuck off From Here😹**"

if Config.LOAD_MYBOT == "True":
    USER_BOT_NO_WARN = (
        "**__Knock Knock__👀Who is There✨\nTHIS is Security Provided By **ƛsτʀ๏ υsєяъ๏т** To [{}](tg://user?id={})\n\n"
        "{}\n\n"
        "Something Important is there🤔→PM me via {}"
        "\nPlease choose why you are here, from the available options\n\n".format(
            MYUSER, myid, MESAG, botname
        )
    )
elif Config.LOAD_MYBOT == "False":
    USER_BOT_NO_WARN = (
        "**PM Security of [{}](tg://user?id={})**\n\n"
        "{}\n"
        "\nPlease choose why you are here, from the available options\n".format(
            MYUSER, myid, MESAG
        )
    )
    
CUSTOM_HELP_EMOJI = os.environ.get("CUSTOM_HELP_EMOJI", "✨")
HELP_ROWS = int(os.environ.get("HELP_ROWS", 3))
HELP_COLOUMNS = int(os.environ.get("HELP_COLOUMNS", 4))

if Config.BOT_USERNAME is not None and tgbot is not None:
    
     @tgbot.on(events.InlineQuery) 
     async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query.startswith("`Userbot"):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_LIST, "helpme")
            result = builder.article(
                "© Astro Help",
                text="{}\nCurrently Loaded Plugins: {}".format(query, len(CMD_LIST)),
                buttons=buttons,
                link_preview=False,
            )
        elif event.query.user_id == bot.uid and query == "**bugs":
         result = builder.article(
            title="bugs",
            text=f"**Facing Problem \n{MYUSER}** \nJoin to us My Devs will help You ",
            buttons=[
              [
                Button.url("Commands Not Working🥺", "https://t.me/Astro_HelpChat")
                ],
                [
                  Button.url("Request For New Plugin", "https://t.me/Astro_HelpChat")
                ],
                [
                  Button.url(
                    "Want To Learn About Commands",
                    "https://t.me/Astro_HelpChat" ,
                    )
                ], 
            ],
        )
        elif event.query.user_id == bot.uid and query.startswith("**PM"):
         result = builder.photo(
            file=ASTROPIC,
            text=USER_BOT_NO_WARN,
            buttons=[
                [
                    custom.Button.inline("To Request😓", data="req"),
                    custom.Button.inline("To Ask Something❔", data="ask")],
                [
                    custom.Button.inline("For Chatting💬", data="cht"),
                    custom.Button.inline("Something else😶", data="lse")],
                [
                    custom.Button.inline("What is This⁉️", data="wht")
                ],
              ],
            ) 
        await event.answer([result] if result else None)
        
@tgbot.on(events.callbackquery.CallbackQuery( data=re.compile(rb"helpme_next\((.+?)\)")))
async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(current_page_number + 1, CMD_LIST, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = (
                "Hey you.🙄 Get Your Own ƛsτʀ๏ υsєяъ๏т Don't touch mine🙂!"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"wht")))
async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "Don't you know what is this🙄?"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"This is the PM Security for {MYUSER} to keep away spammers And Maintain his Account.\n\nProtected by [ASTRO-USERBOT](t.me/Astro_UserBot)"
            )
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"reopen")))
async def megic(event):
        if event.query.user_id == bot.uid:
            buttons = paginate_help(0, CMD_LIST, "helpme")
            await event.edit("Menu Opens Again", buttons=buttons)
        else:
            reply_pop_up_alert = "Hey you.🙄 Get Your Own ƛsτʀ๏ υsєяъ๏т Don't touch mine🙂!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"req")))
async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "is it joke🙄You wanna to request your self\nthis is not for you"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Oki👀You have something to request to {MYUSER}\nIf {MYUSER} knows He will glad to help you😊\nDon't Spam wait till he somes🙂"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {MYUSER}, [{first_name}](tg://user?id={ok}) is **requesting** something in PM!\nSee what he wants to request 👀"
            trt = "⚠️My Master will come Soon :)\nTill Don't spam.. Please wait else Astro will block You🙂"
            await tgbot.send_message(event.query.user_id, trt)
            await tgbot.send_message(GROUP, tosend)
            
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"cht")))
async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "You wanna to chat your self😆\nThis is not for you Master"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"You wanna to chat👀💬\nOki My master is offline now. if {MYUSER} will be in mood of chatting he will talk to you😊\nDon't Spam wait till he somes🙂"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {MYUSER}, [{first_name}](tg://user?id={ok}) wants to PM you for **Random Chatting**!\nIf you are in mood of chatting You can talk to him👀"
            trt = "⚠️My Master will come Soon :)\nTill Don't spam.. Please wait else Astro will block You🙂"
            await tgbot.send_message(event.query.user_id, trt)
            await tgbot.send_message(GROUP, tosend)
            
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ask")))
async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "😆 What are you going to ask yourself\n This is not for you Master"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"👀What you want to ask to {MYUSER} ? Leave Your queies in Single Line\nDon't Spam wait till he somes🙂"
                )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {MYUSER}, [{first_name}](tg://user?id={ok}) wants to **ASK Something** in PM🤔check his DM👀I told him to leave your message!\ngo and Check🙃"
            trt = "My Master will come Soon :)\nTill Don't spam.. Please wait else Astro will block You🙂"
            await tgbot.send_message(event.query.user_id, trt)
            await tgbot.send_message(GROUP, tosend)
            
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"lse")))
async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "what are u doing 🥴This is not for u"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"😶ok..!You have something else For my {MYUSER} \nNow wait...! My master is offline NoW🥴When he will come he will Reply\nDon't Spam till wait he comes 🙂"
                )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {MYUSER}, [{first_name}](tg://user?id={ok}) wants to PM you\nHE HAVE **Something Else** For u😲\nGo and check..."
            trt = "My Master will come Soon :)\nTill Don't spam.. Please wait else Astro will block You🙂"
            await tgbot.send_message(event.query.user_id, trt)
            await tgbot.send_message(GROUP, tosend)
            
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            await event.edit(
                "Menu Closed!!", buttons=[Button.inline("open Again", data="reopen")]
            )
        else:
            reply_pop_up_alert = "Hey you.🙄 Get Your Own ƛsτʀ๏ υsєяъ๏т Don't touch mine🙂"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(rb"helpme_prev\((.+?)\)")))
async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1, CMD_LIST, "helpme")
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Hey you.🙄 Get Your Own ƛsτʀ๏ υsєяъ๏т Don't touch mine🙂"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
            
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"us_plugin_(.*)")))
async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            plugin_name = event.data_match.group(1).decode("UTF-8")
            help_string = ""
            help_string += f"Commands For {plugin_name} - \n"
            try:
                if plugin_name in CMD_HELP:
                    for i in CMD_HELP[plugin_name]:
                        help_string += i
                    help_string += "\n"
                else:
                    for i in CMD_LIST[plugin_name]:
                        help_string += i
                        help_string += "\n"
            except BaseException:
                pass 
            if help_string == "":
                reply_pop_up_alert = "{} has no detailed info.\nUse .help {}".format(
                    plugin_name, plugin_name
                )
            else:
                reply_pop_up_alert = help_string
            reply_pop_up_alert += "\n Use .unload {} to remove this plugin\nƛsτʀ๏ υsєяъ๏т".format(
                plugin_name
            )
            if len(help_string) >= 140:
                oops = "Commands List is Big😓Check Your Saved Message Commands list is Forwarded There🙃"
                await event.answer(oops, cache_time=0, alert=True)
                help_string += "\n\nThis will be auto-deleted in 2 minute!"
                if bot is not None and event.query.user_id == bot.uid:
                    ok = await bot.send_message("me", help_string)
                    await asyncio.sleep(120)
                    await ok.delete()
            else:
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            reply_pop_up_alert = "Hey you.🙄 Get Your Own ƛsτʀ๏ υsєяъ๏т Don't touch mine🙂"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
            
def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = HELP_ROWS
    number_of_cols = HELP_COLOUMNS
    tele = CUSTOM_HELP_EMOJI
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{} {}".format(tele, x), data="us_plugin_{}".format(x)
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⊰≾•ρяєѵıσυs", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline("⎝⎝cłσsє⎠⎠", data="close"),
                custom.Button.inline(
                    "ηєxт•≳⊱", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs

async def userinfo(event):
    target = await event.client(GetFullUserRequest(event.query.user_id))
    first_name = html.escape(target.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    return first_name
