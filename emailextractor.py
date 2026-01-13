from email import message_from_string


class EmailBodyExtractor:
    """
    A utility class for extracting the main content from raw email messages.

    Provides functionality to handle both multipart and single-part email
    messages, decoding the content where applicable.

    :ivar TEXT_CONTENT_TYPES: Tuple containing allowed content types for extraction,
        such as plain text or HTML.
    """
    TEXT_CONTENT_TYPES = ('text/plain', 'text/html')

    def extract(self, raw_email):
        """
        Extract the main content from a raw email, either from a multipart or single-part
        email message.

        :param raw_email: The raw email content as a string.
        :return: Decoded email content if the extraction is successful, None otherwise.
        """
        if not raw_email:
            return None

        message = message_from_string(raw_email)

        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition', ''))

                if (
                        content_type in self.TEXT_CONTENT_TYPES
                        and 'attachment' not in content_disposition.lower()
                ):
                    return part.get_payload(decode=True)
        else:
            return message.get_payload(decode=True)

        return None
