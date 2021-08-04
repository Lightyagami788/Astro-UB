import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

import astro.plugins.sql.pmpermit_sql as pmpermit_sql
from astro.config import Config
from astro import CMD_HELP, CUSTOM_PMPERMIT, bot
from astro.utils import admin_cmd

NAME = Config.NAME
PM_PIC = Config.PM_PIC
ASTROPIC = (
    PM_PIC
    if PM_PIC
    else "https://telegra.ph/file/1dc4cf071ecd2be57e30a.jpg"
)
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
myid = bot.uid
MESAG = (
    str(CUSTOM_PMPERMIT)
    if CUSTOM_PMPERMIT
    else "This is PM security Provided By ƛsτʀ๏ υsєяъ๏т"
)
MYUSER = str(NAME) if NAME else "ASTRO user✨"

USER_BOT_WARN_ZERO = "**🤦I told you lot Not To spam But you didn't stopped..!\nYour Mistake 🙂\nNow Don't Disturb to my master and Fuck off From Here😹**"

USER_BOT_NO_WARN = (
      "__Knock Knock__👀 Who is here This is PM SECURITY provided by **ƛsτʀ๏ υsєяъ๏т** to \n"
      "[{}](tg://user?id={}) is Offline🙃."
      "{}\n\n**⚠️WARNING⚠️** `{}/{}` **TEXTS LEFT For u Don't spam. till my master will come**"
)

@astro.on(admin_cmd(pattern="a ?(.*)"))
@astro.on(admin_cmd(pattern="approve ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            if chat.id in PM_WARNS:
                del PM_WARNS[chat.id]
            if chat.id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat.id].delete()
                del PREV_REPLY_MESSAGE[chat.id]
            pmpermit_sql.approve(chat.id, reason)
            await event.edit(
                "[{}](tg://user?id={}) Now Approved To Text You👀".format(firstname, chat.id)
            )
            await asyncio.sleep(4)
            await event.delete()
            
@bot.on(events.NewMessage(outgoing=True))
async def you_dm_niqq(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            if chat.id not in PM_WARNS:
                pmpermit_sql.approve(chat.id, "outgoing")
                logit = "User - [{}](tg://user?id={}) Approved Due to outgoing Messages.".format(
                    chat.first_name, chat.id
                )
                try:
                    await borg.send_message(Config.PRIVATE_GROUP_ID, logit)
                except BaseException:
                    pass

@astro.on(admin_cmd(pattern="block ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if chat.id == 1258905497:
            await event.edit("Nigga😒You Are trying to Block Astro OWNER @Alone_loverboy 🤩i won't do anything Fuck off i am going off for 200Sec.🧑‍🦯😴💤")
            await asyncio.sleep(200)
        else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "BLOCKED..!!!!!\nFUCK OFF😒\nNibba\nBlocked - [{}](tg://user?id={})".format(
                        firstname, chat.id
                    )
                )
                await asyncio.sleep(3)
                await event.client(functions.contacts.BlockRequest(chat.id))
                
@astro.on(admin_cmd(pattern="da ?(.*)"))
@astro.on(admin_cmd(pattern="disapprove ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if chat.id == 1258905497:
            await event.edit("Are You mad?🙄 He is **ASTRO OWNER** i can't do anything against my God @Alone_loverboy")
        else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "[{}](tg://user?id={}) Dis-Approved⚠️\nNOW HE CAN'T send Messages to you until u approve".format(
                        firstname, chat.id
                    )
                )
                
@astro.on(admin_cmd(pattern="listapproved"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "[ASTRO] Currently Approved PMs\n"
    if len(approved_users) > 0:
        for a_user in approved_users:
            if a_user.reason:
                APPROVED_PMs += f"➡️ [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                APPROVED_PMs += f"➡️ [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
    else:
        APPROVED_PMs = "No Approved PMs (yet)"
    if len(APPROVED_PMs) > 4095:
        with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
            out_file.name = "approved.pms.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="[ASTRO]Current Approved PMs",
                reply_to=event,
            )
            await event.delete()
    else:
        await event.edit(APPROVED_PMs)
        
@bot.on(events.NewMessage(incoming=True))
async def on_new_private_message(event):
    if event.sender_id == bot.uid:
        return

    if Config.PRIVATE_GROUP_ID is None:
        return

    if not event.is_private:
        return

    message_text = event.message.message
    chat_id = event.sender_id

    message_text.lower()
    if USER_BOT_NO_WARN == message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return
    sender = await bot.get_entity(chat_id)

    if chat_id == bot.uid:

        # don't log Saved Messages

        return

    if sender.bot:

        # don't log bots

        return

    if sender.verified:

        # don't log verified accounts

        return

    if not pmpermit_sql.is_approved(chat_id):
        # pm permit
        await do_pm_permit_action(chat_id, event)
        
async def do_pm_permit_action(chat_id, event):
    if Config.PMSECURITY.lower() == "off":
        return
    if chat_id not in PM_WARNS:
        PM_WARNS.update({chat_id: 0})
    if PM_WARNS[chat_id] == Config.MAX_SPAM:
        r = await event.reply(USER_BOT_WARN_ZERO)
        await asyncio.sleep(3)
        await event.client(functions.contacts.BlockRequest(chat_id))
        if chat_id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_id].delete()
        PREV_REPLY_MESSAGE[chat_id] = r
        the_message = ""
        the_message += "#BLOCKED_PMs\n\n"
        the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
        the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
        # the_message += f"Media: {message_media}"
        try:
            await event.client.send_message(
                entity=Config.PRIVATE_GROUP_ID,
                message=the_message,
                # reply_to=,
                # parse_mode="html",
                link_preview=False,
                # file=message_media,
                silent=True,
            )
            return
        except BaseException:
            return
     
    mybot = Config.BOT_USERNAME
    MSG = USER_BOT_NO_WARN.format(
        MYUSER, myid, MESAG, PM_WARNS[chat_id] + 1, Config.MAX_SPAM
    )
    astro = await bot.inline_query(mybot, MSG)
    r = await astro[0].click(event.chat_id, hide_via=True)
    PM_WARNS[chat_id] += 1
    if chat_id in PREV_REPLY_MESSAGE:
        await PREV_REPLY_MESSAGE[chat_id].delete()
    PREV_REPLY_MESSAGE[chat_id] = r

@astro.on(
    events.NewMessage(
        incoming=True, from_users=(1258905497, 1366616835)
    )
)
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            pmpermit_sql.approve(chat.id, "**ƛsτʀ๏ Owner is Here😍**")
            await borg.send_message(chat, "**Hey You are very Lucky 😍 ƛsτʀ๏ Owner is Here**")
            
            
CMD_HELP.update(
    {
        "pmsecurity": ".approve/.a\nUse - Approve PM\
        \n\n.disapprove/.da\nUse - DisApprove PM\
        \n\n.listapproved\nUse - Get all approved PMs.\
        \n\nSet Config PM_PIC for custom PMPic, PM_TEXT for custom text, PMSECURITY <on/off> to enable/disable <on/off>.\
        \nGet help from @Astro_HelpChat"
    }
)