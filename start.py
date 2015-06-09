
#import python stuff
from flask import Flask
from flask import jsonify


#import program stuff
from apis import Streams

host = "0.0.0.0"
port = 8000
debug = True
public = ""

app = Flask(__name__, static_url_path=public)

@app.route("/")
def hello():
    return app.send_static_file("index.html")


@app.route("/api/music/streams")
def HandleGetStreams():
    streams = Streams.getStreams()
    return jsonify(streams)

if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug)