from flask import (
    render_template)
from . import message

@message.route('message', methods=['GET'])
def index():
    return render_template('message/message.html')