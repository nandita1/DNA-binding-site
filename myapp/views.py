from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import re
from dna_features_viewer import GraphicFeature, GraphicRecord
# Create your views here.
def upload(request):
    posted = False
    sequences = []
    ids = []
    organisms = []
    gene_sequence = ''
    locations=[]
    all_locations=[]
    matched_sequences=[]
    matched_organisms=[]
    database=[]
    matched_database=[]
    matched_ids = []
    features=[]
    zipped={}
    figure_name=''
    sequence_nos=[]
    i=0
    if request.method == 'POST':
        posted = True
        uploaded_file = request.FILES['document']
        position = int(request.POST.get('position'))
        #position = int(position)*3
        with open('myapp/Jaspar.txt',"r") as file:
            for line in file:
                line = line.split(';')
                ids.append(line[0])
                sequences.append(line[1])
                organisms.append(line[2])
                database.append(line[3].rstrip('\n'))
        for line in uploaded_file:
            line = line.decode('utf-8')
            gene_sequence+=line
        gene_sequence=gene_sequence[0:position]
        for sequence in sequences:
            locations=[m.start() for m in re.finditer(sequence, gene_sequence)]
            if locations!=[]:
                matched_sequences.append(sequence)
                all_locations.append(locations)
                matched_organisms.append(organisms[i])
                matched_database.append(database[i])
                matched_ids.append(ids[i])
                for location in locations:
                    features.append(GraphicFeature(start=location, end=location+len(sequence), strand=+1, color="#ffd700",label=sequence))
            i+=1
        record = GraphicRecord(sequence_length=len(gene_sequence), features=features)
        ax, _ = record.plot(figure_width=30)
        figure_name=uploaded_file.name+str(position)+'.png'
        ax.figure.savefig('myapp/static/'+uploaded_file.name+str(position)+'.png', bbox_inches='tight')
        print(matched_sequences)
        print(matched_organisms)
        print(all_locations)
        print(matched_database)
        sequence_nos=list(range(len(matched_sequences)))
        zipped = tuple(zip(matched_ids,matched_sequences,matched_organisms,matched_database,all_locations,sequence_nos))
    return render(request,'upload.html',{'posted':posted,'zipped':zipped,'figure_name':figure_name, 'gene_sequence':gene_sequence})
