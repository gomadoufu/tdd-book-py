
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

    def run(self, result: TestResult) -> None:
        result.testStarted()
        self.setUp()
        # 自身のインスタンスの名前(つまりテストメソッド名)を取得し、それを実行する
        try:
            method = getattr(self, self.name)
            method()
        except BaseException:
            result.testFailed()
        self.tearDown()


class TestSuite:
    def __init__(self) -> None:
        self.tests: list[TestCase] = []

    def add(self, test: TestCase) -> None:
        self.tests.append(test)

    def run(self, result: TestResult) -> None:
        for test in self.tests:
            test.run(result)


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
    def setUp(self) -> None:
        self.result = TestResult()

    def testTemplateMethod(self) -> None:
        test = WasRun("testMethod")
        test.run(self.result)
        assert ("setUp testMethod tearDown " == test.log)

    def testResult(self) -> None:
        test = WasRun("testMethod")
        test.run(self.result)
        assert ("1 run, 0 failed" == self.result.summary())

    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert ("1 run, 1 failed" == self.result.summary())

    def testFailedResultFormatting(self) -> None:
        self.result.testStarted()
        self.result.testFailed()
        assert ("1 run, 1 failed" == self.result.summary())

    def testSuite(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.run(self.result)
        assert ("2 run, 1 failed" == self.result.summary())


suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testSuite"))
result = TestResult()
suite.run(result)
print(result.summary())
