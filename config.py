#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import json
import linecache
import os
import random
import string
import sys
import threading
import time
import types
import urllib.request as urlreq

import answers
import cmds
import dicts
import megach
import special_defs

if sys.version_info[0] <= 3 and sys.version_info[1] <= 3:
    import imp

    reload = imp.reload

elif sys.version_info[0] >= 3 and sys.version_info[1] >= 4:
    import importlib

    reload = importlib.reload


##########
# Inicio #
##########

class Bot:
    accounts = [
        ("Acc1", "pass1"),
        ("Acc2", "pass2")
    ]
    prefix = "% &".split()
    bot_names = "ejemplobot botsito examplebot".split()
    bot_lang = "es en".split()[1]
    see_error_r = "pythonrpg farminggames".split()
    pm_connect = True
    see_anons_p = False
    see_users_p = False
    hour_format = "%I:%M:%S:%p|%d/%m/%Y"


class StylesBot:
    font_styles = {"name_color": "000000", "font_color": "000000", "font_face": 1, "font_size": 12}
    titles_style = "<f x{}{}='{}'>".format(
        font_styles["font_size"],
        font_styles["name_color"],
        font_styles["font_face"]
    )
    normal_style = "<f x{}{}='{}'>".format(
        font_styles["font_size"],
        font_styles["font_color"],
        font_styles["font_face"]
    )


class GlobalsV:
    evalp = "milton797 milton megamaster12 linkkg".split()
    anons = "! #".split()


class Paths:
    u_bot = "{0}".format(os.path.dirname(os.path.abspath(sys.argv[0])))

    u_documents = "{0}{2}{1}{2}".format(u_bot, "Documents", os.sep)

    u_wl = "{}{}".format(u_documents, "wl.json")
    u_simi = "{}{}".format(u_documents, "simi.txt")
    u_rooms = "{}{}".format(u_documents, "rooms.json")

    u_langs_file = "{}{}".format(u_documents, "langs.json")


class StylePrint:
    @staticmethod
    def safe_print_bot(self, place, user, message, status):
        try:
            if self._running is True:
                if place.name == self.pm.name:
                    channel_or_status = status
                else:
                    channel_or_status = StylePrint.channel_tipe(message)
                text = "[{}][{}][{}][{}]: {}"
                text = text.format(
                    time.strftime(Bot.hour_format, time.localtime(message.time)),
                    StylePrint.user_room_style(place.name.title()),
                    StylePrint.user_room_style(Tools.user_showname(user.name)),
                    channel_or_status,
                    message.fullbody.replace("", repr("")[1:-1])
                )
                while True:
                    try:
                        print(text)
                        break
                    except UnicodeEncodeError as error:
                        text = "{} (UNICODE) {}".format(text[0:error.start], text[error.end:])
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def user_room_style(room_user):
        try:
            return "{:_^20}".format(room_user)
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def channel_tipe(message):
        try:
            text = "{}|{}"
            channels = {
                32768: "M", 2048: "B", 256: "R", 2304: "R+B",
                34816: "B+M", 33024: "R+M", 35072: "R+A+M", 0: "N"
            }
            badges = {
                1: "SH", 2: "ST", 0: "N"
            }
            final_text = text.format(channels.get(message.channel), badges.get(message.badge))
            return final_text
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def time_now():
        try:
            t = time.strftime(Bot.hour_format, time.localtime(time.time()))
            s = time.time()
            return [t, s]
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def clear_print():
        try:
            if Tools.os_on() != "Windows":
                os.system("clear")
            else:
                os.system("cls")
            text = Database.take_lang_bot(Bot.bot_lang, "console_cleaned")
            print(text.format(StylePrint.time_now()[0]))
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def console_title(title):
        try:
            if Tools.os_on() != "Windows":
                if os.environ.get("TERM") in (
                        "xterm",
                        "xterm-color",
                        "xterm-256color",
                        "linux",
                        "screen",
                        "screen-256color",
                        "screen-bce",
                ):
                    sys.stdout.write("\33]0; {} \a".format(title))
                    sys.stdout.flush()
            else:
                os.system("title {}".format(title))
            return True
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))


class Database:
    class Molds:

        Default_Wl = {
            "lang": "en",
            "lvl": 1,
            "nick": ""
        }

        Default_Wl_Anons = Default_Wl

        Default_Room = {
            "lang": "en"
        }

    ###############################################################################################################

    wl = dicts.wl
    rooms = dicts.rooms
    wl_anons = dicts.wl_anons
    langs = dicts.langs

    ###############################################################################################################

    @staticmethod
    def save_wl():
        try:
            wl_ruta = Paths.u_wl
            with open(wl_ruta, "w") as save_users:
                save_users.write(json.dumps(dict(Database.wl), indent=4, sort_keys=True))
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def save_rooms():
        try:
            rooms_ruta = Paths.u_rooms
            with open(rooms_ruta, "w") as save_rooms:
                save_rooms.write(json.dumps(dict(Database.rooms), indent=4, sort_keys=True))
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def load_wl():
        try:
            Database.wl.clear()
            wl_ruta = Paths.u_wl
            with open(wl_ruta, encoding="utf-8") as load_users:
                Database.wl.update(json.load(load_users, encoding="utf-8"))
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def load_langs():
        try:
            Database.langs.clear()
            langs_ruta = Paths.u_langs_file
            with open(langs_ruta, encoding="utf-8") as load_all_langs:
                Database.langs.update(json.load(load_all_langs, encoding="utf-8"))
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def load_rooms():
        try:
            Database.rooms.clear()
            rooms_ruta = Paths.u_rooms
            with open(rooms_ruta, encoding="utf-8") as load_rooms:
                Database.rooms.update(json.load(load_rooms, encoding="utf-8"))
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def save_all():
        try:
            Database.save_wl()
            Database.save_rooms()
            text = Database.take_lang_bot(Bot.bot_lang, "save_data").format(StylePrint.time_now()[0])
            print(text)
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def load_all():
        try:
            Database.load_wl()
            Database.load_rooms()
            Database.load_langs()
            Simi.load_data(os.path.join(Paths.u_bot, Paths.u_simi))
            text = Database.take_lang_bot(Bot.bot_lang, "load_data").format(StylePrint.time_now()[0])
            print(text)
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def new_user(user):
        try:
            user = user.lower()
            if user not in Database.wl.keys():
                if user[0] not in GlobalsV.anons:
                    Database.wl.update({user: Database.Molds.Default_Wl.copy()})
                    return True
            else:
                return False
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def new_anon(anon):
        try:
            anon = anon.lower()
            if anon not in Database.wl_anons.keys():
                Database.wl_anons.update({anon: Database.Molds.Default_Wl_Anons.copy()})
                return True
            else:
                return False
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def new_room(room):
        try:
            room = room.lower()
            if room not in Database.rooms.keys():
                Database.rooms.update({room: Database.Molds.Default_Room.copy()})
                return True
            else:
                return False
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def erase_user(user):
        try:
            user = user.lower()
            if user in Database.wl.keys():
                del Database.wl[user]
                return True
            else:
                return False
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def erase_anon(anon):
        try:
            anon = anon.lower()
            if anon in Database.wl_anons.keys():
                del Database.wl_anons[anon]
                return True
            else:
                return False
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def erase_room(room):
        try:
            room = room.lower()
            if room in Database.rooms.keys():
                del Database.rooms[room]
                return True
            else:
                return False
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def update_default_user(user):
        try:
            user = user.lower()
            for x, c in Database.Molds.Default_Wl.items():
                if x not in Database.wl[user]:
                    Database.wl[user][x] = c
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def update_default_anon(anon):
        try:
            anon = anon.lower()
            for x, c in Database.Molds.Default_Wl_Anons.items():
                if x not in Database.wl_anons[anon]:
                    Database.wl_anons[anon][x] = c
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def update_default_room(room):
        try:
            room = room.lower()
            for x, c in Database.Molds.Default_Room.items():
                if x not in Database.rooms[room]:
                    Database.rooms[room][x] = c
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def update_all_default_users():
        try:
            u_user = Database.wl
            for x in u_user:
                Database.update_default_user(x)
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def update_all_default_anons():
        try:
            u_anon = Database.wl_anons
            for x in u_anon:
                Database.update_default_anon(x)
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def update_all_default_rooms():
        try:
            u_room = Database.rooms
            for x in u_room:
                Database.update_default_room(x)
            return True
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def take_user(user):
        try:
            user = user.lower()
            if user[0] not in GlobalsV.anons:
                if user not in Database.wl.keys():
                    Database.new_user(user)
                else:
                    Database.update_default_user(user)
                return Database.wl[user]
            else:
                if user not in Database.wl_anons.keys():
                    Database.new_anon(user)
                else:
                    Database.update_default_anon(user)
                return Database.wl_anons[user]
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def take_room(room):
        try:
            room = room.lower()
            if room in Database.rooms.keys():
                Database.update_default_room(room)
                return Database.rooms[room]
            else:
                return False
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def take_lang_bot(lang, traduction):
        try:
            if len(Database.langs) == 0:
                Database.load_langs()
            langs_user_room_bot = Database.langs["for_bot"]
            if lang in langs_user_room_bot and traduction in langs_user_room_bot[lang]:
                return langs_user_room_bot[lang][traduction]
            else:
                text = "No lang: {}, {}"
                text_f = text.format(repr(lang), repr(traduction))
                print(text_f)
                return text_f
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def take_lang_room(lang, traduction):
        try:
            if len(Database.langs) == 0:
                Database.load_langs()
            langs_user_room_bot = Database.langs["for_rooms"]
            if lang in langs_user_room_bot and traduction in langs_user_room_bot[lang]:
                return langs_user_room_bot[lang][traduction]
            else:
                text = "No lang: {}, {}"
                text_f = text.format(repr(lang), repr(traduction))
                print(text_f)
                return text_f
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def take_lang_user(lang, traduction):
        try:
            if len(Database.langs) == 0:
                Database.load_langs()
            langs_user_room_bot = Database.langs["for_users"]
            if lang in langs_user_room_bot and traduction in langs_user_room_bot[lang]:
                return langs_user_room_bot[lang][traduction]
            else:
                text = "No lang: {}, {}"
                text_f = text.format(repr(lang), repr(traduction))
                print(text_f)
                return text_f
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def set_lang_user(user, args):
        try:
            u_langs = Database.langs["for_users"]
            info = Database.take_user(user)
            u_user = Database.wl.keys()
            u_anon = Database.wl_anons.keys()
            if args:
                if user in u_user or user in u_anon:
                    if args.lower() in u_langs:
                        info["lang"] = args.lower().split()[0]
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return None
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def set_lang_room(room, args):
        try:
            u_langs = Database.langs["for_rooms"]
            info = Database.take_room(room)
            u_room = Database.rooms.keys()
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
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())

    @staticmethod
    def set_nick_user(lang, user_, n_nick):
        try:
            info = Database.take_user(user_)
            t = Database.take_lang_user(lang, "nick_set_answer")
            u_user = Database.wl.keys()
            u_anon = Database.wl_anons.keys()
            if user_ in u_user or user_ in u_anon:
                if n_nick:
                    if len(n_nick) < 26:
                        info["nick"] = n_nick
                        return t[0].format(Tools.user_showname(user_))
                    else:
                        return t[3]
                else:
                    nick_s = info.get("nick") if info.get("nick") else t[1]
                    return t[2].format(nick_s)
            else:
                return False
        except (Exception, BaseException):
            return "Error: {}".format(Tools.error_def())


class Tools:

    @staticmethod
    def error_def():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        line = linecache.getline(filename, lineno, f.f_globals)
        if Bot.bot_lang == "es":
            e = "ARCHIVO: {} --> LÍNEA: {} --> {}: --> {}"
        else:
            e = "FILE: {} --> LINE: {} --> {}: --> {}"
        ef = e.format(filename, lineno, line.strip(), exc_obj)
        print(ef)
        return ef.replace("<", "&lt;").replace(">", "&gt;")

    @staticmethod
    def os_on():
        if os.name != "nt":
            u = "Linux"
        else:
            u = "Windows"
        return u

    @staticmethod
    def split_text(user_name, text):
        try:
            vacio = ""
            tag = user_name
            text = text.strip()
            text_s = text.split()
            text_l = len(text_s)

            if text_l <= 0 and not text:
                return vacio, vacio, vacio, vacio

            if text_s[0].lower().startswith("@{}".format(tag)):
                cmd_prefix = text_s[0].lower()
                cmd = text_s[1].lower() if text_l > 1 else ""
                args = " ".join(text_s[2:]) if text_l > 1 else ""
            else:
                cmd_prefix = text_s[0][0].lower()
                cmd = text_s[0][1:].lower()
                args = " ".join(text_s[1:]) if text_l > 1 else ""

            return cmd_prefix, cmd, args, text
        except (Exception, BaseException):
            return "Error split_text {}".format(Tools.error_def())

    @staticmethod
    def answer_pm_rooms(self, place, user, message):
        try:
            # General variables.
            html = True
            answer = ""
            nick = ""
            pm = self.pm
            room = place
            pmname = pm.name
            username = user.name
            roomname = place.name
            pusername = pm.user.showname.lower()
            rusername = place.user.showname.lower()
            usershowname = Tools.user_showname(username)

            # Ignore bot self.
            if (username if username[0] not in "!#" else username[1:]) == rusername:
                return

            # Take room and user dictionary.
            dic = Database.take_user(username)
            dicr = Database.take_room(roomname)

            # Ignore users with lvl -1.
            if dic.get("lvl") == -1:
                return

            # Ignore messages or commands if wl or rooms are empty.
            if len(Database.wl.keys()) == 0 or len(Database.rooms.keys()) == 0:
                return

            # Take user nick.
            if username in Database.wl.keys() or username in Database.wl_anons.keys():
                if dic.get("nick"):
                    nick = "{2}[ {0} - {1} ]{3}".format(
                        usershowname, dic.get("nick"),
                        StylesBot.titles_style,
                        StylesBot.normal_style
                    )
                else:
                    nick = "{1} @{0} {2}".format(
                        usershowname,
                        StylesBot.titles_style,
                        StylesBot.normal_style
                    )

            # Separate args
            cmd_prefix, cmd, cmd_args, original_args = Tools.split_text(rusername, message.body)

            # Check if pm or room
            if roomname is not pmname:
                dicr = Database.take_room(roomname)
                badge_ = message.badge
                channel_ = message.channel
            else:
                dicr = Database.take_room("for_pm")
                badge_ = 0
                channel_ = 0
            dic = Database.take_user(username)

            # Check prefix usage
            if cmd and cmd_prefix in Bot.prefix or cmd_prefix == "@{}".format(rusername):
                prefix = True
            else:
                prefix = False

            # Get answer from answer_cmds or auto_answers.
            if prefix is True:
                threading.Thread(
                    target=cmds.answer_cmds,
                    name="Process_room_cmds",
                    kwargs=locals(),
                    daemon=True
                ).start()
            else:
                cmd_args = message.body.lower()
                if cmd_args:
                    threading.Thread(
                        target=answers.auto_answers,
                        name="Process_room_answers",
                        kwargs=locals(),
                        daemon=True
                    ).start()
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def answer_room_pm(room, respuesta_: str = "", html_: bool = False,
                       user_: str = "", canal_: int = 0, badge_: int = 0,
                       reply_: bool = True):
        try:
            if reply_:
                if room.name != "PM":
                    room.message(str(respuesta_), html=bool(html_),
                                 canal=int(canal_), badge=int(badge_))
                elif room.name == "PM":
                    room.message(str(user_), str(respuesta_).replace("&", "&amp;"),
                                 html=bool(html_))
                else:
                    print(respuesta_)
            else:
                return None
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def room_user_unknow(url):
        try:
            url = "http://{}.chatango.com/".format(url.lower())
            try:
                data = urlreq.urlopen(url).read().decode("utf-8")
            except (Exception, BaseException):
                return False
            user = data.find("buyer") > data.find("seller") > 0 and 1 or 0
            if not user:
                user = data.find("<title>Unknown User!</title>") < 0 < data.find("</head>") and 2 or 0
            if user == 1:
                return "user"
            elif user == 2:
                return "room"
            elif not user:
                return "N/A"
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def reload(module):
        try:
            if not module:
                return False
            else:
                module_g = []
                module_s = module.split()
                for x in module_s:
                    try:
                        reload(sys.modules[x])
                        module_g.append((x, True))
                        time.sleep(0.01)
                    except Exception as e:
                        module_g.append((x, False, e))
                Files.delete_pycache()
                return module_g
        except Exception as e:
            return "Error: {}".format(str(e))

    @staticmethod
    def user_showname(user_):
        try:
            a = megach.User.get(user_).showname
            if user_[0] not in GlobalsV.anons:
                if a == user_.lower():
                    f = a.title()
                else:
                    f = a
            else:
                f = user_.title()
            return f
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def auto_start(bot_self):
        try:
            # Start text
            text = Database.take_lang_bot(Bot.bot_lang, "on_init")
            print(text.format(StylePrint.time_now()[0]))

            # Automatic start of extra variables
            Files.import_special_defs(bot_self)
            StylePrint.console_title("{}".format(random.choice(Bot.bot_names).upper()))

            # Ch automatic start of variables
            bot_self.enableBg()
            bot_self.setNameColor(StylesBot.font_styles["name_color"])
            bot_self.setFontColor(StylesBot.font_styles["font_color"])
            bot_self.setFontFace(StylesBot.font_styles["font_face"])
            bot_self.setFontSize(StylesBot.font_styles["font_size"])
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def auto_tasks():
        try:
            # Task every 15 minutes
            StylePrint.clear_print()
            Database.save_all()
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def start_connections(self, ignore_room: list, anon_room: list):
        try:
            rooms = Database.rooms.keys()
            for x in rooms:
                if x not in ignore_room and x not in anon_room:
                    self.joinRoom(x)
                elif x in anon_room and x not in self.roomnames:
                    self.joinRoom(x, ["", ""])
            return True
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def stop_bot(bot_self):
        print(Database.take_lang_bot(Bot.bot_lang, "keyboard_kill"))
        Files.delete_pycache()
        Database.save_all()
        StylePrint.clear_print()
        bot_self.setTimeout(2, bot_self.stop)


class Files:

    @staticmethod
    def delete_file(u):
        if os.path.exists(u):
            try:
                os.remove(u)
                return True
            except Exception as e:
                return e
        else:
            return False

    @staticmethod
    def delete_files(u):
        if os.path.exists(u):
            try:
                [Files.delete_file("{}{}{}".format(u, os.sep, x)) for x in os.listdir(u)]
                return True
            except Exception as e:
                return e
        else:
            return False

    @staticmethod
    def delete_folder(u):
        if os.path.exists(u):
            try:
                Files.delete_files(u)
                os.removedirs(u)
                return True
            except Exception as e:
                return e
        else:
            return False

    @staticmethod
    def delete_pycache():
        a_a = "{}{}__pycache__".format(Paths.u_bot, os.sep)
        if os.path.exists(a_a):
            try:
                Files.delete_folder(a_a)
                return True
            except Exception as e:
                return e
        else:
            return False

    @staticmethod
    def import_special_defs(bot_self):
        try:
            for x in [z for z in dir(special_defs) if callable(getattr(special_defs, z))]:
                setattr(bot_self, x, types.MethodType(getattr(special_defs, x), bot_self))
            Files.delete_pycache()
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def megach_update():
        try:
            url = "https://raw.githubusercontent.com/LinkkG/megach/master/megach.py"
            file_to_replace = "{}{}megach.py".format(Paths.u_bot, os.sep)
            with urlreq.urlopen(url) as info_online:
                info_online = info_online.read().decode("utf-8").splitlines()
                megach_online_v = [x for x in info_online if "version =" in x][0].split("=")[1]
                megach_online_v = megach_online_v.replace("'", "").lstrip(" ")
            with open(file_to_replace, encoding="utf-8") as a_megach:
                a_megach = a_megach.read().splitlines()
                megach_local_v = [x for x in a_megach if "version =" in x][0].split("=")[1]
                megach_local_v = megach_local_v.replace("'", "").lstrip(" ")
                if a_megach == info_online:
                    download = [False, megach_local_v, megach_online_v]
                else:
                    urlreq.urlretrieve(url, file_to_replace)
                    download = [True, megach_local_v, megach_online_v]
                    urlreq.urlcleanup()
                return download
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))


class Simi:
    loaded_info = list()

    @staticmethod
    def load_data(archivo):
        try:
            with open(archivo, encoding="utf-8") as archivo_open:
                lineas = archivo_open.read().splitlines()
                Simi.loaded_info = lineas
                return Simi.loaded_info
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def clean_text(text):
        try:
            text = text.lower().strip()
            limpio = {
                "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
                "@": "", "?": "", "!": "", ",": "", ".": "", "¿": ""
            }
            for y in limpio:
                if y in text:
                    text = text.replace(y, limpio[y])
            return text
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def create_simi(archivo, text, separator="::"):
        try:
            if not os.path.exists(archivo):
                open(archivo, "a", encoding="utf-8").close()
            else:
                if "::" not in text:
                    return False
                else:
                    clave, definicion = [x.strip() for x in text.split(separator, 1)]
                    with open(archivo, "a", encoding="utf-8") as archivo_open:
                        http = definicion.find("http")
                        if http != -1:
                            definicion = definicion
                        else:
                            definicion = definicion.capitalize()
                        archivo_open.write("{}{}{}\r".format(clave.capitalize(), separator, definicion))
                    Simi.load_data(archivo)
                    return True
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def search_simi(archivo, text="", match=1, separator="::"):
        try:
            if Simi.loaded_info is list():
                Simi.load_data(archivo)
            if Simi.loaded_info:
                lineas = Simi.loaded_info
                sep = Simi.clean_text(text).split()
                matches = []
                for x in lineas:
                    if any([z in Simi.clean_text(x.split(separator, 1)[0]) for z in sep if len(z) >= match]):
                        matches.append(x)
                    if separator not in x:
                        print("Error search_simi path: {}".format(str(x)))
                        return "", ""
                mayor = -1
                filtro = []
                if matches:
                    for x in matches:
                        actual = len([a for a in sep if a in Simi.clean_text(x.split(separator)[0]).split()])
                        if actual > mayor:
                            mayor = actual
                            del filtro[:]
                            filtro.append(x)
                        elif actual == mayor:
                            filtro.append(x)
                    a, b = random.choice(filtro).split(separator, 1)
                    return a, b
                else:
                    return "", ""
            else:
                return "", ""
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

    @staticmethod
    def answer_simi(cmd, user, **kw):
        try:
            u = Database.take_user(user.name).get("lang")
            t = Database.take_lang_user(u, "simi_answers")
            ruta = os.path.join(Paths.u_bot, Paths.u_simi)
            consulta, definicion = Simi.search_simi(ruta, cmd)
            plantilla = string.Template(definicion)
            resultado = plantilla.safe_substitute(**kw)
            return resultado or t[1]
        except (Exception, BaseException):
            return "Error: {}".format(str(Tools.error_def()))

######
# Fin #
######
