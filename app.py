from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# --- App Configuration ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_simple_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', lazy=True, cascade="all, delete-orphan")

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(1), default='A')  # A=Available, O=Occupied
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    reservations = db.relationship('Reservation', backref='spot', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

# --- General & Auth Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for('register'))
        new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], is_admin=False).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = False
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid user credentials.", "danger")
    return render_template('auth/login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin = User.query.filter_by(username=request.form['username'], is_admin=True).first()
        if admin and check_password_hash(admin.password, request.form['password']):
            session['user_id'] = admin.id
            session['username'] = admin.username
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials.", "danger")
    return render_template('auth/admin_login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))


# --- Admin Routes ---
@app.route('/admin/dashboard')
def admin_dashboard():
    # Direct check for admin session
    if not session.get('is_admin'):
        flash("You must be logged in as an admin to view this page.", "warning")
        return redirect(url_for('admin_login'))
    
    all_lots = ParkingLot.query.all()
    lot_stats = []
    for lot in all_lots:
        lot_stats.append({
            'id': lot.id,
            'name': lot.name,
            'occupied': ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count(),
            'available': ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        })
        
    stats = {
        'total_lots': len(all_lots),
        'total_spots': ParkingSpot.query.count(),
        'occupied_spots': ParkingSpot.query.filter_by(status='O').count(),
        'total_users': User.query.filter_by(is_admin=False).count()
    }
    return render_template('admin/dashboard.html', stats=stats, lot_stats=lot_stats)

@app.route('/admin/lots', methods=['GET', 'POST'])
def lots():
    # Direct check for admin session
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        new_lot = ParkingLot(name=request.form['name'], address=request.form['address'], pincode=request.form['pincode'], price=float(request.form['price']), capacity=int(request.form['capacity']))
        db.session.add(new_lot)
        db.session.flush() 
        for i in range(1, new_lot.capacity + 1):
            db.session.add(ParkingSpot(spot_number=i, lot_id=new_lot.id))
        db.session.commit()
        flash(f"Lot '{new_lot.name}' created successfully!", "success")
        return redirect(url_for('lots'))

    all_lots = ParkingLot.query.all()
    return render_template('admin/lots.html', lots=all_lots)

@app.route('/admin/lots/edit/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    # Direct check for admin session
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    lot_to_edit = ParkingLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        occupied_count = ParkingSpot.query.filter_by(lot_id=lot_to_edit.id, status='O').count()
        new_capacity = int(request.form['capacity'])

        if new_capacity < occupied_count:
            flash(f"Capacity cannot be less than the number of occupied spots ({occupied_count}).", "danger")
            return redirect(url_for('edit_lot', lot_id=lot_id))

        lot_to_edit.name, lot_to_edit.address, lot_to_edit.pincode, lot_to_edit.price = request.form['name'], request.form['address'], request.form['pincode'], float(request.form['price'])
        
        if new_capacity > lot_to_edit.capacity:
            for i in range(lot_to_edit.capacity + 1, new_capacity + 1):
                db.session.add(ParkingSpot(spot_number=i, lot_id=lot_to_edit.id))
        elif new_capacity < lot_to_edit.capacity:
            spots_to_remove = ParkingSpot.query.filter_by(lot_id=lot_to_edit.id, status='A').order_by(ParkingSpot.spot_number.desc()).limit(lot_to_edit.capacity - new_capacity)
            for spot in spots_to_remove:
                db.session.delete(spot)

        lot_to_edit.capacity = new_capacity
        db.session.commit()
        flash(f"Lot '{lot_to_edit.name}' updated successfully!", "success")
        return redirect(url_for('lots'))
    
    return render_template('admin/edit_lot.html', lot=lot_to_edit)

@app.route('/admin/lots/delete/<int:lot_id>', methods=['POST'])
def delete_lot(lot_id):
    # Direct check for admin session
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    lot_to_delete = ParkingLot.query.get_or_404(lot_id)
    if ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count() > 0:
        flash("Cannot delete a lot that has parked cars.", "danger")
    else:
        db.session.delete(lot_to_delete)
        db.session.commit()
        flash(f"Lot '{lot_to_delete.name}' has been deleted.", "success")
    return redirect(url_for('lots'))

@app.route('/admin/view_lot/<int:lot_id>')
def view_lot(lot_id):
    # Direct check for admin session
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).order_by(ParkingSpot.spot_number).all()
    return render_template('admin/view_lot.html', lot=lot, spots=spots)

@app.route('/admin/users')
def view_users():
    # Direct check for admin session
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    all_users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=all_users)


# --- User Routes ---
@app.route('/dashboard')
def user_dashboard():
    # Direct check for user session
    if 'user_id' not in session or session.get('is_admin'):
        flash("Please log in to view your dashboard.", "warning")
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    current_booking = Reservation.query.filter_by(user_id=user_id, is_active=True).first()
    booking_history = Reservation.query.filter_by(user_id=user_id, is_active=False).order_by(Reservation.exit_time.desc()).all()
    return render_template('user/dashboard.html', current_booking=current_booking, booking_history=booking_history)

@app.route('/book', methods=['GET', 'POST'])
def book():
    # Direct check for user session
    if 'user_id' not in session or session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        lot_id = request.form.get('lot_id')
        if Reservation.query.filter_by(user_id=session['user_id'], is_active=True).first():
            flash("You already have an active booking.", "danger")
            return redirect(url_for('user_dashboard'))
        
        available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').order_by(ParkingSpot.spot_number).first()
        if available_spot:
            available_spot.status = 'O'
            new_booking = Reservation(user_id=session['user_id'], spot_id=available_spot.id, lot_id=lot_id)
            db.session.add(new_booking)
            db.session.commit()
            flash(f"Successfully booked Spot #{available_spot.spot_number} in {available_spot.lot.name}!", "success")
        else:
            flash("Sorry, no spots were available in that lot.", "danger")
        return redirect(url_for('user_dashboard'))

    # GET request: show the list of lots to choose from
    all_lots = ParkingLot.query.all()
    lots_with_availability = []
    for lot in all_lots:
        lots_with_availability.append({
            'lot': lot, 
            'available_spots': ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        })
    return render_template('user/book.html', lots_with_availability=lots_with_availability)

@app.route('/release/<int:booking_id>', methods=['POST'])
def release(booking_id):
    # Direct check for user session
    if 'user_id' not in session or session.get('is_admin'):
        return redirect(url_for('login'))
    
    booking_to_release = Reservation.query.get_or_404(booking_id)
    if booking_to_release.user_id != session['user_id']:
        flash("This is not your booking.", "danger")
        return redirect(url_for('user_dashboard'))
    
    spot = booking_to_release.spot
    spot.status = 'A'
    
    booking_to_release.exit_time = datetime.utcnow()
    duration_hours = (booking_to_release.exit_time - booking_to_release.entry_time).total_seconds() / 3600
    booking_to_release.cost = round(duration_hours * spot.lot.price, 2)
    booking_to_release.is_active = False
    
    db.session.commit()
    flash(f"Spot released. Total cost: ${booking_to_release.cost:.2f}", "success")
    return redirect(url_for('user_dashboard'))

# --- Main Execution & Database Setup ---
if __name__ == '__main__':
    # This block runs only when the script is executed directly
    # It sets up the database and admin user before starting the app
    with app.app_context():
        db.create_all()
        # Create admin user if it doesn't exist
        if not User.query.filter_by(is_admin=True).first():
            hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')
            admin_user = User(username='admin', password=hashed_password, is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
            print("Database checked and admin user created if not present.")
    
    app.run(debug=True)