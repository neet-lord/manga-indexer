import datetime, os, sys, logging

from scrapy import cmdline
from scrapy.utils.log import configure_logging

from manga_indexer.settings import (
    DATA_ROOT,
    APPLICATION_ROOT
)

from .__prep_run import prep_filesystem
from .__site_args import sites

def start_indexer(args):
    site = sites[args.site]
    process_log, event_log, output_file, job_dir, scrapy_log = prep_filesystem(args, site)

    output_format = args.format

    start_crawling_job(
        job_dir=job_dir,
        scrapy_log=scrapy_log,
        spider=site['spider_name'],
        sitename=site['sitename'],
        event_log=event_log,
        process_log=process_log,
        output_file=output_file,
        output_format=output_format,
        process_dir=APPLICATION_ROOT
    )

def start_crawling_job(
    job_dir,
    scrapy_log,
    spider,
    sitename,
    event_log,
    process_log,
    output_file,
    output_format,
    process_dir
):
    os.chdir(process_dir)

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=scrapy_log,
        filemode = 'a',
        format='%(levelname)s: %(message)s',
        level=logging.DEBUG
    )

    command_template = (
            'scrapy\tcrawl\t{spider}'
            '\t-s\tJOBDIR={job_dir}' + \
            '\t-a\tsitename={sitename}' + \
            '\t-a\tevent_log={event_log}' + \
            '\t-a\tprocess_log={process_log}' + \
            "\t-o\t{output_file}:{output_format}"
    )

    start_spider_command = command_template.format(
        spider=spider,
        scrapy_log=scrapy_log,
        sitename=sitename,
        event_log=event_log,
        process_log=process_log,
        output_file=output_file,
        job_dir=job_dir,
        output_format=output_format
    )

    cmdline.execute(start_spider_command.split('\t'))
