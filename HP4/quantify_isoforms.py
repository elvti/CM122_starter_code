import argparse
import zipfile
import numpy as np


def parse_annotation_file(annotation_fn):
    """
    :param annotation_fn: the gene annotations file
    :return: outputs a list of tuples, "genes". Every tuple represents one gene, the first element of the tuple is the
            list of exon index ranges for that gene, the second element of the tuple is the list of isoforms that exist
            for that gene. For example, genes[0][0][0] references the first exon range of the first gene (in a tuple),
            genes[2][1][3] references the fourth isoform of the third gene.
    """

    with open(annotation_fn, 'r') as aFile:
        N = int(aFile.readline().strip())
        genes = [None]*N
        for i in range(N):
            numExons = int(aFile.readline().strip())
            exons = [None]*numExons
            starts = [int(x) for x in aFile.readline().strip().split(' ')]
            ends = [int(x) for x in aFile.readline().strip().split(' ')]
            for j in range(numExons):
                exons[j] = (starts[j], ends[j])
            numIsoforms = int(aFile.readline().strip())
            isoforms = [None]*numIsoforms
            for j in range(numIsoforms):
                isoforms[j] = [int(x) for x in aFile.readline().strip().split(' ')]
            genes[i] = (exons, isoforms)
    return genes


def parse_genome_file(genome_fn):
    """
    :param genome_fn: the full genome file
    :return: the string containing the genome
    """

    with open(genome_fn, 'r') as gFile:
        return gFile.readline().strip()


def parse_reads_file(reads_fn):
    """
    :param reads_fn: the file of shuffled reads
    :return: a list containing all of the shuffled reads
    """

    with open(reads_fn, 'r') as rFile:
        return rFile.readlines()


def quantify_isoforms(genes, genome, reads):
    """
    :param genes: the list of gene tuples generated by the parser
    :param genome_fn: the full genome file
    :param reads_fn: the file of shuffled reads
    :return: a list of tuples, where the first element of the tuple is the transcript sequence (the isoform in terms of
            the exon sequences that form it in the genome), and the second element of the tuple is the abundance of that
            specific isoform

            NOTE: this skeleton is built assuming the return value exists like this, but as long as you change the way
            the output file is generated, this can be in whatever form you like.
    """

    """
        Within this function, you should go through most of the process of quantifying isoforms given the data.
        This can be broken down into the following few steps:
        
            1. Align reads to the genome, exome, or isoforms
                    your choice of method, but note the length of the genome
            
            2. Use the generated alignment to get exon counts
            
            3. Formulate your RNA seq problem using the isoforms and exon counts (linear algebra)
            
            4. Compute the isoform abundances based on your above formulation
    """



    return [('accccaggtata', .7), ('acccctatatctt', .3)]


if __name__ == "__main__":
    """
    For an example of how you might call this script to run on the data provided:
    
    Usage: python proj4.py -g full_genome.txt -r shuffled_reads.txt -a DATA_PA_1100_0 -o test.out -t hw4_r_4_chr_1
    """
    parser = argparse.ArgumentParser(description='For now this starter code helps parse the files given, but leaves\n'
                                                 'the actual function that must be implemented empty')
    parser.add_argument('-g', '--genome', required=True, dest='genome_file', help='File containing the full genome')
    parser.add_argument('-r', '--reads', required=True, dest='read_file', help='File containing the shuffled reads')
    parser.add_argument('-a', '--annotation', required=True, dest='annotation_file', help='File containing gene '
                                                                                          'annotations')
    parser.add_argument('-o', '--outputFile', required=True, dest='output_file', help='Output file name')
    parser.add_argument('-t', '--outputHeader', required=True, dest='output_header',
                        help='String that needs to be output on the first line of the output file so that the online\n'
                             'submission system recognizes which leaderboard this file should be submitted to. For\n'
                             'hw4, this will be hw4_r_4_chr_1')

    args = parser.parse_args()
    genome_fn = args.genome_file
    reads_fn = args.read_file
    annotation_fn = args.annotation_file
    output_fn = args.output_file

    genes = parse_annotation_file(annotation_fn)
    genome = parse_genome_file(genome_fn)
    reads = parse_reads_file(reads_fn)
    print(len(reads))
    output = quantify_isoforms(genes, genome, reads)
    with open(output_fn, 'w') as oFile:
        oFile.write('>' + args.output_header + '\n')
        oFile.write('>RNA\n')
        for isoform in output:
            out_str = '{} {}\n'.format(isoform[0], isoform[1])
            oFile.write(out_str)

    zip_fn = output_fn + '.zip'
    with zipfile.ZipFile(zip_fn, 'w') as zFile:
        zFile.write(output_fn)
