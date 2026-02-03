from flask import Flask, render_template, request, jsonify, session, make_response
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Tax rate (19% IVA - typical in Chile)
TAX_RATE = 0.19

# Catálogo de productos (10 productos: 5 relojes de lujo y 5 joyas)
products = [
    {
        'id': 1,
        'name': 'Rolex Submariner',
        'category': 'watch',
        'price': 12500.00,
        'description': 'Reloj de buceo icónico con bisel giratorio unidireccional y resistencia al agua de 300 metros.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Rolex+Submariner'
    },
    {
        'id': 2,
        'name': 'Patek Philippe Nautilus',
        'category': 'watch',
        'price': 35000.00,
        'description': 'Reloj deportivo elegante con caja de acero inoxidable y diseño portilla distintivo.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Patek+Philippe'
    },
    {
        'id': 3,
        'name': 'Audemars Piguet Royal Oak',
        'category': 'watch',
        'price': 28000.00,
        'description': 'Reloj de lujo con diseño octogonal característico y acabado "Tapisserie".',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=AP+Royal+Oak'
    },
    {
        'id': 4,
        'name': 'Omega Speedmaster',
        'category': 'watch',
        'price': 6500.00,
        'description': 'El legendario reloj lunar, el único certificado por la NASA para vuelos espaciales.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Omega+Speedmaster'
    },
    {
        'id': 5,
        'name': 'Cartier Santos',
        'category': 'watch',
        'price': 7200.00,
        'description': 'Reloj aviador clásico con tornillos visibles en el bisel y correa de cuero.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Cartier+Santos'
    },
    {
        'id': 6,
        'name': 'Collar de Diamantes',
        'category': 'jewelry',
        'price': 15000.00,
        'description': 'Elegante collar de diamantes de 18 quilates con piedras de corte brillante.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Diamond+Necklace'
    },
    {
        'id': 7,
        'name': 'Anillo de Compromiso',
        'category': 'jewelry',
        'price': 8500.00,
        'description': 'Anillo de compromiso con diamante central de 2 quilates y banda de oro blanco.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Engagement+Ring'
    },
    {
        'id': 8,
        'name': 'Brazalete de Oro',
        'category': 'jewelry',
        'price': 4200.00,
        'description': 'Brazalete de oro amarillo de 18k con diseño entrelazado y cierre de seguridad.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Gold+Bracelet'
    },
    {
        'id': 9,
        'name': 'Pendientes de Esmeralda',
        'category': 'jewelry',
        'price': 9800.00,
        'description': 'Pendientes de esmeralda colombiana con diamantes circundantes en oro blanco.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Emerald+Earrings'
    },
    {
        'id': 10,
        'name': 'Broche de Zafiro',
        'category': 'jewelry',
        'price': 6700.00,
        'description': 'Broche de zafiro azul con diseño de flor y detalles de diamantes.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Sapphire+Brooch'
    }
]

@app.route('/')
def index():
    """Página principal con catálogo completo"""
    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '').lower()
    
    # Filtrar productos
    filtered_products = products
    
    if category != 'all':
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    if search_query:
        filtered_products = [p for p in filtered_products 
                           if search_query in p['name'].lower() or 
                           search_query in p['description'].lower()]
    
    return render_template('index.html', 
                         products=filtered_products, 
                         current_category=category,
                         search_query=search_query if search_query else '')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Página de detalle del producto"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return "Producto no encontrado", 404

@app.route('/api/search')
def api_search():
    """API endpoint para búsqueda dinámica"""
    query = request.args.get('q', '').lower()
    category = request.args.get('category', 'all')
    
    filtered = products
    if category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
    
    if query:
        filtered = [p for p in filtered 
                   if query in p['name'].lower() or query in p['description'].lower()]
    
    return jsonify(filtered)

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get current cart contents"""
    cart = session.get('cart', {})
    cart_items = []
    subtotal = 0
    
    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            subtotal += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
    
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    
    return jsonify({
        'items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'tax_rate': TAX_RATE,
        'total': total
    })

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = data.get('quantity', 1)
    
    # Validate product exists
    product = next((p for p in products if p['id'] == int(product_id)), None)
    if not product:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    # Initialize cart if needed
    if 'cart' not in session:
        session['cart'] = {}
    
    # Add or update quantity
    cart = session['cart']
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({'success': True, 'message': 'Producto agregado al carrito'})

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    """Update cart item quantity"""
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = data.get('quantity', 0)
    
    if 'cart' not in session:
        return jsonify({'error': 'Carrito vacío'}), 400
    
    cart = session['cart']
    
    if quantity <= 0:
        # Remove item if quantity is 0 or negative
        if product_id in cart:
            del cart[product_id]
    else:
        cart[product_id] = quantity
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({'success': True})

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.get_json()
    product_id = str(data.get('product_id'))
    
    if 'cart' in session and product_id in session['cart']:
        cart = session['cart']
        del cart[product_id]
        session['cart'] = cart
        session.modified = True
        return jsonify({'success': True})
    
    return jsonify({'error': 'Item no encontrado en el carrito'}), 404

@app.route('/cart')
def view_cart():
    """View cart page"""
    return render_template('cart.html')

@app.route('/api/invoice/generate', methods=['POST'])
def generate_invoice():
    """Generate PDF invoice for current cart"""
    cart = session.get('cart', {})
    
    if not cart:
        return jsonify({'error': 'El carrito está vacío'}), 400
    
    # Prepare cart data
    cart_items = []
    subtotal = 0
    
    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            subtotal += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
    
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    
    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#FFD700'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    # Header
    elements.append(Paragraph("Relojes de Lujo, Santiago de Chile", title_style))
    elements.append(Paragraph("FACTURA DE COMPRA", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Invoice info
    invoice_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    invoice_number = datetime.now().strftime("%Y%m%d%H%M%S")
    
    info_data = [
        ['Número de Factura:', invoice_number],
        ['Fecha:', invoice_date],
        ['', '']
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Products table
    table_data = [['Producto', 'Precio Unit.', 'Cantidad', 'Subtotal']]
    
    for item in cart_items:
        table_data.append([
            item['product']['name'],
            f"${item['product']['price']:,.2f}",
            str(item['quantity']),
            f"${item['item_total']:,.2f}"
        ])
    
    # Add totals
    table_data.append(['', '', '', ''])
    table_data.append(['', '', 'Subtotal:', f"${subtotal:,.2f}"])
    table_data.append(['', '', f'Impuesto ({int(TAX_RATE*100)}%):', f"${tax:,.2f}"])
    table_data.append(['', '', 'TOTAL:', f"${total:,.2f}"])
    
    products_table = Table(table_data, colWidths=[3*inch, 1.5*inch, 1*inch, 1.5*inch])
    products_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -5), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -5), 1, colors.grey),
        
        # Totals section
        ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (2, -1), (-1, -1), 12),
        ('TEXTCOLOR', (2, -1), (-1, -1), colors.HexColor('#FFD700')),
        ('LINEABOVE', (2, -3), (-1, -3), 2, colors.black),
    ]))
    elements.append(products_table)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Gracias por su compra", footer_style))
    elements.append(Paragraph("Calidad excepcional • Diseño exclusivo • Elegancia atemporal", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Prepare response
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=factura_{invoice_number}.pdf'
    
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
