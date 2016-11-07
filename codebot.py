#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils
import codecs
import time
from slackclient import SlackClient
import json
import traceback
import requests
import signal
import numpy as np 
import random
import math

BOT_ID = " ***** " 

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack client
TOKEN = " ***** "
slack_client = SlackClient(TOKEN)
headers = {'Authorization': 'Bearer %s'%(TOKEN)}

inputs = json.loads(codecs.open('inputs.json',encoding='utf-8').read())

Globals, Locals = globals(), locals()

def handler(signum, frame):
    raise Exception("Time Limit Exceeded: Probably an Infinite Loop")

def handle_command(command, channel):
	if 'import' in command:
		final_response = u"Please do not import anything, everything you may need is already imported"
	elif 'exit' in command:
		final_response = u"Please do not use exit, I'm sure it's not even necessary here"
	elif 'eval' in command or 'exec' in command:
		final_response = u"Please do not use exec/eval, I'm sure it's not even necessary here"
	else:
		final_response = u""
		try:
			signal.signal(signal.SIGALRM, handler)
			signal.alarm(10)
			exec(command, Globals, Locals)
			for problem in inputs.keys():
				if problem in command.replace('(',' ').split():
					response = 'Your code for the problem ' + problem + ' was correct'
					for input in inputs[problem]:
						user_eval = problem + '('
						correct_eval = 'utils.' + user_eval
						for i in input:
							if type(i) != type(' ') and type(i) != type(u' '):
								user_eval += str(i) + ', '
								correct_eval += str(i) + ', '
							else:
								user_eval += "'" + i + "', "
								correct_eval += "'" + i + "', "
						user_eval = user_eval[:-2] + ')'
						correct_eval = correct_eval[:-2] + ')'
						#user_eval = 'ans = ' + user_eval
						#correct_eval = '_ans = ' + correct_eval
						ans = eval(user_eval, Globals, Locals)#, globals(),  locals())
						_ans = eval(correct_eval, Globals, Locals)#,  globals(),  locals())
						#exec(user_eval, Globals, Locals)
						#exec(correct_eval, Globals, Locals)
						if type(ans) == type(int(1)):
							ans = float(ans)
						if type(_ans) == type(int(1)):
							_ans = float(_ans)
						if type(_ans).__module__ == np.__name__:
							if type(ans).__module__ != np.__name__:
								response = 'You had to return an answer in a numpy type'
								break
							if ans.shape == _ans.shape:
								if np.allclose(ans,_ans) == False:
									response = 'Your answer for the problem ' + problem + \
										   ' was ' + str(ans) + ' but the correct answer is ' + \
										   str(_ans) + ' for the input == ' + str(input[:30]) + \
										   ('...' if len(str(input)) > 30 else '')
									break
							else:
								response = 'The shape of your answer for the problem ' + problem + \
									   ' was ' + str(ans.shape) + ' but the shape of the correct answer is ' + \
									   str(_ans.shape) + ' for the input == ' + str(input[:30]) + \
                                                                           ('...' if len(str(input)) > 30 else '')
								break
							continue
						if str(ans) != str(_ans):
							if len(str(ans)) > 30:
								ans = str(ans)[:30] + '...'
							else:
								ans = str(ans)
							if len(str(_ans)) > 30:
								_ans = str(_ans)[:30] + '...'
							else:
								_ans = str(_ans)
							if len(str(input)) > 30:
								input = str(input)[:30] + '...'
							else:
								input = str(input)
							response = 'Your answer for the problem ' + problem + ' was ' + \
							ans + ' but the correct answer is ' + _ans + ' for the input = ' + input
							break
					final_response += response + '\n'
			signal.alarm(0)
		except Exception as e:
			signal.alarm(0)
			final_response += str( traceback.format_exc())
	slack_client.api_call("chat.postMessage", channel=channel,
                          text=final_response, as_user=True)
	return final_response


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            try:
                if not output[u'user'] == BOT_ID:
                    output_text = requests.get(output[u'file'][u'url_private'],headers = headers).text
                    return output_text, output[u'channel']
            except:
                try:
                    if not output[u'user'] == BOT_ID:
                        output_text = output[u'text'].replace(AT_BOT,'').replace('&lt;', '<').replace('&gt;', '>')
                        while len(output_text) > 0 and ( output_text[0] == ' ' or output_text[0] == '\n' \
			      or output_text[0] == '\t'):
                            output_text = output_text[1:] 
                        return output_text.encode("utf-8"), output[u'user'].encode("utf-8")
                except:
                    return None, None
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("CodeBot connected and running!")
        while True:
            t = slack_client.rtm_read()
            command, channel = parse_slack_output(t)
	    #print command, channel
            if command and channel:
                print command
                response = handle_command(command, channel)
		print response
		print channel
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
