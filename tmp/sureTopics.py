import re
import argparse
from collections import defaultdict

def normalize_sources(sources_str):
    sources_str = re.sub(r'\[[^\]]*\]\([^\)]*\)', '', sources_str)
    sources = [s.strip() for s in sources_str.split(',') if s.strip()]
    return sources

def read_topics_file(topics_file):
    with open(topics_file, 'r', encoding='utf-8') as f:
        topics = [line.strip() for line in f if line.strip()]
    return topics

def check_topics_in_file(content_file, topics_file):
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()

    topics = read_topics_file(topics_file)

    sources_map = defaultdict(list)
    not_found = []

    for topic in topics:
        if topic.lower() in content.lower():
            pattern = re.compile(rf"{re.escape(topic)}\s*\|\s*(.*)\|", re.IGNORECASE)
            match = pattern.search(content)
            if match:
                sources = normalize_sources(match.group(1))
            else:
                sources = []
            if sources:
                for src in sources:
                    sources_map[src].append(topic)
        else:
            not_found.append(topic)

    print("\nNot found topics:")
    print("="*50)
    for topic in not_found:
        print(topic)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify solid using topics")
    parser.add_argument("content_file", help="File for verify")
    parser.add_argument("topics_file", help="File with table of topics (one in each string)")
    args = parser.parse_args()

    check_topics_in_file(args.content_file, args.topics_file)
