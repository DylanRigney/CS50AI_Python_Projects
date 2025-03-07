import requests
from bs4 import BeautifulSoup


def decode(url):
    # fetch the document
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text

    # parse the document
    soup = BeautifulSoup(html_content, "html.parser")

    # find the table
    table = soup.find("table")
    if not table:
        raise ValueError("Table not found")

    # extract the text from the table
    data = []
    for row in table.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) < 3:
            continue # the rows should have 3 columns
        try:
            x = int(cells[0].get_text(strip=True))
            unicode = cells[1].get_text(strip=True)
            y = int(cells[2].get_text(strip=True))
            data.append((x, unicode, y))
        except ValueError:
            # Skip rows if they don't contain integers
            continue

    if not data:
        raise ValueError("No data found in the table")

    # get grid dimensions
    max_x = max(x for x, _, _ in data) + 1
    max_y = max(y for _, _, y in data) + 1

    # create the grid
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]

    # Place the characters in the grid
    for x, unicode, y in data:
        grid[y][x] = unicode

    # print the grid
    for row in grid:
        print(''.join(row))

decode("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")
    

        


