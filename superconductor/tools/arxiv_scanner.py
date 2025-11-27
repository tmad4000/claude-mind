#!/usr/bin/env python3
"""
arXiv Scanner for Superconductor Research

Fetches recent papers from arXiv related to superconductivity
and outputs them in a format ready for categorization.

Usage:
    python arxiv_scanner.py [--days 7] [--output results.json]

This script:
1. Queries arXiv API for recent cond-mat.supr-con papers
2. Extracts title, abstract, authors, date
3. Outputs in format ready for further processing
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import argparse
from datetime import datetime, timedelta
import re

ARXIV_API = "http://export.arxiv.org/api/query"

# Keywords that suggest relevance to room-temp superconductivity
HIGH_PRIORITY_KEYWORDS = [
    'room temperature', 'room-temperature', 'high temperature', 'high-temperature',
    'hydride', 'LaH', 'YH', 'H3S', 'superhydride',
    'nickelate', 'infinite-layer', 'La3Ni2O7',
    'cuprate', 'YBCO', 'BSCCO',
    'ambient pressure', 'low pressure',
    'electron-phonon', 'superexchange',
    'Tc prediction', 'machine learning superconductor',
    'BCS', 'Cooper pair',
]

MEDIUM_PRIORITY_KEYWORDS = [
    'superconductivity', 'superconducting',
    'transition temperature', 'critical temperature',
    'pairing mechanism', 'pairing symmetry',
    'DFT', 'first-principles',
    'phonon', 'electron correlation',
]


def search_arxiv(query, max_results=100, start=0):
    """Search arXiv API and return parsed results."""
    params = {
        'search_query': query,
        'start': start,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return parse_arxiv_response(data)
    except Exception as e:
        print(f"Error fetching from arXiv: {e}")
        return []


def parse_arxiv_response(xml_data):
    """Parse arXiv API XML response into list of papers."""
    root = ET.fromstring(xml_data)

    # Define namespace
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }

    papers = []

    for entry in root.findall('atom:entry', ns):
        paper = {}

        # Extract basic info
        paper['title'] = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        paper['abstract'] = entry.find('atom:summary', ns).text.strip()
        paper['id'] = entry.find('atom:id', ns).text.split('/')[-1]
        paper['link'] = f"https://arxiv.org/abs/{paper['id']}"
        paper['pdf'] = f"https://arxiv.org/pdf/{paper['id']}.pdf"

        # Extract date
        published = entry.find('atom:published', ns).text
        paper['date'] = published[:10]  # YYYY-MM-DD

        # Extract authors
        authors = []
        for author in entry.findall('atom:author', ns):
            name = author.find('atom:name', ns).text
            authors.append(name)
        paper['authors'] = authors

        # Extract categories
        categories = []
        for cat in entry.findall('atom:category', ns):
            categories.append(cat.get('term'))
        paper['categories'] = categories

        papers.append(paper)

    return papers


def score_relevance(paper):
    """Score paper relevance to room-temp superconductivity research."""
    text = (paper['title'] + ' ' + paper['abstract']).lower()

    score = 0
    matches = []

    for kw in HIGH_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            score += 3
            matches.append(kw)

    for kw in MEDIUM_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            score += 1
            matches.append(kw)

    return score, matches


def categorize_paper(paper):
    """Categorize paper by contribution type based on keywords."""
    text = (paper['title'] + ' ' + paper['abstract']).lower()

    categories = []

    if any(kw in text for kw in ['experiment', 'synthesis', 'measurement', 'observed', 'fabricat']):
        categories.append('Experimental')

    if any(kw in text for kw in ['predict', 'calculation', 'dft', 'first-principles', 'computed']):
        categories.append('Computational')

    if any(kw in text for kw in ['theory', 'theoretical', 'model', 'mechanism', 'explain']):
        categories.append('Theoretical')

    if any(kw in text for kw in ['review', 'perspective', 'overview', 'progress']):
        categories.append('Review')

    if any(kw in text for kw in ['machine learning', 'neural network', 'deep learning', 'ml']):
        categories.append('ML')

    if not categories:
        categories.append('Other')

    return categories


def identify_related_problems(paper):
    """Identify which problems from PROBLEM_MAP.md this paper might relate to."""
    text = (paper['title'] + ' ' + paper['abstract']).lower()

    problems = []

    # PROB-001: Mechanism
    if any(kw in text for kw in ['mechanism', 'pairing', 'superexchange', 'spin fluctuation', 'cooper pair']):
        problems.append('PROB-001')

    # PROB-002: Prediction
    if any(kw in text for kw in ['predict', 'tc prediction', 'machine learning', 'screening', 'discovery']):
        problems.append('PROB-002')

    # PROB-003: Pressure
    if any(kw in text for kw in ['pressure', 'ambient', 'strain', 'hydride', 'hydrogen']):
        problems.append('PROB-003')

    # PROB-004: Synthesis
    if any(kw in text for kw in ['synthesis', 'growth', 'fabricat', 'thin film', 'single crystal']):
        problems.append('PROB-004')

    # PROB-006: Search space
    if any(kw in text for kw in ['new material', 'novel', 'candidate', 'family', 'class of']):
        problems.append('PROB-006')

    # PROB-007: Computational
    if any(kw in text for kw in ['dft', 'first-principles', 'electron-phonon', 'calculation']):
        problems.append('PROB-007')

    return problems


def main():
    parser = argparse.ArgumentParser(description='Scan arXiv for superconductor papers')
    parser.add_argument('--days', type=int, default=7, help='Look back this many days')
    parser.add_argument('--max', type=int, default=50, help='Maximum papers to fetch')
    parser.add_argument('--output', type=str, default=None, help='Output JSON file')
    parser.add_argument('--verbose', action='store_true', help='Print detailed output')
    args = parser.parse_args()

    print("Scanning arXiv for superconductor papers...")
    print(f"Looking back {args.days} days, max {args.max} results")
    print()

    # Search for superconductivity papers
    query = 'cat:cond-mat.supr-con'
    papers = search_arxiv(query, max_results=args.max)

    print(f"Found {len(papers)} papers")
    print()

    # Score and categorize
    results = []
    for paper in papers:
        score, matches = score_relevance(paper)
        categories = categorize_paper(paper)
        problems = identify_related_problems(paper)

        result = {
            **paper,
            'relevance_score': score,
            'matched_keywords': matches,
            'contribution_types': categories,
            'related_problems': problems
        }
        results.append(result)

    # Sort by relevance
    results.sort(key=lambda x: x['relevance_score'], reverse=True)

    # Print top results
    print("=" * 60)
    print("TOP RELEVANT PAPERS")
    print("=" * 60)

    for i, paper in enumerate(results[:15]):
        if paper['relevance_score'] > 0:
            print(f"\n[{i+1}] Score: {paper['relevance_score']}")
            print(f"    {paper['title'][:80]}...")
            print(f"    Date: {paper['date']} | Categories: {', '.join(paper['contribution_types'])}")
            print(f"    Related: {', '.join(paper['related_problems']) if paper['related_problems'] else 'General'}")
            print(f"    Keywords: {', '.join(paper['matched_keywords'][:5])}")
            print(f"    Link: {paper['link']}")

    # Output JSON if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved {len(results)} papers to {args.output}")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total papers scanned: {len(results)}")
    high_relevance = [p for p in results if p['relevance_score'] >= 5]
    medium_relevance = [p for p in results if 2 <= p['relevance_score'] < 5]
    print(f"High relevance (score >= 5): {len(high_relevance)}")
    print(f"Medium relevance (2-4): {len(medium_relevance)}")

    # Problem coverage
    problem_counts = {}
    for paper in results:
        for prob in paper['related_problems']:
            problem_counts[prob] = problem_counts.get(prob, 0) + 1

    print("\nPapers by problem area:")
    for prob, count in sorted(problem_counts.items()):
        print(f"  {prob}: {count} papers")

    return results


if __name__ == "__main__":
    main()
