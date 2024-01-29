import argparse
import subprocess
import time

import psutil
from rcon.source import Client
from rcon.source.proto import Packet


class ClientFix(Client):
    def run(self, command: str, *args: str, encoding: str = "utf-8"):
        request = Packet.make_command(command, *args, encoding=encoding)
        response = self.communicate(request)

        return response.payload.decode(encoding)


def get_mem_usage():
    # 获取物理内存和swap内存的统计信息
    memory_info = psutil.virtual_memory()
    swap_info = psutil.swap_memory()

    # 已使用的物理内存和swap内存
    used_memory = memory_info.total - memory_info.available
    used_swap = swap_info.used

    # 总的物理内存和swap内存
    total_memory = memory_info.total
    total_swap = swap_info.total

    # 计算(已使用内存+已使用swap)/(总内存+总swap)的比例
    total_used = used_memory + used_swap
    total_resources = total_memory + total_swap
    usage_ratio = total_used / total_resources * 100
    return usage_ratio


def restart_pal(service_name='pal-server'):
    try:
        # 使用systemctl命令重启服务
        subprocess.run(['sudo', 'systemctl', 'restart', service_name], check=True)
        print(f"服务 {service_name} 已重启.")
    except subprocess.CalledProcessError as e:
        print(f"错误: 无法重启服务 {service_name}. 错误信息: {e}")


def check_pal(passwd, restart_mem=80., port=25575):
    mem_usage = get_mem_usage()
    if mem_usage > restart_mem:
        with ClientFix('127.0.0.1', port, passwd=passwd) as client:
            print(f'memory overflow: {mem_usage:.2f}%')
            client.run('Save')
            client.run(f"Server memory usage is above {mem_usage:.2f}%, restart in 10 seconds.")
            time.sleep(10)
            restart_pal()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pal Server Memory Overflow Fucker")
    parser.add_argument("--interval", type=int, default=10 * 60)
    parser.add_argument("--passwd", type=str, default=None, required=True)
    parser.add_argument("--restart_mem", type=float, default=80.)
    args = parser.parse_args()

    while True:
        check_pal(args.passwd, restart_mem=args.restart_mem)
        time.sleep(args.interval)
