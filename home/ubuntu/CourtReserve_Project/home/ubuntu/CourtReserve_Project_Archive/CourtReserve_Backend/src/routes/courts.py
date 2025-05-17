from flask import Blueprint, request, jsonify
from src.models.court import Court
from src.models.booking import Booking # Booking मॉडल को इम्पोर्ट करें यदि उपलब्धता की जाँच के लिए आवश्यक हो
from src.extensions import db # db को main.py से इम्पोर्ट करें
from flask_jwt_extended import jwt_required, get_jwt_identity # यदि कुछ एंडपॉइंट्स को सुरक्षा की आवश्यकता हो
from sqlalchemy import func
import datetime

courts_bp = Blueprint("courts", __name__)

@courts_bp.route("", methods=["GET"])
# @jwt_required() # यदि कोर्ट लिस्टिंग केवल लॉग-इन यूज़र्स के लिए है
def list_courts():
    # यहाँ फ़िल्टरिंग और सर्चिंग पैरामीटर्स जोड़े जा सकते हैं (e.g., request.args.get("search"))
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    query = Court.query.filter(Court.status == "active") # केवल सक्रिय कोर्ट्स दिखाएँ

    # उदाहरण के लिए टेक्स्ट सर्च (नाम या पते पर)
    search_term = request.args.get("search")
    if search_term:
        query = query.filter(Court.name.ilike(f"%{search_term}%") | Court.address.ilike(f"%{search_term}%"))

    # सतह प्रकार द्वारा फ़िल्टर करें
    surface_type = request.args.get("surface_type")
    if surface_type:
        query = query.filter(Court.surface_type.ilike(f"%{surface_type}%"))

    # सेटिंग द्वारा फ़िल्टर करें (इनडोर/आउटडोर)
    setting = request.args.get("setting")
    if setting:
        query = query.filter(Court.setting.ilike(f"%{setting}%"))

    paginated_courts = query.paginate(page=page, per_page=per_page, error_out=False)
    courts_data = [court.to_dict() for court in paginated_courts.items]
    
    return jsonify({
        "message": "Courts retrieved successfully",
        "courts": courts_data,
        "total_pages": paginated_courts.pages,
        "current_page": paginated_courts.page,
        "total_courts": paginated_courts.total
    }), 200

@courts_bp.route("/<int:court_id>", methods=["GET"])
# @jwt_required()
def get_court_details(court_id):
    court = Court.query.get(court_id)
    if not court or court.status != "active":
        return jsonify({"message": "Court not found or not active"}), 404
    return jsonify(court.to_dict()), 200

@courts_bp.route("/<int:court_id>/availability", methods=["GET"])
# @jwt_required()
def get_court_availability(court_id):
    court = Court.query.get(court_id)
    if not court or court.status != "active":
        return jsonify({"message": "Court not found or not active"}), 404

    date_str = request.args.get("date") # YYYY-MM-DD फॉर्मेट में
    if not date_str:
        return jsonify({"message": "Date parameter is required (YYYY-MM-DD)"}), 400

    try:
        target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    # उदाहरण के लिए, हम 1 घंटे के स्लॉट मानते हैं, सुबह 8 बजे से रात 10 बजे तक
    # यह कोर्ट के operating_hours से अधिक डायनामिक होना चाहिए
    available_slots = []
    # कोर्ट के ऑपरेटिंग आवर्स को यहाँ से प्राप्त करें, यदि परिभाषित हैं
    # operating_hours = court.operating_hours or { "default": ["08:00", "22:00"] }
    # day_name = target_date.strftime("%A").lower()
    # start_hour_str, end_hour_str = operating_hours.get(day_name, operating_hours.get("default", ["08:00", "22:00"]))
    
    # सादगी के लिए, हम 8 AM से 10 PM (22:00) तक मानते हैं
    start_hour = 8
    end_hour = 22 # 10 PM तक, इसलिए अंतिम स्लॉट 9 PM पर शुरू होगा

    for hour in range(start_hour, end_hour):
        slot_start_time = datetime.datetime.combine(target_date, datetime.time(hour, 0, 0))
        slot_end_time = slot_start_time + datetime.timedelta(hours=1)

        # इस स्लॉट के लिए मौजूदा बुकिंग्स की जाँच करें
        existing_booking = Booking.query.filter(
            Booking.court_id == court_id,
            Booking.status.in_(["approved", "pending"]), # केवल अप्रूव्ड या पेंडिंग बुकिंग्स स्लॉट को ब्लॉक करती हैं
            Booking.start_time < slot_end_time, # मौजूदा बुकिंग स्लॉट के अंत से पहले शुरू होती है
            Booking.end_time > slot_start_time    # मौजूदा बुकिंग स्लॉट की शुरुआत के बाद समाप्त होती है
        ).first()

        if not existing_booking:
            available_slots.append({
                "start_time": slot_start_time.isoformat(),
                "end_time": slot_end_time.isoformat(),
                "status": "available"
            })
        else:
             available_slots.append({
                "start_time": slot_start_time.isoformat(),
                "end_time": slot_end_time.isoformat(),
                "status": "booked"
            })

    return jsonify({
        "court_id": court_id,
        "date": date_str,
        "slots": available_slots
    }), 200

# एडमिन द्वारा कोर्ट्स बनाने/अपडेट करने/डिलीट करने के लिए एंडपॉइंट्स यहाँ जोड़े जा सकते हैं
# लेकिन यह वर्तमान दायरे से बाहर है क्योंकि एडमिन डेटा को बाहरी रूप से मैनेज करेगा

