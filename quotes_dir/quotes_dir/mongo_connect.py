import mongoengine

def connect_to_mongo():
    mongoengine.connect(db='test',
                        host='mongodb+srv://bartszczepan04:A501796b@firstcluster.dvmoxij.mongodb.net/test')