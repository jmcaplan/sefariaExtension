import json
from botocore.vendored import requests


def is_jastrow_jackpot(obj, source):
    source_tokens = source.split(".")
    if len(source_tokens) > 2:
        source = source_tokens[0] + ' ' + source_tokens[1]
    else:
        source = source.replace('.', ' ')
    source = source.replace('_',' ')
    ref_list = obj["refs"]
    for ref in ref_list:
        if ':' in ref:
            ref = ref[:ref.find(':')]
        if ref == source:
            return True
    return False

def lambda_handler(event, context):
    result = ''
    headword = ''
    word = event["queryStringParameters"]["word"]
    source = event["queryStringParameters"]["source"]
    lexiconResponses = requests.get("https://www.sefaria.org/api/words/" + word).json()
    nothing_found = True
    for obj in lexiconResponses:
        if obj["parent_lexicon"] == "Jastrow Dictionary":
            if nothing_found:
                headword = obj["headword"]
            if is_jastrow_jackpot(obj=obj, source=source):
                result = result + "<div> <h1> <mark> " + obj["headword"] + " WAS A JASTROW JACKPOT!!! </mark> <image src=\"https://www.smileysapp.com/gif-emoji/clapping.gif\" alt=\"clapping emoji\" width=\"50\" height=\"50\"></image> </h1> </div>"
            nothing_found = False
    if nothing_found:
        result = '<h1> Nothing Found for ' + word + '</h1>'
    result = result.replace("href=\"", "href=\"https://www.sefaria.org")
    result = headword + '###' + result
    return {
        'statusCode': 200,
        'body': json.dumps(result),
           
    }
