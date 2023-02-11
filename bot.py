import httpx
import uuid
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes


class Image:

    def __init__(self):
        self.bot = Application.builder().token("YOUR BOT TOKEN").build()
        self.bot.add_handler(MessageHandler(filters.PHOTO | filters.ATTACHMENT, self.doc))
        self.bot.run_polling()

    async def doc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.document:
            if update.message.document.file_size < 20971520:
                name = update.message.document.file_name
                doc = await update.message.document.get_file()
                await doc.download_to_drive(f"image/{name}")
                await self.process_image(f"image/{name}", update.effective_chat.id, context)
            else:
                await context.bot.send_message(update.effective_chat.id, text="Not supporting files larger than 20MB.")

        elif update.message.photo:
            img = await update.message.photo[-1].get_file()
            image_id = str(uuid.uuid4())
            await img.download_to_drive(f"/home/host/image/{image_id}.jpg")
            await self.process_image(f"image/{image_id}.jpg", update.effective_chat.id, context)

        elif update.message.sticker:
            if update.message.sticker.file_size < 20971520:
                img = await update.message.sticker.get_file()
                image_id = str(uuid.uuid4())
                if update.message.sticker.is_video:
                    await img.download_to_drive(f"/home/host/image/{image_id}.webm")
                    await self.process_image(f"/home/host/image/{image_id}.webm", update.effective_chat.id, context)
                elif not update.message.sticker.is_animated and not update.message.sticker.is_video:
                    await img.download_to_drive(f"/home/host/image/{image_id}.webp")
                    await self.process_image(f"/home/host/image/{image_id}.webp", update.effective_chat.id, context)
                else:
                    await context.bot.send_message(update.effective_chat.id, text="Unsupported File Type.")
            else:
                await context.bot.send_message(update.effective_chat.id, text="Not supporting files larger than 20MB.")

    @staticmethod
    async def process_image(image_path, chat_id, context):
        async with httpx.AsyncClient() as client:
            with open(image_path, "rb") as f:
                response = await client.post("http://127.0.0.1:5000/img", files={"image": f})
                await context.bot.send_message(chat_id=chat_id, text=response.text)


run = Image()
