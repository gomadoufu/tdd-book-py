class TestCase:
    def __init__(self, name: str):
        self.name = name

    def run(self) -> None:
        # 自身のインスタンスの名前(つまりテストメソッド名)を取得し、それを実行する
        method = getattr(self, self.name)
        method()


class WasRun(TestCase):
    def __init__(self, name: str):
        self.wasRun: int | None = None
        super().__init__(name)

    def testMethod(self) -> None:
        self.wasRun = 1


class TestCaseTest(TestCase):
    def testRunning(self) -> None:
        test = WasRun("testMethod")
        assert (not test.wasRun)
        test.run()
        assert (test.wasRun)


TestCaseTest("testRunning").run()
