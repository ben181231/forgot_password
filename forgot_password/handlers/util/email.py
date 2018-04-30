# Copyright 2016 Oursky Ltd.
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
import logging

import pyzmail

logger = logging.getLogger(__name__)


class Mailer:
    def __init__(self, **smtp_params):
        self.smtp_params = smtp_params

    def send_mail(self, sender, to, subject, text, html=None, reply_to=None):
        """
        Send email to user.

        Arguments:
        sender - (tuple) a tuple of the form ('Name', 'sender@example.com')
        to - (string) - recipient address
        subject - (str) The subject of the message
        text - (tuple or None) The text version of the message
        html - (tuple or None) The HTML version of the message
        reply_to - (tuple) a tuple of the form ('Name', 'reply@example.com')
        """
        encoding = 'utf-8'
        text_args = (text, encoding)
        html_args = (html, encoding) if html else None
        headers = []

        if reply_to and reply_to[1]:
            reply_to_value = pyzmail.generate.format_addresses(
                [reply_to, ], header_name='from', charset=encoding
            )
            headers.append(('Reply-To', reply_to_value))

        payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(
            sender, [to], subject, encoding, text_args,
            html=html_args, headers=headers)

        try:
            pyzmail.send_mail2(payload,
                               mail_from,
                               rcpt_to,
                               **self.smtp_params)
        except Exception:
            logger.exception('Unable to send email to the receipient.')
            raise Exception('Unable to send email to the receipient.')
