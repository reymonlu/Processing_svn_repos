HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) \
        Gecko/20100101 Firefox/55.0",
}
LIST_DOMAIN_FILE: str = "domains.txt"
LIST_GOOD_DOMAINS: str = "good_domains.txt"
LIST_BAD_DOMAINS: str = "bad_domains.txt"
PROTOCOL: str = "https"

"""
How many seconds to wait for the server to send data
before giving up, as a float, or a :ref:`(connect timeout, read
timeout) <timeouts>` tuple.
"""
TIMEOUT = 4
