package main

import (
	"fmt"
	"net"
)

func scanPort(ip string, port int) bool {
	address := fmt.Sprintf("%s:%d", ip, port)
	conn, err := net.Dial("tcp", address)
	if err != nil {
		return false
	} else {
		defer conn.Close()
		return true
	}
}

func main() {
	var ip string
	fmt.Print("Enter the ip address to scan:")
	fmt.Scanln(&ip)

	for i := 1; i < 65535; i++ {
		if scanPort(ip, i) {
			fmt.Printf("%s:%d is open\n", ip, i)
		}
	}

}

