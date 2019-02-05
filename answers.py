#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import megach
import config

import random

import os, sys

#############################
# Answer autorespuestas Def #
#############################

def answer_answers(self, room = None, args = None, cmd = None, user = None, message = None, **kwargs):
  try:

    locals().update( kwargs )
    pm           = self.pm
    username     = user.name
    roomname     = room.name
    usershowname = config.tools.user_showname( username )
    answer       = ""
    html         = True

    if room.name is not pm.name:
      dicr       = config.database.take_room( roomname )
    else:
      dicr       = config.database.take_room( "for_pm" )
    dic          = config.database.take_user( username )

    if username in config.database.wl or username in config.database.wl_anons:
      if dic["nick"]:
        nick     = "{2}[ {0} - {1} ]{3}".format( usershowname, dic["nick"],
                                                config.styles_bot.titles_style,
                                                config.styles_bot.normal_style )
      else:
        nick     = "{1} @{0}{2}".format( usershowname,
                                        config.styles_bot.titles_style,
                                        config.styles_bot.normal_style )

################
# Auto answers #
################

    args = message.body.lower()
    
    if args:

      mention   = False
      resultado = ""

      room_pm_u = room.user.name
      room_pm_n = roomname.title()

      if roomname is not pm.name:
        simi_args = args
      else:
        simi_args = "{} {}".format( config.bot.bot_names[0], args )

      splitted  = "".join( x for x in simi_args.lower() if x.isalnum() or x in [" "] ).split()

     ######################################################

      for x in config.bot.bot_names + [ room_pm_u.lower() ]:
        if x in splitted:
          simi_petition = __import__( "re" ).sub( 
                                                  "[ ]?@\w+\: `.*?`[ ]?|[ ]?@\w+[ ]?", "", args )
          mention = True
          break

      if not mention:
        return

      if len( splitted ) is 1:
        answer = random.choice( config.database.take_lang_user( dic["lang"],
                               "call_answers") ).format( nick )

      else:
        answer = config.simi.answer_simi( simi_petition, user, nick = nick, r = "\r", 
                                         prefix  = random.choice(config.bot.prefix),
                                         prefix1 = random.choice(config.bot.prefix),
                                         name    = room_pm_u, roomn = room_pm_n )

##########
# Answer #
##########

    if answer is not "":
      config.tools.answer_room_pm( room, answer, html, user.name, message.channel )

##################
# Detector error #
##################

  except:
    return "Answers.py Error: {}".format( str( config.tools.error_def() ) )

#######
# End #
#######