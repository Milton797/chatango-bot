#!/usr/bin/python
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import megach
import cmds
import config
import answers

import threading

megach.debug = False

if megach.debug is True:
  __import__("warnings").simplefilter("always")

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
    threading.Thread( target = self.Process_Order,
                     kwargs = { "pm": self.pm, "room": room, "user": user, "message": message,
                     "body": message.body } ).start()

  def Process_Order(self, room = None, pm = None, user = None, message = None, body = None):

    try:

      # General variables
      username     = user.name
      roomname     = room.name
      usershowname = config.tools.user_showname( username )
      rusername    = room.user.name
      answer       = ""
      html         = True

      print( config.style_print.print_bot( self, room, user, message ) )

      dic          = config.database.take_user( username )
      dicr         = config.database.take_room( roomname )

      if username in config.database.wl:
        if dic["nick"]:
          nick     = "{2}[{0} - {1}]{3}".format( usershowname, dic["nick"],
                                                config.styles_bot.titles_style,
                                                config.styles_bot.normal_style )
        else:
          nick     = "{1} @{0}{2}".format( usershowname,
                                          config.styles_bot.titles_stile,
                                          config.styles_bot.normal_stile )

      if username is rusername or username[0] in config.globals_v.anons or dic["lvl"] is -1:
        return

      # Separate args

      cmd_prefix, cmd, args = config.tools.split_text( message.body )

      # Check command usage

      if cmd and cmd_prefix in config.bot.prefix:
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
        config.tools.answer_room_pm( room, answer, html, user.name, message.channel )

##################
# Detector error #
##################

    except:
      return "Main.py Error: {}".format( str( config.tools.error_def() ) )

#######
# End #
#######