from chatbot.chat_bot import run_chat_bot


def main():
    run_chat_bot()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
