import discord
from discord.ext import commands
import time
from discord.ext.commands import has_permissions, MissingPermissions, BucketType
import asyncio
from async_timeout import timeout
import functools
import itertools
import math
import random
import youtube_dl
import os
import pymongo
from pymongo import MongoClient
import datetime
prefixe = ['c.', 'C.']
bot = commands.Bot(command_prefix=(prefixe), case_insensitive=True)
bot.remove_command('help')

#MENIU DE HELP

@bot.command()
async def help(ctx):
    helpembed = discord.Embed(title="Meniu Help", description="Acesta este meniul de help pentru bot-ul **Clutch**", color=0xffffff)
    helpembed.add_field(name="Comenzi", value=" - `Info` \n - `Ban` \n - `Unban` \n - `Kick` \n - `Embed` \n - `Slowmode` \n - `Clear` \n - `Join (BETA)` \n - `Leave (BETA)` \n - `Wallet` \n - `Work` \n - `Daily` \n - `Pfp` \n - `Number` \n - `Bet` \n - `Shop`", inline=False)
    await ctx.send(embed=helpembed)
    return

#BOT STATUS

@bot.event
async def on_ready():
    activity = discord.Game(name="c.help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Clutch este on!")



#PING

@bot.command()
async def ping(ctx):
    pingembed = discord.Embed(title="Pong", description=f"Pingul botului este de **{round(bot.latency*1000)} ms**", color=0xffffff)
    await ctx.send(embed=pingembed)
    return



#COMENZI DE MODERARE

 #1. BAN
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member:discord.User=None, reason="nu a fost precizat"):
    if member == None:
        banembed=discord.Embed(title="Eroare", description="Va rugam sa specificati pe cineva pentru a putea primi ban.", color=0xffffff)
        banembed.add_field(title="Exemplu:", value="c.ban @Seven#6777 / ID")
        await ctx.send(embed=banembed)
        return
    if member == ctx.message.author:
        banembedauthor=discord.Embed(title="Eroare", description="Nu va puteti acorda ban singur.", color=0xffffff)
        await ctx.send(embed=banembedauthor)
        return
    await ctx.guild.ban(member, reason=reason)
    banembed1=discord.Embed(title="Actiune", description=f"{member} a primit ban de pe server.", color=0xffffff)
    banembed1.add_field(name="Motiv:", value=f"{reason}")
    await ctx.send(embed=banembed1)
    return


@ban.error
async def ban_error(ctx, error):
    if (MissingPermissions):
        banerror=discord.Embed(title="Eroare", description="Nu ai permisiunile necesare pentru a acorda ban sau eu nu am primit permisiunile necesare pentru a acorda unban.", color=0xffffff)
        await ctx.send(embed=banerror)
        return


#2. UNBAN
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, member:discord.User=None, reason="nu a fost precizat"):
    if member == None:
        unbannone=discord.Embed(title="Eroare", description="Va rugam sa specificati pe cineva pentru a putea primi unban.", color=0xffffff)
        unbannone.add_field(name="Exemplu:", description="c.unban @Seven#6777 / ID")
        await ctx.send(embed=unbannone)
        return
    if member == ctx.message.author:
        unbanauthor=discord.Embed(title="Eroare", description="Nu va puteti acorda unban deoarece nu aveti ban.", color=0xffffff)
        await ctx.send(embed=unbanauthor)
        return
    await ctx.guild.unban(member, reason=reason)
    unbanembed=discord.Embed(title="Actiune", description=f"{member}, a primit unban.", color=0xffffff)
    unbanembed.add_field(name="Motiv:", value=f"{reason}")
    await ctx.send(embed=unbanembed)
    return


@unban.error
async def unban_error(ctx, error):
    if (MissingPermissions):
        unbanerror=discord.Embed(title="Eroare", description="Cel caruia incerci sa ii acorzi ban nu are ban de pe server, nu ai permisiunile necesare pentru a acorda unban sau eu nu am permisiunile pentru a acorda unban.", color=0xffffff)
        await ctx.send(embed=unbanerror)
        return

#3. KICK
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member:discord.User=None, reason="nu a fost precizat"):
    if member == None:
        kicknone=discord.Embed(title="Eroare", description="Va rugam sa specificati pe cineva pentru a putea primi kick.", color=0xffffff)
        kicknone.add_field(name="Eroare", value="c.kick @Seven#6777 / ID")
        await ctx.send(embed=kicknone)
        return
    if member == ctx.message.author:
        kickauthor=discord.Embed(title="Eroare", description="Nu va puteti acorda kick singur.", color=0xffffff)
        await ctx.send(embed=kickauthor)
        return
    await ctx.guild.kick(member, reason=reason)
    kickembed=discord.Embed(title="Actiune", description=f"{member} a primit kick.", color=0xffffff)
    kickembed.add_field(name="Motiv", value=f"{reason}")
    await ctx.send(embed=kickembed)
    return


@kick.error
async def kick_error(ctx, error):
    if (MissingPermissions):
        kickerror=discord.Embed(title="Eroare", description="Nu ai permisiunile necesare pentru a acorda kick sau eu nu am permisunile necesare pentru a acorda kick.", color=0xffffff)
        await ctx.send(kickerror)
        return


#EMBED
@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed(ctx, *, msg):
    txt = discord.Embed(description=msg)
    await ctx.send(embed=txt)
    return
@embed.error
async def embed_error(ctx, error):
    if (MissingPermissions):
        await ctx.send("Aceasta comanda este disponibila doar pentru cei din staff.")
        return

#SUGESTIE FILME
@bot.command()
async def msuggest(ctx, *, msuggest1):
    sugestie="Film propus:"
    msuggestembed=discord.Embed(title=sugestie, description=msuggest1, color=0xffffff)
    await ctx.message.delete()
    msg1 = await ctx.send(embed=msuggestembed)
    await msg1.add_reaction("<:like:855503256151392257>")
    await msg1.add_reaction("<:dislike:855503302376423434>")
    return

#MUSIC (ALPHA)
@bot.command()
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send("In acest moment nu te afli pe un canal de voice.")

    await ctx.author.voice.channel.connect()
    await ctx.send(f"Am intrat pe voice. Acum poti incepe sa pui niste piese.")
    return

@bot.command()
async def leave(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send("In acest moment nu te afli pe un canal de voice.")
    mevoicetrue = ctx.guild.me
    if mevoicetrue is None:
        return await ctx.send("Nu sunt conectat pe niciun canal de voice (c.join pentru a ma conecta).")
    await ctx.guild.voice_client.disconnect()
    await ctx.send(f"Am parasit canalul de voice.")
    return

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, *, numar):
    numar = int(numar)
    if numar is None:
        await ctx.send("Nu ai precizat un numar de mesaje.")
        return
    if numar==1:
        await ctx.channel.purge(limit=numar+1)
        await ctx.send("Am sters 1 mesaj.")
        return
    await ctx.channel.purge(limit=numar+1)
    await ctx.send(f"Am sters {numar} mesaje.")
    return



@bot.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, *, secunde):
    secunde=int(secunde)
    if secunde==0:
        await ctx.channel.edit(slowmode_delay=secunde)
        await ctx.send("Slowmode-ul a fost dezactivat.")
        return
    if secunde==1:
        await ctx.channel.edit(slowmode_delay=secunde)
        await ctx.send(f"Slowmode-ul a fost actualizat la {secunde} secunda.")
        return
    await ctx.channel.edit(slowmode_delay=secunde)
    await ctx.send(f"Slowmode-ul a fost actualizat la {secunde} secunde.")
    return

@bot.command()
async def number(ctx):
    x=random.randint(1,10)
    numberembed1=discord.Embed(title="Number Game", description="Informatii: Daca pica numarul 6, ai castigat, daca nu, ai pierdut. Sa incepem!!", color=0xffffff)
    numberembed1.set_image(url="https://s3.envato.com/files/126009095/Digital%20Data%20and%20Numbers%20_Preview.png")
    numberembed2=discord.Embed(title="Number Game", description="A picat numarul...", color=0x34ebdc)
    numberembed2.set_image(url="https://s3.envato.com/files/126009095/Digital%20Data%20and%20Numbers%20_Preview.png")
    numberembed3=discord.Embed(title="Number Game", description=f"Numarul care a picat este {x}.", color=0x34ebdc)
    numberembed3.set_image(url="https://s3.envato.com/files/126009095/Digital%20Data%20and%20Numbers%20_Preview.png")
    numberembedwin=discord.Embed(title="Number Game", description="Felicitari. Ai castigat!", color=0x34ebdc)
    numberembedwin.set_image(url="https://mk0fowmedia08h4dr5sf.kinstacdn.com/wp-content/uploads/2014/08/win-1024x1024.jpg")
    numberembedlose=discord.Embed(title="Number Game", description="Ne pare rau. Ai pierdut!", color=0x34ebdc)
    numberembedlose.set_image(url="https://t3.ftcdn.net/jpg/01/15/89/20/360_F_115892005_HMEE0k02qxE2PMgSoEuulFNokLEvP7kW.jpg")
    msg1 = await ctx.send(embed=numberembed1)
    await asyncio.sleep(3)
    await msg1.edit(embed=numberembed2)
    await asyncio.sleep(2)
    await msg1.edit(embed=numberembed3)
    await asyncio.sleep(1.5)
    if x == 6:
        await msg1.edit(embed=numberembedwin)
        return
    else:
        await msg1.edit(embed=numberembedlose)
        return
    return

@bot.command()
async def pfp(ctx, member: discord.Member=None):
    if member is None:
        member=ctx.author
        avatar=member.avatar_url
        embedpfpme=discord.Embed(title=f"Poza lui {member} de profil :frame_photo:")
        embedpfpme.set_image(url='{}'.format(avatar))
        await ctx.send(embed=embedpfpme)
        return

    embedpfp=discord.Embed(title=f"Poza lui {member} de profil :frame_photo:")
    embedpfp.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embedpfp)
    return


@bot.command()
async def wallet(ctx, member: discord.Member):
    cluster=MongoClient()
    db=cluster["cluster"]
    collection=db["economy"]
    author_id=ctx.author.id
    results = collection.find_one({"_id":author_id})
    results2=collection.find_one({"_id":member})
    if member is None:
        bani = results["Money"]
        walletembed2 = discord.Embed(title="Wallet", description=f"Balanta ta este de {bani} lei! \n`Poti folosi comenzile c.daily si c.work pentru a creste suma de care dispui!`", color=0xffffff)
        await ctx.send(embed=walletembed2)
        return
    if results2 is None:
        datenone2=discord.Embed(description="Userul nu are un cont bancar.", color=0xffffff)
        await ctx.send(embed=datenone2)
        return
    if results is None:
        datenone=discord.Embed(title="Cont bancar", description="O sa va cream un cont bancar imediat deoarece nu detineti unul...", color=0xffffff)
        post={"_id":author_id, "Money":100}
        collection.insert_one(post)
        walletembed1=discord.Embed(title="Wallet", description="Contul bancar a fost creat!", color=0xffffff)
        msg = await ctx.send(embed=datenone)
        await asyncio.sleep(3)
        await msg.edit(embed=walletembed1)
        return

@bot.command()
@commands.cooldown(1, 3600*24, commands.BucketType.user)
async def daily(ctx):
    cluster=MongoClient()
    db=cluster["cluster"]
    collection=db["economy"]
    x=random.randint(500,1000)
    author_id=ctx.author.id
    results=collection.find_one({"_id":author_id})
    if results is None:
        datenone111=discord.Embed(title="Cont bancar", description="Ne pare rau dar nu detii un cont bancar. Va rugam sa creati unul prin comanda c.wallet", color=0xffffff)
        await ctx.send(embed=datenone111)
        return
    bani=results["Money"]
    bonuszilnic=collection.update_one({"_id":author_id}, {"$set":{"Money":bani+x}})
    dailyembed=discord.Embed(title="Daily", description=f"Ai primit {x} lei din bonusul zilnic!", color=0xffffff)
    await ctx.send(embed=dailyembed)
    return

@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
    cluster=MongoClient()
    db=cluster["cluster"]
    collection=db["economy"]
    x=random.randint(100,600)
    author_id=ctx.author.id
    results=collection.find_one({"_id":author_id})
    if results is None:
        datenone11=discord.Embed(title="Cont bancar", description="Ne pare rau dar nu detii un cont bancar. Va rugam sa creati unul prin comanda c.wallet", color=0xffffff)
        await ctx.send(embed=datenone11)
        return
    bani=results["Money"]
    baniwork=collection.update_one({"_id":author_id}, {"$set":{"Money":bani+x}})
    joburi=['ferma', 'santier', 'fabrica', 'birou', 'studio']
    jobembed=discord.Embed(title="Work", description=f"Ai fost sa muncesti la {random.choice(joburi)} si ai primit {x} lei din munca depusa!", color=0xffffff)
    await ctx.send(embed=jobembed)
    return

@bot.command()
async def info(ctx):
    infoembed=discord.Embed(title="Info", color=0xffffff)
    infoembed.add_field(name="Limbaj de programare", value="`Python`", inline=False)
    infoembed.add_field(name="Host", value="`Heroku`", inline=False)
    infoembed.add_field(name="Versiune", value="`Versiunea 0.5.1 (BETA) (c.versiune pentru mai multe detalii despre versiune)`", inline=False)
    await ctx.send(embed=infoembed)
    return

@bot.command()
async def bet(ctx, suma):
    cluster=MongoClient()
    db=cluster["cluster"]
    collection=db["economy"]
    author_id=ctx.author.id
    raspuns=['suma', 'scadere', 'scadere1', 'scadere2']
    z=random.choice(raspuns)
    results=collection.find_one({"_id":author_id})
    if results is None:
        datenone1=discord.Embed(title="Cont bancar", description="Ne pare rau dar nu detii un cont bancar. Va rugam sa creati unul prin comanda c.wallet", color=0xffffff)
        await ctx.send(embed=datenone1)
        return
    bani=results["Money"]
    suma=int(suma)
    if bani==0:
        balanta0=discord.Embed(description="Ne pare rau dar nu ai bani pentru a paria!", color=0xffffff)
        await ctx.send(embed=balanta0)
        return
    if suma==0:
        balanta1=discord.Embed(description="Nu poti paria 0 lei!", color=0xffffff)
        await ctx.send(embed=balanta1)
        return
    if z=="suma":
        if suma>bani and suma>=2000:
            nuaibani3=discord.Embed(description="Nu detii acea suma de bani si nu poti sa pariezi mai mult de 2000 de lei. Va rugam sa reintroduceti o suma de care dispuneti si care poate fi pariata!", color=0xffffff)
            await ctx.send(embed=nuaibani3)
            return
        if suma>bani:
            nuaibani=discord.Embed(description="Nu detii acea suma de bani. Va rugam sa reintroduceti o suma de care dispuneti!", color=0xffffff)
            await ctx.send(embed=nuaibani)
            return
        if suma>=2000:
            peste2001=discord.Embed(description="Nu poti paria mai mult de 2000 de lei!", color=0xffffff)
            await ctx.send(embed=peste2001)
            return
        collection.update_one({"_id":author_id}, {"$set":{"Money":bani+suma*2}})
        tr1=collection.find_one({"_id":author_id})
        bani2=tr1["Money"]
        aicastigat=discord.Embed(title="Ai castigat", description=f"Ti-ai dublat banii!\nContul bancar: `{bani2}`", color=0xffffff)
        await ctx.send(embed=aicastigat)
        return
    if z=="scadere":
        if suma>bani and suma>=2000:
            nuaibani4=discord.Embed(description="Nu detii acea suma de bani si nu poti sa pariezi mai mult de 2000 de lei. Va rugam sa reintroduceti o suma de care dispuneti si care poate fi pariata!", color=0xffffff)
            await ctx.send(embed=nuaibani4)
            return
        if suma>bani:
            nuaibani2=discord.Embed(description="Nu detii acea suma de bani. Va rugam sa reintroduceti o suma de care dispuneti!", color=0xffffff)
            await ctx.send(embed=nuaibani2)
            return
        y=bani-suma
        if y>bani:
            preamultibani=discord.Embed(title="Ai pierdut!", description=f"Ti-ai pierdut restul banilor din contul bancar!\nContul bancar: `{bani2}`", color=0xffffff)
            await ctx.send(embed=preamultibani)
        if suma>=2000:
            peste2002=discord.Embed(description="Nu poti paria mai mult de 2000 de lei!", color=0xffffff)
            await ctx.send(embed=peste2002)
            return
        collection.update_one({"_id":author_id}, {"$set":{"Money":bani-suma}})
        tr2=collection.find_one({"_id":author_id})
        bani2=tr2["Money"]
        aipierdut=discord.Embed(title="Ai pierdut!", description=f"Ti-ai pierdut banii pariati!\nContul bancar: `{bani2}`", color=0xffffff)   
        await ctx.send(embed=aipierdut)
        return
    if z=="scadere1":
        if suma>bani and suma>=2000:
            nuaibani5=discord.Embed(description="Nu detii acea suma de bani si nu poti sa pariezi mai mult de 2000 de lei. Va rugam sa reintroduceti o suma de care dispuneti si care poate fi pariata!", color=0xffffff)
            await ctx.send(embed=nuaibani5)
            return
        if suma>bani:
            nuaibani100=discord.Embed(description="Nu detii acea suma de bani. Va rugam sa reintroduceti o suma de care dispuneti!", color=0xffffff)
            await ctx.send(embed=nuaibani100)
            return
        y=bani-suma
        if y>bani:
            preamultibani2=discord.Embed(title="Ai pierdut!", description=f"Ti-ai pierdut restul banilor din contul bancar!\nContul bancar: `{bani2}`", color=0xffffff)
            await ctx.send(embed=preamultibani2)
        if suma>=2000:
            peste20023=discord.Embed(description="Nu poti paria mai mult de 2000 de lei!", color=0xffffff)
            await ctx.send(embed=peste20032)
            return
        collection.update_one({"_id":author_id}, {"$set":{"Money":bani-suma}})
        tr2=collection.find_one({"_id":author_id})
        bani2=tr2["Money"]
        aipierdut=discord.Embed(title="Ai pierdut!", description=f"Ti-ai pierdut banii pariati!\nContul bancar: `{bani2}`", color=0xffffff)
        await ctx.send(embed=aipierdut)
        return
    if z=="scadere2":
        if suma>bani and suma>=2000:
            nuaibani100=discord.Embed(description="Nu detii acea suma de bani si nu poti sa pariezi mai mult de 2000 de lei. Va rugam sa reintroduceti o suma de care dispuneti si care poate fi pariata!", color=0xffffff)
            await ctx.send(embed=nuaibani100)
            return
        if suma>bani:
            nuaibani1001=discord.Embed(description="Nu detii acea suma de bani. Va rugam sa reintroduceti o suma de care dispuneti!", color=0xffffff)
            await ctx.send(embed=nuaibani1001)
            return
        y=bani-suma
        if y>bani:
            preamultibani21=discord.Embed(title="Ai pierdut!", description=f"Ti-ai pierdut restul banilor din contul bancar!\nContul bancar: `{bani2}`", color=0xffffff)
            await ctx.send(embed=preamultibani21)
        if suma>=2000:
            peste200231=discord.Embed(description="Nu poti paria mai mult de 2000 de lei!", color=0xffffff)
            await ctx.send(embed=peste200321)
            return
        collection.update_one({"_id":author_id}, {"$set":{"Money":bani-suma}})
        tr2=collection.find_one({"_id":author_id})
        bani2=tr2["Money"]
        aipierdut=discord.Embed(title="Ai pierdut!", description=f"Ti-ai pierdut banii pariati!\nContul bancar: `{bani2}`", color=0xffffff)
        await ctx.send(embed=aipierdut)
        return

@bet.error
async def bet_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        sumanone=discord.Embed(title="EROARE", description="Nu ai specificat ce suma doresti sa pariezi!", color=0xffffff)
        sumanone.add_field(name="Exemplu:", value="**c.bet 100**")
        await ctx.send(embed=sumanone)
        return

@bot.command()
async def shop(ctx):
    cluster = MongoClient()
    db = cluster["cluster"]
    collection = db["economy"]
    shop = db["shop"]
    author_id = ctx.author.id
    shopembed=discord.Embed(title="Shop", description="De aici puteti achizitiona mai multe bunuri!", color=0xffffff)
    shopembed.add_field(name="Pro of Money", value="**c.buy 1** (pentru a achizitona) - 2000 lei", inline=False)
    shopembed.add_field(name="Master of Money", value="**c.buy 2** (pentru a achizitona) - 5000 lei", inline=False)
    shopembed.add_field(name="Boss of Money", value="**c.buy 3** (pentru a achizitona) - 10000 lei", inline=False)
    post = {"_id": author_id, "Pro Money": "no", "Boss Money": "no", "Master Money": "no"}
    await ctx.reply(embed=shopembed)
    date=shop.find_one({"_id":author_id})
    if date is None:
        shop.insert_one(post)
        return

@bot.command()
async def buy(ctx, rol):
    cluster=MongoClient()
    db=cluster["cluster"]
    collection=db["economy"]
    shop=db["shop"]
    author_id=ctx.author.id
    rol=int(rol)
    results=collection.find_one({"_id":author_id})
    if rol==1:
        if results is None:
            datenone=discord.Embed(title="Cont bancar", description="Ne pare rau dar nu detii un cont bancar. Va rugam sa creati unul prin comanda c.wallet", color=0xffffff)
            await ctx.send(embed=datenone)
            return
        bani=results["Money"]
        results1=shop.find_one({"_id":author_id})
        buyshop=results1["Pro Money"]
        if bani<2000:
            eroare=discord.Embed(description="Ne pare rau dar nu ai suficienti bani pentru a achizitiona acest rol.", color=0xffffff)
            await ctx.send(embed=eroare)
            return
        if buyshop=="yes":
            buyshopembed=discord.Embed(description="Ne pare rau dar poti achizitiona acest rol o singura data.", color=0xffffff)
            await ctx.send(embed=buyshopembed)
            return
        collection.update_one({"_id":author_id}, {"$set":{"Money":bani-2000}})
        shop.update_one({"_id":author_id}, {"$set":{"Pro Money":"yes"}})
        rol1embed=discord.Embed(description="Vi se achizitioneaza rolul...", color=0xffffff)
        rol1embededit=discord.Embed(description="Rolul a fost achizitionat si respectiv l-ati primit!", color=0xffffff)
        msg1=await ctx.send(embed=rol1embed)
        await asyncio.sleep(3)
        user=ctx.message.author
        await user.add_roles(discord.utils.get(user.guild.roles, name="Pro of Money"))
        await msg1.edit(embed=rol1embededit)
        return
    if rol==2:
        if results is None:
            datenone=discord.Embed(title="Cont bancar", description="Ne pare rau dar nu detii un cont bancar. Va rugam sa creati unul prin comanda c.wallet", color=0xffffff)
            await ctx.send(embed=datenone)
            return
        bani=results["Money"]
        results1=shop.find_one({"_id":author_id})
        buyshop=results1["Master Money"]
        if bani<5000:
            eroare=discord.Embed(description="Ne pare rau dar nu ai suficienti bani pentru a achizitiona acest rol.", color=0xffffff)
            await ctx.send(embed=eroare)
            return
        if buyshop=="yes":
            buyshopembed=discord.Embed(description="Ne pare rau dar poti achizitiona acest rol o singura data.", color=0xffffff)
            await ctx.send(embed=buyshopembed)
            return
        collection.update_one({"_id":author_id}, {"$set":{"Money":bani-5000}})
        shop.update_one({"_id":author_id}, {"$set":{"Master Money":"yes"}})
        rol1embed=discord.Embed(description="Vi se achizitioneaza rolul...", color=0xffffff)
        rol1embededit=discord.Embed(description="Rolul a fost achizitionat si respectiv l-ati primit!", color=0xffffff)
        msg1=await ctx.send(embed=rol1embed)
        await asyncio.sleep(3)
        user=ctx.message.author
        await user.add_roles(discord.utils.get(user.guild.roles, name="Master of Money"))
        await msg1.edit(embed=rol1embededit)
        return
    if rol==3:
        if results is None:
            datenone=discord.Embed(title="Cont bancar", description="Ne pare rau dar nu detii un cont bancar. Va rugam sa creati unul prin comanda c.wallet", color=0xffffff)
            await ctx.send(embed=datenone)
            return
        bani=results["Money"]
        results1=shop.find_one({"_id":author_id})
        buyshop=results1["Boss Money"]
        if bani<10000:
            eroare=discord.Embed(description="Ne pare rau dar nu ai suficienti bani pentru a achizitiona acest rol.", color=0xffffff)
            await ctx.send(embed=eroare)
            return
        if buyshop=="yes":
            buyshopembed=discord.Embed(description="Ne pare rau dar poti achizitiona acest rol o singura data.", color=0xffffff)
            await ctx.send(embed=buyshopembed)
            return
        collection.update_one({"_id":author_id}, {"$set":{"Money":bani-10000}})
        shop.update_one({"_id":author_id}, {"$set":{"Boss Money":"yes"}})
        rol1embed=discord.Embed(description="Vi se achizitioneaza rolul...", color=0xffffff)
        rol1embededit=discord.Embed(description="Rolul a fost achizitionat si respectiv l-ati primit!", color=0xffffff)
        msg1=await ctx.send(embed=rol1embed)
        await asyncio.sleep(3)
        user=ctx.message.author
        await user.add_roles(discord.utils.get(user.guild.roles, name="Boss of Money"))
        await msg1.edit(embed=rol1embededit)
        return

@bot.command()
async def versiune(ctx):
    versiuneembed=discord.Embed(title="Clutch Versiunea 0.5.1 (BETA)", color=0xffffff)
    versiuneembed.add_field(name="Shop", value="Acum botul are un shop de unde poti cumpara 3 roluri (Pro of Money, Master of Money si Boss of Money). Acest shop functioneaza doar pe server-ul G&M. Puteti folosi comanda c.shop pentru a vedea mai multe detalii, precum cat costa un rol sau cum il poti achizitiona")
    versiuneembed.add_field(name="Bet", value="Botul dispune de comanda de bet inca din versiunea 0.5 (BETA) dar s-au facut cateva mdoficari la sansa de castig deoarece se putea abuza foarte mult de aceasta comanda pentru a face bani.")
    versiuneembed.add_field(name="Buguri", value="Avand in vedere ca botul este inca in BETA, pana la iesirea versiunii 1 vor continua sa existe buguri. Am reparat o parte din ele, precum cel in care poti folsoi comenzile de economie fara a avea un cont bancar. Totusi bugul este doar o parte fixat deoarece inca vei avea cooldown chiar daca iti vei face un cont bancar. ")
    versiuneembed.add_field(name="Design", value="Am refacut mare parte din design prin embeds, inclusiv erorile deoarece unele comenzi inca nu erau facute prin embeds")
    versiuneembed.add_field(name="Ce vom avea in versiunea 0.5.2 (BETA)", value="In versiunea 0.5.2 vom reface toate erorile in cat sa fie perfect functionale pentru fiecare caz. Bineinteles ca vom mai adauga si alte lucruri asa ca folositi aceasta comanda daca doriti sa vedeti ce voi mai adauga. Fiecare idee o voi adauga aici.")
    versiuneembed.set_thumbnail(url="https://imgur.com/a/Si890AV")
    await ctx.send(embed=versiuneembed)
    return


bot.run('')
