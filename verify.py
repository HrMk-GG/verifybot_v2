import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")
VERIFY_ROLE_ID = int(os.environ.get("VERIFY_ROLE_ID"))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ----- ボタン View -----
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # FAQリンクボタン
        self.add_item(discord.ui.Button(
            label="FAQ",
            style=discord.ButtonStyle.link,
            url="https://sites.google.com/view/zatudan-server-verifybot/faq"
        ))

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(VERIFY_ROLE_ID)
        if role in interaction.user.roles:
            await interaction.response.send_message("✅ すでに認証済みです！", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("🎉 認証が完了しました！", ephemeral=True)

# ----- Bot 起動時 -----
@bot.event
async def on_ready():
    print(f"{bot.user} でログインしました！")

    channel = bot.get_channel(CHANNEL_ID)
    # message_id.txt に以前送ったメッセージIDがあれば再セット
    try:
        with open("message_id.txt", "r") as f:
            msg_id = int(f.read().strip())
            msg = await channel.fetch_message(msg_id)
            await msg.edit(view=VerifyView())
            print("既存の認証パネルを復元しました。")
    except FileNotFoundError:
        print("message_id.txt が見つかりません。")
    except discord.NotFound:
        print("保存されたメッセージが見つかりません。")

# ----- スラッシュコマンドで送信 -----
@bot.tree.command(name="sendverify", description="認証パネルを送信します")
async def sendverify(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔐 みんなで雑談！へようこそ！",
        description=(
            "このサーバーを利用するには、まず認証が必要です。\n\n"
            "• **Verify** を押して認証を始めよう！\n"
            "• **FAQ** ボタンで詳しい説明を確認できます。"
        ),
        color=0x2F3136
    )
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3064/3064197.png")
    view = VerifyView()

    await interaction.response.send_message(embed=embed, view=view)
    msg = await interaction.original_response()
    
    # 送信したメッセージIDを保存
    with open("message_id.txt", "w") as f:
        f.write(str(msg.id))
    print("認証パネルを送信して message_id.txt に保存しました。")

# --- ファイルの一番下に追加 ---
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# ----- Bot 起動 -----
bot.run(TOKEN)
