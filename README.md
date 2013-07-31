Run instructions
---------------------------------
Here is a typical workflow:

1) Dry run to check on the current status of the jobs you will run. They should all say WILL RUN the first time you run them.
python generate_impute_results.py --runonly= --arrays=<array types> --steps=1 --dry_run 1

2) Remove dry run to schedule the jobs. You will see a lot of qsub outputs. Each Beagle analysis creates 19 qsub jobs.
python generate_impute_results.py --runonly= --arrays=<array types> --steps=1 --dry_run=0

3) Watch job progress with qstat, or by running dry run mode (item 1) again. This time you'll see the jobs as RUNNING

4) To stop all jobs from running for whatever reason.
python generate_impute_results.py --runonly= --arrays=<array types> --steps=1 --dry_run=0 --reset=1 --reset_running=1

5) Or, sometimes, you might want to stop one job and reschedule after modifying some parameters in phase_impute_pipeline.py
python generate_impute_results.py --runonly=
samplesize/test=300/ref=250/step1-ch22-exome 
 --arrays=<array types> --steps=1 --dry_run=0 --reset=1 --reset_running=1

6) To restart failed jobs, run the script with dry_run=0 (item 2). It starts any jobs it thinks it needs to start, picks up where it left off.

Data requirements
---------------------------------
Array markers - all are provided in gzipped format
    * affy6_markers.txt

    * illumina3_markers.txt

    * omni2_5_markers.txt

    * exome_chip/annotatedList.txt

1000 Genomes chromosome 22
    * phase 1 integrated call set can be downloaded from this ftp site:
      ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20110521/

    * Need the following files:

        ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz
        ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.tbi
        ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.vcfidx

Script descriptions
---------------------------------

*generate_vcfs.py

Generates test and reference sets in the format of VCF from the 1000 Genome data. This script
generates sets sample size and population based analysis. This data this script produces is
consumed by generate_impute_results.py.

*phase_impute_pipeline.py

Schedule one phase and impute pipeline. Four pipelines are implemented in this script,
and can be selected by changing the --step parameter. These pipelines are
--step=1 : Beagle
--step=2 : MaCH-Admix
--step=3 : ShapeIt / Impute2
--step=4 : SLRP / Impute2

*generate_impute_results.py

Provides functionalities for job management of phase and impute pipelines.
Jobs can be started, stopped, and inspected by using different parameters.

*lib/analysis.py

This file defines all sets of parameters that are to generate reference and test sets.

*lib/common.py

Common utility methods for our Python scripts. In particular
this provides helper methods for working with qsub.

*lib/make_sample.sh

make .sample file to use as reference panel in shapeit

*lib/run_impute2.py

Helper script used to schedule Impute2 jobs. This script chunks the reference set into multiple
chromosome sections and schedule Impute2 jobs for each chunk in parallel.

*lib/split_vcf_info.py

This file defines logic to deal with chunked VCF files by loading the
metadata file generated by chunking. Designed to work with genotypes
split using splitVcfRef.jar, described here.
http://www.unc.edu/~yunmli/MaCH-Admix/tutorial.php#split

*lib/vcf2impute_gen.pl

This script takes a VCF file and converts it into a .gen file in IMPUTE format.
Written by Bryan Howie.

*lib/vcf2impute_legend_haps.pl

This script takes a VCF file and converts it into a haplotype+legend file
pair in IMPUTE format. Written by Bryan Howie.

Paths to change
---------------------------------
*analysis.py - SAMPLED_DATA_BASE

*phase_impute_pipeline.py - can alter all defaults set

*generate_vcfs.py - can alter all defaults set

    *in gzinput method, alter return path

*generate_impute_results.py - can alter all defaults set