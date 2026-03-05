/**
 * SmartSchool Liquid Core JS v2.0
 * รวมศูนย์ Logic: Dark Mode, Menu Management และ Scroll Logic
 */

const LiquidCore = {
    // --- 1. เริ่มต้นระบบ & Config ---
    init() {
        this.cacheElements();
        this.initTheme();
        this.bindEvents();
        this.initDarkMode();
        this.initEyeComfort();
        
    },

// ตัวแปรเก็บอ้างอิง HTML (ใส่ไว้ใน init หลักของโปรเจกต์คุณ)
initTheme() {
    this.html = document.documentElement;
    this.initDarkMode();
    this.initEyeComfort();
},

// --- 🌙 ระบบโหมดมืด (Dark Mode) ---
initDarkMode() {
    const isDark = localStorage.getItem('dark_theme') === 'dark';
    this.html.classList.toggle('dark', isDark);
    this.updateThemeIcons(isDark);
},

toggleGlobalDarkMode(event) {
    if (event) event.stopPropagation();

    this.html.classList.add('theme-transition');
    const isDark = this.html.classList.toggle('dark');
    localStorage.setItem('dark_theme', isDark ? 'dark' : 'light');
    
    this.updateThemeIcons(isDark);
    // อัปเดต Eye UI ด้วยเพื่อให้สี Address Bar สอดคล้องกัน
    this.updateEyeUI(this.html.classList.contains('eye-comfort'));

    setTimeout(() => this.html.classList.remove('theme-transition'), 700);
},

updateThemeIcons(isDark) {
    document.querySelectorAll('.theme-toggle-icon').forEach(icon => {
        icon.classList.toggle('fa-sun', isDark);
        icon.classList.toggle('fa-moon', !isDark);

        const parent = icon.closest('div') || icon.parentElement;
        if (parent) {
            parent.classList.toggle('bg-slate-800', isDark);
            parent.classList.toggle('text-yellow-400', isDark);
            parent.classList.toggle('text-slate-600', !isDark);
        }
    });
    
    this.updateMetaThemeColor();
},

// --- 👁️ ระบบถนอมสายตา (Eye Comfort) ---
initEyeComfort() {
    const isEyeComfort = localStorage.getItem('eye_comfort') === 'enabled';
    this.html.classList.toggle('eye-comfort', isEyeComfort);
    this.updateEyeUI(isEyeComfort); // เพิ่มบรรทัดนี้เพื่อให้ UI อัปเดตตั้งแต่โหลดหน้า
},

toggleGlobalEyeComfort(event) {
    if (event) event.stopPropagation();

    this.html.classList.add('theme-transition');
    const isEnabled = this.html.classList.toggle('eye-comfort');
    localStorage.setItem('eye_comfort', isEnabled ? 'enabled' : 'disabled');
    
    this.updateEyeUI(isEnabled); // ✅ แก้ไข: เรียกฟังก์ชันที่ถูกต้อง

    setTimeout(() => this.html.classList.remove('theme-transition'), 700);
},

updateEyeUI(isEnabled) {
    document.querySelectorAll('.eye-toggle-icon').forEach(icon => {
        icon.classList.toggle('fa-eye-slash', isEnabled);
        icon.classList.toggle('fa-eye', !isEnabled);

        const parent = icon.closest('div') || icon.parentElement;
        if (parent) {
            parent.classList.toggle('bg-amber-100', isEnabled);
            parent.classList.toggle('dark:bg-amber-900/30', isEnabled);
            icon.classList.toggle('text-amber-600', isEnabled);
            icon.classList.toggle('text-slate-500', !isEnabled);
        }
    });
    
    this.updateMetaThemeColor();
},

// --- 🛠 ฟังก์ชันเสริม: จัดการสีแถบสถานะมือถือ ---
updateMetaThemeColor() {
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) return;

    const isDark = this.html.classList.contains('dark');
    const isEye = this.html.classList.contains('eye-comfort');

    let color = '#F8FAFC'; // Default Light
    if (isDark) color = '#121417';
    else if (isEye) color = '#fdf6e3'; // Warm Light

    metaThemeColor.setAttribute('content', color);
},


cacheElements() {
        this.html = document.documentElement;
        this.body = document.body;
        // ใช้ Getter ภายในฟังก์ชันเพื่อรองรับกรณี Element โหลดช้าในบางหน้า
        this.getElems = () => ({
            backdrop: document.getElementById('global-backdrop'),
            sideMenu: document.getElementById('mobile-menu'),
            slideUpMenu: document.getElementById('slide-up-menu'),
            scrollBtn: document.getElementById("scrollToTopBtn"),
            actionIcon: document.getElementById('action-icon'),
            botBar: document.getElementById('main-botbar')
        });
        
        this.lastScrollTop = 0;
        this.scrollThreshold = 15;
    },

bindEvents() {
        // จัดการ Scroll
        window.addEventListener('scroll', () => this.handleScroll(), { passive: true });
        
        // จัดการ Backdrop
        document.addEventListener('click', (e) => {
            if (e.target.id === 'global-backdrop') this.closeAllMenus();
        });
    },




    // --- 3. ระบบจัดการเมนู (Menu Management) ---
toggleSlideUpMenu() {
    const { slideUpMenu, backdrop } = this.getElems();
    if (!slideUpMenu) {
        console.error("หา id 'slide-up-menu' ไม่เจอ");
        return;
    }

    const isActive = slideUpMenu.classList.toggle('active');

    if (isActive) {
        // 1. แสดง Backdrop
        backdrop?.classList.remove('hidden');
        // 2. ล็อคการเลื่อนหน้าจอ
        document.body.style.overflow = 'hidden';
        
        // 3. ใช้ Timeout เล็กน้อยเพื่อให้ CSS Transition ทำงาน
        setTimeout(() => {
            backdrop?.classList.add('active');
        }, 10);
    } else {
        this.closeAllMenus();
    }
},

// สมมติว่าอยู่ในอ็อบเจกต์ LiquidCore นะครับ
toggleSideMenu() {
    const menu = document.getElementById('mobile-menu');
    const overlay = document.getElementById('menu-overlay');
    const isClosed = menu.classList.contains('-translate-x-full');

    if (isClosed) {
        this.openMobileMenu(menu, overlay);
    } else {
        this.closeMobileMenu(menu, overlay);
    }
},

openMobileMenu(menu, overlay) {
    // แสดงเมนู
    menu.classList.remove('-translate-x-full');
    menu.classList.add('translate-x-0');
    
    // แสดง Overlay
    if (overlay) {
        overlay.classList.remove('hidden');
        // ใช้ setTimeout เพื่อให้เกิด animation fade-in (ถ้าเขียน CSS รองรับ)
        setTimeout(() => overlay.classList.add('opacity-100'), 10);
    }

    // ล็อคการเลื่อนหน้าจอ
    document.body.style.overflow = 'hidden';
},

closeMobileMenu(menu, overlay) {
    // ซ่อนเมนู
    menu.classList.add('-translate-x-full');
    menu.classList.remove('translate-x-0');

    // ซ่อน Overlay
    if (overlay) {
        overlay.classList.remove('opacity-100');
        setTimeout(() => overlay.classList.add('hidden'), 300); // รอให้ animation จบ
    }

    // คืนค่าการเลื่อนหน้าจอ
    document.body.style.overflow = '';
},

closeAllMenus() {
    const { sideMenu, slideUpMenu, backdrop, actionIcon } = this.getElems();

    // 1. ถอน Class 'active' ออกจากเมนูทุกตัวพร้อมกัน
    sideMenu?.classList.remove('active');
    slideUpMenu?.classList.remove('active');

    // 2. หมุนไอคอนกลับ (ถ้ามี)
    if (actionIcon) actionIcon.style.transform = 'rotate(0deg)';

    // 3. จัดการ Backdrop แบบนุ่มนวล
    if (backdrop) {
        backdrop.classList.remove('active');
        
        // รอให้ Animation ของตัวเมนู (0.3s) ทำงานเสร็จก่อน
        setTimeout(() => {
            // เช็คอีกครั้งว่าไม่มีเมนูไหนค้างอยู่จริงๆ
            const isAnyMenuActive = sideMenu?.classList.contains('active') || 
                                   slideUpMenu?.classList.contains('active');
            
            if (!isAnyMenuActive) {
                backdrop.classList.add('hidden');
                document.body.style.overflow = ''; // คืนค่าการ Scroll
            }
        }, 300);
    }
},
    // --- 4. ระบบ Scroll Logic (Top Button & Botbar) ---
    handleScroll() {
        const { scrollBtn, botBar, slideUpMenu, sideMenu } = this.getElems();
        let scrollTop = window.pageYOffset || this.html.scrollTop;

        // 4.1 ปุ่ม Scroll To Top
        if (scrollBtn) {
            if (scrollTop > 400) {
                scrollBtn.classList.remove("hidden");
                scrollBtn.classList.add("flex");
            } else {
                scrollBtn.classList.add("hidden");
                scrollBtn.classList.remove("flex");
            }
        }

        // 4.2 จัดการ Botbar (Mobile Only)
        if (window.innerWidth < 1024 && botBar) {
            if (Math.abs(this.lastScrollTop - scrollTop) > this.scrollThreshold) {
                if (scrollTop > this.lastScrollTop && scrollTop > 100) {
                    // เลื่อนลง -> ซ่อน
                    botBar.style.transform = 'translateY(180%)';
                    botBar.style.transition = 'transform 0.5s cubic-bezier(0.32, 0.72, 0, 1)';
                    
                    // ปิดเมนูอัตโนมัติเมื่อเริ่มอ่านเนื้อหา
                    if (slideUpMenu?.classList.contains('active') || sideMenu?.classList.contains('active')) {
                        this.closeAllMenus();
                    }
                } else {
                    // เลื่อนขึ้น -> แสดง
                    botBar.style.transform = 'translateY(0)';
                }
            }
        }
        this.lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    },

    scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    toggleInfoPanel() {
        const panel = document.getElementById('info-expansion-panel');
        const icon = document.getElementById('info-btn-icon');
        const text = document.getElementById('info-btn-text');

        if (panel.style.maxHeight === '0px' || panel.style.maxHeight === '') {
            panel.style.maxHeight = '500px'; // ปรับตามความสูงจริง
            icon.classList.add('rotate-180');
            text.innerText = 'ซ่อนข้อมูล';
            panel.classList.add('py-4');
        } else {
            panel.style.maxHeight = '0px';
            icon.classList.remove('rotate-180');
            text.innerText = 'แสดงข้อมูลวันนี้';
            panel.classList.remove('py-4');
        }
    },
    getLocation() {
        const btn = document.getElementById('get-loc-btn');
        if (navigator.geolocation) {
            if(btn) btn.innerHTML = '<i class="fa-solid fa-spinner animate-spin mr-2"></i> กำลังระบุพิกัด...';
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    window.location.href = `?lat=${lat}&lng=${lng}`;
                },
                (error) => {
                    if(btn) btn.innerHTML = '<i class="fa-solid fa-location-crosshairs mr-2"></i> อัปเดตพิกัด';
                    alert("ไม่สามารถเข้าถึงตำแหน่งได้: " + error.message);
                }
            );
        } else {
            alert("Browser ของคุณไม่รองรับการระบุตำแหน่ง");
        }
    },

    autoUpdateLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    
                    // ส่งค่าพิกัดไปที่ URL เพื่อให้ Django คำนวณใหม่
                    // ใช้ window.location.replace เพื่อไม่ให้ user กด Back กลับมาหน้าเดิมที่ไม่มีพิกัด
                    const newUrl = window.location.pathname + `?lat=${lat}&lng=${lng}`;
                    window.location.replace(newUrl);
                },
                function(error) {
                    console.error("Error getting location:", error);
                    // หากผู้ใช้ปฏิเสธพิกัด หรือ Error ให้ใช้ค่า Default (ไม่ต้องทำอะไรต่อ)
                },
                { enableHighAccuracy: true, timeout: 5000 }
            );
        }
    },

    highlightNextPrayer() {
    const now = new Date();
    // ดึงเวลาปัจจุบันเป็นนาที (เช่น 11:30 = 690 นาที)
    const currentTime = (now.getHours() * 60) + now.getMinutes();
    console.log("Current Time (min):", currentTime); // เช็คเวลาเครื่อง

    const slots = document.querySelectorAll('.prayer-slot');
    let nextFound = false;

    // 1. ล้างไฮไลต์เก่า
    slots.forEach(slot => {
        slot.classList.remove('bg-emerald-50', 'ring-1', 'ring-emerald-200', 'shadow-inner');
        const p = slot.querySelector('p:last-child');
        if (p) p.classList.remove('animate-pulse');
    });

    // 2. วนลูปหาเวลาถัดไป
    for (let slot of slots) {
        const timeEl = slot.querySelector('[data-time]');
        if (!timeEl) continue;

        const timeStr = timeEl.getAttribute('data-time').trim();
        // แปลง "HH:MM" เป็นนาที
        const [h, m] = timeStr.split(':').map(Number);
        const prayerMinutes = (h * 60) + m;

        console.log(`Checking ${timeStr}: ${prayerMinutes} mins`);

        if (prayerMinutes > currentTime) {
            console.log("👉 Next Prayer Found:", timeStr);
            // ✅ ใส่ Class ไฮไลต์
            slot.classList.add('bg-emerald-50', 'ring-1', 'ring-emerald-200', 'shadow-inner');
            timeEl.classList.add('animate-pulse');
            nextFound = true;
            break; 
        }
    }

    // 3. ถ้าเลยอิชาอ์ไปแล้ว ให้ไปไฮไลต์ซุบฮิ (ของวันพรุ่งนี้)
    if (!nextFound) {
        const fajr = document.getElementById('p-fajr');
        if (fajr) {
            fajr.classList.add('bg-emerald-50', 'ring-1', 'ring-emerald-200');
            fajr.querySelector('[data-time]').classList.add('animate-pulse');
        }
    }
},

    
};

document.addEventListener('DOMContentLoaded', function() {
    // 1. เริ่มต้นระบบพื้นฐาน (LiquidCore)
    if (typeof LiquidCore !== 'undefined') {
        LiquidCore.init();
    }

    // 2. เลื่อนหน้าจอไปที่แถว "วันนี้" ในตารางปฏิทิน (ถ้ามี)
    const todayRow = document.querySelector('.bg-islam-green\\/10');
    if (todayRow) {
        // หน่วงเวลาเล็กน้อยเพื่อให้ Layout นิ่งก่อนเลื่อน
        setTimeout(() => {
            todayRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 300);
    }

    // 3. ตรวจสอบและอัปเดตพิกัดอัตโนมัติ (เฉพาะเมื่อยังไม่มีค่าใน URL)
    const urlParams = new URLSearchParams(window.location.search);
    if (!urlParams.has('lat') || !urlParams.has('lng')) {
        autoUpdateLocation();
    }
});

// รันทันทีเมื่อโหลดหน้า และเช็คทุกๆ 1 นาที
// รันระบบ
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(highlightNextPrayer, 500); // หน่วง 0.5 วินาทีเพื่อให้ HTML Render เสร็จชัวร์ๆ
    setInterval(highlightNextPrayer, 60000);
});


