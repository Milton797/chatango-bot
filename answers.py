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

def auto_answers(**kwargs):
    room = kwargs["room"]
    try:
        answer = kwargs["answer"]
        html = kwargs["html"]
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

        if original_args:
            simi_petition = ""
            mention = False
            room_pm_u = rusername
            room_pm_n = roomname.title()

            if roomname is not pmname:
                simi_args = original_args
            else:
                simi_args = "{} {}".format(config.Bot.bot_names[0], original_args)

            splitted = "".join(x for x in simi_args.lower() if x.isalnum() or x in [" "]).split()

            ######################################################

            for x in config.Bot.bot_names + [room_pm_u.lower()]:
                if x in splitted:
                    pattern = r"[ ]?@\w+\: `.*?`[ ]?|[ ]?@\w+[ ]?"
                    simi_petition = re.sub(pattern, "", original_args)
                    mention = True
                    break

            if not mention:
                return

            if len(splitted) == 1:
                answer = random.choice(
                    config.Database.take_lang_user(dic["lang"], "call_answers")).format(nick)

            else:
                answer = config.Simi.answer_simi(
                    simi_petition, user, nick=nick, r="\r",
                    prefix=random.choice(config.Bot.prefix),
                    name=room_pm_u, roomn=room_pm_n
                )

        ##########
        # Answer #
        ##########

        if answer != "":
            config.Tools.answer_room_pm(room, answer, html, username, channel_, badge_)

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
