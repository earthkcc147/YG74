import time
import requests
import datetime
import pytz

# คอนฟิกต่าง ๆ
config = {
    'accessToken': "9dRBK/OYNakgnQrCQCyy817sGXgTP6l2T4395dUV9ARo+HOxGynZ4+j4KvWFB8BxO6+ne5stqD6rHCinVHzI9HcWpwDJa5nL5IOCYpojc8wZmRECNE8ID1uCvIQqcJK8IxIq2co94N5VlfHE1edupwdB04t89/1O/w1cDnyilFU=",
    'groupId': 'C51c44c32ba5270f731e41370caa63f35',
    'adminId': 'C2e26fe7233b5bc23267e59d09b0a313d',
    'apiUrl': {
        'pushMsg': "https://api.line.me/v2/bot/message/push",
        'userProfile': "https://api.line.me/v2/bot/profile/",
        'groupSummary': "https://api.line.me/v2/bot/group/"
    },
    'activities': [
        {
            'name': '⚡ สงครามเมฆาพายุฝน ⚡',
            'days': ['ทุกวัน'],
            'times': ['12:00', '19:00'],
            'details': '💥 เปิดทุกวัน!!\nระยะเวลา: 12:00 - 13:00, 19:00 - 20:00\n🔥 เตรียมพร้อมลุยกันเลย!!',
            'image_url': "https://i.ibb.co/hcgMBM3/IMG-20241129-125041.jpg"
        },
        {
            'name': '👹 รวมพลฆ่ามอนสเตอร์ 👹',
            'days': ['วันอังคาร', 'วันพฤหัสบดี', 'วันเสาร์'],
            'times': ['14:00'],
            'details': '💀 เปิดทุกวันอังคาร, พฤหัสบดี, เสาร์\nระยะเวลา: 14:00 - 14:20\n💥 มันส์กันแน่!!',
            'image_url': "https://i.ibb.co/cxY6rt9/IMG-20241129-124953.jpg"
        },
        {
            'name': '⚔️ ต่อสู้ในยุทธภพ ⚔️',
            'days': ['วันจันทร์', 'วันพุธ', 'วันอาทิตย์'],
            'times': ['20:00'],
            'details': '🔥 เปิดทุกวันจันทร์, พุธ, อาทิตย์\nระยะเวลา: 20:00 - 20:20\n💣 เตรียมพร้อมสู้รบ!!',
            'image_url': "https://i.ibb.co/cykKdYj/IMG-20241129-125107.jpg"
        },
        {
            'name': '👑 ต่อสู้ระหว่างฝ่าย 👑',
            'days': ['วันเสาร์'],
            'times': ['18:20'],
            'details': '⚔️ เปิดทุกวันเสาร์\nระยะเวลา: 20:00 - 20:20\n💥 สุดยอดสงครามระหว่างฝ่าย!!',
            'image_url': "https://i.ibb.co/sjn3zWK/IMG-20241129-124905.jpg"
        }
    ]
}

# ฟังก์ชันส่งข้อความ
def push_msg(group_id, message, access_token, image_url=None):
    try:
        url = config['apiUrl']['pushMsg']
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        payload = {
            "to": group_id,
            "messages": []
        }

        if image_url:
            payload["messages"].append({
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url
            })

        payload["messages"].append({
            "type": "text",
            "text": message
        })

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"[DEBUG] Message sent successfully! Image included: {bool(image_url)}")
        print(f"[DEBUG] Response Status Code: {response.status_code}")
        print(f"[DEBUG] Response Text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error sending message: {e}")

# ฟังก์ชันแจ้งเตือนกิจกรรมทั้งหมดตอน 8:00
def notify_all_activities(config, current_time):
    print("----- START DEBUG: notify_all_activities -----")
    print(f"[DEBUG] Current Time: {current_time}")
    if current_time == "08:00":
        print("[DEBUG] Preparing to notify all activities for today.")
        message = "🔥 กิจกรรมทั้งหมด 🔥\n"
        # เพิ่ม URL ของภาพที่จะส่ง
        image_url = "https://www.breaker-shoes.com/wp-content/uploads/2024/11/2.png"
        
        # สร้างข้อความกิจกรรมทั้งหมด
        for activity in config['activities']:
            print(f"[DEBUG] Adding activity: {activity['name']} with details.")
            message += f"\n🎯 {activity['name']}\n{activity['details']}\n"
        
        # ส่งรูปภาพก่อนข้อความ
        push_msg(config['groupId'], message, config['accessToken'], image_url)
        print("[DEBUG] All activities notified successfully.")
    else:
        print("[DEBUG] Current time is not 08:00, skipping notification.")
    print("----- END DEBUG: notify_all_activities -----")

# ฟังก์ชันแจ้งเตือนกิจกรรมตามเวลา
def notify_activities(config):
    notified_times = []
    timezone = pytz.timezone("Asia/Bangkok")

    while True:
        now = datetime.datetime.now(timezone)
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")

        days_mapping = {
            "Monday": "วันจันทร์",
            "Tuesday": "วันอังคาร",
            "Wednesday": "วันพุธ",
            "Thursday": "วันพฤหัสบดี",
            "Friday": "วันศุกร์",
            "Saturday": "วันเสาร์",
            "Sunday": "วันอาทิตย์"
        }
        current_day_th = days_mapping[current_day]

        now = datetime.datetime.now(timezone)
        notified_times = [t for t in notified_times if now - t < datetime.timedelta(hours=24)]

        print("----- START DEBUG ROUND -----")
        print(f"[DEBUG] Current Time: {current_time}")
        print(f"[DEBUG] Current Day (EN): {current_day}")
        print(f"[DEBUG] Current Day (TH): {current_day_th}")
        print(f"[DEBUG] Notified Times: {notified_times}")

        # เรียกฟังก์ชันแจ้งเตือนกิจกรรมทั้งหมด
        notify_all_activities(config, current_time)

        for activity in config['activities']:
            print(f"[DEBUG] Checking Activity: {activity['name']}")
            if current_time in activity['times']:
                if current_time not in [t.strftime("%H:%M") for t in notified_times]:
                    if 'ทุกวัน' in activity['days'] or current_day_th in activity['days']:
                        message = f"🔥 กิจกรรม: {activity['name']} 🔥\nรายละเอียด: {activity['details']}"
                        image_url = activity.get('image_url')
                        print(f"[DEBUG] Preparing to send message for activity: {activity['name']}")
                        push_msg(config['groupId'], message, config['accessToken'], image_url)
                        notified_times.append(now)

        print("----- END DEBUG ROUND -----")
        time.sleep(60)

# เริ่มการแจ้งเตือน
notify_activities(config)
