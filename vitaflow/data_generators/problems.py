# coding=utf-8
# Copyright 2019 The vitaFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Forked from https://github.com/tensorflow/tensor2tensor

"""Access vitaFlow Problems."""

from vitaflow.data_generators import all_problems
from vitaflow.utils import registry


def problem(name):
  return registry.problem(name)


def available():
  return registry.list_base_problems()


all_problems.import_modules(all_problems.ALL_MODULES)
