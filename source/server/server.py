from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from rich import print as rprint
from rich import inspect


client = RemoteAPIClient()

if __name__=='__main__':
    
    sim = client.require('sim')