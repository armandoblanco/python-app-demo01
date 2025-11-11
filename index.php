<?php
// Include products data
require_once 'products.php';

// Get filter parameters
$category = isset($_GET['category']) ? $_GET['category'] : 'all';
$search_query = isset($_GET['search']) ? strtolower($_GET['search']) : '';

// Filter products
$filtered_products = $products;

if ($category !== 'all') {
    $filtered_products = array_filter($filtered_products, function($p) use ($category) {
        return $p['category'] === $category;
    });
}

if ($search_query !== '') {
    $filtered_products = array_filter($filtered_products, function($p) use ($search_query) {
        return strpos(strtolower($p['name']), $search_query) !== false ||
               strpos(strtolower($p['description']), $search_query) !== false;
    });
}

// Reset array keys
$filtered_products = array_values($filtered_products);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luxury Timepieces & Jewelry - E-commerce</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            color: #ffffff;
            min-height: 100vh;
        }

        /* Header */
        header {
            background: linear-gradient(90deg, #000000 0%, #1a1a1a 100%);
            padding: 30px 0;
            border-bottom: 2px solid #FFD700;
            box-shadow: 0 4px 6px rgba(255, 215, 0, 0.1);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        h1 {
            color: #FFD700;
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            letter-spacing: 2px;
        }

        .subtitle {
            text-align: center;
            color: #ffffff;
            font-size: 1.2em;
            font-style: italic;
            margin-bottom: 30px;
        }

        /* Search and Filter Section */
        .search-filter-section {
            background: rgba(26, 26, 26, 0.9);
            padding: 30px;
            border-radius: 10px;
            margin: 30px auto;
            max-width: 1000px;
            border: 1px solid #FFD700;
        }

        .search-container {
            margin-bottom: 20px;
        }

        .search-box {
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border: 2px solid #FFD700;
            border-radius: 5px;
            background: #000000;
            color: #ffffff;
            transition: all 0.3s;
        }

        .search-box:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
            border-color: #FFD700;
        }

        .filter-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 12px 30px;
            font-size: 1em;
            border: 2px solid #FFD700;
            background: #000000;
            color: #ffffff;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s;
            font-weight: bold;
        }

        .filter-btn:hover {
            background: #FFD700;
            color: #000000;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
        }

        .filter-btn.active {
            background: #FFD700;
            color: #000000;
        }

        /* Products Grid */
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 30px;
            padding: 30px 0;
        }

        .product-card {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            border: 2px solid #FFD700;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }

        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3);
            border-color: #ffffff;
        }

        .product-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-radius: 5px;
            margin-bottom: 15px;
            background: #000000;
        }

        .product-category {
            display: inline-block;
            padding: 5px 15px;
            background: #FFD700;
            color: #000000;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .product-name {
            font-size: 1.4em;
            color: #FFD700;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .product-description {
            color: #cccccc;
            margin-bottom: 15px;
            line-height: 1.6;
            font-size: 0.95em;
        }

        .product-price {
            font-size: 1.8em;
            color: #ffffff;
            font-weight: bold;
        }

        .price-label {
            font-size: 0.6em;
            color: #FFD700;
        }

        /* No Results Message */
        .no-results {
            text-align: center;
            padding: 60px 20px;
            color: #FFD700;
            font-size: 1.5em;
        }

        /* Footer */
        footer {
            background: #000000;
            color: #FFD700;
            text-align: center;
            padding: 30px 0;
            margin-top: 50px;
            border-top: 2px solid #FFD700;
        }

        footer p {
            margin: 5px 0;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }

            .products-grid {
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
            }

            .filter-buttons {
                flex-direction: column;
            }

            .filter-btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>✨ LUXURY COLLECTION ✨</h1>
            <p class="subtitle">Timepieces & Jewelry of Distinction</p>
        </div>
    </header>

    <main class="container">
        <div class="search-filter-section">
            <div class="search-container">
                <input type="text" 
                       id="searchBox" 
                       class="search-box" 
                       placeholder="🔍 Buscar relojes y joyas de lujo..." 
                       value="<?php echo htmlspecialchars($search_query); ?>">
            </div>
            <div class="filter-buttons">
                <button class="filter-btn <?php echo $category === 'all' ? 'active' : ''; ?>" 
                        onclick="filterCategory('all')">
                    Todos los Productos
                </button>
                <button class="filter-btn <?php echo $category === 'watch' ? 'active' : ''; ?>" 
                        onclick="filterCategory('watch')">
                    Relojes de Lujo
                </button>
                <button class="filter-btn <?php echo $category === 'jewelry' ? 'active' : ''; ?>" 
                        onclick="filterCategory('jewelry')">
                    Joyas Exclusivas
                </button>
            </div>
        </div>

        <div class="products-grid" id="productsGrid">
            <?php if (count($filtered_products) > 0): ?>
                <?php foreach ($filtered_products as $product): ?>
                <a href="product_detail.php?id=<?php echo $product['id']; ?>" class="product-card">
                    <img src="<?php echo htmlspecialchars($product['image']); ?>" 
                         alt="<?php echo htmlspecialchars($product['name']); ?>" 
                         class="product-image">
                    <span class="product-category">
                        <?php echo $product['category'] === 'watch' ? '⌚ Reloj' : '💎 Joya'; ?>
                    </span>
                    <h3 class="product-name"><?php echo htmlspecialchars($product['name']); ?></h3>
                    <p class="product-description"><?php echo htmlspecialchars($product['description']); ?></p>
                    <p class="product-price">
                        <span class="price-label">USD</span> $<?php echo number_format($product['price'], 2); ?>
                    </p>
                </a>
                <?php endforeach; ?>
            <?php else: ?>
                <div class="no-results">
                    <p>No se encontraron productos que coincidan con tu búsqueda.</p>
                    <p style="font-size: 0.8em; margin-top: 20px; color: #ffffff;">
                        Intenta con otros términos o explora todas las categorías.
                    </p>
                </div>
            <?php endif; ?>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2025 Luxury Collection - Timepieces & Jewelry</p>
            <p>Calidad excepcional • Diseño exclusivo • Elegancia atemporal</p>
        </div>
    </footer>

    <script>
        // Búsqueda dinámica
        const searchBox = document.getElementById('searchBox');
        let searchTimeout;

        searchBox.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const query = searchBox.value;
                const urlParams = new URLSearchParams(window.location.search);
                const category = urlParams.get('category') || 'all';
                
                if (query === '' && category === 'all') {
                    window.location.href = 'index.php';
                } else {
                    const params = new URLSearchParams();
                    if (category !== 'all') params.append('category', category);
                    if (query) params.append('search', query);
                    window.location.href = 'index.php?' + params.toString();
                }
            }, 500);
        });

        // Filtrado por categoría
        function filterCategory(category) {
            const searchQuery = document.getElementById('searchBox').value;
            const params = new URLSearchParams();
            
            if (category !== 'all') {
                params.append('category', category);
            }
            if (searchQuery) {
                params.append('search', searchQuery);
            }
            
            window.location.href = 'index.php?' + params.toString();
        }

        // Efecto de scroll suave
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
</body>
</html>
