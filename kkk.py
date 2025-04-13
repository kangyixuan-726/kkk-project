#!/usr/bin/env python3
import sys
import getopt
import time
import os

VERSION = "1.0"
DEFAULT_PROMPT = "> "
INPUT_DELAY = 0.1  # 修正拼写错误 DELAY -> DELAY

class TerminalManager:
    """跨平台终端管理类"""
    def __init__(self):
        self.is_windows = sys.platform == 'win32'
        self.old_settings = None
        
    def __enter__(self):
        if not self.is_windows:
            try:
                # Unix-like系统设置
                import termios
                import tty
                self.fd = sys.stdin.fileno()
                self.old_settings = termios.tcgetattr(self.fd)
                tty.setraw(self.fd)
            except ImportError:
                # 如果Unix系统也没有这些模块则跳过
                pass
        else:
            # Windows禁用行缓冲
            try:
                import msvcrt
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
            except (ImportError, AttributeError):
                pass
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.is_windows and self.old_settings:
            try:
                import termios
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            except ImportError:
                pass

def get_char():
    """跨平台字符读取函数"""
    if sys.platform == 'win32':
        try:
            import msvcrt
            while True:
                if msvcrt.kbhit():
                    ch = msvcrt.getch().decode(errors='ignore')
                    # 处理Windows退格键
                    if ch == '\x08':
                        return '\x7f'
                    return ch
                time.sleep(0.01)
        except ImportError:
            return sys.stdin.read(1)
    else:
        return sys.stdin.read(1)

def typewriter_print(text, delay=INPUT_DELAY, hide_echo=False):
    """跨平台打字机效果输出"""
    with TerminalManager() as tm:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
    print()

def show_help():
    help_text = """
命令行参数:
  -h, --help       显示帮助信息
  -v, --version    显示版本信息
  -p PROMPT, --prompt=PROMPT  设置交互提示符

交互功能:
  - 输入时实时回显
  - 支持退格键删除
  - 输入exit或quit退出程序
  - 输出带有打字机效果
"""
    typewriter_print(help_text, 0.02)

def main():
    prompt = DEFAULT_PROMPT
    
    # 处理命令行参数
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvp:",
            ["help", "version", "prompt="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        show_help()
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-v", "--version"):
            print(f"版本 {VERSION}")
            sys.exit()
        elif opt in ("-p", "--prompt"):
            prompt = arg

    # 主交互循环
    while True:
        try:
            typewriter_print(prompt, 0.01, False)
            user_input = ""
            while True:
                ch = get_char()
                if ch in ('\n', '\r'):  # 回车
                    print()
                    break
                elif ch == '\x7f':  # 退格
                    if len(user_input) > 0:
                        user_input = user_input[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    user_input += ch
                    print(ch, end='', flush=True)
            
            if user_input.lower() in ('exit', 'quit'):
                break
                
            # 处理输入
            typewriter_print(f"你输入了: {user_input}")
            
        except KeyboardInterrupt:
            print("\n使用 exit 或 quit 退出程序")
        except Exception as e:
            print(f"\n发生错误: {str(e)}")

if __name__ == "__main__":
    main()