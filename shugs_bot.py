#!/usr/local/bin/python
# coding: utf-8

import requests as re
import polling
import sb_cfg as cfg

api_key = cfg.bot_api_key
url = 'https://api.telegram.org/bot' + api_key
last_update = 0


def answer_shrugs(offset=0):
    res = re.get(url + '/getUpdates?offset=' + str(offset)).json()['result']
    for req in res:
        if 'inline_query' in req:
            if req['inline_query'] != '':
                reply_id = int(req['inline_query']['id'])
                global last_update
                if int(req['update_id']) > last_update:
                    last_update = int(req['update_id']) + 1
                id = reply_id-1234
                title = req['inline_query']['query'] + ' ¯\_(ツ)_/¯'
                text = {"message_text": title}
                response = [{"type": "article", "id": id, "title": title, "input_message_content": text}]
                data = {"inline_query_id": reply_id, "results": response}
                r = re.post(url + '/answerInlineQuery', json=data)


polling.poll(lambda: answer_shrugs(last_update), ignore_exceptions=(re.exceptions.ConnectionError,), step=0.5, poll_forever=True)
