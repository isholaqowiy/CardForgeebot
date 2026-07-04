# CardForge Bot 🪪🤖

A high-performance asynchronous Python Telegram bot optimized for Render.com free background worker instances that converts text inputs into high-resolution digital business cards.

## 🚀 Step-by-Step Render Deployment Workflows

### Step 1: Push Source Files Directly to your GitHub Root Directory
Ensure that all required structural files (`bot.py`, `handlers.py`, `database.py`, `config.py`, `card_generator.py`, `qr_generator.py`, `utils.py`, `requirements.txt`, etc.) are placed immediately in the root repository folder. Do not isolate or nest them inside any sub-level workspace project folders:
```bash
git init
git add .
git commit -m "Initialize baseline framework package for CardForge Bot Engine"
git branch -M main
git remote add origin [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
git push -u origin main

