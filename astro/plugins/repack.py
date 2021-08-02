# © Astro-UB # 
import asyncio
import os

from astro import CMD_HELP, HNDLR
from astro.utils import admin_cmd, sudo_cmd


@astro.on(admin_cmd(pattern=r"repack ? (.*)", outgoing=True))
@astro.on(sudo_cmd(pattern=r"repack ? (.*)", allow_sudo=True))
async def _(event):
    a = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    b = open(input_str, "w")
    b.write(str(a.message))
    b.close()
    a = await event.reply(f"**Packing into** `{input_str}`")
    await asyncio.sleep(2)
    await a.edit(f"**Uploading** `{input_str}`")
    await asyncio.sleep(2)
    await event.client.send_file(event.chat_id, input_str)
    await a.delete()
    os.remove(input_str)


CMD_HELP.update(
    {
        "repack": ".repack <filename.extension> <reply to text>\nUse - Pack the text and send as a file."
    }
)
