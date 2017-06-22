from flask import jsonify


def err(error, description, code):
    return jsonify({
        "error": error,
        "description": description,
    }), code, {'Content-Type': 'application/json'}


def ip_2_coor(user_ip):
    lo, la = user_ip, user_ip
    return lo, la


def check_ip(IP, user_ip):
    # return False when ip is blocked from ip table
    if IP.find_one({'ip': user_ip}):
        return True
    return False
