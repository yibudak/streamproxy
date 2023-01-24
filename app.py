# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from flask import Flask, request, Response
from m3u_parser import M3uParser
from io import BytesIO
from base64 import b64encode, b64decode
from helpers.url_validator import validate_url
from helpers.config import Config
import requests


config = Config("prod.conf").attrs
ACCESS_TOKEN = config.ACCESS_TOKEN
CHUNK_SIZE = int(config.CHUNK_SIZE)
parser = M3uParser()
app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):
    """
    Return 404 not found
    :param e:
    :return: Response
    """
    return Response(status=200)


@app.route("/playlist")
def playlist_endpoint():
    """
    This endpoint is used to get the original playlist and replace
     the URLs with the proxy URLs.
    :return: The playlist with the proxy URLs. (m3u8)
    """
    if request.args.get("token") != ACCESS_TOKEN:
        return Response(status=200)

    parser.parse_m3u(config.ORIGIN_M3U, check_live=False)
    for line in parser.get_list():
        line["url"] = "http://%s:%s/single_path?token=%s&path_x=%s" % (
            config.SOURCE_IP,
            config.SOURCE_PORT,
            ACCESS_TOKEN,
            b64encode(line["url"].encode("utf-8")).decode("utf-8"),
        )
        if line["logo"] != "":
            line["logo"] = "http://%s:%s/single_logo?token=%s&path_x=%s" % (
                config.SOURCE_IP,
                config.SOURCE_PORT,
                ACCESS_TOKEN,
                b64encode(line["logo"].encode("utf-8")).decode("utf-8"),
            )
    return Response(
        BytesIO(parser._get_m3u_content().encode("utf-8")),
        mimetype="audio/x-mpegurl",
        headers={"Content-Disposition": "attachment; filename=proxied_playlist.m3u"},
    )


@app.route("/single_logo")
@app.route("/single_path")
def stream_data():
    """
    This endpoint is used to stream the data from the origin server.
    :return: data stream
    """
    if not request.args.get("token", False) == ACCESS_TOKEN:
        return Response(status=200)

    path = request.args.get("path_x", False)
    if not path:
        return Response(status=200)

    decoded_path = b64decode(path).decode("utf-8")
    try:
        validate_url(decoded_path)
    except ValueError:
        return Response(status=200)

    try:
        resp = requests.request(
            method=request.method,
            url=decoded_path,
            headers={key: value for (key, value) in request.headers if key != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            # allow_redirects=False,
            stream=True,
        )
    except requests.ConnectionError:
        return Response(status=200)

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = [
        (name, value)
        for (name, value) in resp.raw.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(download_file(resp), resp.status_code, headers)


def download_file(streamable):
    """
    Download the file in chunks
    :param streamable:
    :return:
    """
    with streamable as stream:
        stream.raise_for_status()
        for chunk in stream.iter_content(chunk_size=CHUNK_SIZE):
            yield chunk


if __name__ == "__main__":
    app.run(host=config.SOURCE_IP, port=config.SOURCE_PORT, debug=config.DEBUG)
