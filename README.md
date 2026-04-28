# bloom-filter-implementation

This project implements a Bloom Filter, a space-efficient probabilistic data structure used for fast membership testing.

The filter supports insertion and lookup in constant time while using significantly less memory than storing all elements explicitly. It guarantees no false negatives and allows a tunable false positive rate.

### Features
- Configurable number of hash functions and target false positive rate
- Efficient bit vector representation
- Real-time estimation of false positive probability
- Empirical validation comparing projected vs observed error rates

### Experiment
- Inserted 100,000 words into the filter
- Verified zero false negatives
- Measured false positive rate on unseen data
- Observed results closely match theoretical expectations

### Use Cases
- Caching systems
- Databases and storage optimization
- Network security (e.g., blacklist filtering)
