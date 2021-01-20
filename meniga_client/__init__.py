import requests

USER_AGENT = (
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/45.0.2454.101 Safari/537.36"
)
BASE_URL = "https://api.meniga.is/v1/"


class Meniga:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = None
        self.verification_token = None

    def _authenticate(self):
        self.session = requests.Session()

        r = self.session.post(
            BASE_URL + "authentication",
            headers={
                "user-agent": USER_AGENT,
            },
            json={
                "culture": "is-IS",
                "email": self.username,
                "password": self.password,
            },
        )

        response = r.json()
        self.verification_token = response["data"]["accessToken"]
        if not self.verification_token:
            raise ValueError("Invalid username or password?")

    def _fetch(self, path, params):
        if not self.session:
            self._authenticate()

        r = self.session.get(
            BASE_URL + path,
            headers={
                "user_agent": USER_AGENT,
                "Authorization": f"Bearer {self.verification_token}",
            },
            json=params,
        )

        return r.json()

    def get_transactions(
        self,
        accountIds=None,
        accountTypes=None,
        take=50,
        skip=0,
        useExactDescription=False,
        useExactMerchantTexts=False,
    ):
        """
        take: number
        skip: number
        accountIds: string (comma separated)
        accountTypes: string (comma separated)
        useExactDescription: boolean
        useExactMerchantTexts: boolean

        """

        params = {
            "take": take,
            "skip": skip,
            "useExactDescription": str(useExactDescription),
            "useExactMerchantTexts": str(useExactMerchantTexts),
        }
        if accountIds:
            params["accountIds"] = accountIds
        if accountTypes:
            params["accountTypes"] = accountTypes
        return self._fetch("transactions", params)

    def get_accounts(
        self,
        skip=0,
        take=1000,
        includeHidden=True,
        includeDisabled=True,
    ):
        """
        skip: number
        take: number
        includeHidden: boolean
        includeDisabled: boolean
        """
        params = {
            "skip": skip,
            "take": take,
            "includeHidden": str(includeHidden),
            "includeDisabled": str(includeDisabled),
        }
        return self._fetch("accounts", params)