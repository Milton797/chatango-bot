#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import time
import megach
import config

####################
#   Special_Defs   #
####################

################################################## For_Rooms ##################################################

def onConnect(self, room):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_connect" )
    print( text.format( config.style_print.time_now()[0],
                       config.style_print.user_room_style( room.name.title() ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onDisconnect(self, room):
  try:
    if not self._running:
      return
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_disconnect" )
    print( text.format( config.style_print.time_now()[0],
                       config.style_print.user_room_style( room.name.title() ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onReconnect(self, room):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_reconnect" )
    print( text.format( config.style_print.time_now()[0],
                       config.style_print.user_room_style( room.name.title() ),
                       room.attempts ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onLoginFail(self, args):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_login_fail" )
    if args.name is not self.pm.name:
      if args.name in config.database.rooms:
        config.database.erase_room( args.name )
        status_deleted = True
      else:
        status_deleted = False
    else:
      status_deleted = text[2].format( args.name )
    print( text[0].format( config.style_print.time_now()[0],
                          config.style_print.user_room_style( args.name.title() ),
                          text[1][0] if status_deleted is not False else text[1][1] ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onLoginRequest(self, room):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_login_request" )
    print( text.format( config.style_print.time_now()[0],
                       config.style_print.user_room_style( room.name.title() ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onJoin(self, room, user, ssid):
  try:
    if config.bot.see_users_p is True:
      text = config.database.take_lang_bot( config.bot.bot_lang, "on_join" )
      print( text.format( config.style_print.time_now()[0],
                         config.style_print.user_room_style( room.name.title() ),
                         config.style_print.user_room_style( config.tools.user_showname( user.name ) ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onLeave(self, room, user, ssid):
  try:
    if config.bot.see_users_p is True:
      text = config.database.take_lang_bot( config.bot.bot_lang, "on_leave" )
      print( text.format( config.style_print.time_now()[0],
                         config.style_print.user_room_style( room.name.title() ),
                         config.style_print.user_room_style( config.tools.user_showname( user.name ) ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onAnonJoin(self, room, user, ssid):
  try:
    if config.bot.see_anons_p is True:
      text = config.database.take_lang_bot( config.bot.bot_lang, "on_anon_join" )
      print( text.format( config.style_print.time_now()[0],
                         config.style_print.user_room_style( room.name.title() ),
                         config.style_print.user_room_style( config.tools.user_showname( user.name ) ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onAnonLeave(self, room, user, ssid):
  try:
    if config.bot.see_anons_p is True:
      text = config.database.take_lang_bot( config.bot.bot_lang, "on_anon_leave" )
      print( text.format( config.style_print.time_now()[0],
                         config.style_print.user_room_style( room.name.title() ),
                         config.style_print.user_room_style( config.tools.user_showname( user.name ) ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onUserLogin(self, room, user, puid):
  try:
    if config.bot.see_users_p is True:
      text = config.database.take_lang_bot( config.bot.bot_lang, "on_user_login" )
      print( text.format( config.style_print.time_now()[0],
                         config.style_print.user_room_style( room.name.title() ),
                         config.style_print.user_room_style( config.tools.user_showname( user.name ) ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onUserLogout(self, room, user, puid):
  try:
    if config.bot.see_users_p is True:
      text = config.database.take_lang_bot( config.bot.bot_lang, "on_user_logout" )
      print( text.format( config.style_print.time_now()[0],
                         config.style_print.user_room_style( room.name.title() ),
                         config.style_print.user_room_style( config.tools.user_showname( user.name ) ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onAnonLogin(self, room, user, ssid):
  try:
    if config.bot.see_anons_p is True:
      text = config.database.take_lang_bot( config.bot.bot_lang, "on_anon_login" )
      print( text.format( config.style_print.time_now()[0],
                         config.style_print.user_room_style( room.name.title() ),
                         config.style_print.user_room_style( config.tools.user_showname( user.name ) ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onMessageDelete(self, room, user, message):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_message_delete" )
    u    = config.tools.user_showname( user.name )
    print( text.format( config.style_print.time_now()[0],
                       config.style_print.user_room_style( room.name.title() ),
                       config.style_print.user_room_style( u ), message.body ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onDeleteUser(self, room, user, msgs):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_message_delete_user" )
    u    = config.tools.user_showname( user.name )
    print( text.format( config.style_print.time_now()[0],
                       config.style_print.user_room_style( room.name.title() ),
                       config.style_print.user_room_style( u ),
                       "\n".join( [ "【%s】┇【%s】┇【%s】┇【%s】: %s" %
                                 ( time.strftime( "%I:%M:%S:%p┇%d/%m/%Y", time.localtime( x.time ) ),
                                  config.style_print.user_room_style( x.room.name.title() ),
                                  config.style_print.user_room_style( config.tools.user_showname( x.user.name ) ),
                                  config.style_print.channel_tipe( x ),
                                  x ) for x in reversed( msgs ) ] ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onFloodWarning(self, room):
  try:
    dic  = config.database.take_room( room.name )
    text = config.database.take_lang_room( dic["lang"], "on_flood_warning" )
    if room.name is not pm.name:
      room.setSilent( True )
      self.setTimeout( 30, room.setSilent, False )
      self.setTimeout( 31, room.message, text[0], True )
    else:
      print( t[1] )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onFloodBan(self, room, tiempo):
  try:
    text  = config.database.take_lang_bot( config.bot.bot_lang, "on_flood_ban" )
    print( text[0].format( config.style_print.time_now()[0],
                          config.style_print.user_room_style( room.name.title() ),
                          config.tools.convert_time( config.bot.bot_lang, tiempo, 3 ) ) )
    self.setTimeout( tiempo, print, text[1].format( config.style_print.time_now()[0],
                    config.style_print.user_room_style( room.name.title() ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onFloodBanRepeat(self, room, tiempo):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_flood_ban_repeat" )
    print( text[0].format( config.style_print.time_now[0],
                          config.user_room_style( room.name.title() ),
                          config.tools.convert_time( config.bot.bot_lang, tiempo, 3 ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

################################################## For_PM ##################################################

def onPMConnect(self, pm):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_pm_connect" )
    u    = config.tools.user_showname( pm.currentname )
    print( text.format( config.style_print.time_now()[0],
                       config.style_print.user_room_style( u ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onPMDisconnect(self, pm):
  try:
    if not self._running:
      return
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_pm_disconnect" )
    u    = config.tools.user_showname( pm.currentname )
    print( text.format( config.style_print.time_now()[0],
                       config.style_print.user_room_style( u ) ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onPMMessage(self, pm, user, message):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_pm_message_online" )
    u    = config.tools.user_showname( user.name )
    print( text.format( config.style_print.time_now()[0],
                       pm.name, config.style_print.user_room_style( u ),
                       message.body ) )
    config.tools.cmdspm(self, pm, user, message)
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onPMOfflineMessage(self, pm, user, message):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_pm_message_offline" )
    u    = config.tools.user_showname( user.name )
    print( text.format( config.style_print.time_now()[0],
                       pm.name, config.style_print.user_room_style( u ),
                       message.body ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

def onPMMessageSend(self, pm, user, message):
  try:
    text = config.database.take_lang_bot( config.bot.bot_lang, "on_pm_message_send" )
    u    = config.tools.user_showname( user.name )
    print( text.format( config.style_print.time_now()[0],
                       pm.name, config.style_print.user_room_style( u ),
                       message.body ) )
  except:
    return "Error: {}".format( str( config.tools.error_def() ) )

######
#Fin #
######