#!/usr/bin/env python3
import struct
import sys

def extract_dtb(boot_img_path, output_path):
    with open(boot_img_path, 'rb') as f:
        data = f.read()
    
    # Verifica a magic "ANDROID!"
    if data[:8] != b'ANDROID!':
        print("Erro: Magic ANDROID! não encontrada.")
        sys.exit(1)
    
    # Procura pela assinatura FDT (d00dfeed)
    dtb_start = 0
    for i in range(2048, len(data), 4):
        if data[i:i+4] == b'\xd0\x0d\xfe\xed':
            dtb_start = i
            break
    
    if dtb_start == 0:
        print("DTB não encontrado.")
        sys.exit(1)
    
    # Tamanho do DTB está no offset 4
    dtb_size = struct.unpack('>I', data[dtb_start+4:dtb_start+8])[0]
    
    with open(output_path, 'wb') as f:
        f.write(data[dtb_start:dtb_start+dtb_size])
    
    print(f"DTB extraído com sucesso para {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: extract_dtb.py <boot.img> [output_dtb.img]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "dtb.img"
    
    extract_dtb(input_file, output_file)
