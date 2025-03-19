from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def handle_message(message: Message):
    text = message.text.lower()
    if 'підписка' in text:
        await message.answer("Напишіть /subscribe для оформлення підписки.")