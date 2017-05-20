from flask import render_template
from . import chat


@chat.route('chat', methods=['GET'])
def chats():
    return render_template('chat/chat.html')
