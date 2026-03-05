def menu_context(request):
    return {
        'menu_items': [
            {'name': 'หน้าแรก', 'url_name': 'home', 'icon': 'fa-house', 'is_cms': True},
            {'name': 'หลักสูตร', 'url_name': 'curriculum', 'icon': 'fa-book-open', 'is_cms': True},
            {'name': 'เกี่ยวกับเรา', 'url_name': 'about', 'icon': 'fa-circle-info', 'is_cms': True},
            {'name': 'พิพิธภัณฑ์', 'url_name': 'museum', 'icon': 'fa-monument', 'is_cms': True},
            {'name': 'บทเรียนออนไลน์', 'url_name': 'learning', 'icon': 'fa-graduation-cap', 'is_cms': True},
            {'name': 'เกมการเรียนรู้', 'url_name': 'games', 'icon': 'fa-gamepad', 'is_cms': True},
            {'name': 'ติดต่อเรา', 'url_name': 'contact', 'icon': 'fa-paper-plane', 'is_cms': True},
        ]
    }