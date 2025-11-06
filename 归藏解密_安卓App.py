#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
归藏解密 - Android App版本
使用 Kivy 框架，可打包为 APK
100% 兼容 Python 增强版
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.clock import Clock
import os

try:
    from crypto_utils import CryptoManager
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class DecryptApp(App):
    """归藏解密应用"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_file = None
        self.title = '归藏解密'
        
    def build(self):
        """构建界面"""
        # 设置窗口背景色
        Window.clearcolor = (0.1, 0.11, 0.14, 1)
        
        # 主布局
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title_layout = BoxLayout(size_hint_y=None, height=80)
        title_label = Label(
            text='[b]🔓 归藏解密[/b]',
            markup=True,
            font_size='28sp',
            size_hint_y=None,
            height=80
        )
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)
        
        # 状态标签
        self.status_label = Label(
            text='[color=00d9a3]✓ 就绪[/color]' if CRYPTO_AVAILABLE else '[color=ff9800]⚠ 基础模式[/color]',
            markup=True,
            size_hint_y=None,
            height=30,
            font_size='14sp'
        )
        layout.add_widget(self.status_label)
        
        # 文件选择按钮
        file_btn = Button(
            text='📁 选择文件',
            size_hint_y=None,
            height=50,
            background_color=(0, 0.6, 1, 1),
            font_size='16sp',
            bold=True
        )
        file_btn.bind(on_press=self.show_file_chooser)
        layout.add_widget(file_btn)
        
        # 显示选中的文件
        self.file_label = Label(
            text='未选择文件',
            size_hint_y=None,
            height=40,
            font_size='13sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(self.file_label)
        
        # 密码输入
        password_label = Label(
            text='🔑 解密密码',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            halign='left'
        )
        password_label.bind(size=password_label.setter('text_size'))
        layout.add_widget(password_label)
        
        self.password_input = TextInput(
            hint_text='输入密码（未加密文件可留空）',
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='14sp',
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.6, 1, 1)
        )
        layout.add_widget(self.password_input)
        
        # 显示密码复选框
        checkbox_layout = BoxLayout(size_hint_y=None, height=40)
        self.show_password_cb = CheckBox(size_hint_x=None, width=40)
        self.show_password_cb.bind(active=self.toggle_password)
        checkbox_layout.add_widget(self.show_password_cb)
        checkbox_label = Label(text='显示密码', font_size='13sp', halign='left')
        checkbox_label.bind(size=checkbox_label.setter('text_size'))
        checkbox_layout.add_widget(checkbox_label)
        layout.add_widget(checkbox_layout)
        
        # 解密按钮
        self.decrypt_btn = Button(
            text='🚀 开始解密',
            size_hint_y=None,
            height=60,
            background_color=(0, 0.85, 0.64, 1),
            font_size='18sp',
            bold=True,
            disabled=True
        )
        self.decrypt_btn.bind(on_press=self.start_decrypt)
        layout.add_widget(self.decrypt_btn)
        
        # 进度条
        self.progress = ProgressBar(
            max=100,
            size_hint_y=None,
            height=20
        )
        layout.add_widget(self.progress)
        
        # 结果标签
        self.result_label = Label(
            text='',
            markup=True,
            size_hint_y=None,
            height=100,
            font_size='13sp'
        )
        layout.add_widget(self.result_label)
        
        # 说明
        info_text = (
            '[color=00d9ff]💡 使用说明[/color]\n'
            '1. 点击"选择文件"选择要解密的文件\n'
            '2. 输入密码（未加密可留空）\n'
            '3. 点击"开始解密"\n'
            '4. 文件保存到同一目录'
        )
        info_label = Label(
            text=info_text,
            markup=True,
            size_hint_y=None,
            height=120,
            font_size='12sp'
        )
        layout.add_widget(info_label)
        
        return layout
    
    def show_file_chooser(self, instance):
        """显示文件选择器"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 文件选择器
        filechooser = FileChooserListView(
            path='/storage/emulated/0/',
            filters=['*']
        )
        content.add_widget(filechooser)
        
        # 按钮布局
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        # 选择按钮
        select_btn = Button(text='选择', background_color=(0, 0.85, 0.64, 1))
        select_btn.bind(on_press=lambda x: self.select_file(filechooser.selection, popup))
        btn_layout.add_widget(select_btn)
        
        # 取消按钮
        cancel_btn = Button(text='取消', background_color=(0.5, 0.5, 0.5, 1))
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='选择文件',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def select_file(self, selection, popup):
        """选择文件"""
        if selection:
            self.selected_file = selection[0]
            self.file_label.text = f'[color=00d9ff]{os.path.basename(self.selected_file)}[/color]'
            self.file_label.markup = True
            self.decrypt_btn.disabled = False
            popup.dismiss()
    
    def toggle_password(self, instance, value):
        """切换密码显示"""
        self.password_input.password = not value
    
    def start_decrypt(self, instance):
        """开始解密"""
        if not self.selected_file:
            self.show_error('请先选择文件')
            return
        
        if not os.path.exists(self.selected_file):
            self.show_error('文件不存在')
            return
        
        password = self.password_input.text.strip()
        
        # 在后台线程执行解密
        self.decrypt_btn.disabled = True
        self.status_label.text = '[color=0098ff]⏳ 解密中...[/color]'
        self.status_label.markup = True
        self.progress.value = 0
        
        Clock.schedule_once(lambda dt: self.do_decrypt(password), 0.1)
    
    def do_decrypt(self, password):
        """执行解密"""
        try:
            self.progress.value = 20
            
            # 读取文件
            with open(self.selected_file, 'rb') as f:
                data = f.read()
            
            self.progress.value = 40
            
            # 查找加密数据
            MAGIC_HEADER = b'\x89PNG\r\n\x1a\n'
            pos = data.rfind(MAGIC_HEADER)
            
            if pos == -1:
                # 查找未加密压缩包
                signatures = {
                    'ZIP': b'PK\x03\x04',
                    'RAR': b'Rar!\x1a\x07',
                    '7Z': b'7z\xbc\xaf\x27\x1c',
                }
                
                for format_name, sig in signatures.items():
                    sig_pos = data.find(sig)
                    if sig_pos != -1:
                        self.progress.value = 70
                        extracted = data[sig_pos:]
                        
                        # 保存文件
                        output_dir = os.path.dirname(self.selected_file)
                        base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
                        ext = format_name.lower()
                        output_file = os.path.join(output_dir, f'{base_name}_提取.{ext}')
                        
                        with open(output_file, 'wb') as f:
                            f.write(extracted)
                        
                        self.progress.value = 100
                        self.show_success(f'提取成功！\\n格式: {format_name}\\n大小: {len(extracted)/1024:.1f} KB\\n\\n文件: {os.path.basename(output_file)}')
                        return
                
                self.show_error('未找到加密数据或压缩包')
                return
            
            # 解密
            if not CRYPTO_AVAILABLE:
                self.show_error('加密模块未安装\\n仅支持未加密文件')
                return
            
            if not password:
                self.show_error('此文件已加密，请输入密码')
                return
            
            self.progress.value = 60
            
            encrypted_packet = data[pos:]
            decrypted = CryptoManager.decrypt_data(encrypted_packet, password)
            
            self.progress.value = 80
            
            # 识别格式
            format_name = '未知'
            ext = 'bin'
            if decrypted.startswith(b'PK\x03\x04'):
                format_name = 'ZIP'
                ext = 'zip'
            elif decrypted.startswith(b'Rar!\x1a\x07'):
                format_name = 'RAR'
                ext = 'rar'
            elif decrypted.startswith(b'7z\xbc\xaf\x27\x1c'):
                format_name = '7Z'
                ext = '7z'
            
            # 保存文件
            output_dir = os.path.dirname(self.selected_file)
            base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
            output_file = os.path.join(output_dir, f'{base_name}_解密.{ext}')
            
            with open(output_file, 'wb') as f:
                f.write(decrypted)
            
            self.progress.value = 100
            self.show_success(f'解密成功！\\n格式: {format_name}\\n大小: {len(decrypted)/1024:.1f} KB\\n\\n文件: {os.path.basename(output_file)}')
            
        except Exception as e:
            self.show_error(f'解密失败\\n{str(e)}')
    
    def show_success(self, message):
        """显示成功消息"""
        self.result_label.text = f'[color=00d9a3]✅ {message}[/color]'
        self.result_label.markup = True
        self.status_label.text = '[color=00d9a3]✅ 完成[/color]'
        self.status_label.markup = True
        self.decrypt_btn.disabled = False
        self.progress.value = 100
    
    def show_error(self, message):
        """显示错误消息"""
        self.result_label.text = f'[color=ff6b6b]❌ {message}[/color]'
        self.result_label.markup = True
        self.status_label.text = '[color=ff6b6b]❌ 失败[/color]'
        self.status_label.markup = True
        self.decrypt_btn.disabled = False
        self.progress.value = 0


if __name__ == '__main__':
    DecryptApp().run()

