import requests, json, time

class VendorData(object):

    def __init__(self, vendor, skip, limit):
        self.baseUrl = "https://api.recruiting.app.silk.security/api"
        self.vendor = vendor
        self.skip = skip
        self.limit = limit

    def _retry_with_timeout(exception_raised, tries):
        def inner(func):
            def wrapper(*args, **kwargs):
                mtries, timeout = tries, 0
                while mtries > 0:
                    try:
                        time.sleep(timeout)
                        return func(*args, **kwargs)
                    except exception_raised as e:
                        print("Retrying {}.. {}".format(func.__name__, e))
                        mtries -= 1
                        timeout += 5
                        print("Waiting for {} seconds.".format(timeout))
                return func(*args, **kwargs)
            return wrapper
        return inner

    def __constructUrl(self):
        return f"{self.baseUrl}/{self.vendor}/hosts/get"

    def __constructHeader(self):
         # you should ALWAYS fetch tokens from vault
        token = "arvindd25@gmail.com_e10c07a0-dc9f-49c7-93e4-3134f34eb545"
        header = {
            'accept': 'application/json',
            'token': f'{token}'
            }
        return header

    @_retry_with_timeout(Exception, 5)
    def fireRequest(self):
        url = self.__constructUrl()
        header = self.__constructHeader()
        skip, limit = self.skip, self.limit
        response = {}
        try:
            paramUrl = f'{url}?skip={skip}&limit={limit}'
            # you should ALWAYS fetch ssl certs from vault
            response = requests.post(
            	           paramUrl, 
                           headers=header,
                           # data=data,
                           verify=False)
            response = response.content
        except ConnectionError as exc:
            print(f"Unable to obtain data from {self.vendor}")
            print(exc)
            response = response
        return response


if __name__ == "__main__":
    crwd = VendorData('crowdstrike', 0, 2)
    qsys = VendorData('qualys', 0, 2)
    crwdDetails = crwd.fireRequest()
    qlysDetails = qsys.fireRequest()
    crwdDetails = json.loads(crwdDetails)
    qlysDetails = json.loads(qlysDetails)
    print(len(crwdDetails))
    print(len(qlysDetails))
