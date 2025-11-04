
# from flask import jsonify, request
# from flask_jwt_extended import jwt_required, current_user
# from .models import ParkingLot, ParkingSpot, db
# from .routes import app, role_required
from .models import User, ParkingLot, ParkingSpot, Reservation
from .database import db
from flask_jwt_extended import create_access_token, jwt_required, current_user
from flask import current_app as app, jsonify, request, abort  
from flask_jwt_extended import create_access_token, current_user, jwt_required
from functools import wraps 
from sqlalchemy.orm import joinedload

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn) 
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(message="Not authorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
# def role_required(required_role):
#     def wrapper(fn):
#         @wraps(fn) 
#         @jwt_required()
#         def decorator(*args, **kwargs):
#             if current_user.role != required_role:
#                 return jsonify(message = "You are not authorized"), 403
#             return fn(*args, **kwargs)
#         return decorator
#     return wrapper
 
# @app.route("/login", methods=["POST"])
# def login():
#     username = request.json.get("username", None)
#     password = request.json.get("password", None)

#     user = User.query.filter_by(username=username).one_or_none()
#     if not user or not user.password == password: 
#         return jsonify("Wrong username or password"), 401
    
#     #Notice that we are passing in the actual sqlalchemy user object

#     access_token = create_access_token(identity=user)
#     return jsonify(access_token=access_token)


@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        password=current_user.password,
        role=current_user.role
    )


# dashboard
# @app.route("/dashboard")
# @jwt_required()
# def dashboard():
#     if current_user.role == "admin":
#         return "welcome to admin dashboard!"
#     else:
#         return "welcome to user dashboard!"

# @app.route("/onlyadmin")
# @role_required("admin")
# def admin_endpoint():
#     return "Only admin is allowed"
    # if current_user.role == "admin":
    #     return "You are authorised"
    # else:
    #     return abort(403)





# ---------------------------------------
# 🔐 Role-based Access Decorator
# ---------------------------------------


# ---------------------------------------
# 👤 Register User
# ---------------------------------------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    # vehicle_registration_number = data.get("vehicle_registration_number")

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify(message="User already exists"), 409

    user = User(username=username, email=email, password_hash=password, role="user")
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully",password=password)  


# ---------------------------------------
# 🔑 Login User
# ---------------------------------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or user.password_hash != password:
        return jsonify(message="Invalid credentials"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


# ---------------------------------------
# 🧭 Dashboard (Role-aware)
# ---------------------------------------
# @app.route("/api/dashboard", methods=["GET"])
# @jwt_required()
# def dashboard():
#     if current_user.role == "admin":
#         users = len(User.query.filter_by(role="user").all())
#         card_requests = UserCardDetail.query.filter_by(attr_name = "status").all()
#         requested = under_verification = verified = generated = 0
#         card_request_json = []
#         for detail in card_requests:
#             detail_dict = {}
#             detail_dict["username"] = detail.bearer.username 
#             detail_dict["cardname"] = detail.cardname 
#             detail_dict["status"] = detail.attr_val 
#             if detail.attr_val == "requested":
#                 requested +=1
#             if detail.attr_val == "under_verification":
#                 under_verification +=1 
#             if detail.attr_val == "verified":
#                 verified += 1
#             if detail.attr_val == "generated":
#                 generated += 1 
#             card_request_json.append(detail_dict)
#         return jsonify({
#             "admin_name": current_user.username,
#             "users": users,
#             "card_requests": requested,
#             "under_verification": under_verification,
#             "verified": verified,
#             "card_granted": generated,
#             "available_cards": 4,
#             "card_request_details": card_request_json
#         })
#     else:
#         user_card_details = UserCardDetail.query.filter_by(attr_name="status",user_id=current_user.id).all()
#         available_cards = []
#         card_requests = []
#         for detail in user_card_details:
#             detail_dict = {}
#             if detail.attr_val == "generated":
#                detail_dict["cardname"] = detail.cardname
#                available_cards.append(detail_dict)
#             else: 
#                 detail_dict["cardname"] = detail.cardname
#                 detail_dict["status"]  = detail.attr_val 
#                 card_requests.append(detail_dict)
#     return jsonify({
#         "username": current_user.username,
#         "available_cards": available_cards,
#         "card_requests": card_requests
#     }) 
@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    # return jsonify(message=f"Welcome {current_user.username}, role: {current_user.role}")
    history = get_user_parking_history(current_user.id)
    return jsonify({
        "history": history,
        "username": current_user.username,
        "role": current_user.role
    })


# ---------------------------------------
# 🚗 Admin: Create Parking Lot
# ---------------------------------------
@app.route("/admin/parkinglots", methods=["POST"])
@role_required("admin")
def create_parking_lot():
    data = request.json
    lot = ParkingLot(
        prime_location_name=data.get("prime_location_name"),
        price=data.get("price"),
        address=data.get("address"),
        pin_code=data.get("pin_code"),
        number_of_spots=data.get("number_of_spots")
    )
    db.session.add(lot)
    db.session.commit()

    # Create empty parking spots for this lot
    for _ in range(lot.number_of_spots):
        spot = ParkingSpot(lot_id=lot.id, status='A')
        db.session.add(spot)

    db.session.commit()
    return jsonify(message="Parking lot created successfully", lot_id=lot.id)


# ---------------------------------------
# 🧾 Admin: View All Parking Lots
# ---------------------------------------
@app.route("/admin/parkinglots", methods=["GET"])
@role_required("admin")
def get_parking_lots():
    lots = ParkingLot.query.all()
    spots = ParkingSpot.query.all()
    spot_status=[]
    result = []
    for lot in lots:
        occupied_num=0
        for spot in spots:
            spot_status.append(spot.status)
            if lot.id == spot.lot_id:
               if spot.status == 'O':
                    occupied_num +=1 
        result.append({
            "id": lot.id,
            "name": lot.prime_location_name,
            "price": lot.price,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "number_of_spots": lot.number_of_spots,
            "occupied": occupied_num,
            "spot_status": spot_status
        })
    return jsonify(result)


@app.route("/admin/parkingLots/<int:lot_id>", methods=["GET"])
@role_required("admin")
def get_parking_lot_by_id(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
    return jsonify({
        "id": lot.id,
        "prime_location_name": lot.prime_location_name,
        "price": lot.price,
        "address": lot.address,
        "pin_code": lot.pin_code,
        "number_of_spots": lot.number_of_spots,
        "occupied": occupied
    })

@app.route("/admin/parkingLots/<int:lot_id>", methods=["PUT"])
def update_parking_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking lot not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        old_spot_count = lot.number_of_spots
        new_spot_count = int(data.get("number_of_spots", old_spot_count))

        lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
        lot.price = float(data.get("price", lot.price))
        lot.address = data.get("address", lot.address)
        lot.pin_code = data.get("pin_code", lot.pin_code)
        lot.number_of_spots = new_spot_count

        # --- Adjust parking spots dynamically ---
        if new_spot_count > old_spot_count:
            for _ in range(new_spot_count - old_spot_count):
                new_spot = ParkingSpot(lot_id=lot.id, status='A')
                db.session.add(new_spot)
        elif new_spot_count < old_spot_count:
            removable_spots = (
                ParkingSpot.query.filter_by(lot_id=lot.id, status='A')
                .order_by(ParkingSpot.id.desc())
                .limit(old_spot_count - new_spot_count)
                .all()
            )
            for spot in removable_spots:
                db.session.delete(spot)

        db.session.commit()
        return jsonify({"message": "Parking lot updated successfully"})

    except Exception as e:
        db.session.rollback()
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500



# ✅ Admin: Get parking lot + its spots
@app.route("/api/parkinglot/<int:lot_id>", methods=["GET"])
@role_required("admin")
def get_parking_lot_with_spots(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking lot not found"}), 404

    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
    return jsonify({
        "id": lot.id,
        "prime_location_name": lot.prime_location_name,
        "address": lot.address,
        "number_of_spots": lot.number_of_spots,
        "spot_status": [s.status for s in spots]
    })


# ✅ Admin: Delete an unoccupied spot
@app.route("/api/delete-spot/<int:lot_id>/<int:spot_id>", methods=["DELETE"])
@role_required("admin")
def delete_spot(lot_id, spot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking lot not found"}), 404

    spot = ParkingSpot.query.filter_by(id=spot_id, lot_id=lot_id).first()
    if not spot:
        return jsonify({"error": "Spot not found"}), 404

    if spot.status == "O":  # Occupied
        return jsonify({"error": "Cannot delete an occupied spot"}), 403

    # ✅ Delete the spot
    db.session.delete(spot)

    # ✅ Decrement lot's spot count
    if lot.number_of_spots > 0:
        lot.number_of_spots -= 1

    db.session.commit()

    return jsonify({
        "message": "Spot deleted successfully",
        "updated_number_of_spots": lot.number_of_spots
    })


# @app.route("/api/parkinglot/<int:lotId>", methods=["GET"])
# @role_required("admin")
# def get_parking_lot(lotId):
#     lot = ParkingLot.query.get(lotId)
#     if not lot:
#         return jsonify({"error": "Parking lot not found"}), 404
    
#     # Convert stored JSON/text to Python list
#     try:
#         import json
#         spot_status = json.loads(lot.spot_status)
#     except:
#         spot_status = lot.spot_status.split(",")

#     return jsonify({
#         "id": lot.id,
#         "name": lot.name,
#         "spot_status": spot_status
#     })


# @app.route("/api/delete-spot/<int:lot_id>/<int:spot_index>", methods=["DELETE"])
# def delete_spot(lot_id, spot_index):
#     lot = ParkingLot.query.get(lot_id)
#     if not lot:
#         return jsonify({"error": "Parking lot not found"}), 404

#     try:
#         spots = json.loads(lot.spot_status)
#     except:
#         spots = lot.spot_status.split(",")

#     if spot_index < 0 or spot_index >= len(spots):
#         return jsonify({"error": "Invalid spot index"}), 400

#     # Check if spot is occupied
#     if spots[spot_index] in ["O", "Occupied"]:
#         return jsonify({"error": "Cannot delete an occupied spot"}), 403

#     # Remove the spot
#     spots.pop(spot_index)

#     # Save updated data
#     lot.spot_status = json.dumps(spots)
#     db.session.commit()

#     return jsonify({"message": "Spot deleted successfully", "updated_spots": spots})

# ---------------------------------------
# 🗑️ Admin: Delete Parking Lot
# ---------------------------------------
@app.route("/admin/parkinglots/<int:lot_id>", methods=["DELETE"])
@role_required("admin")
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    # Delete related spots and reservations first
    for spot in lot.spots:
        Reservation.query.filter_by(spot_id=spot.id).delete()
        db.session.delete(spot)

    db.session.delete(lot)
    db.session.commit()
    return jsonify(message="Parking lot deleted")


# ---------------------------------------
# 👀 Admin: View All Spots in a Lot
# ---------------------------------------
@app.route("/admin/parkinglots/<int:lot_id>/spots", methods=["GET"])
@role_required("admin")
def view_spots(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = [{
        "id": spot.id,
        "status": spot.status
    } for spot in lot.spots]
    return jsonify(spots)


# ---------------------------------------
# 📍 User: View Available Parking Lots
# ---------------------------------------
@app.route("/user/parkinglots", methods=["GET"])
@role_required("user")
def list_available_lots():
    lots = ParkingLot.query.all()
    data = []
    for lot in lots:
        available = sum(1 for spot in lot.spots if spot.status == 'A')
        data.append({
            "id": lot.id,
            "location": lot.prime_location_name,
            "price": lot.price,
            "available_spots": available
        })
    return jsonify(data)


# ---------------------------------------
# 🎫 User: Reserve a Parking Spot
# ---------------------------------------
@app.route("/user/reserve", methods=["POST"])
@role_required("user")
def reserve_spot():
    lot_id = request.json.get("lot_id")
    lot = ParkingLot.query.get_or_404(lot_id)

    # Find an available spot
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify(message="No spots available"), 404

    spot.status = 'O'
    reservation = Reservation(
        user_id=current_user.id,
        spot_id=spot.id,
        parking_cost=lot.price
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify(message="Spot reserved", reservation_id=reservation.id)


# ---------------------------------------
# 🔓 User: Release (Vacate) Spot
# ---------------------------------------
@app.route("/user/release", methods=["POST"])
@role_required("user")
def release_spot():
    reservation = Reservation.query.filter_by(user_id=current_user.id, leaving_timestamp=None).first()

    if not reservation:
        return jsonify(message="No active reservation found"), 404

    reservation.leaving_timestamp = db.func.now()
    reservation.spot.status = 'A'

    db.session.commit()
    return jsonify(message="Spot released")


# ---------------------------------------
# 🧾 User: View Active Reservation
# ---------------------------------------
@app.route("/user/myreservation", methods=["GET"])
@role_required("user")
def my_reservation():
    reservation = Reservation.query.filter_by(user_id=current_user.id, leaving_timestamp=None).first()
    if not reservation:
        return jsonify(message="No active reservation")

    return jsonify({
        "spot_id": reservation.spot_id,
        "lot_id": reservation.spot.lot_id,
        "parking_timestamp": reservation.parking_timestamp,
        "cost": reservation.parking_cost
    })


def get_user_parking_history(user_id):
    reservations = (
        db.session.query(Reservation)
        .options(joinedload(Reservation.spot).joinedload(ParkingSpot.lot))
        .filter(Reservation.user_id == user_id)
        .all()
    )

    history = []
    for res in reservations:
        history.append({
            "id": res.id,
            "location": res.spot.lot.prime_location_name,  # Parking Lot Name
            # "vehicle_no": res.vehicle_no,
            "timestamp": res.parking_timestamp.strftime("%Y-%m-%d %H:%M"),
            "action": "Parked Out" if res.leaving_timestamp else "Release"
        })
    return history


@app.route("/user/parkinglots/dadar", methods=["GET"])
@role_required("user")
def parking_lots_dadar():
    # Filter parking lots by address containing 'Dadar Road'
    lots = ParkingLot.query.filter(ParkingLot.address.ilike("%Dadar Road%")).all()
    data = []

    for lot in lots:
        available_spots = sum(1 for spot in lot.spots if spot.status == 'A')
        data.append({
            "id": lot.id,
            "address": lot.address,
            "availability": available_spots,
            "book": True if available_spots > 0 else False
        })

    return jsonify(data)



@app.route('/admin/users', methods=['GET'])
@jwt_required("admin")
def get_users():
    users = User.query.all()
    user_list = [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.username,
            "address": user.password_hash,
            "pin_code": user.role
        }
        for user in users
    ]
    return jsonify({"users": user_list}), 200


@app.route('/admin/search', methods=['GET'])
@jwt_required("admin")
def admin_search():
    search_by = request.args.get('by')
    query = request.args.get('q')

    if not search_by or not query:
        return jsonify({'error': 'Missing parameters'}), 400

    results = []
    if search_by == 'location':
        lots = ParkingLot.query.filter(ParkingLot.prime_location_name.ilike(f"%{query}%")).all()
        for lot in lots:
            occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
            results.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'price': lot.price,
                'pin_code': lot.pin_code,
                'number_of_spots': lot.number_of_spots,
                'occupied': occupied
            })
    elif search_by == 'id':
        lot = ParkingLot.query.filter_by(id=query).first()
        if lot:
            occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
            results.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'price': lot.price,
                'pin_code': lot.pin_code,
                'number_of_spots': lot.number_of_spots,
                'occupied': occupied
            })
    else:
        return jsonify({'error': 'Invalid search type'}), 400

    return jsonify({'results': results})


@app.route('/admin/stats', methods=['GET'])
@jwt_required('admin')
def get_summary():
    # Revenue from each parking lot
    lots = ParkingLot.query.all()
    revenue_data = []
    for lot in lots:
        total_revenue = db.session.query(db.func.sum(Reservation.parking_cost))\
            .join(ParkingSpot).filter(ParkingSpot.lot_id == lot.id).scalar() or 0
        revenue_data.append({
            'lot_name': lot.prime_location_name,
            'revenue': total_revenue
        })

    # Available vs Occupied summary
    total_spots = ParkingSpot.query.count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    available_spots = total_spots - occupied_spots

    occupancy_summary = {
        'available': available_spots,
        'occupied': occupied_spots,
        'total': total_spots
    }

    return jsonify({
        'revenue': revenue_data,
        'occupancy': occupancy_summary
    })
