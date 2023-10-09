import torch
import torch.nn.functional as F
from torchvision import utils as vutils
import uuid

import os
from tqdm import tqdm

from components.models import Generator

def generate_images(output_folder, checkpoint_path, num_images, batch_size=8, image_size=256, noise_dim=256, gpu_index=0):
    device = torch.device(f'cuda:{gpu_index}' if torch.cuda.is_available() else 'cpu')
    
    # Crear el generador y cargar los pesos del checkpoint
    net_ig = Generator(ngf=64, nz=noise_dim, nc=3, im_size=image_size).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=lambda a, b: a)
    net_ig.load_state_dict(checkpoint['g'])
    net_ig.to(device)
    
    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    with torch.no_grad():
        for i in tqdm(range(num_images)):
            unique_id = str(uuid.uuid4())

            # Generar ruido aleatorio
            noise = torch.FloatTensor(1, noise_dim).normal_(0, 1).to(device)  # Cambio aquí
            g_imgs = net_ig(noise)[0]
            g_imgs = F.interpolate(g_imgs, image_size)
            
            for j, g_img in enumerate(g_imgs):
                # Crear el nombre de archivo con la ID única
                filename = f'image_{unique_id}_{i * batch_size + j}.jpg'
                filepath = os.path.join(output_folder, filename)
                
                vutils.save_image(
                    g_img.add(1).mul(0.5), 
                    filepath
                )