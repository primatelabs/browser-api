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

import argparse
import os

import requests

import geekbench

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument("--hostname", default=os.environ.get('BROWSER_API_HOST', 'browser.geekbench.com'))
  parser.add_argument("--protocol", default="https")
  parser.add_argument("--benchmark", default="cpu_v7")
  parser.add_argument('--key', default=os.environ.get('BROWSER_API_KEY'))
  parser.add_argument("--id")


  args = parser.parse_args()

  url = f'{args.protocol}://{args.hostname}/api/v1/{args.benchmark}/{args.id}'

  headers = {
    "Authorization": f"Bearer {args.key}"
  }

  params = {
  }

  response = requests.get(url, headers=headers, params=params)

  data = response.json()['data']

  geekbench.print_document_summary(data)


if __name__ == '__main__':
  main()
