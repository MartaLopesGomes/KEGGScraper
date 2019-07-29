# -*- coding: utf-8 -*-
"""

"""

import grequests


class MultipleRequests:
    def __init__(self, urls, size):
        self.urls = urls
        self.size = size

    def exception(self, request, exception):
        print("Problem: {}: {}".format(request.url, exception))

    def async(self):
        results = grequests.imap((grequests.get(u, stream=False) for u in self.urls), exception_handler=self.exception,
                                 size=self.size)
        return results
