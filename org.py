# Copyright 2022, Hauke Rehfeld
#
# This file is part of whisper.cpp-to-orgmode.
#
# whisper.cpp-to-orgmode is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# whisper.cpp-to-orgmode is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with
# whisper.cpp-to-orgmode. If not, see <https://www.gnu.org/licenses/>.
#
import conventions

org_date_format = "%Y-%m-%d %a %H:%M"


org_ext = ".org"
heading_max_num_words = 20
heading_num_words = 14


def simple_headline(uuid, heading, content_str, created_date):
    created_date = created_date.strftime(org_date_format)

    res = f"""* {heading}
:PROPERTIES:
:CREATED: [{created_date}]
:ID: {uuid}
:END:
{content_str}
"""
    return res


def atomic_note(uuid, text, created_date):
    text_words = text.split()
    if len(text_words) > heading_max_num_words:
        heading = " ".join(text_words[:heading_num_words])
    else:
        heading = text
        text = ''

    note = simple_headline(uuid, heading, text, created_date)
    return note
