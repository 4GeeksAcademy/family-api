"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
        
        members = jackson_family.get_all_members()
        
        response = jsonify(members)
        response.headers['Content-Type'] = 'application/json'
        return response, 200
    

@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
        
        member = jackson_family.get_member(member_id)
        
        if member is None:
            error_response = jsonify({"error": "Member not found"})
            error_response.headers['Content-Type'] = 'application/json'
            return error_response, 404
        
        success_response = jsonify(member)
        success_response.headers['Content-Type'] = 'application/json'
        return success_response, 200
        

@app.route('/members', methods=['POST'])
def add_new_member():
  
    member_data = request.get_json()
    
    if "first_name" not in member_data:
        error_response = jsonify({"error": "Missing first_name"})
        error_response.headers['Content-Type'] = 'application/json'
        return error_response, 400
    
    new_member = jackson_family.add_member(member_data)
    
    success_response = jsonify(new_member)
    success_response.headers['Content-Type'] = 'application/json'
    return success_response, 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    
    deleted_member = jackson_family.delete_member(member_id)
    
    if deleted_member is None:
        error_response = jsonify({"error": "Member not found"})
        error_response.headers['Content-Type'] = 'application/json'
        return error_response, 404
    
    success_response = jsonify({"done": True})
    success_response.headers['Content-Type'] = 'application/json'
    return success_response, 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

