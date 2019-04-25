#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import os

import config
import methods


###################
# Answer cmds def #
###################

def answer_cmds(self, room = None, pm = None, args = None,
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

############
# Commands #
############

    if cmd in ["ev", "eval"]:
      if username in config.globals_v.evalp:
        if args:
          html = False
          locals().update( globals() )
          try:
            answer = str( eval( args, locals() ) )
          except Exception as ev:
            try:
              answer = str( exec( args, locals(), globals() ) )
            except Exception as ex:
              if str( ev ) == str( ex ):
                err = ev
              else:
                err = "{}, {}".format( ev, ex )
              answer = "Eval Error: {}".format( err )

    elif cmd in ["ex", "exec"]:
      if username in config.globals_v.evalp:
        if args:
          html = False
          locals().update( globals() )
          try:
            answer = str( exec( args, locals(), globals() ) )
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
          answer = "Error: {}".format( str( e ) )

    elif cmd in ["megach"]:
      if username in config.globals_v.evalp:
        try:
          a_megach = config.files.megach_update()
          answer = a_megach
        except Exception as e:
          answer = "Error: {}".format( str( e ) )

    elif cmd in ["cmd", "cmds", "comandos", "commands"]:
      try:
        if dic["lang"] == "en":
          cmds = "lang roomlang nick simi join leave yt gis".split()
        elif dic["lang"] == "es":
          cmds = "lang salalang nick simi conecta desconecta yt gis".split()
        answer = ", ".join( sorted( cmds ) ).title()
      except Exception as e:
        answer = "Error: {}".format( str( e ) )

    elif cmd in ["lang"]:
      try:
        t = config.database.take_lang_user( dic["lang"], "set_change_lang_user" )
        b = ", ".join(list(config.database.langs["for_users"].keys()))
        if args:
          c = config.database.set_lang_user( username, args.split()[0] )
          if c is True:
            change = t[0].format( args.split()[0].title() )
          else:
            change = t[1].format( b.title() )
        else:
          change = t[1].format( b.title() )
        answer = change
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["rlang", "roomlang", "langr", "slang", "salalang", "langs"]:
      try:
        t = config.database.take_lang_user( dic["lang"], "set_change_lang_room" )
        if roomname is not pmname:
          b = ", ".join(list(config.database.langs["for_users"].keys()))
          if args:
            c = config.database.set_lang_room( roomname, args.split()[0] )
            if c is True:
              change = t[0].format( args.split()[0].title() )
            else:
              change = t[1].format( b.title() )
          else:
            change = t[1].format( b.title() )
          answer = change
        else:
          answer = t[2]
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["nick"]:
      try:
        answer = config.database.set_nick_user( dic["lang"], username, args )
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
          if a in dict(config.database.rooms):
            if a not in self.roomnames:
              self.joinRoom( a )
              answer = t[1]
            if a in dict(config.database.rooms) and a in self.roomnames:
              answer = t[5]
          else:
            r_ex = config.tools.room_user_unknow( a )
            if r_ex is "room" and r_ex is not False:
              self.joinRoom( a )
              config.database.new_room(a)
              answer = t[2]
            else:
              answer = t[3]
        else:
          answer = t[4]
      except Exception as e:
        answer = "Error: {}".format( e )

    elif cmd in ["desconecta", "disconnect", "leave"]:
      try:
        t = config.database.take_lang_user( dic["lang"], "leave_room_answer" )
        a = args.split()[0].lower() if args else ""
        a = a.lstrip( " " ).rstrip( " " )
        if a:
          if a in dict(config.database.rooms) or a in self.roomnames:
            if a == roomname:
              answer = t[0]
              self.setTimeout( 3, self.leaveRoom, a )
              self.setTimeout( 4, config.database.erase_room, a )
            elif a in dict(config.database.rooms):
              if a not in self.roomnames:
                config.database.erase_room(a)
                answer = t[0]
              if a in dict(config.database.rooms) and a in self.roomnames:
                self.leaveRoom( a )
                config.database.erase_room( a )
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
      if roomname is not pmname:
        answer = "Hello."
      else:
        answer = "bye, o.o not available in pm"

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