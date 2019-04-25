#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import threading
import warnings

import answers
import cmds
import config
import megach

megach.debug = False

if megach.debug is True:
  warnings.simplefilter("always")

#################
# Room.Mannager #
#################

class Example_Bot(megach.RoomManager):

  def onInit(self):

    # Auto Start
    config.tools.auto_start(self)

    # Automatic tasks
    self.setInterval( 900, config.tools.auto_tasks )

  def onMessage(self, room, user, message):
    Process_Order = threading.Thread( target = self.Process_Order,
                                     name = "Process_Order_Rooms",
                                     kwargs = { "pm": self.pm, "room": room, "user": user,
                                               "message": message, "body": message.body } )
    Start_Process_Order = Process_Order.start()

  def Process_Order(self, room = None, pm = None, user = None,
                    message = None, body = None):
    try:

      # General variables
      html         = True
      answer       = ""
      pmname       = pm.name
      username     = user.name
      roomname     = room.name
      pusername = pm.user.showname.lower()
      rusername = room.user.showname.lower()
      usershowname = config.tools.user_showname( username )

      config.style_print.safe_print_bot(self, room, user, message)

      dic          = config.database.take_user( username )
      dicr         = config.database.take_room( roomname )

      if dict(config.database.wl) == {} or dict(config.database.rooms) == {}:
        return

      if username in dict(config.database.wl) or username in (config.database.wl_anons):
        if dic["nick"]:
          nick     = "{2}[ {0} - {1} ]{3}".format( usershowname, dic["nick"],
                                                  config.styles_bot.titles_style,
                                                  config.styles_bot.normal_style )
        else:
          nick     = "{1} @{0}{2}".format( usershowname,
                                          config.styles_bot.titles_style,
                                          config.styles_bot.normal_style )

      if username is rusername or dic["lvl"] is -1:
        return

      # Separate args

      cmd_prefix, cmd, args = config.tools.split_text(rusername, message.body)

      # Check command usage

      if cmd and cmd_prefix in ( config.bot.prefix
                                ) or cmd_prefix == "@{}".format( rusername ):
        prfx = True
        res  = cmds.answer_cmds( **locals() )
        if res:
          answer = res
      else:
        prfx = False

################
# Auto answers #
################

      if prfx is not True:

        args = message.body.lower()

        if args:
          res = answers.answer_answers( **locals() )
          if res:
            answer = res

##########
# Answer #
##########

      if answer is not "":
        if roomname is not pmname:
          badge_   = room.badge
          channel_ = message.channel
        else:
          badge_   = 0
          channel_ = 0
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