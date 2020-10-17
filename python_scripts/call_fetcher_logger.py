import fetcher_logger as fetcher_logger
from tqdm import tqdm

for prior in tqdm(range(131)):
    fetcher_logger.main(days_prior=prior, print_visible=False)
