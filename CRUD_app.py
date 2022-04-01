from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine

# Initailizing Objects Which Requried to Make App Run
mongo_atlas_connection_string = "mongodb+srv://public_user:ExBRARE7qbnPSZNu@copywordbase.pya1y.mongodb.net/Test?retryWrites=true&w=majority"

my_app = Flask(__name__)
my_app.config['MONGODB_HOST'] = mongo_atlas_connection_string
database = MongoEngine()
database.init_app(my_app)


@my_app.route('/', methods=['GET'])
def home():
    return '''Add Mobile - /Mobile/addMobile
            Read book - /Mobile
            Update book - /Mobile/<Modelnumber>
            Delete - /Mobile/<ModelNumber>'''

class Mobile(database.Document):
    # Deinfing Which Type of Data will be stored
    mobile_brand = database.StringField()
    mobile_model = database.StringField()
    mobile_price = database.IntField()

    # Deinfing Schema of API Objects
    def convert_to_josn(self):

        return {
            "Brand" : self.mobile_brand,
            "Model" : self.mobile_model,
            "Price" : self.mobile_price
        }

# Deinfing AlL API endpoints here

@my_app.route('/Mobile/', methods=['GET'])
def see_all_mobiles_listed():
    all_items = []
    for each in Mobile.objects:
        all_items.append(each)

    return make_response(jsonify(all_items),200)

@my_app.route('/Mobile/<modelName>', methods=['GET'])

def see_a_specific_mobile(modelName):
    mobile = Mobile.objects(mobile_model=modelName).first()
    return make_response(jsonify(mobile),200)

@my_app.route('/Mobile/addMobile', methods=['POST'])

def add_new_mobile():

    new_mobile = Mobile(mobile_brand="Apple",
                            mobile_model="iphone 12",
                            mobile_price=120000)

    new_mobile.save()

    return make_response('Object added to server',200)

@my_app.route('/Mobile/updateMobile/<modelName>', methods=['PUT'])

def update_an_existing_mobile(modelName):
    classMobile = Mobile()
    contenttype = request.json
    mobile = classMobile.objects(mobile_model=modelName).first()
    # mobile = classMobile.update(mobile_price=contenttype['mobile_price'])

    return make_response("Update Success", 204)

@my_app.route('/Mobile/deleteMobile/<modelName>', methods=['DELETE'])

def delete_mobile(modelName):
    mobile = Mobile.objects(mobile_model=modelName).first()
    if mobile :
        mobile.delete()
        return make_response('Delete Success', 200)
    else:
        return make_response('Delete Failed', 404)




if __name__ == "__main__" :
    my_app.run(debug=True)
    