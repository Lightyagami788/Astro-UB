
import html
from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
	
from astro.config import Config
from astro.utils import admin_cmd
import asyncio
from .. import CMD_HELP

NAME = Config.NAME
DEFAULTUSER = str(NAME) if NAME else " Astro UB"
DEFAULTUSERBIO = "astro bot OP"
if Config.PRIVATE_GROUP_ID is None:
	    BOTLOG = False
else:
	    BOTLOG = True
	    BOTLOG_CHATID = Config.PRIVATE_GROUP_ID
	
	
@astro.on(admin_cmd(pattern=r"clone (.*)"))
async def _(event):
	    if event.fwd_from:
	        return
	    reply_message = await event.get_reply_message()
	    replied_user, error_i_a = await get_full_user(event)
	    if replied_user is None:
	        await event.edit(str(error_i_a))
	        return False
	    user_id = replied_user.user.id
	    profile_pic = await event.client.download_profile_photo(
	        user_id, Config.TEMP_DOWNLOAD_DIRECTORY
	    )
	   
	    first_name = html.escape(replied_user.user.first_name)
	    
	    
	    if user_id == 1732683058:
	        await event.edit("Sorry, Not Goin To Clone @mrx6767 He Is My Dev!!")
	        await asyncio.sleep(3)
	        return
	    if user_id == 1258905497:
             await event.edit("Sorry,NEVER GOING TO CLONE @Alone_loverboy HE IS MY KING")
             await asyncio.sleep(4)
	    if first_name is not None:
	        
	        
	        first_name = first_name.replace("\u2060", "")
	    last_name = replied_user.user.last_name
	    
	    if last_name is not None:
	        last_name = html.escape(last_name)
	        last_name = last_name.replace("\u2060", "")
	    if last_name is None:
	        last_name = "⁪⁬⁮⁮⁮"
	    
	    user_bio = replied_user.about
	    if user_bio is not None:
	        user_bio = replied_user.about
	    await astro(functions.account.UpdateProfileRequest(first_name=first_name))
	    await astro(functions.account.UpdateProfileRequest(last_name=last_name))
	    await astro(functions.account.UpdateProfileRequest(about=user_bio))
	    pfile = await astro.upload_file(profile_pic) 
	    await astro(
	        functions.photos.UploadProfilePhotoRequest(pfile)  
	    )
	    await event.delete()
	    await astro.send_message(
	        event.chat_id, "**KI HALL**", reply_to=reply_message
	    )
	    if BOTLOG:
	        await event.client.send_message(
	            BOTLOG_CHATID,
	            f"#CLONED\n  I AM  [{first_name}](tg://user?id={user_id })",
	        )
	
	
@astro.on(admin_cmd(pattern=r"revert$"))
async def _(event):
	    if event.fwd_from:
	        return
	    name = f"{DEFAULTUSER}"
	    bio = f"{DEFAULTUSERBIO}"
	    n = 1
	    await astro(
	        functions.photos.DeletePhotosRequest(
	            await event.client.get_profile_photos("me", limit=n)
	        )
	    )
	    await astro(functions.account.UpdateProfileRequest(about=bio))
	    await astro(functions.account.UpdateProfileRequest(first_name=name))
	    await event.edit("succesfully reverted to your account back")
	    if BOTLOG:
	        await event.client.send_message(
	            BOTLOG_CHATID, f"#REVERT\n BOSS IS BACK IN FORM"
	        )
	
	
async def get_full_user(event):
	    if event.reply_to_msg_id:
	        previous_message = await event.get_reply_message()
	        if previous_message.forward:
	            replied_user = await event.client(
	                GetFullUserRequest(
	                    previous_message.forward.from_id
	                    or previous_message.forward.channel_id
	                )
	            )
	            return replied_user, None
	        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
	        return replied_user, None
	    input_str = None
	    try:
	        input_str = event.pattern_match.group(1)
	    except IndexError as e:
	        return None, e
	    if event.message.entities is not None:
	        mention_entity = event.message.entities
	        probable_user_mention_entity = mention_entity[0]
	        if isinstance(probable_user_mention_entity, MessageEntityMentionName):
	            user_id = probable_user_mention_entity.user_id
	            replied_user = await event.client(GetFullUserRequest(user_id))
	            return replied_user, None
	        try:
	            user_object = await event.client.get_entity(input_str)
	            user_id = user_object.id
	            replied_user = await event.client(GetFullUserRequest(user_id))
	            return replied_user, None
	        except Exception as e:
	            return None, e
	    if event.is_private:
	        try:
	            user_id = event.chat_id
	            replied_user = await event.client(GetFullUserRequest(user_id))
	            return replied_user, None
	        except Exception as e:
	            return None, e
	    try:
	        user_object = await event.client.get_entity(int(input_str))
	        user_id = user_object.id
	        replied_user = await event.client(GetFullUserRequest(user_id))
	        return replied_user, None
	    except Exception as e:
	        return None, e
	
	
CMD_HELP.update(
	    {
	        "clone": ".clone <reply to user who you want to clone.\
	    \n**Use - clone the replied user account.\
	    \n\n.revert\
	    \nUse - Reverts back to your profile which you have set in heroku.\
	    "
	    }
	)
