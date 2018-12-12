#!/usr/bin/python
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import megach
import config
import methods

import random

import os, sys
import xml, json
import time, datetime
import urllib.request as urlreq, urllib.parse as urlparse

###################
# Answer cmds def #
###################

def answer_cmds(self, room = None, args = None, cmd = None, user = None, message = None, **kwargs):
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
    if username in config.database.wl:
      if dic["nick"]:
        nick     = "【{2}{0} - {1}{3}】".format( usershowname, dic["nick"],
                                         config.styles_bot.titles_stile,
                                         config.styles_bot.normal_stile )
      else:
        nick     = "{1} @{0}{2}".format( usershowname,
                                 config.styles_bot.titles_stile,
                                 config.styles_bot.normal_stile )

############
# Commands #
############

    if cmd in ["ev", "eval"]:
      if username in config.globals_v.evalp:
        if args:
          html = False
          locals().update( globals() )
          try:
            answer = str( eval(args, locals() ) )
          except Exception as ev:
            try:
              answer = str( exec(args, locals() ) )
            except Exception as ex:
              if str(ev) == str(ex):
                err = ev
              else:
                err = "{}, {}".format(ev, ex)
              answer = "Eval Error: {}".format( err )

    elif cmd in ["ex", "exec"]:
      if username in config.globals_v.evalp:
        if args:
          html = False
          try:
            locals().update( globals() )
            answer = str( exec(args), locals() )
          except Exception as ex:
            answer = "Exec Error: {}".format( ex )

    elif cmd in ["reload"]:
      if username in config.globals_v.evalp:
        try:
          if args:
            a = config.tools.reload( args )
          else:
            a = config.tools.reload( "config cmds methods answers special_defs" )
            config.files.import_special_defs( self )
          answer = a
        except Exception as e:
          answer = e

    elif cmd in ["megach"]:
      if username in config.globals_v.evalp:
        try:
          a_megach = config.files.megach_update()
          answer = a_megach
        except Exception as e:
          answer = e

    elif cmd in ["cmd", "cmds", "comandos", "commands"]:
      answer = ", ".join( sorted( "lang rlang nick simi join yt gis".split() ) ).title() 

    elif cmd in ["lang"]:
      try:
        a = config.database.take_lang_user( dic["lang"], "set_change_lang_user" )
        b = ", ".join( config.database.langs["for_users"].keys() )
        if args:
          c = config.database.set_lang_user( username, args.split()[0] )
          if c is True:
            change = a[0].format( args.split()[0].title() )
          else:
            change = a[1].format( b.title() )
        else:
          change = a[1].format( b.title() )
        answer = change
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["rlang","roomlang","langr"]:
      try:
        a = config.database.take_lang_user( dic["lang"], "set_change_lang_room" )
        if roomname is not pm.name:
          b = ", ".join( config.database.langs["for_users"].keys() )
          if args:
            c = config.database.set_lang_room( roomname, args.split()[0] )
            if c is True:
              change = a[0].format( args.split()[0].title() )
            else:
              change = a[1].format( b.title() )
          else:
            change = a[1].format( b.title() )
          answer = change
        else:
          answer = a[2]
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["nick"]:
      try:
        answer = config.database.set_nick_user( user, args )
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["simi"]:
      try:
        t = config.database.take_lang_user( dic["lang"], "create_simi_answer" )
        if args:
          path = os.path.join( config.paths.u_bot, config.paths.u_simi )
          a    = config.simi.create_simi( path, args )
          if a is True:
            answer = t[0]
          else:
            answer = t[1]
        else:
          answer = t[1]
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["conecta", "join"]:
      try:
        t = config.database.take_lang_user( dic["lang"], "join_room_answer" )
        a = args.split()[0] if args else ""
        a = a.lstrip( " " ).rstrip( " " )
        if a:
          if a == roomname:
            answer = t[0]
          if a in config.database.rooms:
            if a not in self.roomnames:
              self.joinRoom( a )
              answer = t[1]
            if a in config.database.rooms and a in self.roomnames:
              answer = t[5]
          else:
            r_ex = config.tools.room_user_unknow( a )
            if r_ex is "room":
              self.joinRoom( a )
              config.database.new_room(a)
              answer = t[2]
            else:
              answer = t[3]
        else:
          answer = t[4]
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["desconecta", "disconnect"]:
      try:
        t = config.database.take_lang_user( dic["lang"], "leave_room_answer" )
        a = args.split()[0].lower() if args else ""
        a = a.lstrip( " " ).rstrip( " " )
        if a:
          if a in config.database.rooms or a in self.roomnames:
            if a == roomname:
              answer = t[0]
              self.setTimeout( 3, self.leaveRoom, a )
              self.setTimeout( 4, config.database.erase_room, a )
            elif a in config.database.rooms:
              if a not in self.roomnames:
                config.database.erase_room(room)
                answer = t[0]
              if a in config.database.rooms and a in self.roomnames:
                self.leaveRoom( a )
                config.database.erase_room(room)
                answer = t[0]
          else:
            answer = t[2]
        else:
          answer = t[1]
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["yt"]:
      try:
        t = config.database.take_lang_user( dic["lang"], "youtube_answer" )
        if args:
          answer = methods.online_defs.youtube( dic["lang"], args )
        else:
          answer = t[2]
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["gis"]:
      try:
        t = config.database.take_lang_user( dic["lang"], "gis_answer" )
        if args:
          answer = methods.online_defs.search_images( dic["lang"], args )
        else:
          answer = t[2]
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["cmd_pm_example"]:
      if roomname is not pm.name:
        answer = "Hello."
      else:
        answer = "bye, o.o not available in pm"

##########
# Answer #
##########

    if answer is not "":
      config.tools.answer_room_pm( room, answer, html, user.name, message.channel )

##################
# Detector error #
##################

  except:
    return "Cmds.py Error: {}".format( str( config.tools.error_def() ) )

#######
# End #
#######