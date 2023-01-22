# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import re
import urllib

"""
https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
"""
DOMAIN_FORMAT = re.compile(
    r"(?:^(\w{1,255}):(.{1,255})@|^)"  # http basic authentication [optional]
    r"(?:(?:(?=\S{0,253}(?:$|:))"  # check full domain length to be less than or equal to 253 (starting after http basic auth, stopping before port)
    r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"  # check for at least one subdomain (maximum length per subdomain: 63 characters), dashes in between allowed
    r"(?:[a-z0-9]{1,63})))"  # check for top level domain, no dashes allowed
    r"|localhost)"  # accept also "localhost" only
    r"(:\d{1,5})?",  # port [optional]
    re.IGNORECASE,
)
SCHEME_FORMAT = re.compile(
    r"^(http|hxxp|ftp|fxp)s?$", re.IGNORECASE  # scheme: http(s) or ftp(s)
)


def validate_url(url: str):
    url = url.strip()

    if not url:
        raise ValueError  # Exception("No URL specified")

    if len(url) > 2048:
        raise ValueError

    result = urllib.parse.urlparse(url)
    scheme = result.scheme
    domain = result.netloc

    if not scheme:
        raise ValueError  # Exception("No URL scheme specified")

    if not re.fullmatch(SCHEME_FORMAT, scheme):
        raise ValueError

    if not domain:
        raise ValueError  # Exception("No URL domain specified")

    if not re.fullmatch(DOMAIN_FORMAT, domain):
        raise ValueError  # Exception("URL domain malformed (domain={})".format(domain))

    return url
