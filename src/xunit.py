
class TestResult:
    def __init__(self) -> None:
        self.runCount = 0
        self.errorCount = 0

    def testStarted(self) -> None:
        self.runCount = self.runCount + 1

    def testFailed(self) -> None:
        self.errorCount = self.errorCount + 1

    def summary(self) -> str:
        return "%d run, %d failed" % (self.runCount, self.errorCount)


class TestCase:
    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def run(self) -> TestResult:
        result = TestResult()
        result.testStarted()
        self.setUp()
        # 自身のインスタンスの名前(つまりテストメソッド名)を取得し、それを実行する
        try:
            method = getattr(self, self.name)
            method()
        except BaseException:
            result.testFailed()
        self.tearDown()
        return result


class WasRun(TestCase):

    def setUp(self) -> None:
        self.log: str = "setUp "

    def testMethod(self) -> None:
        self.log = self.log + "testMethod "

    def testBrokenMethod(self) -> None:
        raise Exception

    def tearDown(self) -> None:
        self.log = self.log + "tearDown "


class TestCaseTest(TestCase):

    def testTemplateMethod(self) -> None:
        test = WasRun("testMethod")
        test.run()
        assert ("setUp testMethod tearDown " == test.log)

    def testResult(self) -> None:
        test = WasRun("testMethod")
        result = test.run()
        assert ("1 run, 0 failed" == result.summary())

    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        result = test.run()
        assert ("1 run, 1 failed" == result.summary())

    def testFailedResultFormatting(self) -> None:
        result = TestResult()
        result.testStarted()
        result.testFailed()
        assert ("1 run, 1 failed" == result.summary())


print(TestCaseTest("testTemplateMethod").run().summary())
print(TestCaseTest("testResult").run().summary())
print(TestCaseTest("testFailedResult").run().summary())
print(TestCaseTest("testFailedResultFormatting").run().summary())
