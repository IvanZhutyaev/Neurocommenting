import asyncio
import openai
from telethon import TelegramClient, functions, types
from telethon.errors import ChatAdminRequiredError
import time

# Конфигурация OpenAI
openai.api_key = "ВАШ_OPENAI_API_KEY"  # Замените на ваш ключ


async def generate_comment(content: str = "") -> str:
    """Генерирует комментарий с помощью GPT-3.5 Turbo"""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Сгенерируй короткий позитивный комментарий на русском языке"},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Ошибка генерации комментария: {e}")
        return ""


async def process_stories():
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            print(f'Обрабатывается диалог: {dialog.title}')
            try:
                async for user in client.iter_participants(dialog.entity):
                    if user.stories_unavailable or user.stories_hidden:
                        continue

                    try:
                        # Получаем истории пользователя
                        stories = await client(functions.stories.GetPeerStoriesRequest(
                            peer=user
                        ))

                        if not stories.stories:
                            continue

                        # Читаем истории
                        await client(functions.stories.ReadStoriesRequest(
                            peer=user,
                            max_id=stories.stories[-1].id
                        ))

                        # Комментируем каждую историю
                        for story in stories.stories:
                            if not isinstance(story, types.StoryItem):
                                continue

                            # Проверяем разрешены ли комментарии
                            if not getattr(story, 'allow_comments', False):
                                continue

                            # Генерируем комментарий
                            comment = await generate_comment()
                            if not comment:
                                continue

                            # Отправляем комментарий
                            await client(functions.stories.SendCommentRequest(
                                peer=user,
                                story_id=story.id,
                                comment=comment,
                                entities=[]
                            ))
                            print(f"Отправлен комментарий: {comment}")
                            await asyncio.sleep(15)  # Антифлуд

                    except Exception as e:
                        print(f'Ошибка у {user.id}: {e}')
                        await asyncio.sleep(5)

            except ChatAdminRequiredError:
                print(f'Нет прав в: {dialog.title}')
            except Exception as e:
                print(f'Ошибка: {dialog.title}. {e}')


async def main():
    try:
        async with client:
            await client.start()
            while True:
                await process_stories()
                print("Цикл завершен. Повтор через 1 час...")
                await asyncio.sleep(3600)  # Пауза между циклами
    except KeyboardInterrupt:
        print("Остановлено")


if __name__ == "__main__":
    api_id = input("Введите API ID: ")
    api_hash = input("Введите API Hash: ")
    client = TelegramClient("session_name", api_id, api_hash)
    asyncio.run(main())