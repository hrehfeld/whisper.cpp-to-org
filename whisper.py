#!/usr/bin/env python3
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
import sys
import subprocess
from pathlib import Path
import shlex

sample_rate = 16000

ffmpeg_command = [
    "ffmpeg",
    "-loglevel",
    "quiet",
]
ffmpeg_options = [
    "-filter:a",
    "speechnorm=e=50:r=0.0001:l=1:peak=0.99",
    "-ar",
    str(sample_rate),
    "-ac",
    "1",
    "-c:a",
    "pcm_s16le",
    "-f",
    "wav",
]


def transcribe(whisper_command, input_file):

    # temp_filepath = Path(tempfile.mktemp(suffix=".wav"))
    # print("-----", temp_filepath)
    # process = subprocess.check_call(
    # ffmpeg_command
    # + [
    #     "-i",
    #     input_file,
    # ]
    # + ffmpeg_options
    #     stdout=subprocess.DEVNULL,
    # )
    # subprocess.check_call(
    #     whisper_command + ["--output-txt", temp_filepath],
    #     # stdout=subprocess.DEVNULL,
    #     stderr=subprocess.DEVNULL,
    # )
    # # os.remove(temp_filepath)
    # print("-----", temp_filepath)
    # out_filepath = temp_filepath.with_suffix(temp_filepath.suffix + ".txt")

    cmd = (
        ffmpeg_command
        + [
            "-i",
            input_file,
        ]
        + ffmpeg_options
        + ["-"]
    )
    # print(" ".join([shlex.quote(str(x)) for x in cmd]))
    # just text subprocess pipes
    ffmpeg = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
    )
    cmd = whisper_command + ["--output-txt", "-f", "-"]
    # print(" ".join([shlex.quote(str(x)) for x in cmd]))
    whisper = subprocess.Popen(
        cmd,
        stdin=ffmpeg.stdout,
        stdout=subprocess.PIPE,
        # for some reason theres a lot of chatter on stderr
        stderr=subprocess.DEVNULL,
    )
    # fixme: linter complains about stdout being null
    ffmpeg.stdout.close()
    whisper.communicate()

    assert whisper.returncode == 0

    out_filepath = Path("-.txt")

    res = out_filepath.read_text()
    out_filepath.unlink()

    res = res.strip()
    silence_marker = "[Silence]"
    while res.endswith(silence_marker):
        res = res[: -len(silence_marker)].strip()

    return res


if __name__ == "__main__":
    input_files = [Path(p) for p in sys.argv[1:]]

    for input_file in input_files:
        print(f"processing {input_file}")
        res = transcribe(input_file)
        print(res)
