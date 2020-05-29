import discord
import settings
import startup
import processor

mem = startup.main_startup()
reload_count = 0
mem['reload_count'] = reload_count
client = discord.Client()

@client.event
async def on_message(message):  
    # Per the discord.py docs this is to not have the bot respond to itself
    if message.author == client.user:
        return
    #If the bot sees the command !hello we will respond with our msg string
    if message.content.startswith('%shello' % settings.COMMAND_PREFIX):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('%sbane-index' % settings.COMMAND_PREFIX):
        index = int(message.content.split(' ')[1])
        messages = processor.message_processor(processor.bane_processor(mem['banes'][index]))
        for reply in messages:
            await client.send_message(message.channel, '```%s```' % reply.message)
        # await client.send_message(message.channel, msg)
        # await client.send_message(message.channel, "is that satisfactory?")

    if message.content.startswith('%sbane' % settings.COMMAND_PREFIX):
        keyword = " ".join(message.content.split(' ')[1:])
        index = processor.search(mem['banes_index'], keyword)
        print ("Bane search keyword %s" % keyword)
        if index == None:
            await client.send_message(message.channel, 'No such bane, sorry')
            return
        bane = mem['banes'][int(index)]
        messages = processor.message_processor(processor.bane_processor(bane))
        for reply in messages:
            await client.send_message(message.channel, '```%s```' % reply.message)

    if message.content.startswith('%sboon' % settings.COMMAND_PREFIX):
        keyword = " ".join(message.content.split(' ')[1:])
        index = processor.search(mem['boons_index'], keyword)
        print ("Boon search keyword %s" % keyword)
        if index == None:
            await client.send_message(message.channel, 'No such boon, sorry')
            return
        boon = mem['boons'][int(index)]
        messages = processor.message_processor(processor.boon_processor(boon))
        for reply in messages:
            try:
                await client.send_message(message.channel, '```%s```' % reply.message)
            except:
                print(messages)
                return

    if message.content.startswith('%sfeat' % settings.COMMAND_PREFIX):
        keyword = " ".join(message.content.split(' ')[1:])
        index = processor.search(mem['feats_index'], keyword)
        print ("Feat search keyword %s" % keyword)
        if index == None:
            await client.send_message(message.channel, 'No such feat, sorry')
            return
        feat = mem['feats'][int(index)]
        messages = processor.message_processor(processor.feat_processor(feat))
        for reply in messages:
            try:
                await client.send_message(message.channel, '```%s```' % reply.message)
            except:
                print(messages)
                return

    if message.content.startswith('%snp-attack-range' % settings.COMMAND_PREFIX):
        try:
            for tmessage in processor.table_message_processor(mem['np_attack_range'], 'Non-Physical Attack Range Summary'):
                await client.send_message(message.channel, '```%s```' % tmessage.message)
        except processor.MessageTooLongException:
            await client.send_message(message.channel, 'Table content too big')

    if message.content.startswith('%smulti-target' % settings.COMMAND_PREFIX):
        try:
            for tmessage in processor.table_message_processor(mem['multi_target'], 'Multi Targeting Summary'):
                await client.send_message(message.channel, '```%s```' % tmessage.message)
        except processor.MessageTooLongException:
            await client.send_message(message.channel, 'Table content too big')

    if message.content.startswith('%scr-boon' % settings.COMMAND_PREFIX):
        try:
            for tmessage in processor.table_message_processor(mem['boon_cr'], 'Boon Challenge Rating'):
                await client.send_message(message.channel, '```%s```' % tmessage.message)
        except processor.MessageTooLongException:
            await client.send_message(message.channel, 'Table content too big')

    # if message.content.startswith('%swealth-overview' % settings.COMMAND_PREFIX):
    #     try:
    #         for tmessage in processor.table_message_processor(mem['wealth_overview'], 'Wealth Level Overview'):
    #             await client.send_message(message.channel, '```%s```' % tmessage.message)
    #     except processor.MessageTooLongException:
    #         await client.send_message(message.channel, 'Table content too big')

    if message.content == ('%shelp' % settings.COMMAND_PREFIX):
        await client.send_message(message.channel, '```%s ```' % mem['help'])

    if message.content == ('%sreload' % settings.COMMAND_PREFIX):
        global mem
        global reload_count
        if message.author.id == settings.OWNER_ID:
            await client.send_message(message.channel, 'Reloading rulebook')
            mem = startup.main_startup()
            reload_count = reload_count + 1
            mem['reload_count'] = reload_count
            await client.send_message(message.channel, 'Reloading done')
            return
        await client.send_message(message.channel, 'You are not my owner!')

    if message.content == ('%sreload-check' % settings.COMMAND_PREFIX):
        if reload_count == mem['reload_count']:
            await client.send_message(message.channel, 'all reloads completed successfully')
            return
        await client.send_message(message.channel, 'reload count mismatch %s vs %s' % (reload_count, mem['reload_count']))

@client.event
async def on_ready():  
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(settings.TOKEN)