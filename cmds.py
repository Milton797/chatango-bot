#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import os

import answers
import config
import methods


###################
# Answer cmds def #
###################

def answer_cmds(**kwargs):
    room = kwargs["room"]
    try:
        answer = kwargs["answer"]
        html = kwargs["html"]
        cmd_args = kwargs["cmd_args"]
        original_args = kwargs["original_args"]
        nick = kwargs["nick"]
        dic = kwargs["dic"]
        user = kwargs["user"]
        rusername = kwargs["rusername"]
        roomname = kwargs["roomname"]
        pmname = kwargs["pmname"]
        username = kwargs["username"]
        channel_ = kwargs["channel_"]
        badge_ = kwargs["badge_"]
        cmd = kwargs["cmd"]
        self = kwargs["self"]
        message = kwargs["message"]
        pm = kwargs["pm"]

        if cmd in ["ev", "eval"]:
            if username in config.GlobalsV.evalp:
                if cmd_args:
                    html = False
                    locals().update(globals())
                    try:
                        answer = str(eval(cmd_args, locals()))
                    except Exception as ev:
                        try:
                            answer = str(exec(cmd_args, locals(), globals()))
                        except Exception as ex:
                            if str(ev) == str(ex):
                                err = ev
                            else:
                                err = "{}, {}".format(ev, ex)
                            answer = "Eval Error: {}".format(err)

        elif cmd in ["ex", "exec"]:
            if username in config.GlobalsV.evalp:
                if cmd_args:
                    html = False
                    locals().update(globals())
                    try:
                        answer = str(exec(cmd_args, locals(), globals()))
                    except Exception as ex:
                        answer = "Exec Error: {}".format(ex)

        elif cmd in ["reload"]:
            if username in config.GlobalsV.evalp:
                try:
                    if cmd_args:
                        a = config.Tools.reload(cmd_args)
                    else:
                        a = config.Tools.reload("config cmds methods answers special_defs")
                        config.Files.import_special_defs(self)
                    answer = a
                except Exception as e:
                    answer = "Error: {}".format(str(e))

        elif cmd in ["megach"]:
            if username in config.GlobalsV.evalp:
                try:
                    a_megach = config.Files.megach_update()
                    answer = a_megach
                except Exception as e:
                    answer = "Error: {}".format(str(e))

        elif cmd in ["cmd", "cmds", "comandos", "commands"]:
            try:
                cmds = ""
                if dic["lang"] == "en":
                    cmds = "lang roomlang nick simi join leave yt gis".split()
                elif dic["lang"] == "es":
                    cmds = "lang salalang nick simi conecta desconecta yt gis".split()
                answer = ", ".join(sorted(cmds)).title()
            except Exception as e:
                answer = "Error: {}".format(str(e))

        elif cmd in ["lang"]:
            try:
                t = config.Database.take_lang_user(dic["lang"], "set_change_lang_user")
                b = ", ".join(list(config.Database.langs["for_users"].keys()))
                if cmd_args:
                    c = config.Database.set_lang_user(username, cmd_args.split()[0])
                    if c is True:
                        change = t[0].format(cmd_args.split()[0].title())
                    else:
                        change = t[1].format(b.title())
                else:
                    change = t[1].format(b.title())
                answer = change
            except Exception as e:
                answer = "Error: {}".format(e)

        elif cmd in ["rlang", "roomlang", "langr", "slang", "salalang", "langs"]:
            try:
                t = config.Database.take_lang_user(dic["lang"], "set_change_lang_room")
                if roomname is not pmname:
                    b = ", ".join(list(config.Database.langs["for_users"].keys()))
                    if cmd_args:
                        c = config.Database.set_lang_room(roomname, cmd_args.split()[0])
                        if c is True:
                            change = t[0].format(cmd_args.split()[0].title())
                        else:
                            change = t[1].format(b.title())
                    else:
                        change = t[1].format(b.title())
                    answer = change
                else:
                    answer = t[2]
            except Exception as e:
                answer = "Error: {}".format(e)

        elif cmd in ["nick"]:
            try:
                answer = config.Database.set_nick_user(dic["lang"], username, cmd_args)
            except Exception as e:
                answer = "Error: {}".format(e)

        elif cmd in ["simi"]:
            try:
                t = config.Database.take_lang_user(dic["lang"], "create_simi_answer")
                if cmd_args:
                    path = os.path.join(config.Paths.u_bot, config.Paths.u_simi)
                    a = config.Simi.create_simi(path, cmd_args)
                    if a is True:
                        answer = t[0]
                    else:
                        answer = t[1]
                else:
                    answer = t[1]
            except Exception as e:
                answer = "Error: {}".format(e)

        elif cmd in ["conecta", "join"]:
            try:
                t = config.Database.take_lang_user(dic["lang"], "join_room_answer")
                a = cmd_args.split()[0] if cmd_args else ""
                a = a.lstrip(" ").rstrip(" ")
                if a:
                    if a == roomname:
                        answer = t[0]
                    if a in dict(config.Database.rooms):
                        if a not in self.roomnames:
                            self.joinRoom(a)
                            answer = t[1]
                        if a in dict(config.Database.rooms) and a in self.roomnames:
                            answer = t[5]
                    else:
                        r_ex = config.Tools.room_user_unknow(a)
                        if r_ex == "room" and r_ex is not False:
                            self.joinRoom(a)
                            config.Database.new_room(a)
                            answer = t[2]
                        else:
                            answer = t[3]
                else:
                    answer = t[4]
            except Exception as e:
                answer = "Error: {}".format(e)

        elif cmd in ["desconecta", "disconnect", "leave"]:
            try:
                t = config.Database.take_lang_user(dic["lang"], "leave_room_answer")
                a = cmd_args.split()[0].lower() if cmd_args else ""
                a = a.lstrip(" ").rstrip(" ")
                if a:
                    if a in dict(config.Database.rooms) or a in self.roomnames:
                        if a == roomname:
                            answer = t[0]
                            self.setTimeout(3, self.leaveRoom, a)
                            self.setTimeout(4, config.Database.erase_room, a)
                        elif a in dict(config.Database.rooms):
                            if a not in self.roomnames:
                                config.Database.erase_room(a)
                                answer = t[0]
                            if a in dict(config.Database.rooms) and a in self.roomnames:
                                self.leaveRoom(a)
                                config.Database.erase_room(a)
                                answer = t[0]
                    else:
                        answer = t[2]
                else:
                    answer = t[1]
            except Exception as e:
                answer = "Error: {}".format(e)

        elif cmd in ["yt"]:
            try:
                t = config.Database.take_lang_user(dic["lang"], "youtube_answer")
                if cmd_args:
                    answer = methods.OnlineDefs.youtube(dic["lang"], cmd_args)
                else:
                    answer = t[2]
            except Exception as e:
                answer = "Error: {}".format(e)

        elif cmd in ["gis"]:
            try:
                t = config.Database.take_lang_user(dic["lang"], "gis_answer")
                if cmd_args:
                    answer = methods.OnlineDefs.search_images(dic["lang"], cmd_args)
                else:
                    answer = t[2]
            except Exception as e:
                answer = "Error: {}".format(e)

        elif cmd in ["cmd_pm_example"]:
            if roomname is not pmname:
                answer = "Hello."
            else:
                answer = "bye, o.o not available in pm"

        elif cmd in ["stop"]:
            if username in config.GlobalsV.evalp:
                room.message("Ok")
                self.setTimeout(2, config.Tools.stop_bot, self)

        ##########
        # Answer #
        ##########

        if answer != "":
            config.Tools.answer_room_pm(room, answer, html, username, channel_, badge_)
        else:
            answers.auto_answers(**locals())

    ##################
    # Detector error #
    ##################

    except (Exception, BaseException):
        if room.name in config.Bot.see_error_r:
            return "Main.py Error: {}".format(str(config.Tools.error_def()))
        else:
            print("Main.py Error: {}".format(str(config.Tools.error_def())))

#######
# End #
#######
