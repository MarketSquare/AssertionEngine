# Copyright 2021-     Robot Framework Foundation
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
# limitations under the License.

from typing import Any

FALSE_STRINGS = {"FALSE", "NO", "OFF", "0", "UNCHECKED", "NONE", ""}


def type_converter(argument: Any) -> str:
    return type(argument).__name__.lower()


def is_truthy(item: Any) -> bool:
    if isinstance(item, bool):
        return item
    if isinstance(item, str):
        return item.upper() not in FALSE_STRINGS
    return bool(item)


def is_string(item: Any) -> bool:
    return isinstance(item, str)
