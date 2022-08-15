import os
import discord
from discord.ext import commands,tasks

import utils.discord_functions as DC_FUNC



##### DISCORD BOT
discord_config = DC_FUNC.readYaml(f"{os.path.dirname(__file__)}/discord_config.yaml")

CHECK_PROJECT_EVERY = discord_config["CHECK_PROJECT_EVERY"]

if discord_config["ACTIVE"] == True:


    TOKEN = os.getenv("DISCORD_BOXX_BOT")
    DISCORD_GUILD = discord_config["DISCORD_GUILD"]

    client = discord.Client()

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == DISCORD_GUILD:
                break

        print(f'{client.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})')


    @client.event
    async def on_ready():
        print(f'{client.user.name} has connected to Discord!')


    @client.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    @client.event
    async def on_message(message):

        BoxBloxx = client.guilds[0]

        username = str(message.author).split("#")[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        print(f'{username}: {user_message} ({channel})')


        if message.author == client.user:
            return

        if message.channel.name == "rules":
            if user_message.lower() == "hello":
                await message.channel.send(f"hey there @{username}") 
            elif user_message.lower() == "bye":
                await message.channel.send(f"see yeah! @{username}")


        if user_message.lower() == "!hello":
            await message.channel.send(" weeeeeeeooooo!!")

# Deletes channel
        if user_message.lower() == "!delete_channel":

            if username == "LouisRossouw":

                categoryid = message.channel.category_id
                category = client.get_channel(categoryid)

                for text_channel in category.text_channels:
                    await text_channel.delete()

                for voice_channel in category.voice_channels:
                    await voice_channel.delete()

                await category.delete()


    # loop

    version = "v000"

    @tasks.loop(seconds=CHECK_PROJECT_EVERY)
    async def SYNC_projects():
        """ Runs a check on the projects every few seconds """

        # print("Project_Sync")
        channel = client.get_channel(936355472611631124)

        BoxBloxx = client.guilds[0]

        
    # GET PROJECTS FILES
        PIPEDREAM_PROJECTS = DC_FUNC.get_Projects()
    # GET DISCORD CATAGORIES
        DISCORD_CATEGORY_LIST = DC_FUNC.get_Discord_categories(BoxBloxx)
    # GET CHANNELS
        DISCORD_CHANNEL_LIST = DC_FUNC.get_Discord_channels(BoxBloxx)


    # check if pipedreams projects exists in discord channel, if not, create it.
        for project in PIPEDREAM_PROJECTS[1]:
            project_name = project.lower()
            if project_name not in DISCORD_CATEGORY_LIST:
                catagory_name = project_name

                # Create catagory if it does not exist.
                await BoxBloxx.create_category(project_name)

                channel_build_list = ["🧩dailies", "👥chat", "🔴assets", "🟠rigging" ,"🟡anim", "🟢lighting", "🔵fx", "🟣comp"]

                # # get catagory object and create channels.
                category_object = discord.utils.get(BoxBloxx.categories, name=catagory_name)
                # creates sub channels to category name
                for chan in channel_build_list:
                    await BoxBloxx.create_text_channel(chan, category=category_object, sync_permissions=True)
                
                # voice channel
                await BoxBloxx.create_voice_channel("🔊voice", category = category_object, sync_permissions=True)

                # sends message to specific channel under specific category.
                channel_id = discord.utils.get(category_object.channels, name="👥chat")
                channel = client.get_channel(channel_id.id)

                await channel.send(f"New Project added: {project_name}:fire: ")


        #####

        # Check for any new exports / captures / changes and post it to the project on discord.
        pipeline_path = PIPEDREAM_PROJECTS[0]
        project_list = PIPEDREAM_PROJECTS[1]

        for project in project_list:
            project_path = f"{pipeline_path}/{project}"
            for sub_project in os.listdir(project_path):
                sub_Project_path = (f"{project_path}/{sub_project}")

                capture_json = f"{sub_Project_path}/data/captures/capture_data.json"

                try:
                    capture_data = DC_FUNC.read_json(capture_json)
                except Exception:
                    capture_data = None
                    pass

                if capture_data != None:
                    for name in capture_data:
                        for version in capture_data[name]:
                            POSTED_TO_DISCORD = capture_data[name][version]["POSTED_TO_DISCORD"]

                            if POSTED_TO_DISCORD == False:

                                print("its false")

                                project = capture_data[name][version]["PROJECT"]
                                project_names = capture_data[name][version]["PROJECT_NAME"]
                                task = capture_data[name][version]["TASK"]
                                start_frame = capture_data[name][version]["START"]
                                end_frame = capture_data[name][version]["END"]
                                path = capture_data[name][version]["PATH"]
                                user = capture_data[name][version]["USER"]
                                comment = capture_data[name][version]["COMMENT"]

                                text = f":bust_in_silhouette: : {user}: :notepad_spiral: : {comment} \n:tools: | {project_names} \n:green_circle: | {version} \n:computer: | {task} \n:arrow_right: | {str(start_frame)}-{str(end_frame)} \n:placard: | Path: {path}"

                                for i in os.listdir(path):
                                    if i.split(".")[1] == "mp4":

                                        print(f"{path}/{i}")

                                        # # get catagory object and create channels.
                                        category_object = discord.utils.get(BoxBloxx.categories, name=project)
                                        # sends message to specific channel under specific category.
                                        channel_id = discord.utils.get(category_object.channels, name="🧩dailies")
                                        channel = client.get_channel(channel_id.id)

                                        await channel.send(text)
                                        await channel.send(file=discord.File(f"{path}/{i}"))

                                capture_data[name][version]["POSTED_TO_DISCORD"] = True
                                DC_FUNC.write_to_json(capture_json, capture_data)




                export_json = f"{sub_Project_path}/data/exports/exports.json"

                try:
                    export_data = DC_FUNC.read_json(export_json)
                except Exception:
                    export_data = None
                    pass

                if export_data != None:
                    for name in export_data:
                        for version in export_data[name]:
                            POSTED_TO_DISCORD = export_data[name][version]["POSTED_TO_DISCORD"]

                            if POSTED_TO_DISCORD == False:

                                print("its false")

                                shot_name = export_data[name][version]["SHOT"]
                                category_name = export_data[name][version]["CATEGORY"]
                                destination_dir = export_data[name][version]["DESTINATION"]
                                start_frame = export_data[name][version]["START"]
                                end_frame = export_data[name][version]["END"]
                                user = export_data[name][version]["USER"]
                                asset_path = export_data[name][version]["PATH"]

                                text = f"✅ - {category_name}_{name}_{version} - exported | {shot_name} | {destination_dir} | {start_frame} = {end_frame} | {user} | \nPath: {asset_path}"

                                # # get catagory object and create channels.
                                category_object = discord.utils.get(BoxBloxx.categories, name=project)
                                # sends message to specific channel under specific category.
                                channel_id = discord.utils.get(category_object.channels, name="🧩dailies")
                                channel = client.get_channel(channel_id.id)

                                await channel.send(text)

                                export_data[name][version]["POSTED_TO_DISCORD"] = True
                                DC_FUNC.write_to_json(export_json, export_data)





    @client.event
    async def on_ready():
        
        SYNC_projects.start()



    client.run(TOKEN)



else:
    pass