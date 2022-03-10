import numpy as np
from flask import Flask, request, make_response
import json
import pickle

app = Flask(__name__)
model = pickle.load(open('gradient_boosting.pkl', 'rb'))

@app.route('/')
def hello():
    return "Hello"
    # age = int(input("Enter age"))
    # gender = -1
    # while(gender == -1):
    #     sex = input("Enter gender").lower()
    #     if(sex == "female"):
    #         gender = 0
    #     elif(sex == "male"):
    #         gender = 1
    #     else:
    #         print("Wrong input. Enter valied one")

    # bmi = float(input("Enter bmi"))
    # is_smoker = -1
    # while(is_smoker == -1):
    #     smoke = input("Are you smoker or not?").lower()
    #     if(smoke == "yes"):
    #         is_smoker = 1
    #     elif(smoke == "no"):
    #         is_smoker = 0
    #     else:
    #         print("Wrong input. Enter valid one")

    # int_features = [age, gender, bmi, is_smoker]

    # final_features = [np.array(int_features)]

    # prediction = model.predict(final_features)

    # print(prediction)





# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r  #Final Response sent to DialogFlow


# This method processes the incoming request  

def processRequest(req):    

    result = req.get("queryResult")
    parameters = result.get("parameters")
    age = parameters.get("ageinput")
    sex = parameters.get("genderinput")
    if(sex == "female"):
    	gender = 0
    else:
    	gender = 1

    bmi = parameters.get("bmiinput")
    smoker = parameters.get("smokeinput")
    if(smoker == "yes"):
    	is_smoker = 1
    else:
    	is_smoker = 0

    try:
    	int_features = [age, gender, bmi, is_smoker]

    	final_features = [np.array(int_features)]
    except ValueError:
    	return {
    		"fulfillmentText": "Incorrect information supplied"
    	}

    
    intent = result.get("intent").get('displayName')
    
    if (intent == 'DataYes'):
        prediction = model.predict(final_features)

        print(prediction)
        
        fulfillmentText= "Your Health Insurance Premium is:  {} !".format(prediction[0])

        return {
            "fulfillmentText": fulfillmentText
        }

if __name__ == '__main__':
    app.run()
