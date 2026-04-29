from flask import Flask, request, Response
import requests
import json
import os

app = Flask(__name__)

# ✅ دالة لجلب معلومات اللاعب (منها المنطقة)
def get_player_info(player_id):
    cookies = {
        'region': 'MA',
        'language': 'ar',
        'session_key': 'efwfzwesi9ui8drux4pmqix4cosane0y',  # ⚠️ ممكن تحتاج تحديثه
    }

    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://shop2game.com',
        'Referer': 'https://shop2game.com/app/100067/idlogin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-datadome-clientid': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
    }

    json_data = {
        'app_id': 100067,
        'login_id': str(player_id),
        'app_server_id': 0,
    }

    try:
        res = requests.post('https://shop2game.com/api/auth/player_id_login', cookies=cookies, headers=headers, json=json_data)
        if res.status_code == 200:
            data = res.json()
            return {
                "✅ status": "تم جلب المنطقة بنجاح",
                "🆔 UID": player_id,
                "🏷️ Nickname": data.get("nickname", "❌ غير متوفر"),
                "🌍 Region": data.get("region", "❌ غير معروف")
            }
    except Exception as e:
        return {
            "❌ error": f"فشل في الاتصال بالموقع: {str(e)}"
        }

    return {
        "❌ error": "لم يتم العثور على معلومات اللاعب"
    }

# ✅ نقطة الدخول الرئيسية
@app.route("/region", methods=["GET"])
def region():
    player_id = request.args.get("uid", "")

    if not player_id:
        return Response(json.dumps({
            "⚠️ error": "يرجى تحديد UID اللاعب",
            "status_code": 400
        }, indent=4, ensure_ascii=False), mimetype="application/json")

    result = get_player_info(player_id)
    return Response(json.dumps(result, indent=4, ensure_ascii=False), mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))