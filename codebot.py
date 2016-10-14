import utils
import codecs
import time
from slackclient import SlackClient
import json
import traceback
import requests
import signal

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

import numpy
import random
import math

# codebot's ID as an environment variable
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
		final_response = "Please do not import anything, everything you may need is already imported"
	elif 'exit' in command:
		final_response = "Please do not use exit, I'm sure it's not even necessary here"
	elif 'eval' in command or 'exec' in command:
		final_response = "Please do not use exec/eval, I'm sure it's not even necessary here"
	else:
		final_response = ""
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
						ans = eval(user_eval, Globals, Locals)#, globals(),  locals())
						_ans = eval(correct_eval, Globals, Locals)#,  globals(),  locals())
						#print "[", ans, ":", _ans, "]"
						if type(ans) == type(int(1)):
							ans = float(ans)
						if type(_ans) == type(int(1)):
							_ans = float(_ans)
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
							response = 'Your answer for the problem ' + problem + ' was ' + ans + ' but correct answer is ' + _ans + ' for the input = ' + input
	
							break
					final_response += response + '\n'
			signal.alarm(0)
		except Exception as e:
			signal.alarm(0)
			final_response += str( traceback.format_exc())
	slack_client.api_call("chat.postMessage", channel=channel,
                          text=final_response, as_user=True)


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
                        while len(output_text) > 0 and ( output_text[0] == ' ' or output_text[0] == '\n' or output_text[0] == '\t'):
                            output_text = output_text[1:] 
                        return output_text, output[u'channel']
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
            if command and channel:
                print command, channel
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
