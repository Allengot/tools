import ldap3
import argparse

def query_user_by_sid(dc_ip, port, base_dn, username, password, sid):
    server = ldap3.Server(f"ldap://{dc_ip}:{port}")
    connection = ldap3.Connection(server, user=f"{username}@redteam.red", password=password)
    
    try:
        if not connection.bind():
            print(f"LDAP Bind Error: {connection.result}")
        else:
            search_filter = f"(objectSid={sid})"
            attributes = ["distinguishedName"]

            connection.search(search_base=base_dn, search_filter=search_filter, attributes=attributes)

            if connection.entries:
                for entry in connection.entries:
                    dn = entry.distinguishedName.value
                    print(f"DN for SID {sid}: {dn}")
            else:
                print(f"No entry found for SID {sid}")

    except ldap3.core.exceptions.LDAPException as e:
        print(f"LDAP Error: {e}")

    finally:
        connection.unbind()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query user by SID from LDAP server.")
    parser.add_argument("-dc-ip", required=True, help="LDAP server IP address")
    parser.add_argument("-p", default=389, type=int, help="LDAP server port (default is 389)")
    parser.add_argument("-dc", required=True, help="LDAP base DN")
    parser.add_argument("-u", required=True, help="LDAP username")
    parser.add_argument("-pw", required=True, help="LDAP password")
    parser.add_argument("-sid", required=True, help="User SID")

    args = parser.parse_args()

    query_user_by_sid(args.dc_ip, args.p, args.dc, args.u, args.pw, args.sid)

