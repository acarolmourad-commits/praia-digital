"""HTTP failures propagate; ambiguous delivery remains blocked in a private journal."""
import os
import hashlib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from delivery_journal import send_once, mark_csv_committed
from state_store import identity, validate


def notify(client, token, chat_id, text, kind, day):
    configured = os.environ.get('HERMES_NOTIFICATION_STATE_DIR')
    if not configured:
        raise RuntimeError('Private notification state directory required before sending')
    state = Path(configured)
    if not state.is_absolute() or state.resolve().is_relative_to(Path(__file__).resolve().parents[2]):
        raise RuntimeError('Notification state must be absolute and outside checkout')

    bot_id = token.split(':', 1)[0]
    if not bot_id.isdigit():
        raise RuntimeError('Telegram bot identity unavailable')
    account = 'bot:' + bot_id + ':chat:' + hashlib.sha256(str(chat_id).encode()).hexdigest()
    expected = identity('telegram', account, 'notifications', Path(__file__).resolve().parents[2])
    validate(state, expected)

    def transport(recipient, message):
        # No exception URL/body is logged: Telegram URLs contain the bot token.
        response = client.post('https://api.telegram.org/bot' + token + '/sendMessage',
                               json={'chat_id': recipient, 'text': message}, timeout=(5, 20))
        response.raise_for_status()
        payload = response.json()
        result = payload.get('result') if isinstance(payload, dict) else None
        if (not isinstance(payload, dict) or payload.get('ok') is not True or
                not isinstance(result, dict) or type(result.get('message_id')) is not int or
                not isinstance(result.get('from'), dict) or result['from'].get('id') != int(bot_id)):
            raise RuntimeError('Telegram acknowledgement missing')
        return str(result['message_id']), 0

    receipt = send_once(state.resolve(), kind, day, chat_id, text, transport,
                        lambda output, code: output if code == 0 else None, expected)
    return receipt, expected


def complete_notification(receipt):
    path, expected = receipt
    mark_csv_committed(path, expected)
