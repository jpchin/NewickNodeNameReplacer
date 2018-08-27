# NewickNodeNameReplacer
Replaces the name of nodes in Newick trees with the header of a corresponding FASTA sequence

Written because some tools cut the FASTA headers to just the accession, which can make it hard to quickly interpret the resulting data.  May be superfluous, removing spaces and square brackets from the input sequences may resolve this (see FASTAHeaderCleaner).
