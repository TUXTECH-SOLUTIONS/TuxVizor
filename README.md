# 🖥️ TuxVizor v0.2-stable

> **Part of the TuxTech Solutions Ecosystem**  
> *A Modern GTK4 Hypervisor Interface for QEMU/KVM*

![Arch Linux](img.shields.io)
![License](img.shields.io)
![Technology](img.shields.io)

TuxVizor — это мощный и легкий графический интерфейс для управления виртуальными машинами в Linux. Создан для тех, кто ценит эстетику ретро-футуризма и мощь аппаратной виртуализации.

## ✨ Основные возможности
- 🚀 **Hardware Acceleration:** Полная поддержка KVM для работы на скорости реального железа.
- 💿 **ISO Mounting:** Удобный выбор и загрузка любых OS через современный диалог GTK4.
- 🛠️ **Resource Control:** Динамическое выделение оперативной памяти (RAM) и ядер процессора (vCPU).
- 🎨 **Retro-Modern UI:** Глубокий черный интерфейс с неоновыми акцентами в стиле TuxTech.


## 🛠 Установка (для Arch Linux)

### 1. Системные зависимости
Установите QEMU и библиотеки интерфейса:
```bash
sudo pacman -S qemu-full libvirt ebtables bridge-utils python-gobject gtk4 libadwaita


    Склонируйте проект:
    bash

    git clone github.com


Перейдите в папку и запустите:
bash

python3 tuxvizor.py
