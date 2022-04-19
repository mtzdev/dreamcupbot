import discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
import asyncio
import json
import pyrebase
from datetime import datetime

with open('settings.json', 'r') as cf:
    config = json.loads(cf.read())
    token = config['token']
    prefix = config['prefix']
    pyrecfg = config['pyrebase']
intents = discord.Intents().all()
client = commands.Bot(command_prefix = prefix, case_insensitive = True, help_command=None, intents=intents)

status = cycle(['Dreamcup League','Campeonatos de CS:GO','Developed by mtz#9765'])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_ready():
    print('Bot está online!\n')
    change_status.start()

# EVENTOS EVENTOS EVENTOS EVENTOS EVENTOS EVENTOS EVENTOS EVENTOS EVENTOS EVENTOS  
  
@client.event
async def on_member_join(member):
    cargo = get(member.guild.roles, id=717810679192748072)
    await member.add_roles(cargo)
    log = client.get_channel(717811612311879732)
    await log.send(f'**{member.mention} entrou no servidor**\nConta criada em: {member.created_at}')

@client.event
async def on_member_remove(member):
    log = client.get_channel(717811612311879732)
    await log.send(f'**{member.mention} saiu do servidor.**')

@client.event
async def on_message_delete(message):
    log = client.get_channel(886375007725436969)
    await log.send(f'**<:alerta:806352926187978793> Mensagem deletada <:alerta:806352926187978793>**\nAutor: {message.author.mention} - Canal: {message.channel.mention}\nMensagem:\n`{message.content}`')    
    
# COMANDOS COMANDOS COMANDOS COMANDOS COMANDOS COMANDOS COMANDOS COMANDOS COMANDOS     

@client.command(aliases=['info'])
@commands.guild_only()
@commands.has_any_role(717807997467885598)
async def infos(ctx, membro: discord.Member):
    await open_account(membro)
    embed = discord.Embed(color=0xff0000)
    embed.set_author(name=f'Informações de {membro}', icon_url=membro.avatar_url)
    embed.add_field(name='Nome:', value=membro.name, inline=True)
    embed.add_field(name='Discriminador:', value=membro.discriminator, inline=True)
    embed.add_field(name='ID:', value=membro.id, inline=True)
    embed.add_field(name='Conta criada em:', value=membro.created_at.strftime("%d/%m/%Y - %H:%M"), inline=True)
    embed.add_field(name='Entrou em:', value=membro.joined_at.strftime("%d/%m/%Y - %H:%M"), inline=True)
    embed.add_field(name='Banco de Dados:', value=f'Pontos: {db.child(str(membro.id)).child("Pontos").get().val()} / Wins: {db.child(str(membro.id)).child("Wins").get().val()}', inline=False)
    embed.set_thumbnail(url=membro.avatar_url)
    embed.set_footer(text=f'Solicitado por: {membro.id} - DreamCup League')
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)

@infos.error
async def infos_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention} **ERRO!** É necessário mencionar ou inserir o ID do membro para pegar suas informações.', delete_after=8.0)
        await ctx.message.delete()
        
@client.command()
@commands.guild_only()
@commands.has_any_role(717807997467885598)
async def mandarip(ctx, time1: discord.Role, time2: discord.Role, *, ipgotv: str):
    chatgeral = client.get_channel(877326085535178762)
    await chatgeral.send(f'**JOGO COMEÇANDO!**\n{time1.name} **X** {time2.name}\nIP GOTV: `{ipgotv}`')
    await ctx.message.delete()        
    
@mandarip.error
async def mandarip_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention} **ERRO!** É necessário citar o 1º time, o 2º time, e inserir o ip do gotv.', delete_after=8.0)
        await ctx.message.delete()    
        
@client.command(aliases=['register'])
@commands.guild_only()
@commands.cooldown(1,300, commands.BucketType.user)
async def registrar(ctx):
    if ctx.channel.id == 891547982950965258:
        perms = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        canal = await ctx.guild.create_text_channel(f'registro-time-{ctx.author.discriminator}', category=client.get_channel(id=883201218808266772), overwrites=perms)
        await ctx.message.delete()
        await ctx.send(f'{ctx.author.mention}, canal criado com sucesso! {canal.mention}! Lá estarão as próximas instruções!', delete_after=5.0)
        await canal.send(ctx.author.mention, delete_after=0.2)
        embed = discord.Embed(title='Registro de Times', description=f'**Olá {ctx.author.mention}!**\n\nCaso deseja **registrar** o seu time no campeonato **siga os passos abaixo**:\n\n'
        '```\n1º - Confirme que todos os membros do time estejam neste discord.\n2º - Envie o nome do time aqui\n3º - Envie o discord de todos os membros do time, incluindo reservas e coach se tiver.\n```'
        '\n\n**Após fazer isso aguarde que em breve um staff irá verificar e fazer a criação do time se tudo estiver correto.**', color=0xff0000)
        embed.set_footer(text='DreamCup League')
        embed.timestamp = datetime.utcnow()
        await canal.send(embed=embed)
    else:
        await ctx.reply(f'Você só pode executar este comando no canal <#891547982950965258>.', delete_after=6.0)
        ctx.command.reset_cooldown(ctx)
        await asyncio.sleep(6)
        await ctx.message.delete()       
        
@client.command()
@commands.guild_only()
@commands.cooldown(1,120, commands.BucketType.user)
async def suporte(ctx):
    if not ctx.channel.id == 883196216605823006:
        await ctx.reply('Você só pode executar este comando dentro do <#883196216605823006>.', delete_after=8.0)
        await ctx.message.delete(delay=8.0)
        return ctx.command.reset_cooldown(ctx)
    perms = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
    canalsup = await ctx.guild.create_text_channel(f'sup-{ctx.author.discriminator}', category = client.get_channel(id=883201218808266772), overwrites=perms)
    await ctx.message.delete()
    await ctx.send(f'{ctx.author.mention} Ticket de suporte criado! {canalsup.mention}', delete_after=3.0)
    await canalsup.send(f'{ctx.author.mention}',delete_after=0.5)
    embed = discord.Embed(title='Sistema de Tickets de Suporte', description=f'**Olá {ctx.author.mention}!\n\nDescreva sua dúvida ou seu problema abaixo\n\nEm breve um membro da staff realizará o atendimento!**', color=0xff0000)
    embed.set_footer(text='DreamCup League')
    embed.timestamp = datetime.utcnow()
    await canalsup.send(embed=embed)      
    
@client.command()
@commands.guild_only()
@commands.has_any_role(717807997467885598)
async def finalizar(ctx):
    await ctx.message.delete()
    if ctx.channel.name.startswith('sup-'):
        msgbotmotivo = await ctx.send('Insira um motivo abaixo para finalizar este ticket!\n`Você tem 60 segundos para responder`')
        try:
            motivo = await client.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            await msgbotmotivo.delete()
            await motivo.delete()
        except asyncio.TimeoutError:
            await ctx.reply('**Você demorou muito para responder**', delete_after=4.0)
            await msgbotmotivo.delete()
            return
        embed = discord.Embed(title="Ticket Finalizado!",description=f"**Ticket finalizado por: {ctx.author.mention}\n\nMotivo:\n```\n{motivo.content}\n```\nO ticket será deletado em 2 minutos automaticamente.**", color=0xff0000)
        embed.set_footer(text="DreamCup League")
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        await asyncio.sleep(120)
        await ctx.channel.delete()
    else:
        await ctx.send(f'{ctx.author.mention} Este comando só pode ser executado dentro de um ticket.', delete_after=8.0)    

@client.command()
@commands.guild_only()
@commands.has_any_role(717807997467885598)
async def criartime(ctx, membro1: discord.Member, membro2: discord.Member, membro3: discord.Member, membro4: discord.Member, membro5: discord.Member, *, nometime):
    roletime = await ctx.guild.create_role(name=nometime, mentionable=True, reason=f"Cargo de time {nometime} criado.")
    roleedicao = get(ctx.guild.roles, id=888554418142855178) # id do cargo de cada edição
    await ctx.message.delete()
    perms = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        roletime: discord.PermissionOverwrite(read_messages=True, send_messages=True)}
    for player in membro1, membro2, membro3, membro4, membro5:
        await player.add_roles(roletime)
        await player.add_roles(roleedicao)
        try: # try para evitar dm bloqueada e parada no codigo
            await player.send(f'**Você foi adicionado no time:** `{nometime}`!\n**Em breve será enviada as próximas instruções do campeonato.**\n**Caso você ache que isso seja um erro contate um staff.**')
        except discord.Forbidden:
            pass
    canaltime = await ctx.guild.create_text_channel(nometime, overwrites=perms, category= client.get_channel(id=888602889994502155))
    await canaltime.send(f'**Bem vindo a Dreamcup League!\n\nO time `{nometime}` foi registrado e já está participando do campeonato!\n\nCaso haja alguma dúvida, basta enviar neste canal que iremos te responder.**')
    await ctx.send(f'<a:sucesso:883480591276851222> {ctx.author.mention} Time {roletime} criado com êxito e players registrados com sucesso!', delete_after=3.0)

@criartime.error
async def criartime_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention} **ERRO!** É necessário mencionar os 5 membros e inserir o nome do time. Uso correto: `!criartime <membro1> <membro2> <membro3> <membro4> <membro5> Nome do time`', delete_after=10.0)
        await ctx.message.delete()              
        
@client.command()
@commands.guild_only()
async def infopause(ctx):
    await ctx.send(f'{ctx.author.mention}\nTodos os campeonatos contam com o sistema de pause dentro do jogo, e nós temos 2 tipos.\n\nPause tático: Para fins táticos, cada equipe tem 4 deles, sendo cada um 30 segundos, e para utiliza-lo basta iniciar a votação de pausa do próprio CS:GO.\n\nPause técnico: É usado para problemas tecnicos, sendo cada equipe com 5 minutos e para usa-lo basta digitar !pause no chat (Após isso informar o problema dentro do chat do jogo no discord).')

@client.command()
@commands.guild_only()
async def infocamp(ctx):
    await ctx.send(f'{ctx.author.mention}\nEste tipo de campeonato é totalmente gratuito, e as premiações são em um sistema de pontos, que funcionam assim:\n\nO campeonato terá um valor em pontos de premiação, o time que ganhar, terá os pontos divididos entre a sua equipe (a divisão é organizada de acordo com o dono responsável pelo time) e após isso você pode digitar !loja e verificar os produtos e fazer a troca pelos pontos por um produto real!\n\nPara verificar quantos pontos você tem digite !pontos.')

@client.command()
@commands.guild_only()
@commands.has_any_role(717807997467885598)
async def criarsala(ctx, time1: discord.Role, time2: discord.Role):
    msginicialbot = await ctx.send(f'**Envie a data limite para a partida! {ctx.author.mention}**')
    try:
        datamsg = await client.wait_for('message', timeout=15, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await msginicialbot.delete()
        await datamsg.delete()
    except asyncio.TimeoutError:
        await ctx.send(f'**Você demorou muito para responder** {ctx.author.mention}', delete_after=6.0)
        await msginicialbot.delete()
        return

    try:
        msglinkbot = await ctx.send(f'**Envie o link da partida {ctx.author.mention}**')
        linkmsg = await client.wait_for('message', timeout=120, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await msglinkbot.delete()
        await linkmsg.delete()
    except asyncio.TimeoutError:
        await ctx.send(f'**Você demorou muito para responder** {ctx.author.mention}', delete_after=6.0)
        await msglinkbot.delete()
        return

    perms = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        time1: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        time2: discord.PermissionOverwrite(read_messages=True, send_messages=True)}
    canaljogo = await ctx.guild.create_text_channel(f'jogo-{time1}-x-{time2}', overwrites=perms, category= client.get_channel(id=884208349200125992))
    await canaljogo.send(f'**Bem vindo! {time1.mention} {time2.mention}**\n\nEste canal foi criado para vocês marcarem a data do jogo.\n\nConversem e arrumem o melhor horário para jogar, a data limite é: **{datamsg.content}**\n\nAo decidirem um horário, marquem um CEO para mudar o horário da partida no link.\n\n**Link da partida** (necessário os 2 times se inscreverem): {linkmsg.content}\nLembrem de se inscrever com antecedência, pois 5 minutos antes do horario marcado as inscrições fecham')
    await ctx.send(f'Sala criada com sucesso. {canaljogo.mention}, com permissão para `{time1}` e `{time2}`.', delete_after=5.0)
 
@criarsala.error
async def criarsala_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention} ERRO! Uso correto: `!criarsala <time1> <time2>`', delete_after=10.0)
        await ctx.message.delete()
        
@client.command()
@commands.guild_only()
@commands.has_any_role(717807997467885598)
async def criartime2(ctx, membro1: discord.Member, membro2: discord.Member, *, nometime):
    roletime = await ctx.guild.create_role(name=nometime, mentionable=True, reason=f'Cargo do time {nometime} criado!')
    await ctx.message.delete()
    perms = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        roletime: discord.PermissionOverwrite(read_messages=True, send_messages=True)}
    for p in membro1, membro2:
        await p.add_roles(roletime)
        await ctx.send(f'Cargo atribuido a {p.mention} com sucesso! <a:sucesso:883480591276851222>', delete_after=2.0)
        try:
            await p.send(f'<a:sucesso:883480591276851222> **Você foi adicionado no time:** `{nometime}` **para o campeonato de Wingman (Braço direito)!**\n**<:alerta:806352926187978793> Em breve serão enviadas as próximas instruções, fique atento no servidor!**\n**Caso você ache que isso seja um erro contate um staff.**')
        except:
            await ctx.send(f'Mensagem privada não pode ser enviada para {p.mention} pelo possível motivo:\n- Privado bloqueado', delete_after=7.0)
    canaltime = await ctx.guild.create_text_channel(nometime, overwrites=perms, category=client.get_channel(id=888602889994502155))
    await canaltime.send(f'**Bem vindo a Dreamcup League!\n\nO time `{nometime}` foi registrado e já está participando do campeonato de braço-direito!\n\nCaso haja alguma dúvida, basta enviar neste canal que iremos te responder.**')
    await ctx.send(f'<a:sucesso:883480591276851222> {ctx.author.mention} Time {roletime} criado com êxito e players registrados com sucesso!', delete_after=3.5)
        

@client.command()
@commands.guild_only()
@commands.cooldown(1,120, commands.BucketType.user)
async def help(ctx):
    embed = discord.Embed(title="Lista de Comandos", description="**!suporte**: Faz um ticket de suporte\n**!infocamp**: Mostra as informações do campeonato atual.\n**!infopause:** Mostra as informações sobre o sistema de pause.\n**!loja**: Vê os produtos disponíveis para comprar com pontos.\n**!pontos**: Mostra quantos pontos você tem.\n**!transferir**: Transfere pontos para uma pessoa.\n**!perfil**: Mostra o seu perfil com algumas informações.", color=0xff0000)
    embed.set_footer(text='Dreamcup League')
    await ctx.send(embed=embed)
    
# ERROS ERROS ERROS ERROS ERROS ERROS

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send('Os comandos não podem ser executados no privado. <a:negado:883480639167426560>')
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'{ctx.author.mention} Você executou este comando recentemente, aguarde {error.retry_after:.0f} segundos para executar novamente.', delete_after=6.0)
        await ctx.message.delete()
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send(f'{ctx.author.mention} Você não tem permissão para executar este comando. <a:negado:883480639167426560>', delete_after=5.0)
        await ctx.message.delete()    
        
# SISTEMA DE PONTOS

configbase = pyrecfg
firebase = pyrebase.initialize_app(configbase)
db = firebase.database()

@client.command(aliases=['points', 'pontos'])
@commands.guild_only()
async def dinheiro(ctx, pessoa: discord.Member=None):
    if not pessoa:
        await open_account(ctx.author)
        quantia = db.child(str(ctx.author.id)).child("Pontos").get().val()
        await ctx.send(f'{ctx.author.mention} Você possui {quantia} pontos!')
    else:
        await open_account(pessoa)
        quantia = db.child(str(pessoa.id)).child("Pontos").get().val()
        await ctx.send(f'O {pessoa.mention} possui {quantia} pontos no momento!')
        
@client.command()
@commands.guild_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def transferir(ctx, pessoa: discord.Member, quantia: int):
    await open_account(ctx.author)
    seumoney = db.child(str(ctx.author.id)).child("Pontos").get().val()
    if seumoney < quantia:
        await ctx.send(f'{ctx.author.mention} Você não tem pontos suficiente. Seus pontos: {seumoney}.')
    elif quantia < 1:
        await ctx.send(f'{ctx.author.mention} É necessário inserir uma quantia acima de 1.')
    elif ctx.author == pessoa:
        await ctx.send(f'{ctx.author.mention} Você não pode enviar pontos para você mesmo.')
    else:
        await open_account(pessoa)
        moneypessoa = db.child(str(pessoa.id)).child("Pontos").get().val()
        valorreceber = moneypessoa + quantia
        valor = seumoney - quantia
        db.child(str(ctx.author.id)).update({"Pontos": valor}) #quem enviou
        db.child(str(pessoa.id)).update({"Pontos": valorreceber}) #quem recebeu
        #logs + msgs
        await ctx.send(f'<a:sucesso:883480591276851222> {ctx.author.mention} Você enviou {quantia} pontos para {pessoa.mention}!')
        embed = discord.Embed(title='LOG - TRANSFERENCIA', description=f'Transferencia de pontos efetuada! <:alerta:806352926187978793>\n\nEnviador: {ctx.author.mention}\nRecebedor: {pessoa.mention}\nQuantia: {quantia}\n')
        embed.set_footer(text='Logs Dreamcup')
        embed.timestamp = datetime.utcnow()
        log = client.get_channel(717811612311879732)
        await log.send(embed=embed)
        try:
            await pessoa.send(f'**Você recebeu {quantia} pontos de {ctx.author.mention} na Dreamcup League**')
        except discord.Forbidden:
            pass

@transferir.error
async def transferir_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(f'{ctx.author.mention} ERRO! É necessário citar o membro, e inserir uma quantia. Exemplo: `!transferir @membro 10`', delete_after=8.0)
        await ctx.message.delete() 
        
@client.command()
@commands.guild_only()
@commands.cooldown(1,30, commands.BucketType.user)
async def perfil(ctx, membro: discord.Member=None):
    noteam = ['Jogador', 'Capitão', 'Reserva', 'Coach', 'Silenciado', 'Server Booster', 'Campeões 1º Edição 5x5', 'Campeões 2º Edição 5x5'] # Cargos excluidos de times
    membro = ctx.author if not membro else membro
    await open_account(membro)
    pontos = db.child(str(membro.id)).child("Pontos").get().val()
    wins = db.child(str(membro.id)).child("Wins").get().val()
    cargoslist = membro.roles
    teamrole = str(cargoslist[1])
    embed = discord.Embed(color=discord.Color.gold())
    embed.set_author(name=f'Perfil de {membro}', icon_url=membro.avatar_url)
    embed.add_field(name='Pontos:', value=pontos, inline=True)  
    embed.add_field(name='Campeonatos ganhos:', value=wins, inline=True)
    embed.add_field(name='Time Atual:', value='Nenhum' if teamrole in noteam else teamrole, inline=True)
    embed.add_field(name='Entrou no servidor:', value=membro.joined_at.strftime("%d/%m/%Y - %H:%M"), inline=True)
    embed.set_thumbnail(url=membro.avatar_url)
    embed.set_footer(text='DreamCup League')
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)   

@client.command(aliases=['givarpontos', 'givepoints'])
@commands.guild_only()
@commands.has_any_role(717807997467885598)
async def givepontos(ctx, user: discord.Member, quantia: int):
    await open_account(user)
    pontoatual = db.child(str(user.id)).child("Pontos").get().val()
    db.child(str(user.id)).update({"Pontos": quantia+pontoatual})
    await ctx.send(f'Você givou {quantia} pontos para {user.mention}!')
    
@client.command(aliases=['givewin'])
@commands.guild_only()
@commands.has_any_role(717807997467885598)
async def givewins(ctx, membro: discord.Member, quantia: int):
    await open_account(membro)
    winsatuais = db.child(str(membro.id)).child("Wins").get().val()
    db.child(str(membro.id)).update({"Wins": winsatuais+quantia})
    await ctx.send(f'Você givou **{quantia}** wins para o **{membro.mention}** com sucesso!')    
    
@client.command()
@commands.guild_only()
@commands.cooldown(1,90, commands.BucketType.user)
async def loja(ctx):
    embed = discord.Embed(title="Loja Dreamcup", description="Ainda estamos adicionando mais produtos, qualquer sugestão contate um CEO.\n\nGiftcard Steam R$ 20,00: 4.500 pontos\nGiftcard Steam R$ 50,00: 10.500 pontos\nPIX R$ 25,00: 5.000 pontos\nPIX R$ 50,00: 10.000 pontos\n\nPara adquirir um produto, faça um ticket em <#883196216605823006>.", color=0xff0000)
    embed.set_footer(text='Para ver quantos pontos você tem use !pontos.')
    await ctx.send(embed=embed)    
        
# criar conta no banco de dados
async def open_account(user):
    if str(user.id) in db.child().get().val():
        return False
    db.child(str(user.id)).update({"Pontos": 0})
    db.child(str(user.id)).update({"Wins": 0})
    return True

client.run(token)
