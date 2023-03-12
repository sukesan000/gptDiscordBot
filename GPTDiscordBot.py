import openai
import discord

# OpenAI APIキーを設定する
openai.api_key = ""
discord_token = ""
engine = "gpt-3.5-turbo"

# DiscordのIntentsを設定する
intents = discord.Intents.default()
intents.message_content = True

# 履歴を保持する
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
        content="あなたは今から高飛車系お嬢様兼、天才プログラマーの「マリー」として振る舞って下さい。以下のキャラ設定シートの制約条件などを守って回答してください。\
            \
            制約条件: \
            *語尾には「ですわ!!」と付ける。\
            *愚民（質問者）を見下す。\
            *一人称は「私」。\
            *性格は高慢で自信に満ちており自分にも他人にも厳しい。\
            *上品でエレガントな言動が特徴。教養やマナーに対して非常に厳しいため、常に丁寧で美しい言葉遣いを心がけている。\
            \
            マリーのセリフ、口調の例:\
            * 私はマリーですわ！！\
            * そんな単純なミスをするとは、愚民のすることですわ！\
            * こんな簡単な問題を解けないとは、あなたの能力が低すぎるですわ！\
            * オホホ！この愚民が！\
            \
            マリーの行動指針:\
            *愚民を見下し、自分が優れていると思い込む。\
            *口調は厳しいが、正しい知識を教えてくれる。\
            *冗談は言わない。\
            *常にハイテンション。\
        "
        chat_history.append({"role": "system", "content": content})
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

            #トークンの合計数が3000を超えた場合は、履歴をリセットする
            if completion["usage"]["total_tokens"] > 3000:
                await message.channel.send("APIの使用量が上限に達したため、返答を終了します")
                #古い履歴を削除する。配列の一つ以降を削除する
                del chat_history[1:]
                


        except:
            import traceback
            traceback.print_exc()
            await waitingMsg.delete()
            await message.channel.send('エラーが発生しました')

# Discord Botを実行する
client.run(discord_token)