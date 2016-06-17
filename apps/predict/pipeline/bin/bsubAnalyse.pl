use warnings;
use strict;

my $file=shift @ARGV;
my $refFile=shift @ARGV; #has a fasta extension
my $pairend=shift @ARGV; #1 paired end, 0 single end
my $pex=shift @ARGV; #0 single end, _R|.
my $path=shift @ARGV;

use FindBin qw($Bin);
chdir($Bin);

my @name=split('\.',$file);
my $dataFile=$name[0];

# Remove fasta extension from call
$refFile =~ s/\.fasta$//;

if ($pairend>0) {
	system("stampy.py -g $refFile -h $refFile -o ${path}/$dataFile.sam -f sam -M ${path}/${dataFile}${pex}1.fastq ${path}/${dataFile}${pex}2.fastq;");
	#print STDERR "stampy.py -g $refFile -h $refFile -M ${path}/${dataFile}${pex}1.fastq ${path}/${dataFile}${pex}2.fastq -o ${path}/$dataFile.sam -f sam";
} else {
	system("stampy.py -g $refFile -h $refFile -o ${path}/$dataFile.sam -f sam -M ${path}/${dataFile}.fastq;");
	#print STDERR "stampy.py -g $refFile -h $refFile -M ${path}/${dataFile}.fastq -o ${path}/$dataFile.sam -f sam";
}
system("samtools view -bS ${path}/$dataFile.sam > ${path}/$dataFile.bam");
system("samtools sort ${path}/$dataFile.bam ${path}/$dataFile.sorted");
system("samtools index ${path}/$dataFile.sorted.bam");
system("Platypus.py callVariants --bamFiles=${path}/$dataFile.sorted.bam --refFile=$refFile.fasta --output=${path}/$dataFile.h37rv.vcf");
system("perl $Bin/flatAnnotatorVAR.pl ${path}/$dataFile.h37rv.vcf 15 0.1 PASS");
system("mv ${path}/$dataFile.h37rv.var ${path}/output");
system("mv ${path}/$dataFile.h37rv.vcf ${path}/output");
system("python $Bin/generate_matrix.py ${path}/output");

system("Rscript $Bin/TBpredict.R ".'"'."${path}/output/matrix.csv".'"'." >${path}/output/result.json");

my $size= -s "${path}/output/result.json";
#print STDERR "$size\n";
if ($size > 0 ) {
        system("python $Bin/../run_feedback.py ${path}");
}
system("rm ${path}/$dataFile.sam");
system("rm ${path}/$dataFile.sorted.bam");
system("rm ${path}/$dataFile.sorted.bam.bai");
system("rm ${path}/$dataFile.bam");
