import framework
# unique to module

class Module(framework.module):

    def __init__(self, params):
        framework.module.__init__(self, params)
        self.register_option('host', self.goptions['domain']['value'], 'yes', 'target host')
        self.info = {
                     'Name': 'McAfee Domain Affiliation Lookup',
                     'Author': 'Micah Hoffman (@WebBreacher)',
                     'Description': 'Checks mcafee.com site for other domains affiliated with a domain.',
                     'Comments': []
                     }
   
    def module_run(self):
        host = self.options['host']['value']

        url = 'http://www.mcafee.com/threat-intelligence/jsproxy/domain.ashx?q=affiliation&f=%s' % (host)
        self.verbose('URL: %s' % url)
        resp = self.request(url)
        if not resp.json:
            self.error('Invalid JSON response.\n%s' % (resp.text))
            return

        # Output the results in table format
        tdata = [] 
        tdata.append(['Domain/URL', 'Category', 'Links'])
        for col in resp.json:
            tdata.append([col['label'], col['hover'], str(col['link'])]) 
        self.table(tdata, True)
