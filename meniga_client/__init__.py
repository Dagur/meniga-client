import requests
import json
from .utils import meniga_datetime, TokenExtractor

USER_AGENT = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, " \
             "like Gecko) Chrome/45.0.2454.101 Safari/537.36"
BASE_URL = "https://www.meniga.is"


class Meniga:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = None
        self.verification_token = None

    def _authenticate(self):
        self.session = requests.Session()

        r = self.session.post(BASE_URL + "/User/LogOn",
                              headers={"user-agent": USER_AGENT},
                              data={
                                  "culture": "is-IS",
                                  "email": self.username,
                                  "password": self.password})

        parser = TokenExtractor()
        parser.feed(r.text)
        self.verification_token = parser.token
        if not self.verification_token:
            raise ValueError("Invalid username or password?")

    def _fetch(self, path, params):
        if not self.session:
            self._authenticate()

        r = self.session.post(
            BASE_URL + path,
            headers={"user_agent": USER_AGENT, "__RequestVerificationToken": self.verification_token},
            data=json.dumps(params))

        return json.loads(r.text)

    def synchronize(self):
        if not self.session:
            self._authenticate()

        r = self.session.post(BASE_URL + "/Api/Transactions/StartSynchronization",
                              headers={"user_agent": USER_AGENT, "__RequestVerificationToken": self.verification_token},
                              data=json.dumps({"waitForCompleteMilliseconds": 5000}))

        return json.loads(r.text)

    def get_transactions_page(self, params=None):
        """
        {
            'identifier': 'getTransactionsPage',
            'path': '/Api/Transactions/GetTransactionsPage',
            'description': 'Fetches data on transactions and their categories over timespans',
            'params': [
                {'name': 'page', 'type': 'integer', 'description': 'the page number to fetch'},
                {'name': 'transactionsPerPage', 'type': 'integer', 'description': 'the number of transactions per page'},
                {'name': 'filter', 'type': 'object', 'description': 'the filters to apply', 'subProperties': [
                    {'name': 'PeriodFrom', 'type': 'datetime', 'description': 'lower bound timestamp'},
                    {'name': 'PeriodTo', 'type': 'datetime', 'description': 'upper bound timestamp'},
                ]}
            ]
        }
        """
        return self._fetch("/Api/Transactions/GetTransactionsPage", params and params or {})

    def create_user_category(self, params=None):
        """
        {
            identifier: 'createUserCategory',
            path: '/Api/User/CreateUserCategory',
            params: [
              { name: 'categoryType', type: 'string', description: 'expenses ("0")' },
              { name: 'isFixedExpenses', type: 'boolean', description: 'whether this is fixed or variable expenses' },
              { name: 'name', type: 'string', description: 'the name of the new category' },
              { name: 'parentId', type: 'string', description: 'the parent category of the new category' }
            ]
        }
        """
        return self._fetch("/Api/User/CreateUserCategory", params and params or {})

    def get_budget_equation_widget(self, params=None):
        """
        {
            identifier: 'getBudgetEquationWidget',
            path: '/Api/Widgets/GetBudgetEquationWidget',
            params: [
              { name: 'period', type: 'integer', description: 'no idea...' }
            ]
        }
        """
        return self._fetch("/Api/Widgets/GetBudgetEquationWidget", params and params or {})

    def get_user_categories(self, params=None):
        """
        {
            identifier: 'getUserCategories',
            path: '/Api/User/GetUserCategories',
            description: 'Fetches data on all public categories and the ones created by the currently logged in user.',
            params: []
        }
        """
        return self._fetch("/Api/User/GetUserCategories", params and params or {})

    def get_trends_report(self, params=None):
        """
        {
            identifier: 'getTrendsReport',
            path: '/Api/Planning/GetTrendsReport',
            description: 'An analytics endpoint allowing you to analyze your expenses by categories and over timespans',
            params: [
              { name: 'filter', type: 'object', description: 'the filters to apply', subProperties: [
                { name: 'View', type: 'integer', defaults: 1, description: '1 = sum over all months, 2 = group by month' },
                { name: 'Type', type: 'integer', defaults: 1, description: '1 = im not sure, just use that' },
                { name: 'Tags', type: 'array[string]', defaults: null, description: 'the tags to analyze, null to ignore.'},
                { name: 'Period', type: 'string', defaults: '0', description: '0=this month, 1=last month, 3=last 3 months, 6=last 6 months, 12=last 12 months, -1=this year, -2=last year'},
                { name: 'PeriodFrom', type: 'datetime', defaults: null, description: 'lower bound timestamp, overrides "Period".' },
                { name: 'PeriodTo', type: 'datetime', defaults: null, description: 'upper bound timestamp, overrides "Period".' },
                { name: 'Merchants', type: 'string', defaults: null, description: 'im not sure, null is default.' },
                { name: 'Group', type: 'integer', defaults: 1, description: 'im not sure' },
                { name: 'CategoryIds', type: 'array[integer]', description: 'IDs of the categories to analyze' },
                { name: 'AccountIdentifiers', type: '?', defaults: null, description: '?' },
                { name: 'AccountIds', type: '?', defaults: null, description: '?' },
                { name: 'ComparisonPeriod', type: '?', defaults: null, description: '?' },
                { name: 'Options', type: 'object', description: 'additional options to apply', subProperties: [
                  { name: 'AccumulateCategoryExpenses', type: 'boolean', defaults: false, description: '?' },
                  { name: 'DateFormat', type: '?', defaults: null, description: '?' },
                  { name: 'DisableSliceGrouping', type: '?', defaults: false, description: '?' },
                  { name: 'ExcludeNonMappedMerchants', type: '?', defaults: false, description: '?' },
                  { name: 'FutureMonths', type: 'integer', description: '?' },
                  { name: 'GetAverage', type: 'boolean', defaults: false, description: '?' },
                  { name: 'GetFuture', type: 'boolean', description: '?' },
                  { name: 'IncludeSavingsInNetIncome', type: 'boolean', defaults: true, description: '?' },
                  { name: 'IsParent', type: 'boolean', defaults: true, description: '?' },
                  { name: 'MaxSlicesInPie', type: 'integer', defaults: 10, description: '?' },
                  { name: 'MaxTopMerchants', type: 'integer', defaults: 10, description: '?' },
                  { name: 'MinPieSliceValue', type: 'integer', defaults: 1, description: '?' },
                  { name: 'MinSlicesInPie', type: 'integer', defaults: 5, description: '?' },
                  { name: 'SkipInvertedCategories', type: 'boolean', defaults: false, description: '?' },
                  { name: 'UseAndSearchForTags', type: 'boolean', defaults: false, description: '?' }
                ] }
              ] }
            ]
        }
        """
        return self._fetch("/Api/Planning/GetTrendsReport", params and params or {})
