import threaded_crawler
import sys, getopt
import argparse

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True)
    parser.add_argument('--start', '-a', type=int, required=True)
    parser.add_argument('--stop', '-z', type=int, required=True)
    parser.add_argument('--number', '-n', type=int, required=True)
    args = parser.parse_args()

    print('Start:', args.start)
    print('Stop:', args.stop)
    print('Number of workers:', args.number)
    print('Match output filename:', args.file)

    threaded_crawler.threaded_crawler(args.start, args.stop, args.number,\
                                        silent=False, use_selenium=True,\
                                        match_output_filename=args.file)
