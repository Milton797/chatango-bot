#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import config
import example_bot


#################################
# Start the bot to pv and rooms #
#################################

def main_file():
    example_bot_v = example_bot.ExampleBot(accounts=config.Bot.accounts, pm=config.Bot.pm_connect)
    try:
        text_i = config.Database.take_lang_bot(config.Bot.bot_lang, "start")
        text_f = text_i.format(config.Files.delete_pycache())
        print(text_f)

        # Load database.
        config.Database.load_all()

        # Start rooms.
        config.Tools.start_connections(example_bot_v, ignore_room=["for_pm"], anon_room=[])

        # Start bot.
        example_bot_v.main()
    except KeyboardInterrupt:
        config.Tools.stop_bot(example_bot_v)
    except (Exception, BaseException):
        print("Error: {}".format(str(config.Tools.error_def())))


if __name__ == "__main__":
    main_file()

#######
# End #
#######
