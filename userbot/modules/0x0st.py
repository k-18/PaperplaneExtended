# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
import requests
from os import remove as DelFile
from requests.exceptions import ConnectionError
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, BOTLOG, BOTLOG_CHATID
from userbot.events import register

"""Module for reuploading modules and another staff to 0x0.st"""

@register(outgoing=True, pattern=r'^.0x0(?: |$)([\s\S]*)')
async def oxo(st):
	reply_id = st.reply_to_msg_id

	if not reply_id:
		return await st.edit('`You must be reply to a message`')

	if reply_id:
		message = (await st.get_reply_message())
		if message.media:
			downloaded_file_name = await st.client.download_media(
				message,
				TEMP_DOWNLOAD_DIRECTORY,
			)
			try:
				requested = upload_to_0x0st(downloaded_file_name)
			except ConnectionError:
				return await st.edit('`0x0.st is unreachable now. \nPlease try again later.`')
			await st.edit(f"URL for `{downloaded_file_name}`:\n\n`{requested}`")
		else:
			return st.edit('`You must be reply to a message with` **media**')
	if BOTLOG:
		await st.client.send_message(
			BOTLOG_CHATID,
			f"0x0.st query was executed successfully.",
		)

def upload_to_0x0st(path):
	try:
		req = requests.post('https://0x0.st', files={'file': open(path, 'rb')})
	except ConnectionError:
		raise ConnectionError
	DelFile(path)
	return req.text

CMD_HELP.update({
	"0x0":
	".0x0 <reply to media or file>\n"
	"Usage: reupload your documents up to 512MB to 0x0.st and flex without cringe"
})