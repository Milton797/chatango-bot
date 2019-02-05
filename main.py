#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import example_bot
import config
import methods

import socket

#################################
# Start the bot to pv and rooms #
#################################

def main_file():

  try:

    example_bot_v = example_bot.Example_Bot( accounts = config.bot.accounts, pm = config.bot.pm_connect )

    text_i = config.database.take_lang_bot( config.bot.bot_lang, "start" )
    text_f = text_i.format( config.files.delete_pycache(), config.database.load_all() )
    print( text_f )

    for x in config.database.rooms.keys():
      if x != "for_pm":
        example_bot_v.joinRoom( x )
    example_bot_v.main()


  except socket.gaierror as e:

    print( config.database.take_lang_bot( config.bot.bot_lang, "no_conection" ) )

  except KeyboardInterrupt:

    print( config.database.take_lang_bot( config.bot.bot_lang, "keyboard_kill" ) )
    config.files.delete_pycache()
    config.database.save_all()
    config.style_print.clear_print()
    example_bot_v.setTimeout( 3, example_bot_v.stop )

if __name__ == "__main__":
  main_file()

#######
# End #
#######