import threaded_hakem_crawler
import sys, getopt
import argparse

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True)
    parser.add_argument('--number', '-n', type=int, required=True)
    args = parser.parse_args()

    print('Match archive filename:', args.file)
    print('Number of workers:', args.number)

    threaded_hakem_crawler.threaded_crawler(args.number, silent=False, \
                                        use_selenium=True, \
                                        match_input_filename=args.file)
