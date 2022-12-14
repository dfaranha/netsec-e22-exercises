# Exercises: Network Layer Security


## Preliminaries

You should begin by installing required dependencies. Make sure you have the packages installed and the Wireshark setup working in your machine as described last week.

### Ubuntu 21.04 / Debian 11

```
sudo apt install mitmproxy
```

### Windows / WSL

You can try using `mitmproxy` from WSL, but if the virtualzed network interface gives you trouble, switch to the native version.

### Network Layout

Our network will be slightly more complicated than the previous one. Instead of having all nodes connected to the same local network, we will keep `NETSEC` and `SYSSEC` as wireless networks, and segment the wired network to `192.168.3.0/24`. Now the Access Point (AP) serves as the _router_ between the wireless and wired networks. We will abstract the Web server running on a Raspberry Pi in the wired network on an addreess in range `192.168.3.2-49` as some Internet-facing server. A basic layout of the network is pictured below.

![image](https://github.com/dfaranha/netsec-e22-exercises/blob/main/05_network_layer_security/network-layout.png)

Connect your machine to one of the wireless networks using the host system (you know the password) and test that you can connect to `http://192.168.3.2:8000/` using a Web browser.
The traffic between your browser and the server is now being routed by the AP with manually inserted static routes.

Verify that you can capture traffic between the host and `192.168.3.2` using Wireshark, to confirm that the interface is functional in bridged mode.

## Exercise 1: ARP Spoofing against router

*OBS*: If ARP spoofing already worked for you last week, or if ARP spoofing does not work in your platform, it is fine to skip to exercise 3.

Connect a mobile device to the wireless network and take note of its address, referred from here on as `mobile`.
Select one of the addresses in the range `192.168.3.2-49` (which will be called `X` from now on).
Try to impersonate the Web server by running the ARP spoofing attack inside in your machine:

```
sudo arpspoof -i <interface> -t <mobile> 192.168.3.X
```

Contrary to the last session, you can still access the Web server http://192.168.3.X:8000/ in your mobile. This is possible because ARP spoofing is ineffective here, since ARP does not resolve in the network 192.168.3.0 to which packets are routed. However, we can still impersonate the router.

Choose randomly one address in the IP range `192.168.1/2.1-49` (depending if you are connected to `SYSSEC` or `NETSEC`) and manually configure this address as the gateway in your mobile device. You can use the same IP address you had before from DHCP for your mobile device. Now run the ARP spoofing attack below:

```
sudo arpspoof -i <interface> -t <mobile> <gateway>
```

You will notice that connectivity between the mobile device and the Web server will stop, since traffic will be redirected to your machine and not be routed further.

## Exercise 2: Restoring access

Let's change the configuration for traffic to be forwarded again to the Web server.
The following configurations need to be performed in your machine to enable IP forwarding such that it can forward IPv4 traffic while avoiding ICMP redirects:

```
$ sudo sysctl -w net.ipv4.ip_forward=1
$ sudo sysctl -w net.ipv4.conf.all.send_redirects=0

```

After these configurations are put in place, the mobile device will be able to connect again to the Web server.
Start Wireshark in your machine to check that the traffic is still intercepted there. You can use the Login option to enter credentials and observe that they are captured by Wireshark, proving that the traffic is redirected correctly.

## Exercise 3: Running mitmproxy

Stop your ARP spoofing attack and configure your mobile device to use your machine as the router/gateway.

Wireshark will capture traffic and demonstrate the power of a passive eavesdropping attacker. Let's mount a more powerful attack.
We will run `mitmproxy` in your machine to be able to perform some processing of the captured traffic. First, configure the `iptables` firewall to send all HTTP traffic captured at port 8000 in your machine to port 8080 under control of `mitmproxy`:

```
$ sudo iptables -A FORWARD --in-interface <interface> -j ACCEPT
$ sudo iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 8000 -j REDIRECT --to-port 8080
```
If you are not running `iptables`, try to find a way to do the same in your firewall.

Now run `mitmproxy` in _transparent_ mode:

```
$ mitmproxy --mode transparent --showhost
```

If everything is working correctly, you should try again to access the Web server `http://192.168.3.X:8000/` in your mobile device and start seeing captured flows in the `mitmproxy` window.
In this window, you can select a flow by using the arrows and pressing ENTER, while pressing the letter `q` goes back to the overview screen.

## BONUS: Manipulate traffic in mitmproxy

If you reached here we have a bonus round for you. For this last exercise, we will simplify our setup to remove ARP spoofing.
Configure the gateway in your mobile device to point directly to the IP address of your machine and stop the execution of the ARP spoofing attack.

Let's use the scripting capability of `mitmproxy` to mount an _active_ attack.
Our simple website has a login capability, for which the credentials are not known. There should be legitimate traffic in the local network of successful login attempts, so find the correct flows in `mitmproxy` to obtain a pair of correct credentials.

Now access the website through your mobile device with the right credentials and login. You should now be able to access the `View Secrets` and `Upload Secrets` functionalities.
The `View Secrets` functionality will just show you some secret keyword, which should be visible in `mitmproxy` as well.
The `Upload Secrets` functionality is more interesting and allows the user to encrypt a message under a public key returned by the server.
Your final task is to _replace_ that public key with a key pair for which you know the private key (to be able to decrypt).
The code for the server portion is provided for reference in the repository inside the folder `simple-website`.

In order to achieve your goal, generate an RSA key pair in PEM format and plug the values marked as TODO in the file `simple-website/mitm_pk.py`. Now restart `mitmproxy` with the command below:

```
$ mitmproxy --mode transparent --showhost -s mitm_pk.py
```

Recover the message from the encryption provided by the client.
