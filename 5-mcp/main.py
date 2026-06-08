from mcp.server.fastmcp import FastMCP

mcp = FastMCP("the-world-of-llms", json_response=True)

@mcp.tool()
def get_weather(city: str) -> str:
    """
    Takes a city and returns the weather conditions at that city.

    Arguments:
        city (str): The city to get the weather for

    Returns:
        weather (str): The weather at the given city
    """
    return 'Hot with temperatures ranging from 20 to 40 degrees celsius'

if __name__ == '__main__':
    mcp.run(transport='streamable-http')
