import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # get links for page
    links = corpus.get(page)

    num_links = len(links)
    num_pages = len(corpus)

    # if the page has no links then all pages are equally likely
    if num_links == 0:
        distribution = {pg: 1 / len(corpus.keys()) for pg in corpus}
        return distribution

    # find the probability that a random page is selected 1 - d / N
    p_rand_page = (1 - damping_factor) / num_pages

    # find the probability that a random link is selected d / NumLinks(i)
    p_rand_link = damping_factor / num_links

    return {pg: p_rand_page + p_rand_link if pg in links else p_rand_page for pg in corpus}


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # First sample should start from random page
    current_page = random.choice(list(corpus.keys()))
    page_rank = {current_page: 1}
    count = n

    while count > 0:
        count -= 1
        # get the transition model for the current page
        tr_model = transition_model(corpus, current_page, damping_factor)

        # randomly chooses next page based on the transition model and assigns that value to current_page
        pages = list(tr_model.keys())
        probabilities = list(tr_model.values())
        current_page = random.choices(pages, weights=probabilities)[0]

        # increment current page with an additional visit
        page_rank[current_page] = page_rank.get(current_page, 0) + 1

    # find the probability of selecting each page based on the proportion of that page to the total number of samples
    return {page: value / n for page, value in page_rank.items()}

    # # Generate sample
    # # While still more pages to sample
    # while n > 0:
    #     # choose at random from the links
    #     if random.uniform(0, 1) < .85:
    #         # get the links for the current page
    #         links = corpus.get(currentpage)
    #         # choose at random from the links
    #         current_page = random.choice(links)
    #         # add the current page to the sample
    #         page_rank[current_page] = page_rank.get(current_page, 0) + 1

    #     # Choose at random from pages
    #     else:
    #         current_page = random.choice(list(corpus.keys()))
    #         page_rank[current_page] = page_rank.get(current_page, 0) + 1


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    reverse_corpus = {page: [] for page in corpus}
    link_count = {}

    # create dictionary with each key being a page and each value being a list of pages that link to that page
    for linking_page in corpus:

        links = corpus.get(linking_page)

        # create a dictionary with key being a page and value being the number of links it has
        if links:
            link_count[linking_page] = len(links)

            for linked_page in links:
                reverse_corpus[linked_page].append(linking_page)
        else:
            link_count[linking_page] = 0

    # begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    page_ranks = {page: 1 / N for page in corpus}

    # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself)
    # for linking_page in link_count:
    #     if link_count[linking_page] == 0: # page has no links
    #         link_count[linking_page] = N
    #         for page in corpus:  # include pages with no linking pages
    #             if page not in reverse_corpus:
    #                 reverse_corpus[page] = []  # make sure that page is in reverse_corpus
    #             # for every page add this page to list of linking pages
    #             reverse_corpus[page].append(linking_page)

    # repeatedly calculate new rank values based on all of the current rank values, according to the
    # PageRank formula in the “Background” section.

    threshold = .001
    while True:
        new_ranks = {}
        converged = True

        # calculate page rank algorithm
        for p in page_ranks:
            pr = (1 - damping_factor) / N

            for linking_page in reverse_corpus[p]:
                pr += damping_factor * (page_ranks[linking_page]) / link_count[linking_page]

            # some pages have no links so you have to distribute their pageranks across all pages
            no_link = 0

            for page in corpus:
                if link_count[page] == 0:
                    no_link += page_ranks[page]

            no_link = no_link / N
            pr += damping_factor * no_link

            new_ranks[p] = pr

            if abs(new_ranks[p] - page_ranks[p]) > threshold:
                converged = False

        page_ranks = new_ranks

        if converged:
            break

    return page_ranks

if __name__ == "__main__":
    main()
