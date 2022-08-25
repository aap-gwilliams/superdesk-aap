# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
from .aap_newscentre_formatter import AAPNewscentreFormatter
from .category_list_map import get_nzn_category_list
from copy import deepcopy
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE


class NznNewscentreFormatter(AAPNewscentreFormatter):

    name = "NZN NEWSCENTRE"

    type = "NZN NEWSCENTRE"

    def format(self, article, subscriber, codes=None):
        """
        Constructs a dictionary that represents the parameters passed to the IPNews InsertNews stored procedure
        :return: returns the sequence number of the subscriber and the constructed parameter dictionary
        """
        formatted_article = deepcopy(article)
        mapped_source = formatted_article.get('source', '') if formatted_article.get('source', '') != 'AAP' else 'NZN'

        return self.format_for_source(formatted_article, subscriber, mapped_source, codes)

    def _get_category_list(self, category_list):
        return get_nzn_category_list(category_list)

    def can_format(self, format_type, article):
        return format_type == 'NZN NEWSCENTRE' and article[ITEM_TYPE] in [CONTENT_TYPE.TEXT]
