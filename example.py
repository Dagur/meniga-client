from meniga_client import Meniga, meniga_datetime
import json

m = Meniga('your username', 'your password')
params = {
    'PeriodFrom': meniga_datetime(2016, 1, 1),
    'PeriodTo': meniga_datetime(2016, 1, 2)
}
res = m.get_transactions_page(params)

print(json.dumps(res, sort_keys=True, indent=4))
