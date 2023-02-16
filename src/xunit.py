class TestCase:
    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def run(self) -> None:
        self.setUp()
        # 自身のインスタンスの名前(つまりテストメソッド名)を取得し、それを実行する
        method = getattr(self, self.name)
        method()


class WasRun(TestCase):

    def setUp(self) -> None:
        self.wasRun: int | None = None
        self.wasSetUp = 1

    def testMethod(self) -> None:
        self.wasRun = 1


class TestCaseTest(TestCase):
    def setUp(self) -> None:
        self.test = WasRun("testMethod")

    def testRunning(self) -> None:
        self.test.run()
        assert (self.test.wasRun)

    def testSetUp(self) -> None:
        self.test.run()
        assert (self.test.wasSetUp)


TestCaseTest("testRunning").run()
TestCaseTest("testSetUp").run()
