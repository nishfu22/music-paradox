import random

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import ASSISTANT_PREFIX, SUDOERS, app, random_assistant
from Yukki.Database import get_assistant, save_assistant
from Yukki.Utilities.assistant import get_assistant_details

__MODULE__ = "Assistant"
__HELP__ = f"""


/checkassistant
- Periksa asisten yang ditentukan untuk obrolan Anda


**Note:**
- Hanya untuk Pengguna Sudo

{ASSISTANT_PREFIX[0]}block [ Reply to a User Message] 
- Memblokir Pengguna dari Akun Asisten.

{ASSISTANT_PREFIX[0]}unblock [ Reply to a User Message] 
- Buka blokir Pengguna dari Akun Asisten.

{ASSISTANT_PREFIX[0]}approve [ Reply to a User Message] 
- Menyetujui Pengguna untuk DM.

{ASSISTANT_PREFIX[0]}disapprove [ Reply to a User Message] 
- Menolak Pengguna untuk DM.

{ASSISTANT_PREFIX[0]}pfp [ Reply to a Photo] 
- Mengubah PFP akun Asisten.

{ASSISTANT_PREFIX[0]}bio [Bio text] 
- Mengubah Bio Akun Asisten.

/changeassistant [ASS NUMBER]
- Ubah asisten yang dialokasikan sebelumnya menjadi yang baru.

/setassistant [ASS NUMBER or Random]
- Setel akun asisten untuk mengobrol. 
"""


ass_num_list = ["1", "2", "3", "4", "5"]


@app.on_message(filters.command("changeassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**Usage:**\n/changeassistant [ASS_NO]\n\nSelect from them\n{' | '.join(ass_num_list)}"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    num = message.text.split(None, 1)[1].strip()
    if num not in ass_num_list:
        return await message.reply_text(usage)
    ass_num = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Asisten Pra-Tersimpan Tidak Ditemukan.\n\nAnda dapat mengatur Asisten Via /setassistant"
        )
    else:
        ass = _assistant["saveassistant"]
    assis = {
        "saveassistant": ass_num,
    }
    await save_assistant(message.chat.id, "assistant", assis)
    await message.reply_text(
        f"**Mengubah Asisten**\n\nMengubah Akun Asisten dari **{ass}** ke Nomor Asisten **{ass_num}**"
    )


ass_num_list2 = ["1", "2", "3", "4", "5", "Random"]


@app.on_message(filters.command("setassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**Usage:**\n/setassistant [ASS_NO or Random]\n\nSelect from them\n{' | '.join(ass_num_list2)}\n\nUse 'Random' to set random Assistant"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    query = message.text.split(None, 1)[1].strip()
    if query not in ass_num_list2:
        return await message.reply_text(usage)
    if str(query) == "Random":
        ran_ass = random.choice(random_assistant)
    else:
        ran_ass = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        await message.reply_text(
            f"**__Venz Asisten Bot Musik Diberikan__**\n\nAsisten No. **{ran_ass}**"
        )
        assis = {
            "saveassistant": ran_ass,
        }
        await save_assistant(message.chat.id, "assistant", assis)
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"Nomor Asisten Tersimpan Sebelumnya {ass} Found.\n\nAnda dapat mengubah Asisten Via /changeassistant"
        )


@app.on_message(filters.command("checkassistant") & filters.group)
async def check_ass(_, message: Message):
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Asisten Pra-Tersimpan Tidak Ditemukan.\n\nAnda dapat mengatur Asisten Via /play"
        )
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"Asisten yang Disimpan Sebelumnya Ditemukan\n\nNomor Asisten {ass} "
        )
