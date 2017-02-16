from main import GithubAPI
import unittest

class TestMethods(unittest.TestCase):

    """
    Unit tests for Github API class
    """

    def __init__(self, *args, **kwargs):
        self.api = GithubAPI()
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_build_repo_query(self):
        self.assertTrue('https://api.github.com/search/repositories?q=org:google&sort=forks',
                        self.api.build_repo_query('google'))

    def test_build_committers_query(self):
        self.assertTrue('https://api.github.com/repos/histrix/histrix/contributors',
                        self.api.build_committers_query('histrix', 'histrix'))

    def test_process(self):
        self.api.process('google', 5,3)
        results = self.api.get_results()
        self.assertTrue(len(results), 5)
        self.assertTrue(len(results[0]), 3)

suite = unittest.TestLoader().loadTestsFromModule(TestMethods())
unittest.TextTestRunner().run(suite)