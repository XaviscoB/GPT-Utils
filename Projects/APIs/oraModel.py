import requests
import json

class Model:
    def sendMessage(self, prompt: str):
        api = "https://ora.ai/api/conversation"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0",
            "referer": "https://ora.ai/early-red-dymn/chatgpt",
            "Content-Type": "application/json"
        }
        data = {
            "chatbotId": "c95d0e53-a166-4d0d-b897-0fac177ab7fb",
            "input": prompt,
            "conversationId": "a0df25f2-bd0f-4d4b-9eb7-f51befc7e542",
            "userId": "auto:9b937fed-eb68-4abd-af1f-8fc250e68e67",
            "provider": "OPEN_AI",
            "config": False,
            "includeHistory": False
        }
        json_data = json.dumps(data)
        r = requests.post(api, headers=headers, data=json_data)
        jsonData = r.json()
        return jsonData['response']