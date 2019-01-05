#!/usr/bin/python
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import megach

import random
import shutil
import linecache

import os, sys
import xml, json
import time, datetime
import urllib.request as urlreq, urllib.parse as urlparse

try: from importlib import reload
except: reload = __import__("imp").reload

##########
# Inicio #
##########

###############################################################################################################

class bot:

  accounts    = [ ( "Acc1", "pass1" ),
                 ( "Acc2", "pass2" )     ]
  prefix      = "% &".split()
  bot_names   = "ejemplobot botsito examplebot".split()
  bot_lang    = "es en".split()[1]
  pm_connect  = True
  see_anons_p = True

###############################################################################################################

class styles_bot:

  name_color   = "000000"
  font_color   = "000000"
  font_face    = 1
  font_size    = 12
  titles_style = "<f x{}{}='{}'>".format( font_size, name_color, font_face )
  normal_style = "<f x{}{}='{}'>".format( font_size, font_color, font_face )

###############################################################################################################

class globals_v:

  evalp       = "milton797 milton megamaster12 linkkg".split()
  anons       = "! #".split()

###############################################################################################################

class paths:

  u_bot         = "{0}".format( os.path.dirname( os.path.abspath( sys.argv[0] ) ) )

  u_documents   = "{0}{2}{1}{2}".format( u_bot, "Documents", os.sep )

  u_simi        = "{}{}".format( u_documents, "simi.txt" )
  u_rooms       = "{}{}".format( u_documents, "rooms.json" )
  u_wl          = "{}{}".format( u_documents, "wl.json" )

  u_langs_file  = "{}{}".format( u_documents, "langs.json" )

###############################################################################################################

class style_print:

  def print_bot(self, room, user, message):
    text   = "[{}][{}][{}][{}]: {}"
    text_i = text
    u_sho  = tools.user_showname( user.name )
    text_f = text_i.format( style_print.time_now()[0],
                           style_print.user_room_style( room.name.title() ),
                           style_print.user_room_style( u_sho ),
                           style_print.channel_tipe( message ),
                           message.body )
    return text_f

  def user_room_style(room_user):
    return "{:_^20}".format( room_user )

  def channel_tipe(message):
    text  = "{}|{}"
    textf = text.format( {32768: "M", 2048: "B", 256: "R", 2304: "R+B", 34816: "B+M", 
                          33024: "R+M", 34816: "B+M", 33024: "R+M", 35072: "R+A+M", 0: "N"}.get( message.channel ),
                          {1: "SH", 2: "ST", 0: "N"}.get( message.badge ) )
    return textf

  def time_now():
    t = time.strftime( "%I:%M:%S:%p", time.localtime() )
    s = time.time()
    return [t, s]

  def clear_print():
    try:
      if tools.os_on() is not "Windows":
        os.system( "clear" )
      else:
        os.system( "cls" )
      text = database.take_lang_bot( bot.bot_lang, "console_cleaned" )
      print( text.format( style_print.time_now()[0] ) )
    except:
      return "Error: {}".format( str( tools.error_def() ) )

  def console_title(title):
    try:
      if tools.os_on() is not "Windows":
        if os.environ.get("TERM") in (
          "xterm",
          "xterm-color",
          "xterm-256color",
          "linux",
          "screen",
          "screen-256color",
          "screen-bce",
          ):
          sys.stdout.write( "\33]0; {} \a".format( title ) )
          sys.stdout.flush()
      else:
        os.system( "title {}".format( title ) )
      return True
    except:
      return "Error: {}".format( str( tools.error_def() ) )

###############################################################################################################

class database:

  class molds:

    Default_Wl = {
                   "lang": "en",
                   "lvl": 1,
                   "nick": ""
                 }

    Default_Wl_Anons = Default_Wl

    Default_Room = {
                     "lang": "en",
                   }

  wl       = {}
  wl_anons = {}
  rooms    = {}

  langs    = {}

  def save_wl():
    try:
      wl      = database.wl
      wl_ruta = paths.u_wl
      with open( wl_ruta, "w" ) as save_users:
        save_users.write( json.dumps( wl, indent = 4, sort_keys = True ) )
      save_users.close()
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def save_rooms():
    try:
      rooms      = database.rooms
      rooms_ruta = paths.u_rooms
      with open( rooms_ruta, "w" ) as save_room:
        save_room.write( json.dumps( rooms, indent = 4, sort_keys = True ) )
      save_room.close()
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def load_wl():
    try:
      wl      = database.wl
      wl_ruta = paths.u_wl
      with open( wl_ruta, encoding = "utf-8" ) as load_users:
        wl.update( json.load( load_users, encoding = "utf-8" ) )
      load_users.close()
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def load_langs():
    try:
      langs        = database.langs
      langs_ruta   = paths.u_langs_file
      with open ( langs_ruta, encoding = "utf-8" ) as load_all_langs:
        langs.update( json.load( load_all_langs, encoding = "utf-8" ) )
      load_all_langs.close()
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def load_rooms():
    try:
      rooms      = database.rooms
      rooms_ruta = paths.u_rooms
      with open( rooms_ruta, encoding = "utf-8" ) as load_room:
        rooms.update( json.load( load_room, encoding = "utf-8" ) )
      load_room.close()
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def save_all():
    try:
      database.save_wl()
      database.save_rooms()
      text = database.take_lang_bot(bot.bot_lang, "save_data").format( style_print.time_now()[0] )
      print( text )
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def load_all():
    try:
      database.load_wl()
      database.load_rooms()
      database.load_langs()
      text = database.take_lang_bot(bot.bot_lang, "load_data").format( style_print.time_now()[0] )
      print( text )
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def new_user(user):
    try:
      user = user.lower()
      if user not in database.wl:
        if user[0] not in "# !".split():
          database.wl.update( {user: database.molds.Default_Wl.copy()} )
          return True
      else:
        return False
    except:
      return "Error {}".format( tools.error_def() )

  def new_anon(anon):
    try:
      anon = anon.lower()
      if anon not in database.wl_anons:
        database.wl_anons.update( {anon: database.molds.Default_Wl_Anons.copy()} )
        return True
      else:
        return False
    except:
      return "Error {}".format( tools.error_def() )

  def new_room(room):
    try:
      room = room.lower()
      if room not in database.rooms:
        database.rooms.update( {room: database.molds.Default_Room.copy()} )
        return True
      else:
        return False
    except:
      return "Error {}".format( tools.error_def() )

  def erase_user(user):
    try:
      user = user.lower()
      if user in database.wl:
        del database.wl[user]
        return True
      else:
        return False
    except:
      return "Error {}".format( tools.error_def() )

  def erase_anon(anon):
    try:
      anon = anon.lower()
      if anon in database.wl_anons:
        del database.wl_anons[anon]
        return True
      else:
        return False
    except:
      return "Error {}".format( tools.error_def() )

  def erase_room(room):
    try:
      room = room.lower()
      if room in database.rooms:
        del database.rooms[room]
        return True
      else:
        return False
    except:
      return "Error {}".format( tools.error_def() )

  def update_default_user(user):
    try:
      user = user.lower()
      for x, c in database.molds.Default_Wl.items():
        if x not in database.wl[user]:
          database.wl[user][x] = c
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def update_default_anon(anon):
    try:
      anon = anon.lower()
      for x, c in database.molds.Default_Wl_Anons.items():
        if x not in database.wl_anons[anon]:
          database.wl_anons[anon][x] = c
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def update_default_room(room):
    try:
      room = room.lower()
      for x, c in database.molds.Default_Room.items():
        if x not in database.rooms[room]:
          database.rooms[room][x] = c
      return True
    except:
      return "Error {}".format( tools.error_def() )

  def take_user(user):
    try:
      user = user.lower()
      if user[0] not in globals_v.anons:
        if user not in database.wl:
          database.new_user( user )
        else:
          database.update_default_user( user )
        return database.wl[user]
      else:
        if user not in database.wl_anons:
          database.new_anon( user )
        else:
          database.update_default_anon( user )
        return database.wl_anons[user]
    except:
      return "Error {}".format( tools.error_def() )

  def take_room(room):
    try:
      room = room.lower()
      if room in database.rooms:
        database.update_default_room( room )
        return database.rooms[room]
      else:
        return False
    except:
      return "Error {}".format( tools.error_def() )

  def take_lang_bot(lang, traduction):
    try:
      if len( database.langs ) is 0:
        database.load_langs()
      langs_user_room_bot = database.langs["for_bot"]
      if lang in langs_user_room_bot and traduction in langs_user_room_bot[lang]:
        return ( langs_user_room_bot[lang][traduction] )
      else:
        text   = "No lang: {}, {}"
        text_f = text.format( repr( lang ), repr( traduction ) )
        print( text )
        return text
    except:
      return "Error {}".format( tools.error_def() )

  def take_lang_room(lang, traduction):
    try:
      if len( database.langs ) is 0:
        database.load_langs()
      langs_user_room_bot = database.langs["for_rooms"]
      if lang in langs_user_room_bot and traduction in langs_user_room_bot[lang]:
        return ( langs_user_room_bot[lang][traduction] )
      else:
        text   = "No lang: {}, {}"
        text_f = text.format( repr( lang ), repr( traduction ) )
        print( text )
        return text
    except:
      return "Error {}".format( tools.error_def() )

  def take_lang_user(lang, traduction):
    try:
      if len( database.langs ) is 0:
        database.load_langs()
      langs_user_room_bot = database.langs["for_users"]
      if lang in langs_user_room_bot and traduction in langs_user_room_bot[lang]:
        return ( langs_user_room_bot[lang][traduction] )
      else:
        text   = "No lang: {}, {}"
        text_f = text.format( repr( lang ), repr( traduction ) )
        print( text )
        return text
    except:
      return "Error {}".format( tools.error_def() )

  def set_lang_user(user, args):
    try:
      u_langs = database.langs["for_users"]
      info    = database.take_user( user )
      u_user  = database.wl
      u_anon  = database.wl_anons
      if args:
        if user in u_user or user in u_anon:
          if args in u_langs:
            info["lang"] = args.lower().split()[0]
            return True
          else:
            return False
        else:
          return False
      else:
        return None
    except:
      return "Error {}".format( tools.error_def() )

  def set_lang_room(room, args):
    try:
      u_langs = database.langs["for_rooms"]
      info    = database.take_room( room )
      u_room  = database.rooms
      if args:
        if room in u_room and args in u_langs:
          if args in u_langs:
            info["lang"] = args.lower().split()[0]
            return True
          else:
            return False
        else:
          return False
      else:
        return None
    except:
      return "Error {}".format( tools.error_def() )

  def set_nick_user(lang, user_, n_nick):
    try:
      info = database.take_user( user_ )
      t    = database.take_lang_user( lang, "nick_set_answer" )
      u_user  = database.wl
      u_anon  = database.wl_anons
      if user_ in u_user or user_ in u_anon:
        if n_nick:
          if len(n_nick) < 26:
            nick_s = info["nick"] = n_nick
            return t[0].format( tools.user_showname( user_ ) )
          else:
            return t[3]
        else:
          nick_s = info["nick"] if info["nick"] else t[1]
          return t[2].format( nick_s )
      else:
        return False
    except:
      return "Error {}".format( tools.error_def() )

###############################################################################################################

class tools:

  def error_def():
    exc_type, exc_obj, tb = sys.exc_info()
    f        = tb.tb_frame
    lineno   = tb.tb_lineno
    filename = f.f_code.co_filename
    line     = linecache.getline(filename, lineno, f.f_globals)
    if bot.bot_lang == "es":
      e      = "ARCHIVO: {} --> LÍNEA: {} --> {}: --> {}"
    else:
      e      = "FILE: {} --> LINE: {} --> {}: --> {}"
    ef       = e.format( filename, lineno, line.strip(), exc_obj )
    print(ef)
    return ef.replace("<","&lt;").replace(">","&gt;")

  def os_on():
    if os.name is not "nt":
      u = "Linux"
    else:
      u = "Windows"
    return u

  def split_text(text):
    try:
      vacio  = ""
      vacio1 = " "
      if not text:
        return vacio, vacio, vacio
      else:
        text = text.lstrip( vacio1 ).rstrip( vacio1 )

      if len( text.split( vacio1 ) ) > 1:
        cmd, args = text.split( vacio1, 1 )
      else:
        cmd, args = text, vacio
      cmd_prefix  = cmd[0]

      if len( cmd ) > 1:
        cmd = cmd[1:].lower()
      return cmd_prefix, cmd, args
    except:
      return "Error split_text {}".format( tools.error_def() )

  def cmdspm(self, pm, user, message):
    try:
      cmd_prefix, cmd, args = tools.split_text( message.body )
      room = pm
      
      if cmd and cmd_prefix in bot.prefix:
        prfx = True
      else:
        prfx = False

      # Auto answers in pm

      if prfx is not True:

        args = message.body.lower()

        if args:
          pm.message( user.name, __import__("answers").answer_answers( **locals() ), True )

      # cmds in pm

      else:
        res  = __import__("cmds").answer_cmds( **locals() )
        if res:
          pm.message( user, str( res ) )

    except:
      return "Error: {}".format( str( tools.error_def() ) )

  def answer_room_pm(room, respuesta_: str = "", html_: bool = False,
                     user_: str = "", canal_: int = 0, badge_: int = 0):
    try:
      if room.name is not "PM":
        room.message( str( respuesta_ ), html = bool( html_ ),
                     canal = int( canal_ ), badge = int( badge_ ) )
      elif room.name is "PM":
        respuesta_ = respuesta_.replace("&", "&amp;")
        room.message( str( user_ ), str( respuesta_ ),
                     html = bool( html_ ) )
    except:
      return "Error: {}".format( str( tools.error_def() ) )

  def room_user_unknow(url):
    try:
      url  = "http://{}.chatango.com/".format( url.lower() )
      data = urlreq.urlopen( url ).read().decode("utf-8")
      user = data.find( "buyer" ) > data.find( "seller" ) > 0 and 1 or 0
      if not user:
        user = data.find( "<title>Unknown User!</title>" ) < 0 < data.find( "</head>" ) and 2 or 0
      if user == 1:
        return "user"
      elif user == 2:
        return "room"
      elif not user:
        return "N/A"
    except:
      return "Error: {}".format( str( tools.error_def() ) )

  def reload(modulo):
    try:
      modulos_folder_bot = [ x.split(".")[0] for x in os.listdir(
                            paths.u_bot ) if x.endswith( ".py" ) ]
      if not modulo:
        return False
      else:
        for x in modulos_folder_bot:
          if x in modulo:
            [ ( reload( __import__( x ) ), time.sleep( 0.1 ) ) for x in modulo.split() ]
            database.load_all()
            files.delete_pycache()
            return True
        else:
          return False
    except Exception as e:
      return "Error: {}".format( str( e ) )
 
  def user_showname(user_):
    try:
      a = megach.User.get( user_ ).showname
      if user_[0] not in globals_v.anons:
        if a == user_.lower():
          f = a.title()
        else:
          f = a
      else:
        f = a.title()
      return f
    except:
      return "Error: {}".format( str( tools.error_def() ) )

  def auto_start(self):
    # Start text

    text = database.take_lang_bot( bot.bot_lang, "on_init" )
    print( text.format( style_print.time_now()[0] ) )

    # Automatic start of extra variables

    files.import_special_defs(self)
    style_print.console_title( "{}".format( bot.bot_names[1].upper() ) )

    # Ch automatic start of variables

    self.enableBg()
    self.setNameColor( styles_bot.name_color )
    self.setFontColor( styles_bot.font_color )
    self.setFontFace( styles_bot.font_face )
    self.setFontSize( styles_bot.font_size )

  def auto_tasks():
    # Task every 15 minutes

    style_print.clear_print()
    database.save_all()

###############################################################################################################

class files:

  def delete_file(u):
    if os.path.exists(u):
      try:
        os.remove(u)
        return True
      except Exception as e:
        return e
    else:
      return False

  def delete_files(u):
    if os.path.exists(u):
      try:
        [files.delete_file( "{}{}{}".format( u, os.sep, x ) ) for x in os.listdir( u )]
        return True
      except Exception as e:
        return e
    else:
      return False

  def delete_folder(u):
    if os.path.exists(u):
      try:
        files.delete_files(u)
        os.removedirs(u)
        return True
      except Exception as e:
        return e
    else:
      return False

  def delete_pycache():
    a_a = "{}{}__pycache__".format( paths.u_bot, os.sep )
    if os.path.exists( a_a ):
      try:
        files.delete_folder( a_a )
        return True
      except Exception as e:
        return e
    else:
      return False

  def import_special_defs(self):
    try:
      special_defs = __import__( "special_defs" )
      for x in [ z for z in dir( special_defs ) if callable( getattr( special_defs, z ) ) ]:
        setattr( self, x, __import__( "types" ).MethodType( getattr( special_defs, x ), self ) )
      files.delete_pycache()
    except:
      return "Error: {}".format( str( tools.error_def() ) )

  def megach_update():
    try:
      url             = "https://raw.githubusercontent.com/LinkkG/megach/master/megach.py"
      file_to_replace = "{}{}megach.py".format( paths.u_bot, os.sep )
      with urlreq.urlopen( url ) as info_online:
        info_online = info_online.read().decode("utf-8").splitlines()
        megach_online_v = [ x for x in info_online if "version =" in x ][0].split("=")[1]
        megach_online_v = megach_online_v.replace("'", "").lstrip( " " )
      with open( file_to_replace, encoding = "utf-8" ) as a_megach:
        a_megach = a_megach.read().splitlines()
        megach_local_v = [ x for x in a_megach if "version =" in x ][0].split("=")[1]
        megach_local_v = megach_local_v.replace("'", "").lstrip( " " )
        if a_megach == info_online:
          download = [ False, megach_local_v, megach_online_v ]
        else:
          urlreq.urlretrieve( url, file_to_replace )
          download = [ True, megach_local_v, megach_online_v ]
          urlreq.urlcleanup()
        return download
      a_megach.close()
      info_online.close()
    except:
      return "Error: {}".format( str( tools.error_def() ) )

###############################################################################################################

class simi:

  def clean_text(text):
    text = text.lower().strip()
    limpio = {
              "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
              "@": "", "?": "", "!": "", ",": "", ".": "", "¿": ""
             }
    for y in limpio:
      if y in text:
        text = text.replace( y, limpio[y] )
    return text

  def create_simi(archivo, text):
    try:
      separator = "::"
      if not os.path.exists( archivo ):
        open( archivo, "a", encoding = "utf-8" ).close()
      else:
        if "::" not in text:
          return False
        else:
          clave, definicion = [ x.strip() for x in text.split( separator, 1 ) ]
          with open(archivo, "a", encoding = "utf-8") as archivo_open:
            http = definicion.find("http")
            if http != -1:
              definicion = definicion
            else:
              definicion = definicion.capitalize()
            archivo_open.write( "{}{}{}\r".format( clave.capitalize(), separator, definicion ) )
          archivo_open.close()
          return True
    except:
      return "Error {}".format( str( tools.error_def() ) )

  def search_simi(archivo, text = "", match = 1):
    try:
      separator = "::"
      if not os.path.exists( archivo ):
        open( archivo, "a", encoding = "utf-8" ).close()
      with open( archivo, encoding = "utf-8" ) as archivo_open:
        sep = simi.clean_text( text ).split()
        lineas = archivo_open.read().splitlines()
        matches = []
        for x in lineas:
          if any( [z in simi.clean_text( x.split( separator, 1 )[0] ) 
                 for z in sep if len( z ) >= match] ):
            matches.append( x )
          if separator not in x:
            print( "Error search_simi path: {}".format( str( x ) ) )
            return "", ""
        mayor = -1
        filtro = []
        if matches:
          for x in matches:
            actual = len( [ a for a in sep if a in 
                         simi.clean_text( x.split( separator )[0] ).split() ] )
            if actual > mayor:
              mayor = actual
              del filtro[:]
              filtro.append( x )
            elif actual == mayor:
              filtro.append( x )
          a, b = random.choice( filtro ).split( separator, 1 )
          return a, b
        else:
          return "", ""
      archivo_open.close()
    except Exception as e:
      return "Error {}".format( str( tools.error_def() ) )

  def answer_simi(cmd, user, **kw):
    try:
      u    = database.take_user( user.name )["lang"]
      t    = database.take_lang_user( u, "simi_answers" )
      ruta = os.path.join( paths.u_bot, paths.u_simi )
      consulta, definicion = simi.search_simi( ruta, cmd )
      plantilla = __import__("string").Template( definicion )
      if "room" in kw:
        donde = kw["room"].name
      else:
        donde = t[0]
      resultado = plantilla.safe_substitute( **kw )
      return resultado or t[1]
    except:
      return "Error {}".format( str( tools.error_def() ) )

######
#Fin #
######