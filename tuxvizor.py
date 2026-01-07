import sys
import os
import subprocess
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw, GLib, Gdk

CSS = """
window { background-color: #050505; }
.hyper-box { 
    background: rgba(0, 255, 65, 0.05); 
    border: 1px solid #00ff41; 
    border-radius: 12px;
    padding: 25px;
}
.status-text { color: #ffb000; font-family: 'Monospace', monospace; font-size: 13px; }
label { color: #00ff41; font-family: 'Courier New', monospace; }
.iso-path { color: #888; font-size: 11px; margin-top: 5px; }
.launch-btn { 
    background: #00ff41; 
    color: #000; 
    font-weight: bold; 
    margin-top: 20px;
    padding: 10px;
}
.title-1 { font-size: 20px; font-weight: bold; color: #00ff41; }
"""

class TuxVizorApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='io.kiber.tuxvizor',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.iso_path = None

    def do_activate(self):
        display = Gdk.Display.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_display(display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.win = Adw.ApplicationWindow(application=self)
        self.win.set_title("TuxVizor Hypervisor 2026")
        self.win.set_default_size(550, 600)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_margin_top(30); main_box.set_margin_bottom(30)
        main_box.set_margin_start(30); main_box.set_margin_end(30)
        self.win.set_content(main_box)

        # Header
        header = Gtk.Label(label="[ TUX_VIZOR v0.2-STABLE ]")
        header.add_css_class("title-1")
        main_box.append(header)

        # Control Panel
        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        panel.add_css_class("hyper-box")
        main_box.append(panel)

        # ISO Setup
        panel.append(Gtk.Label(label="ОБРАЗ СИСТЕМЫ (.ISO):"))
        self.iso_btn = Gtk.Button(label="ВЫБРАТЬ ФАЙЛ")
        self.iso_btn.connect("clicked", self.on_open_file)
        panel.append(self.iso_btn)
        
        self.iso_label = Gtk.Label(label="Файл не выбран")
        self.iso_label.add_css_class("iso-path")
        panel.append(self.iso_label)

        panel.append(Gtk.Separator())

        # RAM Setup
        self.ram_val_label = Gtk.Label(label="ВЫДЕЛЕНО RAM: 2048 MB")
        panel.append(self.ram_val_label)
        self.ram_adj = Gtk.Adjustment(value=2048, lower=1024, upper=16384, step_increment=1024)
        ram_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.ram_adj)
        ram_scale.connect("value-changed", self.on_ram_changed)
        panel.append(ram_scale)

        # CPU Setup
        self.cpu_val_label = Gtk.Label(label="ЯДРА (vCPU): 2")
        panel.append(self.cpu_val_label)
        self.cpu_adj = Gtk.Adjustment(value=2, lower=1, upper=8, step_increment=1)
        cpu_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.cpu_adj)
        cpu_scale.connect("value-changed", self.on_cpu_changed)
        panel.append(cpu_scale)

        # Launch Button
        start_btn = Gtk.Button(label="INITIALIZE BOOT SEQUENCE")
        start_btn.add_css_class("launch-btn")
        start_btn.connect("clicked", self.on_start_vm)
        panel.append(start_btn)

        # Console
        self.console = Gtk.Label(label="> Hypervisor Ready.")
        self.console.add_css_class("status-text")
        main_box.append(self.console)

        self.win.present()

    def on_ram_changed(self, scroll):
        val = int(scroll.get_adjustment().get_value())
        self.ram_val_label.set_label(f"ВЫДЕЛЕНО RAM: {val} MB")

    def on_cpu_changed(self, scroll):
        val = int(scroll.get_adjustment().get_value())
        self.cpu_val_label.set_label(f"ЯДРА (vCPU): {val}")

    def on_open_file(self, btn):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Выберите ISO образ")
        filter_iso = Gtk.FileFilter()
        filter_iso.set_name("ISO Images")
        filter_iso.add_pattern("*.iso")
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(filter_iso)
        dialog.set_filters(filters)
        dialog.open(self.win, None, self.on_file_dialog_response)

    def on_file_dialog_response(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file:
                self.iso_path = file.get_path()
                self.iso_label.set_label(f"FILE: {os.path.basename(self.iso_path)}")
                self.update_console(f"> Loaded: {os.path.basename(self.iso_path)}")
        except:
            self.update_console("> Выбор файла отменен")

    def update_console(self, text):
        self.console.set_label(text)

    def on_start_vm(self, button):
        if not self.iso_path:
            self.update_console("> ERROR: PLEASE SELECT ISO FIRST")
            return

        ram = int(self.ram_adj.get_value())
        cpu = int(self.cpu_adj.get_value())
        
        self.update_console(f"> Launching Virtual Kernel...")
        
        # Исправленные параметры для Arch Linux
        cmd = [
            "qemu-system-x86_64",
            "-m", str(ram),
            "-smp", str(cpu),
            "-enable-kvm",
            "-cdrom", self.iso_path,
            "-boot", "d",
            "-vga", "std",        # Стандартный видеодрайвер
            "-display", "default" # Авто-выбор (обычно GTK или SDL)
        ]
        
        try:
            subprocess.Popen(cmd)
            self.update_console("> VM STATUS: RUNNING\n> Проверьте новое окно")
        except FileNotFoundError:
            self.update_console("> ERROR: QEMU NOT FOUND\n> Run: sudo pacman -S qemu-full")
        except Exception as e:
            self.update_console(f"> EXECUTION ERROR: {str(e)}")

if __name__ == "__main__":
    app = TuxVizorApp()
    app.run(sys.argv)
