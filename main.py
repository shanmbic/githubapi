import requests
import sys

URL_ROOT = 'https://api.github.com/'

class GithubAPI(object):
    
    """
    Class to interact with GithubAPI
    """

    def __init__(self):
        self.session = requests.Session()
        self.results = []
    
    def build_repo_query(self,name):
        """
        Builds the query to get top n repositories of an organisation 
        based on number of forks
        
        Params:
        name: organisation_name 
        """

        query = URL_ROOT + 'search/repositories?q=org:'+name+'&sort=forks'
        return query
    
    def build_committers_query(self, repo, owner):
        """
        Builds the query to get top m committers of the repository

        Params:
        repo: repository_name
        """

        query = URL_ROOT + 'repos/' + owner + '/' + repo + '/contributors'
        return query
        

    def fetch_results(self, query_url):
        """
        Fetch the results from https://api.github.com and returns the results 
        from the Json data returned.

        Params:
        query_url: The full qualified url including the search parameters.
        """
        
        data = self.session.get(query_url).json()
        return data

    def get_results(self):
        return self.results

    def process(self, org_name, n, m):
        """
        Main method to fetch top repositories and then iterate over repositories 
        to fetch top committers

        Params:
        org_name : Organisation
        n : number of repositories
        m : number of committers
        """

        repo_query = self.build_repo_query(org_name)
        repositories = self.fetch_results(repo_query)
        count = n

        if repositories['total_count'] < n:
            print("Only %s repositories available" % format(repositories['total_count']))
            count = repositories['total_count']
        
        for repo in repositories['items'][:count]:

            name = repo['name']
            owner = repo['owner']['login']

            data = {'repo_name':name, 'owner':owner, 'contributors':[]}

            committer_query = self.build_committers_query(name, owner)
            contributors = self.fetch_results(committer_query)
            contri_count = m

            if len(contributors) < m:
                print("Only %s contributors available for Repo:%s" % format(str(len(contributors)), name))
                contri_count = len(contributors)
            
            for contributor in contributors[:contri_count]:
                data['contributors'].append({'name':contributor['login'], 
                                              'commit_counts':contributor['contributions']  })
            
            self.results.append(data)


if __name__=="__main__":
    api = GithubAPI()

    if len(sys.argv)>1:
        """User provided input"""

        org_name,n,m = sys.argv[1:]
        api.process(org_name, int(n), int(m))
        print(api.get_results()) 

    else:
        """Custom input"""

        #Google Test case
        api.process('google', 5,3)
        print (api.get_results())

        #Microsoft Test case
        api.process('microsoft', 6,4)
        print (api.get_results())

                                        
                    
                    

            
            


    

        
        
        
        
        
