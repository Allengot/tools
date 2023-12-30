import ldap3
import base64
import struct
import argparse

def safe_b64decode(encoded_str):
    # 使用“=”填充字符串，使其长度成为4的倍数
    padding = b'=' * (len(encoded_str) % 4)
    # 进行解码
    decoded_str = base64.b64decode(encoded_str + padding)
    return decoded_str

def decode_msds_creator_sid(encoded_sid):
    try:
        # Ensure that the encoded SID has at least 8 bytes (1+1+6)
        if len(encoded_sid) < 8:
            raise ValueError("Invalid SID format")

        # Extract components of the SID with correct byte order
        revision, sub_authority_count = struct.unpack("<BB", encoded_sid[:2])
        identifier_authority = encoded_sid[2:8][::-1]
        sub_authorities = struct.unpack("<" + "I" * sub_authority_count, encoded_sid[8:])

        # Build SID string
        sid_string = f"S-{revision}-{int.from_bytes(identifier_authority, 'little')}-{'-'.join(map(str, sub_authorities))}"

        return sid_string

    except (struct.error, ValueError) as e:
        print(f"Error decoding SID: {e}")
        return None

def ldap_search(dc_ip, port, username, password, base_dn, domain, category, attributes):
    ldap_server = f"ldap://{dc_ip}:{port}"
    user_dn = f"{username}@{domain}"

    # 定义 LDAP 服务器
    server = ldap3.Server(ldap_server, get_info=ldap3.ALL)

    conn = None

    try:
        # 连接到 LDAP 服务器
        conn = ldap3.Connection(server, user=user_dn, password=password, auto_bind=True)
        print(f"LDAP connection successful: {conn}")

        # 执行查询
        filter_str = f"(&(objectcategory={category})(sAMAccountName=*))"
        print(f"Executing LDAP search with filter: {filter_str}")
        search_result = conn.search(search_base=base_dn, search_filter=filter_str, attributes=attributes)

        # 打印查询结果数量
        print(f"Number of entries found: {len(conn.entries)}")

        # 处理查询结果
        for entry in conn.entries:
            print(f"Entry DN: {entry.entry_dn}")
            for attr in attributes:
                if attr in entry.entry_attributes:
                    values = entry[attr].values
                    print(f"{attr}: {values}")

                    if attr == "mS-DS-CreatorSID" and values:
                        # 解密并显示可读的SID字符串
                        decoded_sid = decode_msds_creator_sid(values[0])
                        if decoded_sid:
                            print(f"Decoded {attr}: {decoded_sid}")

    except ldap3.core.exceptions.LDAPException as e:
        print(f"LDAP Error: {e}")

    finally:
        if conn:
            # 关闭连接
            conn.unbind()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LDAP Search Tool")
    parser.add_argument("-u", "--username", help="LDAP username", required=True)
    parser.add_argument("-p", "--password", help="LDAP password", required=True)
    parser.add_argument("-dc", "--base_dn", help="LDAP base DN", required=True)
    parser.add_argument("-dc-ip", "--dc_ip", help="LDAP server IP", required=True)
    parser.add_argument("-port", "-P", default=389, type=int, help="LDAP server port (default is 389)")
    parser.add_argument("-domain", "--domain", help="Domain name", required=True)
    parser.add_argument("-category", "--category", help="Object category (e.g., weblogic)", required=True)
    args = parser.parse_args()

    dc_ip = args.dc_ip
    port = args.port
    username = args.username
    password = args.password
    base_dn = args.base_dn
    domain = args.domain
    category = args.category
    attributes = ["mS-DS-CreatorSID"]

    # 调用查询函数
    ldap_search(dc_ip, port, username, password, base_dn, domain, category, attributes)
