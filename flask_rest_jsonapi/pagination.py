# -*- coding: utf-8 -*-

"""Helper to create pagination links according to jsonapi specification"""

from __future__ import division
from six.moves.urllib.parse import urlencode
from copy import copy

from flask import current_app


def add_pagination_links(data, object_count, querystring, base_url):
    """Add pagination links to result

    :param dict data: the result of the view
    :param int object_count: number of objects in result
    :param QueryStringManager querystring: the managed querystring fields and values
    :param str base_url: the base url for pagination
    """
    links = {}
    all_qs_args = copy(querystring.querystring)

    links['self'] = base_url

    # compute self link
    if all_qs_args:
        links['self'] += '?' + urlencode(all_qs_args)

    if querystring.pagination.get('limit') != '0' and object_count > 1:
        # compute last link
        limit = int(querystring.pagination.get('limit', 0)) or current_app.config['PAGE_SIZE']
        last_page = (object_count - 1) // limit

        if object_count > limit:
            links['first'] = links['last'] = base_url

            offset = int(all_qs_args.pop('page[offset]', 0))

            # compute first link
            if all_qs_args:
                links['first'] += '?' + urlencode(all_qs_args)

            all_qs_args.update({'page[offset]': last_page * limit})
            links['last'] += '?' + urlencode(all_qs_args)

            # compute previous and next link
            if offset > limit:
                all_qs_args.update({'page[offset]': offset - limit})
                links['prev'] = '?'.join((base_url, urlencode(all_qs_args)))
            if offset + limit < object_count:
                all_qs_args.update({'page[offset]': offset + limit})
                links['next'] = '?'.join((base_url, urlencode(all_qs_args)))

    data['links'] = links
