from flask import Flask, request
from model import Model
from socket import gethostbyname, gethostname
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    print('Hello World!')
    print(request.args.get('info'))
    return request.args.__str__()


@app.route('/post/run', methods=['POST'])
def register():
    # if get post form /register
    # print(request.headers)
    set_config = request.get_data()
    if set_config is None or set_config == "":
        return "Parameter set_config can not be empty"
    set_config = json.loads(set_config)
    print(set_config)
    file = set_config.get('logId', '')
    if file:
        model = Model(file)
        model.read_data()
        model.solve()
        model.write()
        # model.error()
        if model.status == 'error':
            # return some error message
            return "error"
        return "finish"
    else:
        return "no information in parameters"



if __name__ == '__main__':
    res = gethostbyname(gethostname())
    app.run(host=res, port=9030, debug=True)
