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
import asyncio
import json
import logging
import os
import sys

import websockets

import geekbench


log = logging.getLogger('firehose')


def handle_frame(raw):
  try:
    frame = json.loads(raw)
  except json.JSONDecodeError:
    log.warning(f'Ignoring non-JSON frame: {raw}')

  frame_type = frame.get('type')

  # Control frames from Action Cable. The control frames (or messages) follow
  # the Action Cable protocol. This sample firehose client ignores most of the
  # control frames to keep the implementation simple.

  if frame_type == 'ping':
    return
  if frame_type == 'welcome':
    log.info('welcome')
    return
  if frame_type == 'confirm_subscription':
    log.info('confirm subscription')
    return
  if frame_type == 'reject_subscription':
    log.info('reject subscription')
    return
  if frame_type == 'disconnect':
    reason = frame.get('reason', 'unknown')
    raise ConnectionError(f'Server requested disconnect: {reason}')

  # Data frames (or messages). This sample firehose client ignores the
  # identifier field since the Browser API only implements one channel.

  message = frame.get('message')
  if isinstance(message, str):
    try:
      message = json.loads(message)
    except json.JSONDecodeError:
      return
  if not isinstance(message, dict):
    return

  event = message.get('type')

  # The create event triggers whenever a new benchmark document is uploaded
  # to the Geekbench Browser. The event contains both metadata (e.g., the
  # Geekbench Browser identifier for the document) and data (i.e., the
  # document JSON file).

  if event == 'create':
    data = message.get('data') or {}
    geekbench.print_document_summary(data)
  if event == 'update':
    pass


async def main():
  parser = argparse.ArgumentParser()

  parser.add_argument("--hostname", default=os.environ.get('BROWSER_API_HOST', 'browser.geekbench.com'))
  parser.add_argument('--key', default=os.environ.get('BROWSER_API_KEY'))

  args = parser.parse_args()

  logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stderr,
  )

  url = f'wss://{args.hostname}/cable'

  headers = {
    "Authorization": f"Bearer {os.environ['BROWSER_API_KEY']}"
  }

  params = {
  }

  async with websockets.connect(url, additional_headers=headers) as ws:
    log.info('connected')
    subscribe_message = {
      "command": "subscribe",
      "identifier": "{\"channel\": \"DocumentsChannel\"}"
    }
    await ws.send(json.dumps(subscribe_message))
    log.info(f'sent: {subscribe_message}')

    try:
      async for raw in ws:
        handle_frame(raw)
    except websockets.ConnectionClosed:
      log.warning('disconnected')


if __name__ == '__main__':
  asyncio.run(main())
