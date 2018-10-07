from slackclient import SlackClient
import json
import os
import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter


# setup slack client
slack_token = os.environ['SLACK_API_TOKEN']
sc = SlackClient(slack_token)

# setup Avro schema
schemaText = """{
 "namespace": "slack_fun",
 "type": "record",
 "name": "message",
 "fields": [
     {"name": "channel", "type": "string"},
 	 {"name": "ts", "type": "string"},
     {"name": "type", "type": "string"},
     {"name": "text",  "type": "string"},
     {"name": "author", "type": "string"},
     {"name": "reactions", "type": {
     	"type": "array",
 		"items": {
 			"type": "record",
 			"name" : "reaction",
 			"namespace": "slack_fun",
 			"fields": [
                    {"name": "name", "type": "string"},
                    {"name": "count", "type": "int"},
                    {"name": "users", "type": { 
                    	"type": "array", "items": "string" 
                	} 
                	}
            ]
 		}
 	}
     }
 ]
}"""
schema = avro.schema.parse(schemaText)

writer = DataFileWriter(open("messages.avro", "wb"), DatumWriter(), schema)

# setup users cache
users=sc.api_call("users.list")
usersCache={}
for member in users["members"]:
	usersCache[member["id"]] = member["name"]

# display_name
# name
# id

# delation = C037D8L9J

messages=sc.api_call("channels.history", channel="C037D8L9J")


for message in messages["messages"]:
	reactionsRecord = []
	for reaction in message["reactions"]:
		reactionRecord = { "count": reaction["count"], "name" : reaction["name"], "users": reaction["users"] }
		reactionsRecord.append(reactionsRecord)
	record = {"channel": "delation", "ts": message["ts"], "type": message["type"], "text" : message["text"], "author": message["user"], "reactions": reactionsRecord}
	writer.append(record)

writer.close()




