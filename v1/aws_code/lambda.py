import json
from botocore.vendored import requests

'''
def is_jastrow_jackpot(obj, source):
    ref_list = obj["refs"]
    for ref in ref_list:
        if ref == source:
            return True
    return False
'''

def is_jastrow_jackpot(obj, source):
    source_tokens = source.split(".")
    if len(source_tokens) > 2:
        source = source_tokens[0] + ' ' + source_tokens[1]
    else:
        source = source.replace('.', ' ')
    ref_list = obj["refs"]
    for ref in ref_list:
        if ':' in ref:
            ref = ref[:ref.find(':')]
        print("source is " + source)
        print("ref is " + ref)
        if ref == source:
            return True
    return False

def lambda_handler(event, context):
    result = ''
    word = event["queryStringParameters"]["word"]
    source = event["queryStringParameters"]["source"]
    lexiconResponses = requests.get("https://www.sefaria.org/api/words/" + word).json()
    nothing_found = True
    for obj in lexiconResponses:
        if obj["parent_lexicon"] == "Jastrow Dictionary":
            result = result + "<div><h3>" + obj["headword"] + obj["content"]["senses"][0]["definition"] + "</h3></div>"
            if is_jastrow_jackpot(obj=obj, source=source):
                result = result + "<div> <h1> THIS WAS A JASTROW JACKPOT!!! </h1> </div>"
            result = result + "<hr></hr>"
            nothing_found = False
    if nothing_found:
        result = '<h1> Nothing Found for ' + word + '</h1>'
    return {
        'statusCode': 200,
        'body': json.dumps(result),
    }
