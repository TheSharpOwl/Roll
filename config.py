#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 3978))
    APP_ID = os.environ.get("MICROSOFT_APP_ID", "")
    APP_PASSWORD = os.environ.get("MICROSOFT_APP_PASSWORD", "")
    # You can put the knowledge base qna service keys here (put them as environment variables in your os and they will be subsitituded here)
    QNA_KNOWLEDGEBASE_ID = os.environ.get("QNA_KNOWLEDGEBASE_ID", "")
    QNA_ENDPOINT_KEY = os.environ.get("QNA_ENDPOINT_KEY", "")
    QNA_ENDPOINT_HOST = os.environ.get("QNA_ENDPOINT_HOST", "")
