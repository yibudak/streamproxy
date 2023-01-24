
![Logo](./streamproxy.png)

[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


streamproxy is an application developed using Python and Flask that you can use to tunnel your M3U playlists.

## Installation

Clone and install dependencies

```bash
  git clone https://github.com/yibudak/streamproxy
  cd streamproxy
  python3 -m venv venv
  source ./venv/bin/activate
  python3 -m pip install -r requirements.txt
```

Reconfigure the parameters

```bash
  cp sample.conf prod.conf
  nano prod.conf
```

And run

```bash
  python3 app.py
```
## Roadmap

- Add HTTPS support
- IP address as domain


## Authors

- [@yibudak](https://www.github.com/yibudak)


## Contributing

Contributions are always welcome!

If you encounter an error, you can leave a message in the issue section. We also welcome pull requests to add new features or bug-fixes.

Make sure to use the [Black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) code style when writing your code.
## License

[GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)

