import sys
import argparse

from . import ugsearch
from . import ugopen
from . import config

def configure_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    subparsers = root.add_subparsers(dest='subcommand')

    root.add_argument('--no-bold', action='store_true',
        help='Force chord names to not be bolded')

    searchap: argparse.ArgumentParser = subparsers.add_parser('search')
    searchap.add_argument('keyword')
    searchap.add_argument('--limit', nargs='?', type=int, 
        help='Limit the number of results')

    openap: argparse.ArgumentParser = subparsers.add_parser('open')
    openap.add_argument('url')

    luckyap: argparse.ArgumentParser = subparsers.add_parser('lucky')
    luckyap.add_argument('keyword')

    return root


def get_search_results(keyword: str, flags):
    results = ugsearch.search(keyword)

    if results is None:
        return None

    results = list(filter(
        lambda r: r.type is not None and r.type not in config.EXCLUDE_TYPES,
        results))
    
    return results

def do_seach(flags):
    results = get_search_results(flags.keyword, flags)

    if results is None:
        print('Error performing search.')
        return 1
    
    if len(results) == 0:
        print('No results found.')
        return 1
    
    if flags.limit is not None:
        if len(results) > flags.limit:
            results = results[0:flags.limit]
    
    for r in results:
        r.print()
    
    return 0

def use_bold(flags):
    return sys.stdout.isatty() and not flags.no_bold

def do_open(flags):
    result = ugopen.open(flags.url)

    if result is None:
        print('Could not open url.')
        return 1

    result.print(use_bold(flags))
    return 0

def do_lucky(flags):
    results = get_search_results(flags.keyword, flags)
    if results is None:
        print('Error performing search.')
        return 1
    
    if len(results) == 0:
        print('No results found.')
        return 1

    top_result = results[0]
    print('------------')
    top_result.print()
    print('\n------------\n')

    open_result = ugopen.open(top_result.url)

    if open_result is None:
        print('Could not open url.')
        return 1

    open_result.print(use_bold(flags))

    return 0

def main():
    ap = configure_parser()
    flags = ap.parse_args()

    if flags.subcommand == 'search':
        return do_seach(flags)

    if flags.subcommand == 'open':
        return do_open(flags)

    if flags.subcommand == 'lucky':
        return do_lucky(flags)

    ap.print_usage()
    return 1


if __name__ == '__main__':
    sys.exit(main())
