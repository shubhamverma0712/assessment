from flask import Flask, jsonify, request, make_response, abort, send_from_directory
from assessment.basic import table_db, find_search_string,find_elements_or

simple_api = Flask(__name__)

@simple_api.errorhandler(404)
def not_found(error):
    """
    Returns a JSON with failed status and Error 404
    """
    return make_response(jsonify({'error': 'Not found',
                                  'status': 'failed'}), 404)


@simple_api.errorhandler(400)
def bad_request(error):
    """
    Returns a JSON with failed status and Error 400
    """
    return make_response(jsonify({'error': 'Bad request',
                                  'status': 'failed'}), 400)


@simple_api.errorhandler(500)
def internal_error_server(error):
    """
    Returns a JSON with failed status and Error 500
    """
    return make_response(jsonify({'error': 'Something Bad Happened',
                                  'status': 'failed'}), 500)


@simple_api.route('/search')

def search():
    if (not request.args.get('string') and
            not request.args.get('pincode') and
            not request.args.get('cityname')):
        abort(400)
    if (request.args.get('string')):
        return_list = find_search_string(table_db,request.args.get('string'))
    elif (request.args.get('pincode')):
        return_list = find_elements_or(table_db,{"Pincode":request.args.get('pincode')})
    elif (request.args.get('cityname')):
        return_list = find_elements_or(table_db,{"Place_Name":request.args.get('cityname')})
    else :
        abort(400)
    return jsonify({"results":return_list}),200