# bm

So far I believe I'm building parts of a Boltzmann machine? Not entirely sure, otherwise it's interesting.

### process

When this is completed I should be able to provide the script (or at least this proof of concept) a CSV similar to the [sample](sample.csv) and spit out the _He_, then pluck random records from the dataset and attempt to find records that can improve the He value (increase it).

### todo

- [ ] clarification on whether I should be using freq/2*len or freq^2 for lookup table He calculation, believe it's the former
- [ ] when a record doesn't improve anything, what do I do with it? do I mark it as 'okay' and just not use it again or what?
