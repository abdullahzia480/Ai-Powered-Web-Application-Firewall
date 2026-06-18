from flask import Flask, render_template, request, redirect, url_for, session

def create_app():
    app = Flask(__name__)
    app.secret_key = 'vulnerable_secret_key'

    # Expanded Mock Database
    products = [
        # Processors
        {'id': 1, 'name': 'Quantum Core i9', 'price': 5000, 'category': 'Processors', 'rating': 4.8, 'img': 'cpu.png', 'desc': 'Next-gen quantum processing unit for consumer decks.'},
        {'id': 2, 'name': 'Neural Interface V2', 'price': 12000, 'category': 'Implants', 'rating': 4.9, 'img': 'neural.png', 'desc': 'Direct brain-to-machine interface with sub-ms latency.'},
        {'id': 3, 'name': 'Synaptic Accelerator', 'price': 3500, 'category': 'Processors', 'rating': 4.5, 'img': 'synaptic.png', 'desc': 'Boosts thought processing speed by 200%.'},
        
        # Gadgets
        {'id': 4, 'name': 'Hologram Projector', 'price': 850, 'category': 'Gadgets', 'rating': 4.2, 'img': 'holo.png', 'desc': 'Portable 3D holographic display unit.'},
        {'id': 5, 'name': 'Optical Camo Cloak', 'price': 15000, 'category': 'Gadgets', 'rating': 5.0, 'img': 'camo.png', 'desc': 'Active camouflage system for urban stealth.'},
        {'id': 6, 'name': 'Wrist Deck MK-IV', 'price': 900, 'category': 'Gadgets', 'rating': 4.6, 'img': 'deck.png', 'desc': 'Wearable cyberdeck for hacking on the go.'},

        # Energy
        {'id': 7, 'name': 'Fusion Battery', 'price': 300, 'category': 'Energy', 'rating': 4.7, 'img': 'battery.png', 'desc': 'Miniaturized cold fusion power cell.'},
        {'id': 8, 'name': 'Zero-Point Module', 'price': 45000, 'category': 'Energy', 'rating': 5.0, 'img': 'zpm.png', 'desc': 'Experimental infinite energy source.'},
        {'id': 9, 'name': 'Plasma Capacitor', 'price': 150, 'category': 'Energy', 'rating': 3.9, 'img': 'plasma.png', 'desc': 'High-output capacitor for energy weapons.'},

        # Implants
        {'id': 10, 'name': 'Ocular Implant Z-Eye', 'price': 6000, 'category': 'Implants', 'rating': 4.8, 'img': 'eye.png', 'desc': 'Zoom, infrared, and night vision capabilities.'},
        {'id': 11, 'name': 'Subdermal Armor', 'price': 8000, 'category': 'Implants', 'rating': 4.9, 'img': 'armor.png', 'desc': 'Graphene-mesh plating for ballistic protection.'},
        {'id': 12, 'name': 'Reflex Booster', 'price': 4200, 'category': 'Implants', 'rating': 4.4, 'img': 'reflex.png', 'desc': 'Overclocks nervous system for enhanced reaction time.'},
    ]

    @app.route('/')
    def index():
        # Get featured products (top rated)
        featured = sorted(products, key=lambda x: x['rating'], reverse=True)[:4]
        return render_template('home.html', featured=featured)

    @app.route('/shop')
    def shop():
        category = request.args.get('category')
        if category:
            filtered = [p for p in products if p['category'] == category]
        else:
            filtered = products
        return render_template('shop.html', products=filtered)
        
    @app.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            return "Product not found", 404
        # Mock reviews (Vulnerable to Stored XSS if we had a DB, here we assume extraction)
        return render_template('product.html', product=product)

    @app.route('/review', methods=['POST'])
    def submit_review():
        # Vulnerable Endpoint: Stored XSS (Simulated)
        # In a real app, this would save to DB. 
        # Here we just reflect it back on a confirmation page or similar.
        comment = request.form.get('comment', '')
        # WAF should catch <script> tags here
        return f"<h1>Review Submitted!</h1><p>You said: {comment}</p><a href='/shop'>Back</a>"

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        query = request.args.get('q', '')
        if request.method == 'POST':
            query = request.form.get('q', '')
        
        # Vulnerable Logic: Filter using string containment
        results = [p for p in products if query.lower() in p['name'].lower()]
        return render_template('shop.html', products=results, search_query=query)

    @app.route('/newsletter', methods=['POST'])
    def newsletter():
        email = request.form.get('email')
        # Vulnerable to Command Injection (Simulated) logic if passed to os.system
        # WAF should inspect this.
        return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # VULNERABLE SQLi LOGIC
            if username == 'admin' and password == 'password123':
                session['user'] = username
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Invalid Credentials")
        
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        if 'user' in session:
            return redirect(url_for('profile'))
        return redirect(url_for('login'))

    @app.route('/profile')
    def profile():
        if 'user' not in session:
            return redirect(url_for('login'))
        
        # IDOR Vulnerability Simulator
        # ?order_id=123 (Simulate fetching another user's order)
        order_id = request.args.get('order_id')
        current_order = None
        if order_id:
             current_order = f"Order #{order_id}: 1x Neural Interface (Shipped to Neo Tokyo)"
        
        return render_template('profile.html', user=session['user'], order=current_order)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
             message = request.form.get('message')
             # Vulnerable to XSS
             return f"<h1>Message Sent!</h1><p>We received: {message}</p>"
        return render_template('contact.html')

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        return redirect(url_for('index'))

    return app
