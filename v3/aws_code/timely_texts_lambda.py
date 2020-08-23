import json
from botocore.vendored import requests

def is_in_tanakh_section(ref, section_url):
     # section_ref will be in the form of 'Deuteronomy.16.18-21.9'
    section_tokens = section_url.replace('-','.').split('.')
    section_book = section_tokens[0]
    section_start_chapter = int(section_tokens[1])
    section_start_verse = int(section_tokens[2])
    section_end_chapter = int(section_tokens[3])
    section_end_verse = ''
    try:       
        section_end_verse = int(section_tokens[4])
    except IndexError:
        section_end_verse = int(section_tokens[3])
        section_end_chapter = section_start_chapter
         
    # ref will be in the form of 'Deuteronomy 24:1'
    ref_book = ''
    ref_tokens = ''
    ref_chapter = ''
    ref_verse = ''
    try:
        ref_split_index = ref.index(':') - 2
        ref_book = ref[:ref_split_index].rstrip()
        ref_tokens = ref[ref_split_index:].lstrip().split(':')
        ref_chapter = int(ref_tokens[0])
        ref_verse = int(ref_tokens[1])
    except ValueError:
        ref_split_index = len(ref) - 2
        ref_book = ref[:ref_split_index].rstrip()
        ref_chapter = ref[ref_split_index:].lstrip()
        if ref_book == section_book and (ref_chapter == section_start_chapter or ref_chapter == section_end_chapter):
            return True
        else:
            return False 

    if ref_book == section_book:
        if section_start_chapter < ref_chapter < section_end_chapter:
            return True
        elif section_start_chapter == ref_chapter:
            if section_start_verse <= ref_verse:
                return True
        elif section_end_chapter == ref_chapter:
            if section_end_verse >= ref_verse:
                return True   
    return False

def is_in_mishna_yomi(ref, mishna_yomi):
    #
    return False

    
def lambda_handler(event, context):
    result = ''
    
    # Getting all the calendar info for today
    calResponse = requests.get("https://www.sefaria.org/api/calendars")
    calResponses = calResponse.json()
    parashat_hashavua = calResponses['calendar_items'][0]['displayValue']['en']
    parashat_hashavua_url = calResponses['calendar_items'][0]['url']
    haftara = calResponses['calendar_items'][1]['displayValue']['en']
    haftara_url = calResponses['calendar_items'][1]['url']
    daf_yomi = calResponses['calendar_items'][2]['displayValue']['en']
    perek_tanach = calResponses['calendar_items'][3]['ref']
    mishna = calResponses['calendar_items'][4]['displayValue']['en']
    rambam_1 = calResponses['calendar_items'][5]['displayValue']['en']
    rambam_3 = calResponses['calendar_items'][6]['displayValue']['en']
    daf_hashavua = calResponses['calendar_items'][7]['displayValue']['en']
    halakha = calResponses['calendar_items'][8]['displayValue']['en']

    source = event["queryStringParameters"]["source"]
    sourceResponses = requests.get("https://www.sefaria.org/api/texts/" + source + "?commentary=1").json()  
    commentaryArray = sourceResponses['commentary']
    tanakh_connections = set()
    talmud_connections = set()
    mishna_connections = set()
    for obj in commentaryArray:
        if obj['category'] == 'Tanakh' and obj['type'] == "":
            tanakh_connections.add(obj['ref'])
        elif obj['category'] == 'Talmud':
            talmud_connections.add(obj['ref'])
        elif obj['category'] == 'Mishnah':
            mishna_connections.add(obj['ref'])
    no_matches_found = True
    for ref in tanakh_connections:
        if is_in_tanakh_section(ref, parashat_hashavua_url):
            result = result + "<div>" + 'Congratulations, your source quotes the verse (' + ref + ') which is in this week\'s Parasha, ' + parashat_hashavua + '!!!' + "</div>"  
            no_matches_found = False
        elif is_in_tanakh_section(ref, haftara_url):
            result = result + "<div>" + 'Congratulations, your source quotes the verse (' + ref + ') which is in this week\'s Haftara!!!' + "</div>"  
            no_matches_found = False
        if ref.split(':')[0] == perek_tanach:
            result = result + "<div>" + 'Congratulations, your source quotes the verse (' + ref + ') which is in today\'s Chapter in 929!!!' + "</div>"  
            no_matches_found = False
    for ref in talmud_connections:
        # the ref will be in the form of Eruvin 9b:12
        ref_daf = ref.split(':')[0][:-1]
        if ref_daf == daf_yomi:
            result = result + "<div>" + 'Congratulations, your source quotes the Talmudic passage (' + ref + ') which is in today\'s page in Daf Yomi!!!' + "</div>"  
            no_matches_found = False
        if ref_daf == daf_hashavua:
            result = result + "<div>" + 'Congratulations, your source quotes the Talmudic passage (' + ref + ') which is in this week\'s Daf Hashavua!!!' + "</div>"  
            print('*** Congratulations, your source quotes the Talmudic passage (' + ref + ') which is in this week\'s Daf Hashavua!!!')  
            no_matches_found = False

    if no_matches_found:
        result = "<div> Sorry, your source is not connected to any timely texts! </div>"
   

    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
