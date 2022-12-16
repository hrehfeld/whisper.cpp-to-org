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
import datetime


def guess_date_from_filename(filename):
    date = datetime.datetime.strptime(filename.stem, "%Y-%m-%d %H.%M.%S")
    return date
