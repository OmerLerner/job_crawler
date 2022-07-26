class Parser:
    def __init__(self,job_title,location,range,keywords):
        self.job_title = job_title
        self.location = location
        self.range = range
        self.keywords = keywords
        self.jobs_per_page = 25
        self.COLUMN_INDEX = ['A', 'B', 'C', 'D', 'E', 'F']
        self.COLUMNS = ['Job Title', 'Company', 'Location', 'Relevant Keyword', 'Job Link']

        self.extracted_data = []
        self.titles = []
        self.companies = []
        self.locations = []
        self.links = []
        self.relevant_keyword = []

    @abstractmethod
    def parse_job_title(self,job):
        pass

    @abstractmethod
    def parse_job_company(self, job):
        pass

    @abstractmethod
    def parse_job_link(self, job):
        pass

    @abstractmethod
    def parse_job_location(self, job):
        pass

    def add_job(self,job,keyword):
        self.titles.append(self.parse_job_title(job))
        self.companies.append(self.parse_job_company(job))
        self.links.append(self.parse_job_link(job))
        self.locations.append(self.parse_job_location(job))
        self.relevant_keyword.append(keyword)
