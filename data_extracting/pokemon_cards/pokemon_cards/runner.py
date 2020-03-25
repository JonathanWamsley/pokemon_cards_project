from scrapy.cmdline import execute
from datetime import date
import sys


def scrape(job_name):
    """
        runs a scrapy job executing a spider to yield the collected data and log data in a json file
        The file name format is the job name then the current date
        The file destination is scraped_data

    :param job_name:
        executes the spider with the job name

    :yields json data
    """

    execute(
        [
            'scrapy',
            'crawl',
            job_name,
            '-o',
            f'scraped_data/{job_name}_{date.today()}.json',
            '--logfile',
            f'scraped_data/{job_name}_log_{date.today()}.text',
        ])


if __name__ == "__main__":
    scrape(sys.argv[1])
