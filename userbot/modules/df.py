import io
import asyncio

from userbot import CMD_HELP, bot
from userbot.events import register
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest

async def resize_photo(photo):
	""" Resize the given photo to 512x512 """
	image = Image.open(photo)
	maxsize = (512, 512)
	if (image.width and image.height) < 512:
		size1 = image.width
		size2 = image.height
		if image.width > image.height:
			scale = 512 / size1
			size1new = 512
			size2new = size2 * scale
		else:
			scale = 512 / size2
			size1new = size1 * scale
			size2new = 512
		size1new = math.floor(size1new)
		size2new = math.floor(size2new)
		sizenew = (size1new, size2new)
		image = image.resize(sizenew)
	else:
		image.thumbnail(maxsize)

	return image

@register(outgoing=True, pattern='^.df(?: |$)(.*)')
async def arrestant(fryer):
	if fryer.fwd_from:
		return 
	if not fryer.reply_to_msg_id:
	   await fryer.edit("```Reply to any user message.```")
	   return
	reply_message = await fryer.get_reply_message() 
	if not reply_message.media:
	   await fryer.edit("```This message contains any media?????```")
	   return
	chat = "@image_deepfrybot"
	sender = reply_message.sender
	if reply_message.sender.bot:
	   await fryer.edit("```Reply to actual users message.```")
	   return
	await fryer.edit("```Processing...```")
	async with bot.conversation(chat) as conv:
		try:
			response = conv.wait_event(events.NewMessage(incoming=True,from_users=432858024))
			await bot.send_message(chat, reply_message)
			response = await response
			await bot.send_read_acknowledge(conv.chat_id)
		except YouBlockedUserError: 
			await fryer.reply("```Please unblock @image_deepfrybot and try again```")
			return
		if response.text.startswith("Forward"):
		  	await fryer.edit("```Can you kindly disable your forward privacy settings for good?```")
		else:
			async with bot.action(fryer.chat_id, 'document'):
				await asyncio.sleep(2)
				await fryer.delete()
				await bot.send_message(fryer.chat_id, response.message, reply_to=reply_message.id)

CMD_HELP.update({
	"df":
	".df <reply to media> \n"
	"Fryes your media using @image_deepfrybot"
})