from types import SimpleNamespace

from app import ask as ask_module


class FakeChat:
    def __init__(self):
        self.questions = []

    def send_message(self, question):
        self.questions.append(question)
        return SimpleNamespace(
            usage_metadata=SimpleNamespace(
                prompt_token_count=1,
                candidates_token_count=2,
            ),
            text=f"回答: {question}",
        )


def test_run_conversation_reuses_chat_and_stops_on_empty_question(monkeypatch):
    chat = FakeChat()
    questions = iter(["続きの質問", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    ask_module.run_conversation("最初の質問", chat)

    assert chat.questions == ["最初の質問", "続きの質問"]


def test_ask_sends_question_to_given_chat(capsys):
    chat = FakeChat()

    answer = ask_module.ask("質問", chat)

    assert answer == "回答: 質問"
    assert chat.questions == ["質問"]
    assert "[入力トークン数] 1" in capsys.readouterr().out
