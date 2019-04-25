#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import random
import re

import config


#############################
# Answer autorespuestas Def #
#############################

def answer_answers(self, room = None, pm = None, args = None,
                   cmd = None, user = None, message = None, **kwargs):
  try:

    locals().update( kwargs )
    html         = True
    answer       = ""
    pmname       = pm.name
    username     = user.name
    roomname     = room.name
    pusername = pm.user.showname.lower()
    rusername = room.user.showname.lower()
    usershowname = config.tools.user_showname( username )

    if roomname is not pmname:
      dicr       = config.database.take_room( roomname )
      badge_     = room.badge
      channel_   = message.channel
    else:
      dicr       = config.database.take_room( "for_pm" )
      badge_     = 0
      channel_   = 0
    dic          = config.database.take_user( username )

    if username in dict(config.database.wl) or username in dict(config.database.wl_anons):
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

      room_pm_u = rusername
      room_pm_n = roomname.title()

      if roomname is not pmname:
        simi_args = args
      else:
        simi_args = "{} {}".format( config.bot.bot_names[0], args )

      splitted  = "".join( x for x in simi_args.lower() if x.isalnum() or x in [" "] ).split()

     ######################################################

      for x in config.bot.bot_names + [ room_pm_u.lower() ]:
        if x in splitted:
          simi_petition = re.sub( "[ ]?@\w+\: `.*?`[ ]?|[ ]?@\w+[ ]?", "", args )
          mention = True
          break

      if not mention:
        return

      if len( splitted ) is 1:
        answer = random.choice( config.database.take_lang_user( dic["lang"],
                               "call_answers") ).format( nick )

      else:
        answer = config.simi.answer_simi( simi_petition, user, nick = nick, r = "\r",
                                         prefix  = random.choice( config.bot.prefix ),
                                         name    = room_pm_u, roomn = room_pm_n )

##########
# Answer #
##########

    if answer is not "":
      config.tools.answer_room_pm( room, answer, html, username, channel_, badge_ )

##################
# Detector error #
##################

  except:
    if roomname in config.bot.see_error_r:
      return "Main.py Error: {}".format( str( config.tools.error_def() ) )
    else:
      print( "Main.py Error: {}".format( str( config.tools.error_def() ) ) )

#######
# End #
#######