import sys
import time
import hashlib
import hmac
import struct
import os
import base64
import math
import subprocess
import tempfile
import textwrap
import random

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    if os.name == 'nt': os.system('color')

class FileManager:
    @staticmethod
    def smart_save(data):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') if os.name == 'nt' else '.'
        base = os.path.join(desktop, "cqve_cikis")
        ext = ".txt"
        filename = f"{base}{ext}"
        cnt = 1
        while os.path.exists(filename):
            filename = f"{base}_{cnt}{ext}"
            cnt += 1
        try:
            with open(filename, "w", encoding="utf-8") as f: f.write(data)
            return True, filename
        except Exception as e: return False, str(e)

class Clipboard:
    @staticmethod
    def copy(text):
        if not text: return False, "Boş veri."
        try:
            if os.name == 'nt':
                fd, path = tempfile.mkstemp()
                with os.fdopen(fd, 'w', encoding='utf-8') as tmp: tmp.write(str(text))
                subprocess.run(f"powershell -NoProfile -Command \"Get-Content -LiteralPath '{path}' -Raw -Encoding UTF8 | Set-Clipboard\"", shell=True, check=True)
                os.remove(path)
                return True, "Kopyalandı"
            elif sys.platform == 'darwin':
                p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                p.communicate(input=str(text).encode('utf-8'))
                return True, "Kopyalandı"
            else:
                try:
                    p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                    p.communicate(input=str(text).encode('utf-8'))
                except:
                    p = subprocess.Popen(['xsel', '-b'], stdin=subprocess.PIPE)
                    p.communicate(input=str(text).encode('utf-8'))
                return True, "Kopyalandı"
        except Exception as e: return False, f"Hata: {e}"

    @staticmethod
    def paste():
        try:
            if os.name == 'nt':
                return True, subprocess.check_output("powershell -NoProfile -Command Get-Clipboard", shell=True).decode('utf-8').strip()
            elif sys.platform == 'darwin':
                return True, subprocess.check_output('pbpaste').decode('utf-8')
            else:
                try:
                    return True, subprocess.check_output(['xclip', '-o', '-selection', 'clipboard']).decode('utf-8')
                except:
                    return True, subprocess.check_output(['xsel', '-b', '-o']).decode('utf-8')
        except: return False, "Okuma Hatası."

class CQVECore:
    def __init__(self):
        self.magic = b'CQVE3'
        self.phi = (1 + math.sqrt(5)) / 2

    def _derive_keys(self, password, salt, timestamp):
        raw = password.encode() + salt + struct.pack(">Q", timestamp)
        return hashlib.shake_256(hashlib.sha3_512(raw).digest()).digest(256)

    def _generate_lattice_noise(self, key_material, length):
        noise = []
        for i in range(length):
            k = key_material[i % len(key_material)]
            val = (k * 1664525 + 1013904223) % 256
            noise.append(val)
        return bytes(noise)

    def _lattice_transform(self, data, key_material, mode='encrypt'):
        noise = self._generate_lattice_noise(key_material, len(data))
        result = bytearray(len(data))
        for i in range(len(data)):
            term = (noise[i] * 7) % 256
            if mode == 'encrypt':
                result[i] = (data[i] + term) % 256
            else:
                result[i] = (data[i] - term) % 256
        return result

    def _fluid_diffusion(self, data, key_material, mode='encrypt'):
        indices = list(range(len(data)))
        seed = int.from_bytes(key_material[:8], 'big')
        rng = random.Random(seed)
        rng.shuffle(indices)
        result = bytearray(len(data))
        if mode == 'encrypt':
            for i, new_pos in enumerate(indices):
                result[new_pos] = data[i]
        else:
            for i, original_pos in enumerate(indices):
                result[i] = data[original_pos]
        return result

    def _feistel_function(self, R, sub_key):
        temp = (R + sub_key) & 0xFFFFFFFF
        rotated = ((temp << 5) | (temp >> 27)) & 0xFFFFFFFF
        result = (rotated * 2654435761) & 0xFFFFFFFF
        return result

    def process(self, input_data, password, mode='encrypt'):
        try:
            if mode == 'encrypt':
                if not input_data: return False, "Boş veri şifrelenemez."
                salt = os.urandom(32)
                timestamp = int(time.time() * 1000)
                pad_len = 8 - (len(input_data) % 8)
                input_data += chr(pad_len) * pad_len
                data_bytes = bytearray(input_data.encode('utf-8'))
            else:
                input_data = str(input_data).strip()
                if len(input_data) < 20:
                    return False, "Geçersiz Veri: Girdiğiniz kod çok kısa."
                
                missing_padding = len(input_data) % 4
                if missing_padding:
                    input_data += '=' * (4 - missing_padding)
                
                try:
                    raw_pkg = base64.urlsafe_b64decode(input_data)
                except: return False, "Format Hatası: Veri doğru bir CQVE kodu değil."
                
                if not raw_pkg.startswith(self.magic):
                    return False, "İmza Hatası: Bu kod CQVE v3.0 formatında değil."
                
                if len(raw_pkg) < 110:
                     return False, "Veri Paketi Eksik: Kodun tamamını kopyaladığınızdan emin olun."

                try:
                    timestamp = struct.unpack(">Q", raw_pkg[5:13])[0]
                    salt = raw_pkg[13:45]
                    signature = raw_pkg[45:109]
                    data_bytes = bytearray(raw_pkg[109:])
                except: return False, "Paket Ayrıştırma Hatası."

            key_mat = self._derive_keys(password, salt, timestamp)
            
            if mode == 'decrypt':
                calc_sig = hmac.new(key_mat, data_bytes, hashlib.sha3_512).digest()
                if not hmac.compare_digest(signature, calc_sig):
                    return False, "GÜVENLİK UYARISI: Şifre yanlış veya veri değiştirilmiş!"
                
                data_bytes = self._fluid_diffusion(data_bytes, key_mat, 'decrypt')
                data_bytes = self._lattice_transform(data_bytes, key_mat, 'decrypt')

            processed = bytearray()
            for i in range(0, len(data_bytes), 8):
                block = data_bytes[i:i+8]
                L = int.from_bytes(block[:4], 'big')
                R = int.from_bytes(block[4:], 'big')
                
                rounds = 64
                for r in range(rounds):
                    r_idx = r if mode == 'encrypt' else (rounds - 1 - r)
                    k_start = (r_idx * 4) % 200
                    sub_key = int.from_bytes(key_mat[k_start:k_start+4], 'big')
                    
                    if mode == 'encrypt':
                        F = self._feistel_function(R, sub_key)
                        new_R = L ^ F
                        L = R; R = new_R
                    else:
                        F = self._feistel_function(L, sub_key)
                        new_L = R ^ F
                        R = L; L = new_L

                block_res = L.to_bytes(4, 'big') + R.to_bytes(4, 'big')
                processed.extend(block_res)

            if mode == 'encrypt':
                processed = self._lattice_transform(processed, key_mat, 'encrypt')
                processed = self._fluid_diffusion(processed, key_mat, 'encrypt')
                
                sig = hmac.new(key_mat, processed, hashlib.sha3_512).digest()
                final_pkg = self.magic + struct.pack(">Q", timestamp) + salt + sig + processed
                return True, base64.urlsafe_b64encode(final_pkg).decode('utf-8')
            else:
                try:
                    pad_len = processed[-1]
                    if pad_len > 8 or pad_len < 1: return False, "Veri Bütünlüğü Bozuk (Padding)."
                    return True, processed[:-pad_len].decode('utf-8')
                except: return False, "Çözümleme Hatası (UTF-8)."

        except Exception as e: return False, f"Çekirdek Hatası: {str(e)}"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_effect(text, speed=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def banner():
    print(f"""{Colors.PURPLE}
      ██████╗  ██████╗ ██╗   ██╗███████╗
     ██╔════╝ ██╔═══██╗██║   ██║██╔════╝
     ██║      ██║   ██║██║   ██║█████╗  
     ██║      ██║▄▄ ██║╚██╗ ██╔╝██╔══╝  
     ╚██████╗ ╚██████╔╝ ╚████╔╝ ███████╗
      ╚═════╝  ╚══▀▀═╝   ╚═══╝  ╚══════╝{Colors.RESET}
    {Colors.BOLD}>> CodexCore Security | CQVE Protocol v3.0{Colors.RESET}
    {Colors.CYAN}>> CodexCore Quantum Vortex Engine{Colors.RESET}
    """)

def intro_animation():
    clear_screen()
    banner()
    type_effect(f"{Colors.GREEN}[+] Sistem Aktif.{Colors.RESET}", 0.015)
    time.sleep(0.5)

def get_input_pro(label, is_password=False):
    print(f"\n{Colors.CYAN}{label}{Colors.RESET}")
    print(f"{Colors.YELLOW}(Panodan yapıştırmak için 'v' + Enter){Colors.RESET}")
    
    user_in = input(f"{Colors.GREEN}Giriş Yapınız >> {Colors.RESET}").strip()
    
    if user_in.lower() == 'v':
        ok, txt = Clipboard.paste()
        if ok:
            if is_password:
                print(f"{Colors.PURPLE}   [+] Anahtar Alındı (Uzunluk: {len(txt)}){Colors.RESET}")
                print(f"{Colors.CYAN}   >> ****** (Gizli){Colors.RESET}")
            else:
                print(f"{Colors.PURPLE}   [+] Veri Alındı (Uzunluk: {len(txt)}):{Colors.RESET}")
                print(f"{Colors.CYAN}   >> {txt}{Colors.RESET}")
            return txt
        else:
            print(f"{Colors.RED}   [!] Pano Boş.{Colors.RESET}")
            return input(f"{Colors.GREEN}Manuel Giriniz >> {Colors.RESET}").strip()
    return user_in

def show_result_pro(data, title):
    width = 60
    print(f"\n{Colors.GREEN}" + "="*width)
    print(f" {title} ".center(width, "="))
    print("="*width + f"{Colors.RESET}")
    
    clean_data = str(data).strip()
    if len(clean_data) < 40:
        print(f"\n{Colors.PURPLE}{clean_data.center(width)}{Colors.RESET}\n")
    else:
        wrapped = textwrap.fill(clean_data, width=width)
        print(f"\n{Colors.PURPLE}{wrapped}{Colors.RESET}\n")
    
    print(f"{Colors.GREEN}" + "="*width + f"{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[1] Kopyala  [2] Kaydet  [Enter] Menü{Colors.RESET}")
    choice = input(f"{Colors.GREEN}>> {Colors.RESET}").strip()
    
    if choice == '1':
        ok, msg = Clipboard.copy(clean_data)
        if ok: print(f"{Colors.GREEN}[✓] Kopyalandı.{Colors.RESET}")
        else: print(f"{Colors.RED}[X] {msg}{Colors.RESET}")
        time.sleep(1)
    elif choice == '2':
        ok, path = FileManager.smart_save(clean_data)
        if ok: print(f"{Colors.GREEN}[✓] Kaydedildi: {path}{Colors.RESET}")
        else: print(f"{Colors.RED}[X] Hata: {path}{Colors.RESET}")
        time.sleep(2)

def main():
    engine = CQVECore()
    intro_animation()
    
    while True:
        try:
            clear_screen()
            banner()
            print(f"\n{Colors.BOLD}--- MENÜ ---{Colors.RESET}")
            print(f"{Colors.CYAN}[1]{Colors.RESET} Şifrele")
            print(f"{Colors.CYAN}[2]{Colors.RESET} Çöz")
            print(f"{Colors.CYAN}[3]{Colors.RESET} Çıkış")
            
            try:
                secim = input(f"\n{Colors.GREEN}root@cqve:~$ {Colors.RESET}").strip()
            except: break
            
            if secim == '1':
                clear_screen(); banner()
                print(f"\n{Colors.BOLD}>> MOD: ŞİFRELEME{Colors.RESET}")
                
                txt = get_input_pro("Metin:")
                if not txt: continue
                pwd = get_input_pro("Anahtar:", True)
                if not pwd: continue
                
                ok, res = engine.process(txt, pwd, 'encrypt')
                if ok: show_result_pro(res, "SONUÇ")
                else: 
                    print(f"\n{Colors.RED}[!] {res}{Colors.RESET}")
                    input("\nDevam etmek için Enter...")
                    
            elif secim == '2':
                clear_screen(); banner()
                print(f"\n{Colors.BOLD}>> MOD: ÇÖZÜMLEME{Colors.RESET}")
                
                token = get_input_pro("Kod:")
                if not token: continue
                pwd = get_input_pro("Anahtar:", True)
                if not pwd: continue
                
                ok, res = engine.process(token, pwd, 'decrypt')
                if ok: show_result_pro(res, "ORİJİNAL VERİ")
                else:
                    print(f"\n{Colors.RED}[!] {res}{Colors.RESET}")
                    input("\nDevam etmek için Enter...")
                    
            elif secim == '3':
                print(f"\n{Colors.PURPLE}Çıkış...{Colors.RESET}")
                break
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[!] İptal.{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}[!] Hata: {e}{Colors.RESET}")
            input("\nDevam etmek için Enter...")

if __name__ == "__main__":
    main()