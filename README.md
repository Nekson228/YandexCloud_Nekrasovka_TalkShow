# YandexCloud Nekrasovka Digest

Yandex Cloud Project for MIPTxYandex Studcamp 2025

## Мультиформатный дайджест с интеграцией нескольких изданий

Создание комплексного медиапродукта, объединяющего материалы из разных газет:

- Работа с несколькими газетными изданиями за одну дату (или период времени), их агрегация и сравнение освещения событий
- Создание тематических блоков с перекрестным анализом ("как это событие освещали разные издания")
- Внедрение формата ток-шоу с "экспертными комментариями"
- Разработка алгоритма для автоматического выявления противоречий или расхождений в освещении одних и тех же событий
- Акцент на создание единой информационной картины дня из разрозненных источников

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.9 or higher
- `pip` (Python package manager)
- A valid Telegram bot token (from [BotFather](https://core.telegram.org/bots#botfather))
- Access to Yandex Cloud services:
  - Yandex Cloud ML Platform
  - Yandex SpeechKit
- At least 1GB of free disk space for historical newspaper data
- Required Python dependencies (see below)

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```
4. Set up your environment variables for the Telegram bot token and any other necessary configurations. You can create a `.env` file in the project directory with the following content:

```env
BOT_TOKEN=your_telegram_bot_token
API_KEY=your_api_key (yandex cloud)
FOLDER_ID=your_folder_id (yandex cloud)
```

5. Configure Yandex Cloud services:
   - Set up Yandex Cloud ML SDK with your credentials
   - Configure SpeechKit access for voice synthesis
   - Initialize the data pipeline for newspaper processing

6. Run the bot:

```bash
python main.py
```

## Usage

Once the bot is running, you can interact with it through Telegram. Send text queries about historical newspapers from 1936 (currently), and the bot will:
- Process your query using the RAG pipeline
- Return relevant information from the newspaper archive
- Provide an audio version of the response when available

## Project Structure

```
├── main.py                         # Application entry point
├── requirements.txt                # Project dependencies
├── nodes/                          # Historical newspaper data (1936)
│   └── [dates]/                    # Daily newspaper articles
├── notebooks/             
│   └── preproc.ipynb               # Data preprocessing notebook
└── src/
    ├── bot/                        # Telegram bot implementation
    │   ├── handlers.py             # Message handlers
    │   ├── queue_manager.py        # Request queue management
    │   └── utils.py                # Utility functions
    ├── models/                     # Data models
    │   └── date_range.py           # Date handling model
    ├── rag_pipeline/               # RAG pipeline
    │   ├── assistant/              # AI assistant management
    │   ├── data/                   # Data handling
    │   ├── indexing/               # Search indexing
    │   ├── uploading/              # Data upload functionality
    │   └── pipeline.py             # Main pipeline implementation
    ├── services/                   # External services integration
    │   ├── ai.py                   # AI service implementation
    │   └── speech.py               # Speech synthesis service
    ├── utils/                      # Utility functions
    │   └── date_llm_parser.py      # Date parsing utilities
    └── settings.py                 # Application configuration
```
