import argparse
from ldap3 import Server, Connection, SUBTREE

# 默认的用户过滤器
default_user_filter = '(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=524288))'

# 默认的机器过滤器
default_machine_filter = '(&(samAccountType=805306369)(userAccountControl:1.2.840.113556.1.4.803:=524288))'

def ldap_query(dc_ip, port, username, password, ldap_base, ldap_filter, prefix):
    # LDAP服务器的地址和端口
    ldap_server = Server(f'ldap://{dc_ip}:{port}')

    try:
        # 创建LDAP连接
        with Connection(ldap_server, user=username, password=password, auto_bind=True) as conn:
            # 执行LDAP查询
            conn.search(ldap_base, ldap_filter, SUBTREE)

            # 获取查询结果
            entries = [f'{prefix}: {entry.entry_dn}' for entry in conn.entries]
            print('\n'.join(entries))  # 每个查询结果占用一行

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='LDAP Query Script')

    # 添加参数
    parser.add_argument('-dc-ip', help='LDAP server IP', required=True)
    parser.add_argument('-port', help='LDAP server port', required=True)
    parser.add_argument('-u', '--username', help='LDAP username', required=True)
    parser.add_argument('-p', '--password', help='LDAP password', required=True)
    parser.add_argument('-dc', '--ldap-base', help='LDAP base', required=True)

    # 添加 -all 参数，用于同时显示用户和机器
    parser.add_argument('-all', '--ldap-filter-all', action='store_true',
                        help='Use both default LDAP filters for user and machine delegation')

    # 添加 -user 参数，用于指定用户过滤器，默认为给定的过滤器
    parser.add_argument('-user', '--ldap-filter-user', action='store_true',
                        help='Use default LDAP filter for user delegation')

    # 添加 -machine 参数，用于指定机器过滤器，默认为给定的过滤器
    parser.add_argument('-machine', '--ldap-filter-machine', action='store_true',
                        help='Use default LDAP filter for machine delegation')

    # 添加 -filter 参数，用于指定自定义过滤器
    parser.add_argument('-filter', '--ldap-filter', help='LDAP filter', default=None)

    # 解析命令行参数
    args = parser.parse_args()

    # 根据参数使用相应的过滤器进行LDAP查询
    if args.ldap_filter_all:
        ldap_filter_user = default_user_filter
        ldap_filter_machine = default_machine_filter
    elif args.ldap_filter_user:
        ldap_filter_user = args.ldap_filter
        ldap_filter_machine = None
    elif args.ldap_filter_machine:
        ldap_filter_user = None
        ldap_filter_machine = args.ldap_filter
    else:
        ldap_filter_user = ldap_filter_machine = args.ldap_filter

    if ldap_filter_user:
        ldap_query(args.dc_ip, args.port, args.username, args.password, args.ldap_base, ldap_filter_user, 'User')
    
    if ldap_filter_machine:
        print('--------------------------------------------------')  # 添加这一行作为分隔线
        ldap_query(args.dc_ip, args.port, args.username, args.password, args.ldap_base, ldap_filter_machine, 'Machine')
