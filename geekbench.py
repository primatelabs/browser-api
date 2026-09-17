#!/usr/bin/env python3

# Copyright 2026 Primate Labs Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import json

def print_document_summary(data):
  document = data.get('document') or {}
  metrics = get_metrics(document)

  print(data.get('created_at'), data.get('id'))

  document_version = document.get('document_version')
  document_type = document.get('document_type')

  if document_version in [6, 7]:
    if document_type in [0]:
      # CPU Benchmark result from Geekbench 6 or Geekbench 7.

      print('Model:                   ', metrics.get('Model'))
      print('CPU:                     ', metrics.get('CPU'))
      print('Platform:                ', metrics.get('Platform'))
      print('Single-Core Score:       ', document.get('score'))
      print('Multi-Core Score:        ', document.get('multicore_score'))

    if document_type in [1]:
      # GPU Benchmark result from Geekbench 6 or Geekbench 7.

      # Geekbench 7 switched from using "compute" to using "gpu" in variable
      # names. Handle that switch here when gathering the GPU API and name.

      if document_version == 6:
        api_id = document.get('compute_api')
        device = document.get('compute_device_name')
      if document_version == 7:
        api_id = document.get('gpu_api')
        device = document.get('gpu_device_name')
      api = lookup_gpu_api(api_id)

      print('Model:                   ', metrics.get('Model'))
      print('GPU:                     ', device)
      print('Platform:                ', metrics.get('Platform'))
      print('GPU API:                 ', api)
      print('GPU Score:               ', document.get('score'))

  if document_version in [1]:
    if document_type in [1]:
      # AI Benchmark result from Geekbench AI.

      print('Model:                   ', metrics.get('Model'))
      print('AI Device:               ', document.get('device_name'))
      print('AI Framework:            ', document.get('framework_name'))
      print('AI Backend:              ', document.get('backend_name'))
      print('Platform:                ', metrics.get('Platform'))
      print('Single Precision Score:  ', document.get('f32_score'))
      print('Half Precision Score:    ', document.get('f16_score'))
      print('Quantized Score:         ', document.get('i8_score'))

  print('---')

# Returns a dictionary of metrics for the document. The keys will be the name
# of the metric and the values will be the value entry of the metric.

def get_metrics(document, metric_names=[]):
  result = {}
  for metric_name in metric_names:
    result[metric_name] = ''

  document_metrics = document['metrics']
  for document_metric in document_metrics:
    document_metric_name = lookup_name(document_metric['id'])
    result[document_metric_name] = document_metric['value']

  return result

# Returns the GPU API name for the given GPU API identifier. Iidentifiers are
# stable across all Geekbench versions.

def lookup_gpu_api(id):
  gpu_api_names = {
    1: "CUDA",
    2: "Metal",
    3: "OpenCL",
    4: "OpenGL",
    5: "RenderScript",
    6: "Vulkan"
  }
  return gpu_api_names.get(id)

# Returns the system metric name for the given system metric identifier.
# Iidentifiers are stable across all Geekbench versions.

def lookup_name(id):
  metric_names = {
    1: "Platform",
    2: "Compiler",
    3: "Operating System",
    4: "Model ID",
    5: "Model",
    6: "Motherboard",
    7: "Processor ID",
    8: "Processor Brand",
    9: 'CPU',
    10: "Processor Codename",
    11: "Processor Package",
    12: "Threads",
    13: "Cores",
    14: "CPUs",
    15: "Processor Frequency",
    16: "Stock Processor Frequency",
    17: "L1 Instruction Cache",
    18: "L1 Instruction Cache Count",
    19: "L1 Data Cache",
    20: "L1 Data Cache Count",
    21: "L2 Cache",
    22: "L2 Cache Count",
    23: "L3 Cache",
    24: "L3 Cache Count",
    25: "L4 Cache",
    26: "L4 Cache Count",
    27: "Bus Frequency",
    28: "Stock Bus Frequency",
    29: "Memory Size",
    30: "Memory Type",
    31: "BIOS",
    32: "Northbridge",
    33: "Southbridge",
    34: "GPU 1",
    38: "Chassis Manufacturer",
    39: "Chassis Type",
    40: "Power Mode",
    41: "Build",
    42: "Build Tags",
    43: "Secure",
    44: "Governor",
    45: "Cluster Count",
    46: "Cluster 1 Description",
    47: "Cluster 1 Core Count",
    48: "Cluster 1 Minimum Frequency",
    49: "Cluster 1 Maximum Frequency",
    51: "Cluster 2 Description",
    52: "Cluster 2 Core Count",
    53: "Cluster 2 Minimum Frequency",
    54: "Cluster 2 Maximum Frequency",
    56: "Cluster 3 Description",
    57: "Cluster 3 Core Count",
    58: "Cluster 3 Minimum Frequency",
    59: "Cluster 3 Maximum Frequency",
    61: "Cluster 4 Description",
    62: "Cluster 4 Core Count",
    63: "Cluster 4 Minimum Frequency",
    64: "Cluster 4 Maximum Frequency",
    66: "Processor Minimum Multiplier",
    67: "Processor Maximum Multiplier",
    68: "Processor Minimum Frequency",
    69: "Processor Maximum Frequency",
    70: "Power Plan",
    71: "Screen Width",
    72: "Screen Height",
    73: "Screen Scale",
    74: "OS Release ID",
    75: "Memory Frequency",
    76: "Memory Channels",
    77: "CAS Latency",
    78: "RAS to CAS Delay",
    79: "RAS Precharge",
    80: "Cycle Time",
    81: "Bank Cycle Time",
    82: "Command Rate",
    87: "Transfer Rate",
    88: "Compiler Name",
    89: "CPU Frequency (MHz)",
    90: "Kernel",
    122: "Hostname",
    123: "Thermal State",
    1000: "Compute Device",
    1003: "API",
    1004: "Driver Version",
    10000: "Framework",
    10001: "Backend",
    10027: "Device",
    15000: "GenAI Framework",
    15001: "GenAI Backend",
    15002: "GenAI Device",
  }
  return metric_names.get(id)
