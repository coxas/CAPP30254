# Alyssa Cox
# Machine Learning
# Homework 1, part 2


from urllib2 import Request, urlopen, URLError

def get_request(url):
    '''
     Sends a request to the API url.

     Inputs: url, as a string.

     Outputs: request object if successful or error if cannot read request.
    '''
    request = Request(url)

    census_data = None
    error = None
    try:
        response = urlopen(request)
        census_data = response.read()
    except URLError:
        error = "Error with URL"
    if census_data != None:
        return census_data
    else:
        return error