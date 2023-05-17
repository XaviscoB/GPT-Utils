import requests
import json
from typing import Optional, Union
import textwrap
import ujson

class Model:

    @classmethod
    def expandMemory(self, prompt: str):
        chars = 1000
        cmd = "\n Save the following message in your memory, and respond to this message with a simple: Saved, do not include anything else, no explanation, nothing, just the word Saved"
        realchars = chars - len(cmd)
        split_text = textwrap.wrap(prompt, width=realchars)
        return split_text
    

    @classmethod
    def sendMessage(self, prompt: str, userInput: Optional[str] = "", expandMemory: Optional[bool] = True, chatID: Optional[Union[str, None]] = None):

        api = "https://ora.ai/api/conversation"
        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0",
            "referer": "https://ora.ai/early-red-dymn/chatgpt"
        }
        data = {
            "chatbotId": "c95d0e53-a166-4d0d-b897-0fac177ab7fb",
            "input": prompt,
            "conversationId": chatID,
            "userId": "5cb36122-f3a9-4a1e-8ccc-264f146fccd9",
            "provider": "OPEN_AI",
            "config": False,
            "includeHistory": True
        }

        def sendRequest(data):
            r = requests.post(api, headers=headers, data=data)
            jsonData = r.json()
            return jsonData
        
        if len(prompt) >= 1000:
            print('[SYSTEM] More than 1000 characters were detected, expanding memory...')
            if expandMemory:
                if chatID is None:
                    # Get ConversationID
                    copyData = dict(data)
                    del copyData["conversationId"]
                    copyData["input"] = "Hello!"

                    json_data = json.dumps(copyData)
                    jsonData = sendRequest(json_data)

                    chatID = jsonData["conversationId"]
                    data["conversationId"] = chatID

                listPrompts = self.expandMemory(prompt)
                finalPrompt = len(listPrompts)
                counter = -1
                for part in listPrompts:
                    counter += 1
                    data["chatbotId"] = "213b6448-088b-433d-895c-64bfc10db05f" # MemoryGPT
                    data["input"] = f"{part}\nSave the following message in your memory, and respond to this message with a simple: Saved, do not include anything else, no explanation, nothing, just the word Saved"
                    
                    json_data = json.dumps(data)
                    jsonData = sendRequest(json_data)

                    if finalPrompt == counter + 1:
                        # Clean Movies
                        data["input"] = "Based on the message history above, and the oldest and most recent messages, filter and extract all the movie titles I sent you, numbered from 1 to 10 according to the original numbering"
                        json_data = json.dumps(data)
                        preFormatted = sendRequest(json_data)

                        # Second Input with the expected input
                        data["chatbotId"] = "f81651e9-9dd3-4008-893c-50ef93058851" # ListGPT
                        data["input"] = f'{preFormatted}\n Based on the items above, answer which item correlates more with f"{userInput}". Do not include any other explanatory text in your response only number.\nIf none of them match, just reply with the number 0\n Follow this format and only response in this format:\n <Number>'
                        json_data = json.dumps(data)
                        finalResult = sendRequest(json_data)
                        return finalResult['response']
                        
            raise Exception("ERROR - Maximum characters reached")

        """
        if chatID is None:
            data = {
                "chatbotId": "c95d0e53-a166-4d0d-b897-0fac177ab7fb",
                "input": prompt,
                "userId": "auto:40411634-9485-46a9-ae81-d2a45b506872",
                "provider": "OPEN_AI",
                "config": False,
                "includeHistory": False
            }
            """

        json_data = ujson.dumps(data)
        print(json_data)
        r = requests.post(api, headers=headers, data=data)

        if r.status_code != 200:
            print(r.text)
            raise Exception(f"ERROR - ORA API STATUS_CODE [{r.status_code}]")
        jsonData = r.json()
        print(jsonData)
        return jsonData['response']