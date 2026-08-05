# Discord AI Messages Assistant
DAMA (Discord AI Messages Assistant) is an AI-powered Discord bot built with **Python**, **discord.py**, and **Google Gemini** that helps communities interact with their conversations through AI.

## Features
- 💬 **/ask** — Ask Gemini anything directly from Discord.
- 📝 **/summary** — Summarize recent channel discussions with context awareness.
- 🧠 Prompt-based architecture for easy customization.
- ☁️ Deployed on Railway for 24/7 availability.

## Tech Stack
- Python 3.11
- discord.py
- Google Gemini API
- Railway

## Project Structure

```text
.
├── bot.py
├── config/
├── prompts/
├── services/
├── requirements.txt
└── .env
```

## Quick Start

```bash
git clone https://github.com/mxsry/Discord-AI-Messages-Assistant.git
cd Discord-AI-Messages-Assistant

python -m venv .venv
pip install -r requirements.txt

python bot.py
```

Create a `.env` file:

```env
DISCORD_TOKEN=your_discord_token
GEMINI_API_KEY=your_gemini_api_key
```

## Commands

| Command | Description |
|---------|-------------|
| `/ask` | Ask the AI a question |
| `/summary` | Summarize recent channel messages |

## Roadmap

- [x] AI Chat
- [x] Conversation Summarization
- [x] Prompt Template System
- [x] Railway Deployment
- [ ] Context-aware AI
- [ ] Server Knowledge Base
- [ ] Semantic Search (RAG)
