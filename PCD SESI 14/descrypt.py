import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def is_one(matrix):
    """
    Fungsi untuk mengecek apakah determinan dari matrix adalah 1
    """
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    d = matrix[1][1]
    return (a * d) - (b * c) == 1

def encrypt(image, matrix):
    """
    Fungsi untuk mengenkripsi gambar menggunakan matriks transformasi 2x2
    """
    if not is_one(matrix):
        return "Determinan matrix harus 1"
    
    # Membuat array hasil dengan ukuran yang sama dengan gambar asli
    result = np.zeros_like(image)
    a, b = matrix[0]
    c, d = matrix[1]
    
    # Iterasi setiap piksel dalam gambar
    for i in range(0, image.shape[0] - 1, 2):  # Mengambil dua baris sekaligus
        for j in range(image.shape[1]):       # Iterasi setiap kolom
            # Operasi pada channel merah (R)
            r1 = ((image[i, j, 0] * a) + (image[i + 1, j, 0] * c)) % 256
            r2 = ((image[i, j, 0] * b) + (image[i + 1, j, 0] * d)) % 256

            # Operasi pada channel hijau (G)
            g1 = ((image[i, j, 1] * a) + (image[i + 1, j, 1] * c)) % 256
            g2 = ((image[i, j, 1] * b) + (image[i + 1, j, 1] * d)) % 256

            # Operasi pada channel biru (B)
            b1 = ((image[i, j, 2] * a) + (image[i + 1, j, 2] * c)) % 256
            b2 = ((image[i, j, 2] * b) + (image[i + 1, j, 2] * d)) % 256

            # Menyimpan hasil transformasi ke array hasil
            result[i, j, 0] = r1
            result[i, j, 1] = g1
            result[i, j, 2] = b1
            result[i + 1, j, 0] = r2
            result[i + 1, j, 1] = g2
            result[i + 1, j, 2] = b2
    
    return result

def decrypt(image, matrix):
    """
    Fungsi untuk mendekripsi gambar menggunakan invers dari matriks transformasi
    """
    if not is_one(matrix):
        return "Determinan matrix harus 1"
    
    # Menghitung invers matrix
    a, b = matrix[0]
    c, d = matrix[1]
    inverse_matrix = np.array([[d, -b], [-c, a]])
    
    # Gunakan invers matrix untuk dekripsi
    return encrypt(image, inverse_matrix)

# Path gambar input
filename = "C:/Users/komputer 4/Pictures/PCD SESI 14/rabit.webp"  # Ganti dengan nama file gambar Anda

# Membaca gambar menggunakan PIL dan mengkonversi ke numpy array
image = np.array(Image.open(filename))

# Definisi matriks transformasi
matrix = np.array([[1, 1], [1, 2]])  # Matriks dengan determinan 1

# Mengenkripsi gambar
encrypted_image = encrypt(image, matrix)

# Mendekripsi gambar
decrypted_image = decrypt(encrypted_image, matrix)

# Menampilkan gambar asli, terenkripsi, dan terdekripsi
if isinstance(encrypted_image, str):
    print(encrypted_image)
else:
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.title("Original Image")
    plt.imshow(image)
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title("Encrypted Image")
    plt.imshow(encrypted_image)
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title("Decrypted Image")
    plt.imshow(decrypted_image)
    plt.axis('off')

    plt.show()

    # Menyimpan hasil enkripsi dan dekripsi
    Image.fromarray(encrypted_image.astype(np.uint8)).save('encrypted_' + filename)
    Image.fromarray(decrypted_image.astype(np.uint8)).save('decrypted_' + filename)