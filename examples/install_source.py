# Copyright 2021 RelationalAI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

from argparse import ArgumentParser
import json
from os import path
from urllib.request import HTTPError
from railib import api, config, show


# Reeturns the file basename without extension.
def _sansext(fname: str) -> str:
    return path.splitext(path.basename(fname))[0]


def run(database: str, engine: str, fname: str):
    sources = {}
    with open(fname) as fp:
        sources[_sansext(fname)] = fp.read()  # source name => source
    cfg = config.read()
    ctx = api.Context(**cfg)
    rsp = api.install_source(ctx, database, engine, sources)
    print(json.dumps(rsp, indent=2))


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("database", type=str, help="database name")
    p.add_argument("engine", type=str, help="engine name")
    p.add_argument("file", type=str, help="source file")
    args = p.parse_args()
    try:
        run(args.database, args.engine, args.file)
    except HTTPError as e:
        show.http_error(e)
