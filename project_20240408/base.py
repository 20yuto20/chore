from collections import Counter

with open('/Users/yutokohata/Desktop/chores/project_20240408/sequence.fa', 'r') as f:
    sequences = f.read().strip().split('>')

for sequence in sequences:
    if sequence:
        header, seq = sequence.split('\n', 1)
        seq = seq.replace('\n', '')
        base_counts = dict(Counter(seq))
        print(f'[{header}] A: {base_counts.get("A", 0)}, T: {base_counts.get("T", 0)}, C: {base_counts.get("C", 0)}, G: {base_counts.get("G", 0)}')