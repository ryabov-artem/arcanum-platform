# Arcanum 2.0 Architecture

## Goal

Arcanum 2.0 is not a redesign of the Tarot bot UI.

Arcanum 2.0 is the infrastructure foundation for a network of AI Telegram bots:

- Tarot
- Numerology
- Astrology
- Runes
- Dream interpretation

## Current production app

Current working bot lives in:

```text
app/

Production services:

tarot-bot.service
tarot-webhook.service

Current database:

/opt/bots/tarot_bot/data/database.db
Safety rules

Do not break production.

Before changing files:

cp file.py file.py.bak_$(date +%F_%H-%M-%S)

After significant changes:

git add .
git commit -m "description"
git push

Backups are already configured:

local backups: /opt/backups/arcanum
Google Drive: ArcanumBackups
cron: daily at 03:00
Target structure
core/
  ai/
  database/
  payments/
  analytics/
  users/
  mailing/

bots/
  tarot/
  numerology/
  astrology/
  runes/
  dreams/

admin/
docs/
Current file map
app/main.py

Main monolith. Contains:

user handlers
admin handlers
payment creation
keyboards
spread access logic
broadcast logic
bot startup

Target split:

core/users/
core/payments/
core/analytics/
core/mailing/
admin/
bots/tarot/
app/database.py

Database layer. Contains:

users
daily cards
spreads
free spread access
balance
payments
analytics
top users

Target split:

core/database/
core/users/
core/payments/
core/analytics/
bots/tarot/storage
app/ai.py

AI interpretation functions.

Target split:

core/ai/client.py
bots/tarot/ai.py
app/webhook.py

YooKassa webhook and Telegram payment notification.

Target split:

core/payments/yookassa_webhook.py
core/notifications/telegram.py
app/cards.py, app/tarot.py, app/prompts.py

Tarot-specific logic.

Target:

bots/tarot/
Migration strategy
Phase 1

Create architecture folders and documentation only.
No production imports changed.

Phase 2

Extract admin handlers from app/main.py.

Phase 3

Extract payment creation from app/main.py.

Phase 4

Extract user handlers from app/main.py.

Phase 5

Split database layer by domain.

Phase 6

Create reusable core for new bots.

Phase 7

Create first new bot: Numerology.

Important principle

Each refactoring step must preserve production behavior.

After each step:

python -m py_compile app/*.py
sudo systemctl restart tarot-bot.service
sudo systemctl restart tarot-webhook.service
sudo systemctl status tarot-bot.service
sudo systemctl status tarot-webhook.service
git add .
git commit -m "..."
git push

