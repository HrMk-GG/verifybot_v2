import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# --------------------------
# 環境変数から Token を取得
load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN が環境変数に設定されていません。")

# --------------------------
# インテント
intents = discord.Intents.default()
intents.members = True  # メンバー情報取得用

bot = commands.Bot(command_prefix="!", intents=intents)

# --------------------------
# 認証後に付与するロールID
VERIFY_ROLE_ID = 1429026945458507816  # 自分のサーバーIDに置き換えてね

# --------------------------
# 認証パネルボタン
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # FAQ ボタンはリンクボタン
        self.add_item(discord.ui.Button(
            label="FAQ",
            style=discord.ButtonStyle.link,
            url="https://your-faq-link"  # 自分の FAQ URL に置き換え
        ))

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(VERIFY_ROLE_ID)
        if role in interaction.user.roles:
            await interaction.response.send_message("✅ すでに認証済みです！", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("🎉 認証が完了しました！", ephemeral=True)

# --------------------------
# サーバーID（ギルドID）
GUILD_ID = 1429022740517748836  # 自分のサーバーID

@bot.event
async def on_ready():
    # ギルド単位でスラッシュコマンド同期
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"{bot.user} でログインしました！")

# --------------------------
# スラッシュコマンドで認証パネル送信
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

# --------------------------
# Bot 起動
bot.run(TOKEN)
