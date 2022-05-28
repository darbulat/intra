from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models

from intra.models import User


class MessageModel(models.Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='user',
                             related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                                  verbose_name='recipient',
                                  related_name='to_user')
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField('body')

    def __str__(self):
        return str(self.body)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id),
                                                notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id),
                                                notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()
