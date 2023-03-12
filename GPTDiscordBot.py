import openai
import discord

# OpenAI APIキーを設定する
openai.api_key = ""
discord_token = ""
engine = "gpt-3.5-turbo"

# DiscordのIntentsを設定する
intents = discord.Intents.default()
intents.message_content = True

# 履歴を保持するS
chat_history = []

#クライアントを作成
client = discord.Client(intents=intents)

@client.event
async def on_message(message,chat_history=chat_history):

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if message.author == client.user:
        return
    
    # メッセージが「/gpt」で始まる場合は、chatGPTを実行する
    if message.content.startswith('/gpt'):
        content="日本語で返答してください"
        chat_history.append({"role": "user", "content": content})
        waitingMsg = await message.channel.send("生成中...")

        try:
            prompt = message.content[4::]
            # メッセージが空の場または「/gpt」のみの場合は、質問内容がありませんと返す
            if prompt == "" or prompt == "/gpt":
                await waitingMsg.delete()
                await message.channel.send("質問内容がありません")
                return 
            
            # メッセージが「/gpt」で始まる場合は、chatGPTを実行する
            chat_history.append({"role": "user", "content": prompt})
            completion = openai.ChatCompletion.create(
                model=engine,
                messages=chat_history,
            )
            # 回答を取得する
            ans = completion["choices"][0]["message"]["content"]
            chat_history.append({"role": "assistant", "content": ans})

            await waitingMsg.delete()
            await message.channel.send(ans)

            #トークンの合計数が3000を超えた場合は、返答を終了する
            if completion["usage"]["total_tokens"] > 3000:
                await message.channel.send("APIの使用量が上限に達したため、返答を終了します")
                chat_history = []
        except:
            import traceback
            traceback.print_exc()
            await waitingMsg.delete()
            await message.channel.send('エラーが発生しました')

# Discord Botを実行する
client.run(discord_token)