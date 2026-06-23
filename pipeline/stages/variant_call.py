import subprocess
from pipeline.utils.logger import setup_logger

logger = setup_logger(__name__)

def call_variants(bam_file, reference_fasta, output_vcf, min_depth=10):
    """Call variants using samtools/bcftools"""
    logger.info(f"Calling variants from {bam_file}...")
    
    try:
        pileup_cmd = [
            'samtools', 'mpileup',
            '-f', reference_fasta,
            '-q', '20',
            bam_file
        ]
        
        call_cmd = [
            'bcftools', 'call',
            '-m', '-v',
            '-O', 'z',
            '-o', output_vcf
        ]
        
        pileup_proc = subprocess.Popen(pileup_cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
        call_proc = subprocess.Popen(call_cmd, stdin=pileup_proc.stdout, 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pileup_proc.stdout.close()
        
        stdout, stderr = call_proc.communicate()
        
        if call_proc.returncode != 0:
            logger.error(f"Variant calling failed: {stderr.decode()}")
            raise RuntimeError(f"Variant calling error: {stderr.decode()}")
        
        logger.info(f"? Variants called: {output_vcf}")
        
    except Exception as e:
        logger.error(f"Variant calling failed: {str(e)}")
        raise
