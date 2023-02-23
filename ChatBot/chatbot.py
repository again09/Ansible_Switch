import os
import Credential

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from ansible_runner import run

app = App(token=Credential.SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_mention(event, say):
    user_id = event["user"]    

    if "Ansible_Switch" in event["text"]:
        inventory = "../inventory/inventory.ini"
        playbook = "../main.yml"

        blocks = event["blocks"][0]["elements"]

        for block in blocks:
            if block["type"] == "rich_text_preformatted":
                with open("../inventory/inventory.ini", "w") as file:
                    file.write(block["elements"][0]["text"])

        result = run(
            private_data_dir=".",
            playbook=playbook,
            inventory=inventory
        )

        say(f"Ansible_Switch " + result.status)

    elif "Ansible_Switch_Destination" in event["text"]:
        with open("../inventory/inventory.ini", "r") as f:
            content = f.read()
        message = f"현재 자동화 대상은 아래와 같습니다.\n"
        say(message + "```" + content + "```")


    else:
        with open("../inventory/inventory.ini.ex", "r") as f:
            content_ex = f.read()
        message = f"나를 멘션(@Automation Bot) 하고, Keyword를 입력해주세요.\n"
        message = message + "현재 사용 가능 키워드: Ansible_Switch_Destination(현재 자동화 대상), Ansible_Switch 2가지 입니다.\n"
        message = message + "만약에 자동화 대상을 설정할 필요가 있다면 아래와 같은 양식을 사용하세요!\n\nex)\n@Automation Bot Switch Setup\n"
        say(message + "```" + content_ex + "```")

handler = SocketModeHandler(app_token=Credential.SLACK_APP_TOKEN, app=app)

if __name__ == "__main__":
    handler.start()
