from flask import render_template, g
from flask_login import current_user

from pyforum.chat import chat
from  pyforum.chat.models import ChatMessage, ChatRoom

@chat.before_request
def before_request():
    g.user = current_user


@chat.route('chat', methods=['GET'])
def chats():
    return render_template('chat/chat.html')
