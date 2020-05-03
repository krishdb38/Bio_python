def fasta_description(fasta_file):
    from Bio import SeqIO
    print("\t\t\t\t\t",fasta_file[6:-3])
    record = SeqIO.read(fasta_file,"fasta")
    print("\t\t",record.id)
    print("Length of Sequence is --> ",len(record.seq),"\nSequence in %s Position is -->"%fasta_file[6:-3], record.seq[201])
    print("\n"+"*"*20+"All Sequence is"+"*"*20)
    print(record.seq[:201]+"\n-->"+record.seq[201]+"<--\n"+record.seq[202:])

#def fasta_description(fasta_file):
#    print("\t\t\t\t\t",fasta_file[6:-3])
#    record = SeqIO.read(fasta_file,"fasta")
#    print("\t\t\t",record.id)
#    print("Total length of Our Sequence is --> ",len(record.seq),"\t&\t Sequence in %s Position is -->"%fasta_file[6:-3], record.seq[201])
#    print("\n"+"*"*50+"All Sequence is"+"*"*60)
#    print(record.seq[:201]+"\n-->"+record.seq[201]+"<--\n"+record.seq[202:])

if __name__ == "__main__":
    pass
    
